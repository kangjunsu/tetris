#!/bin/bash

# GitHub 개인 랜딩 페이지 배포 스크립트
# 사용법: ./github-pages-deploy.sh [GitHub-username]

echo "==================================="
echo "GitHub Pages 개인 랜딩 페이지 배포"
echo "==================================="
echo ""

# GitHub username 입력
if [ -z "$1" ]; then
    read -p "GitHub username을 입력하세요: " GITHUB_USER
else
    GITHUB_USER=$1
fi

REPO_NAME="${GITHUB_USER}.github.io"
echo ""
echo "저장소 이름: ${REPO_NAME}"
echo ""

# 현재 디렉토리 저장
CURRENT_DIR=$(pwd)
TETRIS_FILE="${CURRENT_DIR}/tetris.html"

# 저장소가 이미 있는지 확인
if [ -d "$HOME/${REPO_NAME}" ]; then
    echo "⚠️  ${REPO_NAME} 디렉토리가 이미 존재합니다."
    read -p "기존 디렉토리를 사용하시겠습니까? (y/n): " USE_EXISTING

    if [ "$USE_EXISTING" = "y" ] || [ "$USE_EXISTING" = "Y" ]; then
        cd "$HOME/${REPO_NAME}"
    else
        echo "다른 이름을 사용하거나 기존 디렉토리를 삭제해주세요."
        exit 1
    fi
else
    # 임시 디렉토리로 이동
    cd $HOME

    # 새 저장소 클론 또는 초기화
    echo "GitHub에서 ${REPO_NAME} 저장소를 찾습니다..."

    if git ls-remote "git@github.com:${GITHUB_USER}/${REPO_NAME}.git" &> /dev/null; then
        echo "✓ 저장소가 존재합니다. 클론합니다..."
        git clone "git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
        cd "${REPO_NAME}"
    else
        echo "✗ 저장소가 없습니다."
        echo ""
        echo "=========================================="
        echo "GitHub에서 새 저장소를 생성해야 합니다:"
        echo "=========================================="
        echo "1. https://github.com/new 접속"
        echo "2. Repository name: ${REPO_NAME}"
        echo "3. Public 선택"
        echo "4. Create repository 클릭"
        echo ""
        read -p "저장소를 생성했습니까? (y/n): " CREATED

        if [ "$CREATED" = "y" ] || [ "$CREATED" = "Y" ]; then
            mkdir "${REPO_NAME}"
            cd "${REPO_NAME}"
            git init
            git remote add origin "git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
        else
            echo "저장소 생성 후 다시 실행해주세요."
            exit 1
        fi
    fi
fi

# 파일 복사
echo ""
echo "테트리스 게임을 복사합니다..."
cp "${TETRIS_FILE}" index.html

# README 생성
cat > README.md << 'EOF'
# 🎮 My Games Portfolio

Personal gaming portfolio hosted on GitHub Pages.

## Games

- [Tetris](index.html) - Classic Tetris with modern UI/UX

## Features

- Modern glassmorphism design
- Mobile responsive
- Touch controls for mobile devices
- Ghost piece preview
- Combo messages
- Best score tracking

---

Built with ❤️ by Claude Code
EOF

# Git 커밋
echo ""
echo "Git 커밋을 생성합니다..."
git add index.html README.md
git commit -m "Add Tetris game to personal landing page

- Modern UI with glassmorphism effects
- Mobile-responsive design with touch controls
- Ghost piece preview and combo messages
- Best score tracking with localStorage

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 푸시
echo ""
echo "GitHub에 푸시합니다..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 배포 완료!"
echo ""
echo "=========================================="
echo "접속 URL (5-10분 후 활성화):"
echo "https://${GITHUB_USER}.github.io/"
echo "=========================================="
echo ""
echo "GitHub Pages 설정 확인:"
echo "https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages"
