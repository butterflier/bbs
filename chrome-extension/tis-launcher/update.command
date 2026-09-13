#!/bin/sh
# 더블클릭하면 최신 버전을 내려받습니다. (macOS)
cd "$(dirname "$0")" || exit 1
git fetch origin claude/intelligent-clarke-li1uhy || exit 1
git pull origin claude/intelligent-clarke-li1uhy || exit 1
echo
echo "업데이트 완료. chrome://extensions 에서 'TIS 교무 런처'의 새로고침(↻)을 눌러주세요."
echo "이 창은 닫으셔도 됩니다."
