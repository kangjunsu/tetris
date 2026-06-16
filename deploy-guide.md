# Tetris 게임 배포 가이드

## 1. GitHub Pages 배포 (추천)

### 옵션 A: gh-pages 브랜치 사용
```bash
# 배포용 디렉토리 생성
mkdir -p gh-pages-deploy
cp tetris.html gh-pages-deploy/index.html

# gh-pages 브랜치 생성 및 배포
git checkout --orphan gh-pages
git rm -rf .
cp tetris.html index.html
git add index.html
git commit -m "Deploy Tetris game"
git push origin gh-pages
git checkout main
```

접속: https://[username].github.io/[repo-name]/

### 옵션 B: docs 폴더 사용
```bash
# docs 폴더 생성
mkdir -p docs
cp tetris.html docs/index.html
git add docs/
git commit -m "Add Tetris game for GitHub Pages"
git push origin main

# GitHub 설정: Settings → Pages → Source: main branch, /docs folder
```

## 2. Netlify Drop (가장 간단)

1. https://app.netlify.com/drop 접속
2. tetris.html 파일을 드래그 앤 드롭
3. 즉시 배포 완료!
4. 무료 URL: https://[랜덤이름].netlify.app

## 3. Vercel (빠르고 강력)

```bash
# Vercel CLI 설치
npm install -g vercel

# 배포
cd [tetris.html이 있는 디렉토리]
vercel

# 프로덕션 배포
vercel --prod
```

## 4. Surge.sh (간단한 CLI)

```bash
# Surge 설치
npm install -g surge

# 배포
surge tetris.html

# 커스텀 도메인
surge tetris.html my-tetris-game.surge.sh
```

## 5. 커스텀 도메인 연결

배포 후 자신의 도메인을 연결하려면:
- GitHub Pages: CNAME 파일 추가
- Netlify/Vercel: 대시보드에서 도메인 설정

## 6. 파일 최적화 (선택사항)

배포 전 HTML 최적화:
```bash
# HTML 압축 (공백 제거)
# 온라인 도구: https://htmlcompressor.com/compressor/
```

## 7. SEO 및 메타태그 추가 (선택사항)

tetris.html에 추가:
```html
<head>
    <!-- 기존 메타태그 아래에 추가 -->
    <meta name="description" content="브라우저에서 즐기는 현대적인 테트리스 게임">
    <meta name="keywords" content="tetris, 테트리스, game, 게임">
    <meta property="og:title" content="테트리스 게임">
    <meta property="og:description" content="브라우저에서 즐기는 현대적인 테트리스">
    <meta property="og:type" content="website">
</head>
```
