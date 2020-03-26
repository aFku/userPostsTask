import unittest
import main
import json
from contextlib import contextmanager
import sys


@contextmanager
def supp_stderr():
    save_stderr = sys.stderr    # save stderr

    class NullStd(object):
        def write(self, _): pass
    sys.stderr = NullStd()     # create object which data from print()
    try:
        yield          # call generator
    finally:
        sys.stderr = save_stderr   # make stderr to it`s previous state

with open("examples/example_test_post.json", "r") as posts_file, \
     open("examples/example_test_user.json", "r") as users_file, \
     open("examples/example_single_post.json", "r") as s_post, \
     open("examples/example_single_user.json", "r") as s_user:
    posts_test = json.loads(''.join(posts_file.readlines()))
    users_test = json.loads(''.join(users_file.readlines()))
    single_post = json.loads(''.join(s_post.readlines()))
    single_user = json.loads(''.join(s_user.readlines()))


def create_post_list(post_source):
    return [main.Post(post) for post in post_source]


def create_user_list(user_source, post_source):
    relation = main.make_relation(create_post_list(post_source))
    return [main.User(user, relation) for user in user_source]


class TestPost(unittest.TestCase):

    def test_create_post_from_json(self):
        try:
            create_post_list(posts_test)
        except:
            self.fail("Cannot create Post instance!")

    def test_if_post_created_correctly_from_json(self):
        post = main.Post(single_post[0])
        check = main.Post({})
        check_attr = (("userId", 10), ("id", 123), ("title", "Beautiful weather!"),
                      ("body", "Hello! Such a beautiful day"))
        for key, value in check_attr:
            check.__setattr__(key, value)
        self.assertEqual(post, check)


    def test_search_nonunique(self):
        self.assertEqual(main.search_nonunique_titles(create_post_list(posts_test)), ["Sad weather!"])

    def test_make_relation(self):
        posts = create_post_list(posts_test)
        id_ = (1, 3, 5)
        check = ([main.Post({"userId": 1, "id": 1, "title": "Beautiful weather!", "body": "Hello! Such a beautiful day"}),
                  main.Post({"userId": 1, "id": 21, "title": "Sad weather!", "body": "Haha, I lied! :)"})],
                 [main.Post({"userId": 3, "id": 54, "title": "Future plans", "body": "Tomorrow I will go to cinema!"})],
                 [main.Post({"userId": 5, "id": 23, "title": "Sad weather!", "body": "Such a lonely day ~ System of a down"}),
                  main.Post({"userId": 5, "id": 10, "title": "Bored!", "body": "This boredom is very annoying!"}),
                  main.Post({"userId": 5, "id": 101, "title": "Lier!", "body": "I don`t like liers!"})])
        check_dict = dict(zip(id_, check))
        self.assertEqual(main.make_relation(posts), check_dict)


class TestUser(unittest.TestCase):

    def test_create_user_from_json(self):
        try:
            create_user_list(users_test, posts_test)
        except:
            self.fail("Cannot create User instance!")

    def test_if_user_created_correctly_from_json(self):
        user = main.User(single_user[0], {})

        with supp_stderr():
            check = main.User({}, {})   # need to suppress stderr, because empty object has not id attribute

        check_attr = (("id", 1), ("name", "Leanne Graham"), ("username", "Bret"), ("email", "Sincere@april.biz"),
                      ("address", {"street": "Kulas Light", "suite": "Apt. 556", "city": "Gwenborough",
                                   "zipcode": "92998-3874", "geo": {"lat": "-37.3159", "lng": "81.1496"}}))
        for key, value in check_attr:
            check.__setattr__(key, value)
        self.assertEqual(user, check)

    def test_post_count(self):
        users = create_user_list(users_test, posts_test)
        for user, posts_count in zip(users, (2, 3, 1, 0)):
            self.assertEqual(user.get_posts_count(), posts_count)

    def test_get_coords(self):
        users = create_user_list(users_test, posts_test)
        for user, coords in zip(users, ((-37.3159, 81.1496), (-43.9509, -34.4618),
                                        (-68.6102, -47.0653), (29.4572, -164.2990))):
            self.assertEqual(user.get_coords(), coords)

    def test_count_user_posts(self):
        users = create_user_list(users_test, posts_test)
        message = ["Leanne Graham napisał(a) 2 postów.", "Ervin Howell napisał(a) 3 postów.",
                   "Clementine Bauch napisał(a) 1 postów.", "Patricia Lebsack napisał(a) 0 postów."]
        self.assertEqual(main.count_user_posts(users), message)

    def test_find_friends(self):
        users = create_user_list(users_test, posts_test)
        friends = [("Leanne Graham", "Ervin Howell"), ("Ervin Howell", "Clementine Bauch"),
                   ("Clementine Bauch", "Ervin Howell"), ("Patricia Lebsack", "Ervin Howell")]
        self.assertEqual(main.find_friends(users), friends)


class TestOtherGlobals(unittest.TestCase):

    def test_calc_distance(self):
        self.assertEqual(round(main.calc_distance((1, 5), (3, 9)), 5), 4.47214)
        self.assertEqual(round(main.calc_distance((1, 1), (1, 1)), 5), 0)
        self.assertEqual(round(main.calc_distance((-43, 0), (-12, -6)), 5), 31.57531)
        self.assertEqual(round(main.calc_distance((0.4, 2), (-2.3, 97.3)), 5), 95.33824)









