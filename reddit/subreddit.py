from utils.console import print_markdown, print_step, print_substep
import praw
import random
from dotenv import load_dotenv
import os


def get_subreddit_threads():

    """
    Returns a list of threads from the AskReddit subreddit.
    """

    load_dotenv()

    print_step("Getting AskReddit threads...")

    if os.getenv("REDDIT_2FA").lower() == "yes":
        print(
            "\nEnter your two-factor authentication code from your authenticator app.\n"
        )
        code = input("> ")
        print()
        pw = os.getenv("REDDIT_PASSWORD")
        passkey = f"{pw}:{code}"
    else:
        passkey = os.getenv("REDDIT_PASSWORD")

    content = {}

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing AskReddit threads",
        username=os.getenv("REDDIT_USERNAME"),
        password=passkey,
    )

    if os.getenv("SUBREDDIT"):
        subreddit = reddit.subreddit(os.getenv("SUBREDDIT"))
    else:
        # ! Prompt the user to enter a subreddit
        try:
            subreddit = reddit.subreddit(
                input("What subreddit would you like to pull from? ")
            )
        except ValueError:
            subreddit = reddit.subreddit("askreddit")
            print_substep("Subreddit not defined. Using AskReddit.")

    threads = subreddit.hot(limit=25)

    should_continue = True

    while should_continue:
        # TODO: threads is probably some sort of async thing, this is why for loop doesn't work, please check
        submission = list(threads)[random.randrange(0, 25)]
        print_substep(f"Video will be: {submission.title} :thumbsup:")
        accept_thread = input("> Continue? Y/N: ")
        if accept_thread is "Y" or "y":
            should_continue = False
            print("Okaay, let's go")
            try:

                content["thread_url"] = submission.url
                content["thread_title"] = submission.title
                content["comments"] = []

                for top_level_comment in submission.comments:
                    content["comments"].append(
                        {
                            "comment_body": top_level_comment.body,
                            "comment_url": top_level_comment.permalink,
                            "comment_id": top_level_comment.id,
                        }
                    )

            except AttributeError as e:
                pass
            print_substep("Received AskReddit threads successfully.", style="bold green")
        else:
            print("Okay, skipping this one.")

    return content
