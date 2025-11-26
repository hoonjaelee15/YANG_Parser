# GitHub Token 환경 변수 설정 가이드

## 방법 1: 현재 세션에만 적용 (임시)

터미널에서 직접 실행:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**특징:**
- 현재 터미널 세션에서만 유효
- 터미널을 닫으면 사라짐
- 다른 터미널에는 적용되지 않음

**확인 방법:**
```bash
echo $GITHUB_TOKEN
```

## 방법 2: 영구적으로 적용 (권장)

### 2-1. ~/.bashrc에 추가

```bash
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### 2-2. ~/.bash_profile에 추가 (macOS)

```bash
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.bash_profile
source ~/.bash_profile
```

### 2-3. ~/.profile에 추가 (일부 시스템)

```bash
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.profile
source ~/.profile
```

**특징:**
- 모든 새 터미널 세션에 자동 적용
- 시스템 재시작 후에도 유지

## 방법 3: 스크립트 사용

프로젝트 디렉토리에서:

```bash
./setup_github_token.sh
```

또는:

```bash
bash setup_github_token.sh
```

## 방법 4: .env 파일 사용 (프로젝트별)

```bash
# .env 파일 생성
echo 'GITHUB_TOKEN=ghp_your_token_here' > .env

# 사용 시
source .env
```

**주의:** `.env` 파일은 `.gitignore`에 추가되어 있어야 합니다!

## 사용 예시

### Git 푸시 시 자동 사용

환경 변수가 설정되면 Git이 자동으로 사용합니다:

```bash
git push origin main
```

### 수동으로 사용

```bash
# API 호출 시
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# 또는
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/hoonjaelee15/YANG_Parser
```

## 확인 방법

```bash
# 환경 변수 확인
echo $GITHUB_TOKEN

# Git에서 사용 확인
git config --global credential.helper store
git push origin main  # 이제 토큰 입력 없이 작동
```

## 보안 주의사항

⚠️ **중요:**
- 환경 변수는 `ps aux` 명령으로 볼 수 있습니다
- 스크립트에 하드코딩하지 마세요
- 공개 저장소에 토큰을 커밋하지 마세요
- `.env` 파일은 `.gitignore`에 추가하세요

## 문제 해결

### 환경 변수가 적용되지 않을 때

```bash
# 현재 셸에서 확인
echo $GITHUB_TOKEN

# 셸 재시작
exec bash

# 또는
source ~/.bashrc
```

### 다른 셸 사용 시

- **zsh**: `~/.zshrc`에 추가
- **fish**: `~/.config/fish/config.fish`에 `set -gx GITHUB_TOKEN "..."` 추가



