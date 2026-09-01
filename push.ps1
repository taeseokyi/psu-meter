# psu-meter -> GitHub push
# 실행:  powershell -ExecutionPolicy Bypass -File .\push.ps1
#   또는 파일 우클릭 → "PowerShell에서 실행"

param(
    # 커밋 메시지. 생략하면 아래 기본값을 씁니다.
    #   powershell -ExecutionPolicy Bypass -File .\push.ps1 "회절 모델 수정"
    [string]$Message = '설계 자료 갱신'
)

$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Repo = 'https://github.com/taeseokyi/psu-meter.git'
Set-Location -LiteralPath $PSScriptRoot

Write-Host '=========================================================='
Write-Host '  psu-meter  ->  GitHub push'
Write-Host "  $Repo"
Write-Host '=========================================================='
Write-Host ''

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host '[오류] git 을 찾을 수 없습니다.' -ForegroundColor Red
    Write-Host '       Git for Windows 설치 여부와 PATH 등록을 확인하세요.'
    Read-Host '`n엔터를 누르면 종료합니다'
    exit 1
}

# 1) 저장소 초기화
if (-not (Test-Path '.git')) {
    Write-Host '[1/6] 저장소 초기화'
    git init
    if ($LASTEXITCODE -ne 0) { Read-Host '실패. 엔터로 종료'; exit 1 }
} else {
    Write-Host '[1/6] 기존 저장소를 그대로 사용합니다'
}

# 2) 한글 파일명 표시
Write-Host ''
Write-Host '[2/6] 한글 파일명이 깨져 보이지 않도록 설정'
git config core.quotepath false

# 3) 스테이징
Write-Host ''
Write-Host '[3/6] 파일 추가'
git add -A
if ($LASTEXITCODE -ne 0) { Read-Host '실패. 엔터로 종료'; exit 1 }

# 4) 커밋
Write-Host ''
Write-Host "[4/6] 커밋  —  $Message"
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
    Write-Host '       변경 사항이 없어 커밋을 건너뜁니다.' -ForegroundColor DarkGray
}

# 5) 브랜치
Write-Host ''
Write-Host '[5/6] 기본 브랜치를 main 으로'
git branch -M main

# 6) 원격 연결 및 푸시
Write-Host ''
Write-Host '[6/6] 원격 저장소 연결 및 푸시'
git remote get-url origin *> $null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $Repo
} else {
    git remote set-url origin $Repo
}

git push -u origin main
$pushRc = $LASTEXITCODE

Write-Host ''
Write-Host '=========================================================='
if ($pushRc -ne 0) {
    Write-Host '  [실패] 푸시가 완료되지 않았습니다.' -ForegroundColor Red
    Write-Host ''
    Write-Host '  가장 흔한 원인은 인증입니다. GitHub 는 2021년부터'
    Write-Host '  HTTPS 푸시에 계정 비밀번호를 받지 않습니다.'
    Write-Host '  비밀번호 자리에 Personal Access Token 을 넣거나,'
    Write-Host '  아래 중 하나를 먼저 설정하십시오.'
    Write-Host ''
    Write-Host '      gh auth login'
    Write-Host '      또는 Git Credential Manager 설치 확인'
    Write-Host ''
    Write-Host '  저장소가 없다는 오류라면 GitHub 에서 먼저'
    Write-Host '  taeseokyi/psu-meter 저장소를 만들어 주십시오.'
} else {
    Write-Host '  [완료]  https://github.com/taeseokyi/psu-meter' -ForegroundColor Green
}
Write-Host '=========================================================='
Write-Host ''
Read-Host '엔터를 누르면 종료합니다'
exit $pushRc
