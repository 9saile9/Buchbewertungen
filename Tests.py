from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post, PostResponse

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

class PostModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_creation(self):
        u = User(username='author', email='author@example.com')
        db.session.add(u)
        db.session.commit()

        now = datetime.utcnow()
        post = Post(title="Sample Book", general_info="A book about testing", initial_rating=4, author=u, timestamp=now)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(post.title, "Sample Book")
        self.assertEqual(post.general_info, "A book about testing")
        self.assertEqual(post.initial_rating, 4)
        self.assertEqual(post.author.username, "author")

    def test_average_rating(self):
        u = User(username='author', email='author@example.com')
        db.session.add(u)
        db.session.commit()

        post = Post(title="Sample Book", general_info="A book about testing", initial_rating=4.5, author=u)
        db.session.add(post)
        db.session.commit()

        r1 = PostResponse(body="Great book!", rating=5, user=u, post=post)
        r2 = PostResponse(body="Not bad", rating=4, user=u, post=post)
        db.session.add_all([r1, r2])
        db.session.commit()

        average_rating = post.calculate_average_rating()
        self.assertEqual(average_rating, 4.5)

    def test_response_creation(self):
        u = User(username='author', email='author@example.com')
        u2 = User(username='commenter', email='commenter@example.com')
        db.session.add_all([u, u2])
        db.session.commit()

        post = Post(title="Sample Book", general_info="A book about testing", initial_rating=4, author=u)
        db.session.add(post)
        db.session.commit()

        response = PostResponse(body="Great post!", user=u2, post=post)
        db.session.add(response)
        db.session.commit()

        self.assertEqual(response.body, "Great post!")
        self.assertEqual(response.user.username, "commenter")
        self.assertEqual(response.post.title, "Sample Book")

if __name__ == '__main__':
    unittest.main(verbosity=2)
