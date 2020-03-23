import requests
import json

posts = []
users = []


class Request:
    _req = None

    def __init__(self, url: str):
        self._req = requests.get(url)

    def get_text(self):
        return self._req.text

    def __str__(self):
        return self._req.url


class Post:

    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])


class User:

    user_posts = []

    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        self.check_new_posts()

    def check_new_posts(self):
        global posts
        self.user_posts = [post for post in posts if post.userId == self.id]



if __name__ == "__main__":
    req_users = Request("https://jsonplaceholder.typicode.com/users")
    req_posts = Request("https://jsonplaceholder.typicode.com/posts")

    users_list = json.loads(req_users.get_text())
    posts_list = json.loads(req_posts.get_text())

    posts = [Post(line) for line in posts_list]
    users = [User(line) for line in users_list]


    for x in users:
        print(x.name + ":")
        for k,y in enumerate(x.user_posts):
            print("\t" + str(k+1) + "." + y.title)


