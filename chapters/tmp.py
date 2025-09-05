from models import User, Post
from db import SessionLocal
from sqlalchemy import select, asc 

def create_user(name: str, email:str):
  with SessionLocal() as session:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 

def create_post(user_id: int, title: str, content:str):
  with SessionLocal() as session:
    post = Post(user_id=user_id, title=title, content=content)
    session.add(post)
    session.commit()

def get_user_by_id(user_id: int):
    with SessionLocal() as session:
      user = session.get_one(User, user_id)
      return user

def get_post_by_id(post_id: int):
    with SessionLocal() as session:
      stmt = select(Post).where(Post.id == post_id)
      post = session.scalars(stmt).one()
      return post 

def get_all_users():
    with SessionLocal() as session:
       stmt = select(User)
       users = session.scalars(stmt).all()
       return users

def get_posts_by_user(user_id: int):
    with SessionLocal() as session:
       user = session.get(User, user_id)
       posts = user.posts if user else []
       return posts

def update_user_email(user_id: int, new_email: str):
    with SessionLocal() as session:
       user = session.get(User, user_id)
       if user:
          user.email = new_email
          session.commit()
       return user 

def get_users_ordered_by_name():
    with SessionLocal() as session:
       stmt = select(User).order_by(asc(User.name))
       users = session.scalars(stmt).all()
       return users 