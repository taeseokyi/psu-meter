@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set REPO=https://github.com/taeseokyi/psu-meter.git

rem 커밋 메시지: 인자로 주면 그것을, 없으면 기본값을 쓴다.
rem   push.bat "회절 모델 수정"
set "MSG=%~1"
if "%MSG%"=="" set "MSG=설계 자료 갱신"

echo ==========================================================
echo   psu-meter  ^-^>  GitHub push
echo   %REPO%
echo ==========================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo [오류] git 을 찾을 수 없습니다.
  echo        Git for Windows 를 설치했는지, PATH 에 등록되어 있는지 확인하세요.
  echo.
  pause
  exit /b 1
)

if not exist ".git" (
  echo [1/6] 저장소 초기화
  git init
  if errorlevel 1 goto :fail
) else (
  echo [1/6] 기존 저장소를 그대로 사용합니다
)

echo.
echo [2/6] 한글 파일명이 깨져 보이지 않도록 설정
git config core.quotepath false

echo.
echo [3/6] 파일 추가
git add -A
if errorlevel 1 goto :fail

echo.
echo [4/6] 커밋  -  %MSG%
git commit -m "%MSG%"
if errorlevel 1 (
  echo        변경 사항이 없어 커밋을 건너뜁니다.
)

echo.
echo [5/6] 기본 브랜치를 main 으로
git branch -M main

echo.
echo [6/6] 원격 저장소 연결 및 푸시
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin %REPO%
) else (
  git remote set-url origin %REPO%
)

git push -u origin main
set PUSHRC=%errorlevel%

echo.
echo ==========================================================
if not "%PUSHRC%"=="0" (
  echo   [실패] 푸시가 완료되지 않았습니다.
  echo.
  echo   가장 흔한 원인은 인증입니다. GitHub 는 2021년부터
  echo   HTTPS 푸시에 계정 비밀번호를 받지 않습니다.
  echo   비밀번호 자리에 Personal Access Token 을 넣거나,
  echo   아래 중 하나를 먼저 설정하십시오.
  echo.
  echo     gh auth login
  echo     또는 Git Credential Manager 설치 확인
  echo.
  echo   저장소가 없다는 오류라면 GitHub 에서 먼저
  echo   taeseokyi/psu-meter 저장소를 만들어 주십시오.
) else (
  echo   [완료]  https://github.com/taeseokyi/psu-meter
)
echo ==========================================================
echo.
pause
exit /b %PUSHRC%

:fail
echo.
echo [오류] 위 단계에서 실패했습니다. 메시지를 확인하십시오.
echo.
pause
exit /b 1
