#!/usr/bin/env pwsh

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = 'stop'

if ($IsWindows) {
    $fontForgeDir = "${env:ProgramFiles}\FontForgeBuilds"
    $env:PATH = "$fontForgeDir;$env:PATH"
}

New-Item -ItemType Directory -Force -Path "$PSScriptRoot/build" | Out-Null

Get-ChildItem -Path "$PSScriptRoot/liberation-1.7-fonts/src" -Filter "*.sfd" | ForEach-Object {
    $inputFile = $_.FullName
    $outputFile = "$PSScriptRoot/build/$([System.IO.Path]::GetFileNameWithoutExtension($inputFile)).txt"
    fontforge -script "$PSScriptRoot/dump-glyphs.py" $inputFile > $outputFile
}

Get-ChildItem -Path "$PSScriptRoot/build" -Filter "*.txt" | ForEach-Object {
    $inputUnicode = $_.FullName
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($inputUnicode)
    Write-Output "Subsetting font ${filename} ..."
    $inputFont = "$PSScriptRoot/liberation-fonts/src/${filename}.sfd"
    $outputFont = "$(Split-Path $PSScriptRoot -Parent)/$(${filename}.Replace('Liberation', 'LiberaLean')).otf"
    fontforge -script "$PSScriptRoot/subset-export.py" $inputUnicode $inputFont $outputFont
}
