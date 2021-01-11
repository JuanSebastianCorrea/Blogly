"""Seed file to make sample data for users db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# ////////////////////////////
# Add users
mario = User(first_name='Mario', last_name='Bro', image_url="https://vignette.wikia.nocookie.net/ssb/images/4/47/Mario_%28NSMBU%29.png/revision/latest?cb=20130617010229")
bowser = User(first_name='Bowser', last_name="Koopa", image_url="http://en.wikipedia.org/wiki/Special:FilePath/BowserNSMBUD.png")
luigi = User(first_name='Luigi', last_name='Bro', image_url="http://2.bp.blogspot.com/-WrWwCnEkaVY/UiN-1xlLppI/AAAAAAAAAKM/blgGlLOa7yI/s1600/Luigi_SM3DW.png")
yoshi = User(first_name='Yoshi', last_name='Dino')


# Add new objects to session, so they'll persist
db.session.add_all([mario, bowser, luigi, yoshi])

# Commit--otherwise, this never gets saved!
db.session.commit()

# ////////////////////////////
# Add posts
post1 = Post(title="Mushrooms", content="Good mushroom!", user_id=1)
post2 = Post(title="Plumbing Services", content="Call us! We're the best!", user_id=3)
db.session.add_all([post1, post2])
db.session.commit()


# ////////////////////////////
# Add tags
tag1 = Tag(name="Fun")
tag2 = Tag(name="Plumbing")

db.session.add_all([tag1, tag2])
db.session.commit()