import re

def resize_images_in_markdown(md_content):
    # Markdown 이미지 문법을 찾는 정규 표현식
    img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    # 이미지 태그를 HTML로 바꾸는 함수
    def replace_to_html_img(match):
        alt_text = match.group(1)
        img_url = match.group(2)
        return f'<img src="{img_url}" style="width: 50%;" />'

    # 모든 Markdown 이미지 태그를 HTML로 바꿈
    return img_pattern.sub(replace_to_html_img, md_content)