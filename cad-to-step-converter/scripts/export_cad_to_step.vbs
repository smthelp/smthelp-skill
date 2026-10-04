Option Explicit

Dim fso, env
Set fso = CreateObject("Scripting.FileSystemObject")
Set env = CreateObject("WScript.Shell").Environment("Process")

Dim root, outputRoot, logRoot, extsCsv, resumeMode, limitSeconds, recurseMode, inventoryOnly, maxFiles
root = EnvOrDefault("CAD_STEP_ROOT", "")
extsCsv = EnvOrDefault("CAD_STEP_EXTS", "x_t,x_b,sldprt,sldasm,stl")
resumeMode = (EnvOrDefault("CAD_STEP_RESUME", "1") <> "0")
limitSeconds = CLng(EnvOrDefault("CAD_STEP_LIMIT_SECONDS", "0"))
recurseMode = (EnvOrDefault("CAD_STEP_RECURSE", "0") <> "0")
maxFiles = CLng(EnvOrDefault("CAD_STEP_MAX_FILES", "0"))
inventoryOnly = False

ParseArgs

If Len(root) = 0 Then
  WScript.Echo "ERROR: Provide /root:<folder> or set CAD_STEP_ROOT."
  WScript.Quit 2
End If

root = fso.GetFolder(root).Path
If Len(outputRoot) = 0 Then outputRoot = fso.BuildPath(root, "ai-reports\" & DateStamp() & "-cad-to-step\output-step")
If Len(logRoot) = 0 Then logRoot = fso.BuildPath(fso.GetParentFolderName(outputRoot), "logs")

EnsureFolder outputRoot
EnsureFolder logRoot

Dim runId, reportPath, summaryPath
runId = MakeRunId()
reportPath = fso.BuildPath(logRoot, "cad-to-step-report-" & runId & ".csv")
summaryPath = fso.BuildPath(logRoot, "cad-to-step-summary-" & runId & ".txt")

Dim report
Set report = fso.CreateTextFile(reportPath, True, True)
report.WriteLine "run_id,index,source_path,source_extension,source_size_mb,output_path,output_size_mb,status,message,duration_sec"
report.Close

Dim extMap
Set extMap = BuildExtMap(extsCsv)

Dim files
Set files = CreateObject("System.Collections.ArrayList")
CollectFiles root, files, extMap, recurseMode
files.Sort
If maxFiles > 0 Then
  Do While files.Count > maxFiles
    files.RemoveAt files.Count - 1
  Loop
End If

WScript.Echo "Root: " & root
WScript.Echo "OutputRoot: " & outputRoot
WScript.Echo "Report: " & reportPath
WScript.Echo "Files selected: " & files.Count

Dim converted, skipped, unsupported, failed, stoppedByLimit
converted = 0
skipped = 0
unsupported = 0
failed = 0
stoppedByLimit = False

Dim sw
Set sw = Nothing
If Not inventoryOnly Then
  Set sw = GetSolidWorks()
  If sw Is Nothing Then
    WScript.Echo "ERROR: Could not create or attach to SOLIDWORKS."
    WScript.Quit 3
  End If
  On Error Resume Next
  sw.Visible = False
  sw.UserControl = False
  sw.CommandInProgress = True
  On Error GoTo 0
End If

Dim i, batchStarted
batchStarted = Timer
For i = 0 To files.Count - 1
  If limitSeconds > 0 Then
    If ElapsedSeconds(batchStarted) >= limitSeconds Then
      stoppedByLimit = True
      Exit For
    End If
  End If
  ConvertOne sw, files(i), i + 1, converted, skipped, unsupported, failed
Next

If Not sw Is Nothing Then
  On Error Resume Next
  sw.CommandInProgress = False
  On Error GoTo 0
End If

Dim summary
Set summary = fso.CreateTextFile(summaryPath, True, True)
summary.WriteLine "run_id=" & runId
summary.WriteLine "root=" & root
summary.WriteLine "output_root=" & outputRoot
summary.WriteLine "report_csv=" & reportPath
summary.WriteLine "selected_count=" & files.Count
summary.WriteLine "converted=" & converted
summary.WriteLine "skipped=" & skipped
summary.WriteLine "unsupported=" & unsupported
summary.WriteLine "failed=" & failed
summary.WriteLine "stopped_by_limit=" & stoppedByLimit
summary.WriteLine "inventory_only=" & inventoryOnly
summary.WriteLine "note=Original CAD files were not modified. STEP files are generated in output_root."
summary.Close

WScript.Echo "Summary: " & summaryPath
WScript.Echo "converted=" & converted & " skipped=" & skipped & " unsupported=" & unsupported & " failed=" & failed & " stopped_by_limit=" & stoppedByLimit

Sub ParseArgs()
  Dim arg, p, key, value
  outputRoot = EnvOrDefault("CAD_STEP_OUTPUT_ROOT", "")
  logRoot = EnvOrDefault("CAD_STEP_LOG_ROOT", "")
  For Each arg In WScript.Arguments
    p = InStr(arg, ":")
    If p > 0 Then
      key = LCase(Left(arg, p - 1))
      value = Mid(arg, p + 1)
      Select Case key
        Case "/root"
          root = value
        Case "/out"
          outputRoot = value
        Case "/log"
          logRoot = value
        Case "/exts"
          extsCsv = value
        Case "/resume"
          resumeMode = (value <> "0")
        Case "/limitseconds"
          limitSeconds = CLng(value)
        Case "/recurse"
          recurseMode = (value <> "0")
        Case "/inventory"
          inventoryOnly = (value <> "0")
        Case "/max"
          maxFiles = CLng(value)
      End Select
    End If
  Next
End Sub

Function EnvOrDefault(name, fallback)
  Dim value
  value = env(name)
  If Len(value) = 0 Then value = fallback
  EnvOrDefault = value
End Function

Function BuildExtMap(csv)
  Dim map, parts, i, ext
  Set map = CreateObject("Scripting.Dictionary")
  parts = Split(csv, ",")
  For i = 0 To UBound(parts)
    ext = LCase(Trim(parts(i)))
    If Len(ext) > 0 Then
      If Left(ext, 1) <> "." Then ext = "." & ext
      map(ext) = True
    End If
  Next
  Set BuildExtMap = map
End Function

Sub CollectFiles(folderPath, files, extMap, recursive)
  Dim folder, file, subFolder, ext
  Set folder = fso.GetFolder(folderPath)
  For Each file In folder.Files
    ext = LCase("." & fso.GetExtensionName(file.Name))
    If Left(file.Name, 2) <> "~$" And extMap.Exists(ext) Then
      files.Add file.Path
    End If
  Next
  If recursive Then
    For Each subFolder In folder.SubFolders
      If LCase(subFolder.Name) <> ".git" And LCase(subFolder.Name) <> "ai-reports" And LCase(subFolder.Name) <> "chrome_profile_notebooklm" Then
        CollectFiles subFolder.Path, files, extMap, recursive
      End If
    Next
  End If
End Sub

Function GetSolidWorks()
  On Error Resume Next
  Dim app
  Set app = GetObject(, "SldWorks.Application")
  If Err.Number <> 0 Then
    Err.Clear
    Set app = CreateObject("SldWorks.Application.34")
  End If
  If Err.Number <> 0 Then
    WScript.Echo "SOLIDWORKS COM error: " & Err.Number & " " & Err.Description
    Err.Clear
    Set app = Nothing
  End If
  On Error GoTo 0
  Set GetSolidWorks = app
End Function

Sub ConvertOne(sw, sourcePath, index, ByRef converted, ByRef skipped, ByRef unsupported, ByRef failed)
  Dim file, ext, outputPath
  Set file = fso.GetFile(sourcePath)
  ext = LCase("." & fso.GetExtensionName(file.Name))
  outputPath = GetOutputPath(file, ext)

  If inventoryOnly Then
    WriteRow index, file, ext, outputPath, "inventory", "Inventory only; no conversion attempted.", 0
    Exit Sub
  End If

  If Not IsConvertible(ext) Then
    unsupported = unsupported + 1
    WriteRow index, file, ext, outputPath, "unsupported", "Unsupported by this exporter.", 0
    Exit Sub
  End If

  If resumeMode And fso.FileExists(outputPath) Then
    If fso.GetFile(outputPath).Size > 0 Then
      skipped = skipped + 1
      WriteRow index, file, ext, outputPath, "skipped_existing", "Output already exists and resume mode is on.", 0
      Exit Sub
    End If
  End If

  Dim started, model
  started = Timer
  Set model = OpenForExport(sw, sourcePath, ext)

  If model Is Nothing Then
    failed = failed + 1
    WriteRow index, file, ext, outputPath, "failed_load", "SOLIDWORKS did not return a document.", ElapsedSeconds(started)
    Exit Sub
  End If

  Dim title
  title = ""
  On Error Resume Next
  title = model.GetTitle()
  On Error GoTo 0

  On Error Resume Next
  Dim code
  code = model.SaveAs3(CStr(outputPath), CLng(0), CLng(1))
  If Err.Number <> 0 Then
    Dim saveMessage
    saveMessage = Err.Description
    Err.Clear
    failed = failed + 1
    WriteRow index, file, ext, outputPath, "failed_save", saveMessage, ElapsedSeconds(started)
  ElseIf fso.FileExists(outputPath) And fso.GetFile(outputPath).Size > 0 Then
    converted = converted + 1
    WriteRow index, file, ext, outputPath, "converted", "Exported STEP. SaveAs3 code=" & code, ElapsedSeconds(started)
  Else
    failed = failed + 1
    WriteRow index, file, ext, outputPath, "failed_save", "SaveAs3 produced no output file. Code=" & code, ElapsedSeconds(started)
  End If
  On Error GoTo 0

  If Len(title) > 0 Then
    On Error Resume Next
    sw.CloseDoc title
    On Error GoTo 0
  End If
End Sub

Function OpenForExport(sw, sourcePath, ext)
  On Error Resume Next
  Dim model, docType, loaded
  Set model = Nothing

  If ext = ".sldasm" Then
    docType = CLng(2)
  Else
    docType = CLng(1)
  End If

  If ext = ".sldprt" Or ext = ".sldasm" Then
    Set model = sw.OpenDoc(CStr(sourcePath), docType)
    If Err.Number <> 0 Then
      Err.Clear
      Set model = Nothing
    End If
  Else
    loaded = sw.LoadFile(CStr(sourcePath))
    If Err.Number <> 0 Then
      Err.Clear
      Set model = Nothing
    Else
      Set model = sw.ActiveDoc
    End If
  End If
  On Error GoTo 0
  Set OpenForExport = model
End Function

Function IsConvertible(ext)
  Select Case ext
    Case ".sldprt", ".sldasm", ".x_t", ".x_b", ".stl"
      IsConvertible = True
    Case Else
      IsConvertible = False
  End Select
End Function

Function GetOutputPath(file, ext)
  Dim stem, extTag, hash
  stem = SafeStem(fso.GetBaseName(file.Name))
  extTag = Replace(ext, ".", "")
  hash = SimpleHash(file.Path)
  GetOutputPath = fso.BuildPath(outputRoot, stem & "__from_" & extTag & "__" & hash & ".STEP")
End Function

Function SafeStem(value)
  Dim invalid, i, ch, out
  invalid = "\/:*?""<>|"
  out = ""
  For i = 1 To Len(value)
    ch = Mid(value, i, 1)
    If InStr(invalid, ch) > 0 Then
      out = out & "_"
    Else
      out = out & ch
    End If
  Next
  out = Trim(out)
  If Len(out) = 0 Then out = "converted"
  If Len(out) > 120 Then out = Left(out, 120)
  SafeStem = out
End Function

Function SimpleHash(value)
  Dim i, code, h
  h = CDbl(0)
  For i = 1 To Len(value)
    code = AscW(Mid(value, i, 1))
    If code < 0 Then code = code + 65536
    h = CDbl(h) * CDbl(131) + CDbl(code)
    h = h - Fix(h / CDbl(2147483647)) * CDbl(2147483647)
  Next
  SimpleHash = LCase(Hex(CLng(h)))
End Function

Sub WriteRow(index, file, ext, outputPath, status, message, durationSec)
  Dim outSize
  outSize = 0
  If fso.FileExists(outputPath) Then outSize = fso.GetFile(outputPath).Size

  Dim line, appendReport
  line = Csv(runId) & "," & _
    CStr(index) & "," & _
    Csv(file.Path) & "," & _
    Csv(ext) & "," & _
    Csv(Round(file.Size / 1048576, 3)) & "," & _
    Csv(outputPath) & "," & _
    Csv(Round(outSize / 1048576, 3)) & "," & _
    Csv(status) & "," & _
    Csv(message) & "," & _
    Csv(Round(durationSec, 2))

  Set appendReport = fso.OpenTextFile(reportPath, 8, True, -1)
  appendReport.WriteLine line
  appendReport.Close
  WScript.Echo index & " " & status & " " & file.Name
End Sub

Function Csv(value)
  Dim text
  text = CStr(value)
  text = Replace(text, """", """""")
  Csv = """" & text & """"
End Function

Function ElapsedSeconds(started)
  Dim nowValue
  nowValue = Timer
  If nowValue < started Then
    ElapsedSeconds = (86400 - started) + nowValue
  Else
    ElapsedSeconds = nowValue - started
  End If
End Function

Sub EnsureFolder(path)
  If fso.FolderExists(path) Then Exit Sub
  Dim parent
  parent = fso.GetParentFolderName(path)
  If Len(parent) > 0 And Not fso.FolderExists(parent) Then EnsureFolder parent
  fso.CreateFolder path
End Sub

Function DateStamp()
  Dim d
  d = Date
  DateStamp = Year(d) & "-" & Right("0" & Month(d), 2) & "-" & Right("0" & Day(d), 2)
End Function

Function MakeRunId()
  Dim d
  d = Now
  MakeRunId = Year(d) & Right("0" & Month(d), 2) & Right("0" & Day(d), 2) & "-" & Right("0" & Hour(d), 2) & Right("0" & Minute(d), 2) & Right("0" & Second(d), 2)
End Function
