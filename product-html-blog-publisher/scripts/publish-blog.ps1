# publish-blog.ps1 - Publish/update a blog markdown to both Southern Machinery blog CMS sites.
# Encapsulates the PS 5.1-safe API flow validated on 2026-09-02 (S-EPCOS run).
# Tokens are passed as parameters (load from env vars at call site); never logged.

param(
    [Parameter(Mandatory=$true)][string]$ContentPath,
    [Parameter(Mandatory=$true)][string]$Slug,
    [Parameter(Mandatory=$true)][string]$Title,
    [string]$Excerpt = "",
    [string]$CoverImage = "",
    [string]$SeoTitle = "",
    [string]$SeoDescription = "",
    [string[]]$Tags = @(),
    [string]$Locale = "en",
    [string]$SmtaToken = "",
    [string]$JasonwuToken = "",
    [string]$SmtaPostId = "",
    [string]$JasonwuPostId = ""
)

# ContentPath : blog content markdown file (UTF-8)
# SmtaToken / JasonwuToken : blogcms_... tokens (or set SMTA_BLOG_TOKEN / JASONWU_BLOG_TOKEN env)
# SmtaPostId + JasonwuPostId : provide BOTH to PATCH (update existing posts) instead of POST

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12

if(-not $SmtaToken){ $SmtaToken = [System.Environment]::GetEnvironmentVariable('SMTA_BLOG_TOKEN','User') }
if(-not $JasonwuToken){ $JasonwuToken = [System.Environment]::GetEnvironmentVariable('JASONWU_BLOG_TOKEN','User') }
if(-not $SmtaToken -or -not $JasonwuToken){ throw "Missing blog tokens. Set SMTA_BLOG_TOKEN / JASONWU_BLOG_TOKEN env vars or pass parameters." }
if(-not (Test-Path -LiteralPath $ContentPath)){ throw "Content file not found: $ContentPath" }

# PS 5.1-safe read: never Get-Content -Raw for payload content
$content = [System.IO.File]::ReadAllText($ContentPath, [System.Text.Encoding]::UTF8)

$payload = @{
    title = $Title
    slug = $Slug
    excerpt = $Excerpt
    coverImage = $CoverImage
    contentMarkdown = $content
    status = "published"
    source = "ai"
    seoTitle = $SeoTitle
    seoDescription = $SeoDescription
    tags = $Tags
    locale = $Locale
}
$json = $payload | ConvertTo-Json -Depth 5
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)

function Invoke-BlogApi {
    param([string]$Url,[string]$Token,[byte[]]$Bytes,[string]$Method)
    $req=[System.Net.HttpWebRequest]::Create($Url)
    $req.Method=$Method
    $req.ContentType="application/json; charset=utf-8"
    $req.Headers.Add("Authorization","Bearer $Token")
    $req.Timeout=120000
    $req.ContentLength=$Bytes.Length
    $s=$req.GetRequestStream(); $s.Write($Bytes,0,$Bytes.Length); $s.Close()
    try {
        $resp=$req.GetResponse()
        $code=[int]$resp.StatusCode
        $sr=New-Object System.IO.StreamReader($resp.GetResponseStream())
        $txt=$sr.ReadToEnd(); $sr.Close(); $resp.Close()
        return @{ ok=$true; code=$code; body=$txt }
    } catch [System.Net.WebException] {
        $r=$_.Exception.Response
        $code=0; $txt=$_.Exception.Message
        if($r){
            $code=[int]$r.StatusCode
            $sr=New-Object System.IO.StreamReader($r.GetResponseStream())
            $txt=$sr.ReadToEnd(); $sr.Close()
        }
        return @{ ok=$false; code=$code; body=$txt }
    }
}

$sites = @(
    @{ name="smta";    url="https://smta.smthelp.eu/api/posts";    token=$SmtaToken;    postId=$SmtaPostId },
    @{ name="jasonwu";url="https://jasonwu.smthelp.eu/api/posts"; token=$JasonwuToken; postId=$JasonwuPostId }
)

$results = @()
foreach($site in $sites){
    $method = "POST"; $url = $site.url
    if($site.postId){ $method = "PATCH"; $url = "$($site.url)/$($site.postId)" }
    $r = Invoke-BlogApi -Url $url -Token $site.token -Bytes $bytes -Method $method
    $out = @{ site=$site.name; method=$method; http=$r.code }
    if($r.ok){
        $j = $r.body | ConvertFrom-Json
        $out.postId = $j.data.id
        $out.slug = $j.data.slug
        $out.url = $j.data.url
        $out.status = $j.data.status
        if($j.data.url){
            try {
                $verify = Invoke-WebRequest -Uri $j.data.url -UseBasicParsing -TimeoutSec 60
                $out.verifyHttp = [int]$verify.StatusCode
            } catch { $out.verifyHttp = "verify failed" }
        }
    } else {
        # never echo token; response body contains no tokens
        $out.error = ($r.body -replace 'blogcms_[a-f0-9]+','blogcms_***')
    }
    $results += $out
}

# Summary output (no tokens)
$results | ConvertTo-Json -Depth 4
