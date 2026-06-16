# 테트리스 게임 with FastAPI Backend

이메일 기반 사용자 인증과 리더보드 기능을 갖춘 모던 테트리스 게임입니다.

## 기능

- 🎮 클래식 테트리스 게임플레이
- 👤 이메일 기반 회원가입/로그인
- 📊 실시간 리더보드
- 💾 게임 기록 자동 저장
- 🏆 개인 및 전체 순위 추적
- 📱 반응형 디자인 (데스크톱 & 모바일)

## 기술 스택

### Backend
- FastAPI 0.109.0
- SQLAlchemy 2.0.25 (SQLite)
- JWT 인증 (python-jose)
- Bcrypt 비밀번호 해싱 (passlib)

### Frontend
- Vanilla JavaScript
- HTML5 Canvas
- CSS3 (Flexbox, 애니메이션)

## 설치 및 실행

### 1. 백엔드 설정

```bash
cd backend

# Python 가상환경 생성 (선택사항)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 SECRET_KEY를 변경하세요

# 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

백엔드가 http://localhost:8001 에서 실행됩니다.
API 문서: http://localhost:8001/docs

### 2. 프론트엔드 실행

```bash
# 프로젝트 루트 디렉토리에서
python3 -m http.server 5500

# 또는 Node.js가 있다면
npx http-server -p 5500
```

브라우저에서 http://localhost:5500 접속

## API 엔드포인트

### 인증
- `POST /api/v1/auth/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인

### 사용자
- `GET /api/v1/users/me` - 현재 사용자 정보 및 통계

### 게임
- `POST /api/v1/games/submit` - 게임 결과 제출 (인증 필요)
- `GET /api/v1/games/leaderboard` - 리더보드 조회
- `GET /api/v1/games/my-history` - 내 게임 기록 (인증 필요)

## 데이터베이스 스키마

### Users
```sql
- id: INTEGER PRIMARY KEY
- email: VARCHAR(255) UNIQUE
- hashed_password: VARCHAR(255)
- username: VARCHAR(100) UNIQUE
- created_at: DATETIME
- updated_at: DATETIME
- is_active: BOOLEAN
```

### GameRecords
```sql
- id: INTEGER PRIMARY KEY
- user_id: INTEGER (FK -> users.id)
- score: INTEGER
- lines_cleared: INTEGER
- level_reached: INTEGER
- duration_seconds: INTEGER
- played_at: DATETIME
- device_type: VARCHAR(50)
```

## 게임 조작법

### 키보드
- ← / → : 좌우 이동
- ↓ : 소프트 드롭 (빠르게 내리기)
- ↑ / Space : 회전
- Shift : 하드 드롭 (즉시 내리기)
- P / Esc : 일시정지

### 모바일 (터치)
- 좌우 스와이프: 이동
- 위로 스와이프: 회전
- 아래로 스와이프: 소프트 드롭
- 탭: 하드 드롭

## 점수 계산

- 1줄 제거: 100점 × 레벨
- 2줄 제거: 300점 × 레벨
- 3줄 제거: 500점 × 레벨
- 4줄 제거 (테트리스): 800점 × 레벨
- 소프트 드롭: 1점/칸
- 하드 드롭: 2점/칸

## 보안

- 비밀번호는 bcrypt로 해싱 (cost factor 12)
- JWT 토큰 기반 인증 (1시간 유효)
- CORS 설정으로 허용된 오리진만 접근 가능
- 비밀번호 강도 검증 (최소 8자, 대소문자, 숫자 포함)

## 프로덕션 배포

### 백엔드 배포 (예: Railway, Render, DigitalOcean)

1. PostgreSQL 데이터베이스로 변경
   ```python
   # .env
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

2. SECRET_KEY 변경 (32자 이상 랜덤 문자열)
   ```bash
   openssl rand -hex 32
   ```

3. ALLOWED_ORIGINS 업데이트
   ```python
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

### 프론트엔드 배포 (GitHub Pages, Netlify, Vercel)

1. index.html의 API_BASE_URL 수정
   ```javascript
   const API_BASE_URL = 'https://your-backend-domain.com/api/v1';
   ```

2. 정적 파일 배포

## 라이센스

MIT License

## 개발자

개발 기간: 2026년 6월
