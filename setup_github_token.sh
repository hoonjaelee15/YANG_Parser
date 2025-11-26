#!/bin/bash
# GitHub Token 환경 변수 설정 스크립트

echo "=========================================="
echo "GitHub Token 환경 변수 설정"
echo "=========================================="
echo ""

# key 파일에서 토큰 읽기
if [ -f "key" ]; then
    TOKEN=$(cat key | tr -d '\n' | tr -d ' ')
    echo "✅ key 파일에서 토큰을 읽었습니다."
    echo ""
    echo "현재 세션에만 적용 (임시):"
    echo "  export GITHUB_TOKEN=$TOKEN"
    echo ""
    echo "영구적으로 적용하려면 ~/.bashrc 또는 ~/.bash_profile에 추가:"
    echo "  echo 'export GITHUB_TOKEN=$TOKEN' >> ~/.bashrc"
    echo ""
    echo "현재 세션에 적용하시겠습니까? (y/n)"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        export GITHUB_TOKEN=$TOKEN
        echo "✅ 환경 변수가 설정되었습니다!"
        echo "확인: echo \$GITHUB_TOKEN"
    fi
else
    echo "❌ key 파일을 찾을 수 없습니다."
    echo ""
    echo "수동으로 설정하는 방법:"
    echo "  export GITHUB_TOKEN=ghp_your_token_here"
fi

