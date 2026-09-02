param(
    [string]$BaseUrl = "https://ph.smthelp.com",
    [string]$PackageDir = $(if ($env:SMTHELP_IMAGE_PACKAGE_DIR) { $env:SMTHELP_IMAGE_PACKAGE_DIR } else { "seo-webp-upload-$(Get-Date -Format 'yyyy-MM-dd')" }),
    [string]$AlbumName = $(if ($env:SMTHELP_PH_ALBUM_NAME) { $env:SMTHELP_PH_ALBUM_NAME } else { "southern-machinery-image-seo-webp-$(Get-Date -Format 'yyyy-MM-dd')" })
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$Workspace = if ($env:SMTHELP_IMAGE_WORKSPACE) { $env:SMTHELP_IMAGE_WORKSPACE } else { (Get-Location).Path }
$Root = Resolve-Path -LiteralPath $Workspace
$PackagePath = Resolve-Path -LiteralPath (Join-Path $Root $PackageDir)
$ManifestJson = Join-Path $PackagePath "seo-webp-manifest.json"
$ManifestCsv = Join-Path $PackagePath "seo-webp-manifest.csv"
$ResultsJson = Join-Path $PackagePath "upload-results-curl.json"
$SummaryMd = Join-Path $PackagePath "upload-summary.md"
$TempDir = [System.IO.Path]::GetTempPath()
$CookieJar = Join-Path $TempDir ("ph-upload-" + [guid]::NewGuid().ToString("N") + ".cookies.txt")
$LoginHtml = Join-Path $TempDir ("ph-login-" + [guid]::NewGuid().ToString("N") + ".html")
$UploadHtml = Join-Path $TempDir ("ph-upload-" + [guid]::NewGuid().ToString("N") + ".html")
$ResponseFile = Join-Path $TempDir ("ph-response-" + [guid]::NewGuid().ToString("N") + ".json")

function Write-Step {
    param([string]$Message)
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$stamp] $Message"
}

function Get-AuthToken {
    param([string]$Path)
    $html = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    $match = [regex]::Match($html, 'PF\.obj\.config\.auth_token\s*=\s*"([^"]+)"')
    if (-not $match.Success) {
        throw "Could not find auth_token in $Path"
    }
    return $match.Groups[1].Value
}

function Save-Json {
    param($Payload)
    $Payload | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $ResultsJson -Encoding UTF8
}

function Write-Manifest {
    param($Rows)
    $Rows | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ManifestJson -Encoding UTF8
    $Rows | Export-Csv -LiteralPath $ManifestCsv -NoTypeInformation -Encoding UTF8
}

function Read-ResponseJson {
    param([string]$Path)
    $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    if ([string]::IsNullOrWhiteSpace($text)) {
        return $null
    }
    try {
        return $text | ConvertFrom-Json
    } catch {
        return [pscustomobject]@{
            error = [pscustomobject]@{
                message = $text.Substring(0, [Math]::Min(500, $text.Length))
                context = "non-json-response"
            }
        }
    }
}

function Get-ImageObject {
    param($Payload)
    if ($null -eq $Payload) { return $null }
    if ($Payload.PSObject.Properties.Name -contains "image") { return $Payload.image }
    if (($Payload.PSObject.Properties.Name -contains "success") -and $Payload.success -and ($Payload.success.PSObject.Properties.Name -contains "image")) {
        return $Payload.success.image
    }
    return $null
}

try {
    $Username = $env:SMTHELP_PH_USERNAME
    $Password = $env:SMTHELP_PH_PASSWORD
    if ([string]::IsNullOrWhiteSpace($Username) -or [string]::IsNullOrWhiteSpace($Password)) {
        throw "Set SMTHELP_PH_USERNAME and SMTHELP_PH_PASSWORD before running this script."
    }

    $BaseUrl = $BaseUrl.TrimEnd("/")
    $Rows = Get-Content -LiteralPath $ManifestJson -Raw -Encoding UTF8 | ConvertFrom-Json
    $Results = [ordered]@{
        generated = (Get-Date).ToString("s")
        base_url = $BaseUrl
        album_name = $AlbumName
        album = $null
        login_status = "not-started"
        success_count = 0
        failure_count = 0
        results = @()
    }
    Save-Json $Results

    Write-Step "Fetching login page"
    & curl.exe --max-time 30 --connect-timeout 10 -sS -L -c $CookieJar "$BaseUrl/login" -o $LoginHtml
    $LoginToken = Get-AuthToken $LoginHtml

    Write-Step "Submitting login form"
    & curl.exe --max-time 45 --connect-timeout 10 -sS -b $CookieJar -c $CookieJar `
        -H "X-Requested-With: XMLHttpRequest" `
        -H "Accept: application/json, text/html" `
        -H "Referer: $BaseUrl/login" `
        --data-urlencode "login-subject=$Username" `
        --data-urlencode "password=$Password" `
        --data-urlencode "auth_token=$LoginToken" `
        "$BaseUrl/login" -o $ResponseFile

    Write-Step "Checking upload page"
    & curl.exe --max-time 30 --connect-timeout 10 -sS -L -b $CookieJar -c $CookieJar "$BaseUrl/upload" -o $UploadHtml
    $uploadPage = Get-Content -LiteralPath $UploadHtml -Raw -Encoding UTF8
    if ($uploadPage -match '<body id="login"' -or $uploadPage -match 'Username or Email address') {
        $Results.login_status = "failed"
        Save-Json $Results
        throw "Login failed: upload page still shows login form."
    }
    $UploadToken = Get-AuthToken $UploadHtml
    $Results.login_status = "ok"
    Save-Json $Results

    Write-Step "Creating album: $AlbumName"
    $AlbumDescription = "Southern Machinery CE, MD, ISO and RoHS certification images converted to SEO-friendly WebP files for SMT, THT, board handling and PCB assembly equipment references."
    & curl.exe --max-time 60 --connect-timeout 10 -sS -b $CookieJar -c $CookieJar `
        -H "X-Requested-With: XMLHttpRequest" `
        -H "Accept: application/json" `
        -H "Referer: $BaseUrl/upload" `
        --data-urlencode "action=create-album" `
        --data-urlencode "type=album" `
        --data-urlencode "auth_token=$UploadToken" `
        --data-urlencode "album[name]=$AlbumName" `
        --data-urlencode "album[description]=$AlbumDescription" `
        --data-urlencode "album[privacy]=public" `
        --data-urlencode "album[password]=" `
        --data-urlencode "album[new]=true" `
        "$BaseUrl/json" -o $ResponseFile
    $AlbumPayload = Read-ResponseJson $ResponseFile
    $Album = if ($AlbumPayload -and ($AlbumPayload.PSObject.Properties.Name -contains "album")) { $AlbumPayload.album } else { $null }
    $AlbumId = ""
    if ($Album) {
        $AlbumId = if ($Album.id_encoded) { [string]$Album.id_encoded } else { [string]$Album.id }
        $Results.album = $Album
        Write-Step "Album created: $($Album.url)"
    } else {
        $Results.album = $AlbumPayload
        Write-Step "Album creation did not return an album; continuing upload without album_id"
    }
    Save-Json $Results

    $index = 0
    foreach ($row in $Rows) {
        $index += 1
        if ($row.upload_status -eq "uploaded" -and -not [string]::IsNullOrWhiteSpace([string]$row.uploaded_url)) {
            $Results.success_count += 1
            $Results.results += [pscustomobject]@{
                index = $index
                seo_filename = $row.seo_filename
                status = "skipped-existing"
                uploaded_url = $row.uploaded_url
            }
            Save-Json $Results
            continue
        }

        $source = Join-Path $Root $row.webp_relative_path
        Write-Step "Uploading [$index/$($Rows.Count)] $($row.seo_filename)"
        $curlArgs = @(
            "--max-time", "120",
            "--connect-timeout", "10",
            "-sS",
            "-b", $CookieJar,
            "-c", $CookieJar,
            "-H", "X-Requested-With: XMLHttpRequest",
            "-H", "Accept: application/json",
            "-H", "Referer: $BaseUrl/upload",
            "-F", "source=@$source;filename=$($row.seo_filename);type=image/webp",
            "-F", "action=upload",
            "-F", "type=file",
            "-F", "privacy=public",
            "-F", ("timestamp=" + [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()),
            "-F", "auth_token=$UploadToken",
            "-F", "title=$($row.title)",
            "-F", "description=$($row.description)",
            "-F", "tags=$($row.tags)",
            "-F", "category_id=",
            "-F", "nsfw=0"
        )
        if (-not [string]::IsNullOrWhiteSpace($AlbumId)) {
            $curlArgs += @("-F", "album_id=$AlbumId")
        }
        $curlArgs += @("$BaseUrl/json", "-o", $ResponseFile)

        try {
            & curl.exe @curlArgs
            $Payload = Read-ResponseJson $ResponseFile
            $Image = Get-ImageObject $Payload
            if ($Image -and $Image.url) {
                $viewer = if ($Image.url_viewer) { [string]$Image.url_viewer } elseif ($Image.url_short) { [string]$Image.url_short } else { [string]$Image.url }
                $row.upload_status = "uploaded"
                $row.uploaded_url = $viewer
                $row.direct_url = [string]$Image.url
                $row.image_id = if ($Image.id_encoded) { [string]$Image.id_encoded } else { [string]$Image.id }
                $row.uploaded_album_id = $AlbumId
                if ($Album -and $Album.url) { $row.uploaded_album_url = [string]$Album.url }
                $Results.success_count += 1
                $Results.results += [pscustomobject]@{
                    index = $index
                    seo_filename = $row.seo_filename
                    status = "uploaded"
                    uploaded_url = $viewer
                    direct_url = [string]$Image.url
                    image_id = $row.image_id
                }
                Write-Step "Uploaded: $viewer"
            } else {
                $message = "Unknown upload error"
                if ($Payload -and ($Payload.PSObject.Properties.Name -contains "error") -and $Payload.error.message) {
                    $message = [string]$Payload.error.message
                }
                $row.upload_status = "failed"
                $row.upload_error = $message
                $Results.failure_count += 1
                $Results.results += [pscustomobject]@{
                    index = $index
                    seo_filename = $row.seo_filename
                    status = "failed"
                    error = $message
                }
                Write-Step "Failed: $message"
            }
        } catch {
            $row.upload_status = "failed"
            $row.upload_error = $_.Exception.Message
            $Results.failure_count += 1
            $Results.results += [pscustomobject]@{
                index = $index
                seo_filename = $row.seo_filename
                status = "failed"
                error = $_.Exception.Message
            }
            Write-Step "Failed: $($_.Exception.Message)"
        }

        Save-Json $Results
        Write-Manifest $Rows
    }

    $albumUrl = ""
    if ($Album -and $Album.url) { $albumUrl = [string]$Album.url }
    @(
        "# Upload Summary"
        "- Generated: $((Get-Date).ToString("s"))"
        "- Site: $BaseUrl"
        "- Album name requested: $AlbumName"
        "- Album URL: $albumUrl"
        "- Login status: $($Results.login_status)"
        "- Uploaded: $($Results.success_count)"
        "- Failed: $($Results.failure_count)"
        "- Results JSON: $ResultsJson"
        "- Updated manifest JSON: $ManifestJson"
        "- Updated manifest CSV: $ManifestCsv"
        ""
        "## Notes"
        "- Upload executed via logged-in Chevereto web session flow using temporary cookies."
        "- Tags were submitted as a field when uploading; Chevereto Free may ignore tags if the instance does not support them."
    ) | Set-Content -LiteralPath $SummaryMd -Encoding UTF8

    Write-Step "Done. Uploaded=$($Results.success_count), Failed=$($Results.failure_count)"
} finally {
    Remove-Item -LiteralPath $CookieJar,$LoginHtml,$UploadHtml,$ResponseFile -Force -ErrorAction SilentlyContinue
}
