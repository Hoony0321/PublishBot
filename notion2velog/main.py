from time import sleep
from notion2velog.web_actions import init_driver, do_login, write_post, publish_post
import notion2velog.settings as settings
import argparse

def main():
    parser = argparse.ArgumentParser(description='Set settings for the Notion to Velog automation.')
    parser.add_argument('--id', type=str, help='Google ID for Velog')
    parser.add_argument('--pw', type=str, help='Google Password for Velog')
    parser.add_argument('--page', type=str, help='Notion Page ID')
    parser.add_argument('--database', type=str, help='Notion Page ID')

    args = parser.parse_args()

    if args.id is not None:
        settings.VELOG_GOOGLE_ID = args.id
    if args.pw is not None:
        settings.VELOG_GOOGLE_PASSWORD = args.pw
    if args.page is not None:
        settings.NOTION_PAGE_ID = args.page
    if args.database is not None:
        settings.NOTION_DATABASE_ID = args.database


    driver = init_driver()
    do_login(driver)
    write_post(driver)
    publish_post(driver)
    sleep(settings.SEC_WAIT_VERY_LONG)

# main에서 실행하지 않으면 오류가 남
# https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/486#issuecomment-1032009193 참조
if __name__ == "__main__":
    main()
