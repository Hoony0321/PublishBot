import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from notion2velog.settings import *
from notion2velog.notion_api import notion_to_markdown, get_notion_page, get_title_and_tag_in_page
from notion2velog.utils import resize_images_in_markdown



velog_google_login_url = 'https://v2.velog.io/api/v2/auth/social/redirect/google?next=/&isIntegrate=0'

def init_driver():
    driver = uc.Chrome()
    return driver

# Velog 로그인 함수 - 구글 로그인 (인증은 수동)
def do_login(driver):

    # Velog 구글 로그인 페이지로 이동
    driver.get(velog_google_login_url)

    # ID 입력
    email_elem = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_elem.send_keys(VELOG_GOOGLE_ID)
    email_elem.send_keys(Keys.RETURN)

    # 비밀번호 입력
    password_elem = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='password' or @name='Passwd']"))
    )
    password_elem.send_keys(VELOG_GOOGLE_PASSWORD)
    password_elem.send_keys(Keys.RETURN)

    #TODO : 이 사이에 사용자 구글 인증을 수동으로 진행해야함 -> 자동화 필요

    # 로그인 완료까지 기다림
    WebDriverWait(driver, SEC_WAIT_LONG).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="새 글 작성"]'))
    )

# Velog 글 작성 함수
def write_post(driver):
    # Notion 페이지에서 글 제목 & 태그 & 본문 내용을 가져옵니다.
    page_data = get_notion_page(NOTION_PAGE_ID)
    title, tags = get_title_and_tag_in_page(page_data)
    content = notion_to_markdown(NOTION_PAGE_ID)
    content = resize_images_in_markdown(content)
    escaped_content = json.dumps(content)

    # 새 글 작성 버튼 클릭
    driver.find_element(By.XPATH,'//button[text()="새 글 작성"]').click()

    # 제목 입력창이 나올 때까지 기다림
    titleElement =  WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.element_to_be_clickable((By.XPATH, '//textarea[@placeholder="제목을 입력하세요"]'))
    )
    # 제목 입력
    titleElement.send_keys(title, Keys.ENTER)
    
    # 태그 입력창이 나올 때까지 기다림
    tagElement = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="태그를 입력하세요"]'))
    )
    # 태그 입력
    for tag in tags:
        tagElement.send_keys(tag, Keys.ENTER)

    # 본문 입력 (WebDriverWait로 기다리면 CodeMirror가 로드되지 않아서 에러가 남)
    js_script = f"""
    var cm = document.querySelector('.CodeMirror').CodeMirror;
    cm.setValue({escaped_content});
    """
    driver.execute_script(js_script)

    # 글 작성 버튼 클릭
    postElement = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="출간하기"]'))
    )
    postElement.click()

# Velog 글 출간 함수
def publish_post(driver):

    # 시리즈 설정 버튼 클릭
    series_set_element = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="시리즈에 추가하기"]'))
    )
    series_set_element.click()

    # "Daily" 텍스트를 가진 리스트 아이템이 나타날 때까지 기다림
    daily_element = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.presence_of_element_located((By.XPATH, '//li[text()="Daily"]'))
    )
    # 리스트 아이템 클릭
    daily_element.click()

    # 선택하기 버튼 클릭
    select_element = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="선택하기"]'))
    )
    select_element.click()

    # '출간하기' 버튼을 모두 찾습니다.
    publish_buttons = WebDriverWait(driver, SEC_WAIT_SHORT).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[text()="출간하기"]'))
    )

    # y값이 가장 작은 버튼을 찾습니다. (가장 위에 있는 버튼)
    top_button = min(publish_buttons, key=lambda button: button.location['y'])

    # y값이 가장 작은 버튼을 클릭합니다.
    top_button.click()