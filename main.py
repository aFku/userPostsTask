import requests
import json
import math

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
        self.user_posts = [post for post in posts if post.userId == self.id]

    def post_count(self):
        return len(self.user_posts)

    def get_coords(self):
        geo = self.address["geo"]
        return (float(geo["lat"]), float(geo["lng"]))



def postCounter_allUsers():
    return [user.name + " wrote " + str(user.post_count()) + " posts." for user in users]


def search_nonuniqueTitles():
    return [post.title for post in posts if posts.count(post.title) > 1]


def calc_distance(point1, point2):
    # Distance between points --> |AB| = sqrt( (x2-x1)^2 + (y2-y1)^2 )
    calculation = math.pow(point2[0]-point1[0],2) + math.pow(point2[1]-point1[1] ,2)
    return math.sqrt(calculation)


def find_friends():
    # Return list of two elements tuples. First element -> seeker, Second element -> nearest user
    result = []
    for user in users:
        best = {"User": None, "Distance": math.inf}
        for others in users:
            distance = calc_distance(user.get_coords(), others.get_coords())
            if others is not user and distance < best["Distance"]:
                best["User"] = others
                best["Distance"] = distance
            else:
                pass
        result.append((user.name, best["User"].name))
    return result


if __name__ == "__main__":
    req_users = Request("https://jsonplaceholder.typicode.com/users")
    req_posts = Request("https://jsonplaceholder.typicode.com/posts")

    users_list = json.loads(req_users.get_text())
    posts_list = json.loads(req_posts.get_text())

    posts = [Post(line) for line in posts_list]
    users = [User(line) for line in users_list]

    print("#"*200)

    print(postCounter_allUsers())
    print("\n\n\n\n")
    print(search_nonuniqueTitles())
    print("\n\n\n\n")
    print(find_friends())
    print("\n\n\n\n")

    for x in users:
        print(x.name + ":")
        for k, y in enumerate(x.user_posts):
            print("\t" + str(k + 1) + "." + y.title)
    print("\n\n\n\nEach user wrote 10 posts")

    print(len(set(posts)))
    print("\n\n\n\nNo non-unique titles here")


