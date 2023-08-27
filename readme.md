# Notion to Velog 자동화봇

한 줄 소개: Notion 기록을 자동으로 Velog에 게시해주는 자동화 툴입니다.
사용기술: Notion API, Python, Selenium, Zapier
프로젝트 기간: 2023년 8월 13일 → 2023년 8월 27일

# ❤️ Motivation

Notion에 하루하루 개발했던 내용이나 의미있던 경험을 기록한다.

그리고 해당 내용을 정리해서 Velog에 게시한다.

하지만 이런 일련의 과정이 귀찮아서 이를 한번에 자동화 시키는 봇을 만들고자 한다.

# 🎮 서비스 소개

`Notion`에 기록했던 내용을 `Velog`에 게시하는 일련의 과정을 자동화 시켜주는, 일명 `PublishBot`이다.

1. `Notion API` 를 통해 Notion에 기록한 내용을 가져오고,
2. `Python Selenium`을 통해 웹 프론트와 로그인 및 상호작용을 하여 게시하고,
3. `Zapier` 를 통해 배치 작업으로 매일 일정시간에 해당 로봇이 돌 수 있게 해줄 예정이다.

~~(배치 작업을 하기 위해선, `로그인 자동화` & `서버 배포` 까지 해야해서 일단은 1,2번만 진행하고 추후에 3번을 진행할 예정이다.)~~

# ✍🏻 사용 방법

1. `notion2velog/settings.py` 상수값 설정 (이후에 CLI 파라미터로 해당 값 넘겨줄 수 있음)

   ```
   NOTION_API_KEY = "[NOTION_API_KEY]"
   NOTION_DATABASE_ID = "[NOTION_DATABASE_ID]"
   NOTION_PAGE_ID = '[NOTION_PAGE_ID]'
   VELOG_GOOGLE_ID = "[VELOG 계정 ID(GOOGLE)]"
   VELOG_GOOGLE_PASSWORD = "[VELOG 계정 PW(GOOGLE)]"
   ```

2. **터미널 CLI로 실행 (값 안 넘겨주면 settings.py에 설정된 값으로 들어감)**

   ```bash
   notion2velog --id [google_id] --pw [google_pw] --database [database_id] --page [page_id]
   ```

# 🚦자동화 부분

- 기록한 Notion 내용 → `markdown`으로 다운로드
- Velog `로그인`
- Velog `새 글 작성` 클릭
- Velog `제목 및 태그` 설정
- Velog `본문` 작성
  - Notion에서 `markdown 문법`으로 다운받은 내용 넣기
  - `이미지`는 local 환경에서 직접 업로드
- 게시하기 → 올릴 `시리즈` 설정

# 🕹️ 개발 기능

- **자동 로그인** 기능 구현
  - `selenium` 이용
- **Notion 게시글 정보 가져오기** 기능 구현
  - `Notion API` 이용
  - 제목 / 태그 / 날짜 / 본문 내용 정보 이용
  - `Notion2md` 라이브러리를 이용하여 Notion 게시글을 `markdown` 폼으로 변형해서 사용
- **Velog** **자동 게시** 기능 구현
  - Velog 자체에서 따로 API를 제공하지 않아서 `Selenium`을 이용
  - 제목 설정 / 태그 설정 / 시리즈 설정 / 본문 설정
  - Velog는 본문 내용 입력 받을때 `CodeMirror` 라는 웹 에디터를 이용함.
    ⇒ `Selenium WebDriver` 을 이용해서 본문 내용 입력 불가.
    ⇒ **js_script**를 이용해서 요소 자체에 접근해서 본문 내용 입력함.
    (+특수문자 이용을 위해서 **문자열 escape** 시킨 후 입력함)
    ```tsx
    js_script = f"""
      var cm = document.querySelector('.CodeMirror').CodeMirror;
      cm.setValue({escaped_content});
      """
    driver.execute_script(js_script)
    ```
- **CLI 방식**을 통한 게시 기능 구현
  기존에서 [settings.py](http://settings.py) 설정을 하고 main.py를 실행시키는 방식으로 자동화 코드 실행시킴
  ⇒ 계속 IDE를 키도 설정하는 방식이 번거로움.
  따라서 **터미널 CLI**를 통해서 **자동 게시글 업로드 기능**을 구현하고자 함.
