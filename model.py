class RedditModel:
    def __init__(self, reddit_id, name, title, score, url, created_utc):
        self.reddit_id = reddit_id
        self.name = name
        self.title=title
        self.score = score
        self.url = url
        self.created_utc = created_utc

    def __iter__(self):
        return iter([self.reddit_id,
                     self.name,
                     self.title,
                    self.score,
                     self.url,
                     self.created_utc, ])
