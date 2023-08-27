import requests
from notion2velog.settings import NOTION_API_KEY
from notion2md.exporter.block import MarkdownExporter, StringExporter

# 헤더 설정
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-02-22",  # 이 버전은 변경될 수 있으므로 Notion API 문서를 확인하세요.
    "Content-Type": "application/json"
}


def get_notion_database(database_id):
    # API endpoint 설정
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    # API 요청
    response = requests.post(url, headers=headers)
    data = response.json()

    # 데이터 출력
    return data

def get_notion_page(page_id):
    # API endpoint 설정
    url = f"https://api.notion.com/v1/pages/{page_id}"

    # 페이지 내용 가져오기
    response = requests.get(url, headers=headers)
    data = response.json()

    # 데이터 반환
    return data

def get_title_and_tag_in_page(page_data):
    properties = page_data["properties"]

    raw_title = properties["Name"]["title"][0]["plain_text"]
    title = 'TIL - ' + raw_title.split()[-1]

    raw_tags = properties["태그"]["multi_select"]
    tags = [tag["name"] for tag in raw_tags]

    return title, tags

def get_notion_blocks(page_id):
    # API endpoint 설정
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    # 페이지의 block 정보 가져오기
    response = requests.get(url, headers=headers)
    data = response.json()

    # 데이터 출력
    return data["results"]

def notion_to_markdown(page_id):
    md = StringExporter(block_id=page_id, output_path="./").export()
    return md

