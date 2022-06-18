from praw import models


class Post:
    def __init__(self, submission):
        self.url = None
        self.title = None
        self.comments = None
        self.is_valid = False

        try:
            self.url = submission.url
            self.title = submission.title
            self.comments = []

            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, models.MoreComments):
                    continue
                self.comments.append(
                    {
                        "comment_body": top_level_comment.body,
                        "comment_url": top_level_comment.permalink,
                        "comment_id": top_level_comment.id,
                    }
                )
            self.is_valid = True
            print("Received AskReddit threads successfully.")
        except AttributeError as e:
            print('Warn! ', str(e))

