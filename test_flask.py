from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://tse2.mm.bing.net/th?id=OIP.Ex0s30pnjZSp8I5UfSAgYQHaGs&pid=Api&P=0&w=177&h=160")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user_profile(self):
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
            # how to test that an img loaded?

    def test_show_edit_form(self):
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}/edit")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
            self.assertIn('<h2>Edit User</h2>', html)


    def test_add_new_user(self):
        with app.test_client() as client:
            d = {"first-name": "Test2", "last-name": "User2", "img-url": "../static/user-solid.svg"}
            response = client.post("/users/new", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<li><a href="/users/2">Test2 User2</a></li>', html)
            


    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         d1 = {"first-name": "Test", "last-name": "User", "img-url": "../static/user-solid.svg"}
    #         
    #         client.post("/users/new", data=d1, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("<h1>TestPet2</h1>", html)

class PostViewsTestCase(TestCase):
    """Tests for views for Post."""
    def setUp(self):
        """Add sample user and sample post."""
        User.query.delete()
        user = User(first_name="Test", last_name="User", image_url="https://tse2.mm.bing.net/th?id=OIP.Ex0s30pnjZSp8I5UfSAgYQHaGs&pid=Api&P=0&w=177&h=160")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        Post.query.delete()
        post = Post(title="Test", content="This is a test!", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_show_post_form(self):
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}/posts/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Add Post for Test User</h1>', html)