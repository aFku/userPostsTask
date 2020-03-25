import requests
import json
import math
from collections import Counter
import sys


class Post:

    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])

    def __eq__(self, other):
        for attr in self.__dict__.keys():
            if self.__dict__[attr] != getattr(other, attr, None):
                return False
        return True


class User:

    user_posts = []

    def __init__(self, data: dict, post_dict: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        self.user_posts = post_dict.get(self.id, [])

    def get_posts_count(self):
        return len(self.user_posts)

    def get_coords(self):
        geo = self.address["geo"]
        return (float(geo["lat"]), float(geo["lng"]))


def count_user_posts(user_list: list):
    return [user.name + " napisał(a) " + str(user.get_posts_count()) + " postów." for user in user_list]


def search_nonunique_titles(post_list: list):
    titles_map = Counter([post.title for post in post_list])
    return [title for title in titles_map.keys() if titles_map[title] > 1]


def calc_distance(point1, point2):
    """
    Distance between points --> |AB| = sqrt( (x2-x1)^2 + (y2-y1)^2 )

    Take two tuples with two floats (points). Return magnitude of vector between them.
    """
    calculation = math.pow(point2[0]-point1[0], 2) + math.pow(point2[1]-point1[1], 2)
    return math.sqrt(calculation)


def find_friends(user_list: list):
    """ Return list of two elements tuples. First element -> seeker, Second element -> nearest user. """
    result = []
    for user in user_list:
        best = {"User": None, "Distance": math.inf}
        for others in user_list:
            distance = calc_distance(user.get_coords(), others.get_coords())
            if others is not user and distance < best["Distance"]:
                best["User"] = others
                best["Distance"] = distance
            else:
                pass
        result.append((user.name, best["User"].name))
    return result

def make_relation(post_list: list):
    result = {post.userId: [] for post in post_list}  # Map userId: list of post objects
    for post in post_list:
        result[post.userId].append(post)
    return result

def main():

    try:
        req_users = requests.get("https://jsonplaceholder.typicode.com/users")
        req_posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    except requests.exceptions.RequestException:
        print("Given URLs are unreachable! Leaving...", file=sys.stderr)
        exit()

    users_list = json.loads(req_users.text)
    posts_list = json.loads(req_posts.text)

    posts = [Post(line) for line in posts_list]

    relation = make_relation(posts)

    users = [User(line, relation) for line in users_list]

    print("Initialization completed!\n")

    for user in users:
        print("User with ID: ", str(user.id), " wrote this posts:", user.user_posts)
    print("\n\n")

    for string_ in count_user_posts(users):
        print(string_)

    print("\n\nList of non-unique titles: ", search_nonunique_titles(posts), "\n\n")

    print("Nearest person for each user:")
    for pair in find_friends(users):
        print(pair)


if __name__ == "__main__":
    main()
