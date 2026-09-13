@echo off
REM 더블클릭하면 최신 버전을 내려받습니다. (Windows)
cd /d "%~dp0"
git fetch origin claude/intelligent-clarke-li1uhy || goto :err
git pull origin claude/intelligent-clarke-li1uhy || goto :err
echo.
echo 업데이트 완료. chrome://extensions 에서 'TIS 교무 런처'의 새로고침 버튼을 눌러주세요.
pause
exit /b 0
:err
echo.
echo 업데이트에 실패했습니다. 인터넷 연결과 git 설치 여부를 확인해주세요.
pause
exit /b 1
