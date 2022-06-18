from utils.console import print_markdown
import time

from reddit.subreddit import get_posts
from video_creation.background import download_background, chop_background_video
from video_creation.voices import save_text_to_wav
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.final_video import make_final_video
from dotenv import load_dotenv
import os

print_markdown(
    "### Thanks for using this tool! [Feel free to contribute to this project on GitHub!](https://lewismenelaws.com) If you have any questions, feel free to reach out to me on Twitter or submit a GitHub issue."
)

time.sleep(3)
load_dotenv()

thread_count = int(os.getenv("THREADS_COUNT"))
reddit_objects = get_posts(thread_count)

for reddit_post in reddit_objects:
    print("Okaay, let's go")
    length, number_of_comments = save_text_to_wav(reddit_post)
    download_screenshots_of_reddit_posts(reddit_post, number_of_comments, os.getenv("THEME"))
    download_background()
    chop_background_video(length)
    final_video = make_final_video(number_of_comments)
