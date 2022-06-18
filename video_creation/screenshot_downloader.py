from playwright.sync_api import sync_playwright, ViewportSize
from pathlib import Path
from rich.progress import track
from utils.console import print_step, print_substep
import json


NSFW_PROMPT = '[data-testid="content-gate"]'
NSFW_PROMPT_ACCEPT_BUTTON = '[data-testid="content-gate"] button'
THREAD_TITLE_LABEL = '[data-test-id="post-content"]'


def download_screenshots_of_reddit_posts(reddit_object, screenshot_num, theme):
    """Downloads screenshots of reddit posts as they are seen on the web.

    Args:
        reddit_object: The Reddit Object you received in askreddit.py
        screenshot_num: The number of screenshots you want to download.
    """
    print_step("Downloading Screenshots of Reddit Posts 📷")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/png").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser...")

        browser = p.chromium.launch()
        context = browser.new_context()

        if theme.casefold() == "dark":
            cookie_file = open('video_creation/cookies.json')
            cookies = json.load(cookie_file)
            context.add_cookies(cookies)

        # Get the thread screenshot
        page = context.new_page()
        erred = False
        try:
            page.goto(reddit_object["thread_url"])
        except Exception as e:
            print_substep("There was an exception while opening reddit thread. " + str(e))
            print_substep("Something is not ok, will skip this thread.")
            erred = True

        if not erred:
            page.set_viewport_size(ViewportSize(width=1920, height=1080))
            if page.locator(NSFW_PROMPT).is_visible():
                # This means the post is NSFW and requires to click the proceed button.

                print_substep("Post is NSFW. You are spicy...")
                page.locator(NSFW_PROMPT_ACCEPT_BUTTON).click()

            page.locator(THREAD_TITLE_LABEL).screenshot(
                path="assets/png/title.png"
            )

            for idx, comment in track(
                    enumerate(reddit_object["comments"]), "Downloading screenshots..."
            ):
                # Stop if we have reached the screenshot_num
                if idx >= screenshot_num:
                    break

                if page.locator('[data-testid="content-gate"]').is_visible():
                    page.locator('[data-testid="content-gate"] button').click()

                page.goto(f'https://reddit.com{comment["comment_url"]}')
                page.locator(f"#t1_{comment['comment_id']}").screenshot(
                    path=f"assets/png/comment_{idx}.png"
                )

            print_substep("Screenshots downloaded Successfully.",
                          style="bold green")
