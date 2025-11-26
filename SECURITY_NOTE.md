# 보안 주의사항

## ⚠️ Personal Access Token은 Git에 커밋하지 마세요!

GitHub의 Push Protection 기능이 Personal Access Token을 자동으로 감지하고 푸시를 차단합니다.

## 안전한 토큰 관리 방법

### 방법 1: 환경 변수 사용 (권장)
```bash
export GITHUB_TOKEN=ghp_your_token_here
git push origin main
```

### 방법 2: Git Credential Helper
```bash
git config --global credential.helper store
# 첫 푸시 시 토큰 입력하면 자동 저장
```

### 방법 3: SSH 키 사용
```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개 키를 GitHub에 추가
# https://github.com/settings/keys
```

## .gitignore에 추가된 항목
- `*.key`
- `*.token`
- `*credentials*`
- `.env`

이제 key 파일은 자동으로 무시됩니다.

