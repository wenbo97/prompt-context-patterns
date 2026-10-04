$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$localRuby = Join-Path $projectRoot '.tools\ruby\bin'
if (Test-Path -LiteralPath (Join-Path $localRuby 'ruby.exe')) { $env:PATH = $localRuby + ';' + $env:PATH }
Push-Location -LiteralPath $projectRoot
try {
    & node scripts/catalog/generate.mjs
    if ($LASTEXITCODE -ne 0) { throw 'Catalog generation failed' }
    & bundle exec jekyll serve --host 127.0.0.1 --port 4000
} finally { Pop-Location }
