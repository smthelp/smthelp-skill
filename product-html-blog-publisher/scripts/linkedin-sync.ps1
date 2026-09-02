# linkedin-sync.ps1 - LinkedIn image post sync for a published blog.
# Validated flow from 2026-09-02: initializeUpload -> PUT bytes -> poll AVAILABLE -> POST (201) -> verify.
# Token MUST come from env LINKEDIN_ACCESS_TOKEN (User scope). Never logged, never stored.

param(
    [Parameter(Mandatory=$true)][string]$ImageUrl,       # validated direct image URL (HTTP 200, image/*)
    [Parameter(Mandatory=$true)][string]$BlogUrl,       # published blog post URL
    [Parameter(Mandatory=$true)][string]$Commentary,     # EN text: pain -> solution -> link -> 3-5 hashtags
    [string]$AltText = "Southern Machinery equipment"    # keyword + product category
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12

$tok=[System.Environment]::GetEnvironmentVariable('LINKEDIN_ACCESS_TOKEN','User')
if(-not $tok){ Write-Output @{status="needs_token"; error="LINKEDIN_ACCESS_TOKEN not set"} | ConvertTo-Json; exit 1 }

$owner = "urn:li:organization:3039402"
$hdrVer = "202601"

function New-LiRequest {
    param([string]$Url,[string]$Method)
    $req=[System.Net.HttpWebRequest]::Create($Url)
    $req.Method=$Method
    $req.Headers.Add("Authorization","Bearer $tok")
    $req.Headers.Add("LinkedIn-Version",$hdrVer)
    $req.Headers.Add("X-Restli-Protocol-Version","2.0.0")
    return $req
}

# 1. Download image bytes
$imgBytes = (Invoke-WebRequest -Uri $ImageUrl -UseBasicParsing -TimeoutSec 90).Content
if($imgBytes -isnot [byte[]]){ $imgBytes = [byte[]]$imgBytes }
$contentType = "image/png"; if($ImageUrl -match '\.webp($|\?)'){ $contentType = "image/webp" }
elseif($ImageUrl -match '\.jpe?g($|\?)'){ $contentType = "image/jpeg" }

# 2. initializeUpload
$initJson = @{ initializeUploadRequest = @{ owner = $owner } } | ConvertTo-Json
$req = New-LiRequest "https://api.linkedin.com/rest/images?action=initializeUpload" "POST"
$req.ContentType = "application/json"
$b = [System.Text.Encoding]::UTF8.GetBytes($initJson)
$req.ContentLength = $b.Length
$s = $req.GetRequestStream(); $s.Write($b,0,$b.Length); $s.Close()
try {
    $resp = $req.GetResponse()
    $sr = New-Object System.IO.StreamReader($resp.GetResponseStream())
    $j = ($sr.ReadToEnd() | ConvertFrom-Json); $sr.Close(); $resp.Close()
    $imageUrn = $j.value.image
    $uploadUrl = $j.value.uploadUrl
} catch [System.Net.WebException] {
    $r = $_.Exception.Response
    $code = if($r){ [int]$r.StatusCode } else { 0 }
    $errTxt = ""
    if($r){ $sr = New-Object System.IO.StreamReader($r.GetResponseStream()); $errTxt = $sr.ReadToEnd(); $sr.Close() }
    Write-Output @{ status="failed"; http=$code; stage="initializeUpload"; error=$errTxt } | ConvertTo-Json
    exit 1
}

# 3. PUT image bytes
$req = [System.Net.HttpWebRequest]::Create($uploadUrl)
$req.Method = "PUT"
$req.ContentType = $contentType
$req.Headers.Add("Authorization","Bearer $tok")
$req.Timeout = 300000
$req.ContentLength = $imgBytes.Length
$s = $req.GetRequestStream(); $s.Write($imgBytes,0,$imgBytes.Length); $s.Close()
try { $resp = $req.GetResponse(); $resp.Close(); $putCode = [int]$resp.StatusCode } catch [System.Net.WebException] {
    $r = $_.Exception.Response
    $code = if($r){ [int]$r.StatusCode } else { 0 }
    $errTxt = ""
    if($r){ $sr = New-Object System.IO.StreamReader($r.GetResponseStream()); $errTxt = $sr.ReadToEnd(); $sr.Close() }
    Write-Output @{ status="failed"; http=$code; stage="uploadBytes"; error=$errTxt } | ConvertTo-Json
    exit 1
}

# 4. Poll until AVAILABLE (max 10 tries)
$encoded = [System.Uri]::EscapeDataString($imageUrn)
$status = ""
for($i=0; $i -lt 10; $i++){
    Start-Sleep -Seconds 2
    $req = New-LiRequest "https://api.linkedin.com/rest/images/$encoded" "GET"
    try {
        $resp = $req.GetResponse()
        $sr = New-Object System.IO.StreamReader($resp.GetResponseStream())
        $j = ($sr.ReadToEnd() | ConvertFrom-Json); $sr.Close(); $resp.Close()
        $status = $j.status
        if($status -eq "AVAILABLE"){ break }
    } catch { $status = "poll error" }
}
if($status -ne "AVAILABLE"){
    Write-Output @{ status="failed"; stage="pollImage"; imageStatus=$status; imageUrn=$imageUrn } | ConvertTo-Json
    exit 1
}

# 5. Create post (NO isReshareDisabled - causes 422)
$postPayload = @{
    author = $owner
    commentary = $Commentary
    visibility = "PUBLIC"
    distribution = @{ feedDistribution = "MAIN_FEED"; targetEntities = @(); thirdPartyDistributionChannels = @() }
    lifecycleState = "PUBLISHED"
    content = @{ media = @{ id = $imageUrn; altText = $AltText } }
} | ConvertTo-Json -Depth 6
$req = New-LiRequest "https://api.linkedin.com/rest/posts" "POST"
$req.ContentType = "application/json"
$b = [System.Text.Encoding]::UTF8.GetBytes($postPayload)
$req.ContentLength = $b.Length
$s = $req.GetRequestStream(); $s.Write($b,0,$b.Length); $s.Close()
try {
    $resp = $req.GetResponse()
    $code = [int]$resp.StatusCode
    $postUrn = $resp.Headers["x-restli-id"]
    $sr = New-Object System.IO.StreamReader($resp.GetResponseStream())
    $null = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
} catch [System.Net.WebException] {
    $r = $_.Exception.Response
    $code = if($r){ [int]$r.StatusCode } else { 0 }
    $errTxt = ""
    if($r){ $sr = New-Object System.IO.StreamReader($r.GetResponseStream()); $errTxt = $sr.ReadToEnd(); $sr.Close() }
    Write-Output @{ status="failed"; http=$code; stage="createPost"; error=$errTxt } | ConvertTo-Json
    exit 1
}

# 6. Verify post
$encodedPost = [System.Uri]::EscapeDataString($postUrn)
$req = New-LiRequest "https://api.linkedin.com/rest/posts/$encodedPost" "GET"
try {
    $resp = $req.GetResponse()
    $sr = New-Object System.IO.StreamReader($resp.GetResponseStream())
    $j = ($sr.ReadToEnd() | ConvertFrom-Json); $sr.Close(); $resp.Close()
    $verified = ($j.lifecycleState -eq "PUBLISHED")
} catch { $verified = $false }

Write-Output @{
    status = "published"
    http = $code
    postUrn = $postUrn
    postUrl = "https://www.linkedin.com/feed/update/$postUrn"
    imageUrn = $imageUrn
    verified = $verified
} | ConvertTo-Json
