from db import engine
from tables import users, posts
from sqlalchemy import insert, select, update, delete, asc, desc, func, text

def create_user(name: str, email: str, phone: int):
  with engine.connect() as conn:
    stmt = insert(users).values(name=name, email=email, phone=phone) 
    conn.execute(stmt)
    conn.commit() 

def create_post(user_id: int, title: str, content: str):
    with engine.connect() as conn:
        stmt = insert(posts).values(user_id=user_id, title=title, content=content)
        conn.execute(stmt)
        conn.commit()

def get_user_by_id(user_id: int):
   with engine.connect() as conn:
        stmt = select(users).where(users.c.id == user_id)
        result = conn.execute(stmt).first()
        return result
   
def get_all_users():
   with engine.connect() as conn:
        stmt = select(users)
        result = conn.execute(stmt).fetchall()
        return result

def get_posts_by_user(user_id: int):
   with engine.connect() as conn:
        stmt = select(posts).where(posts.c.user_id == user_id)
        result = conn.execute(stmt).fetchall()
        return result   

def update_user_email(user_id: int, new_email: str):
   with engine.connect() as conn:
        stmt = update(users).where(users.c.id == user_id).values(email=new_email)
        conn.execute(stmt)
        conn.commit()

def delete_post(post_id: int):
   with engine.connect() as conn:
        stmt = delete(posts).where(posts.c.id == post_id)
        conn.execute(stmt)
        conn.commit()

def get_users_ordered_by_name():
    with engine.connect() as conn:
        stmt = select(users).order_by(asc(users.c.name))
        result = conn.execute(stmt).fetchall()
        return result
    
def get_posts_latest_first():
    with engine.connect() as conn:
        stmt = select(posts).order_by(desc(posts.c.id))
        result = conn.execute(stmt).fetchall()
        return result

def get_post_count_per_user():
    with engine.connect() as conn:
        stmt = select(
            posts.c.user_id,
            func.count(posts.c.id).label("total_posts")
        ).group_by(posts.c.user_id)
        result = conn.execute(stmt).fetchall()
        return result

def get_posts_with_author():
    with engine.connect() as conn:
        stmt = select(
           posts.c.id,
           posts.c.title,
           users.c.name.label("author_name")
        ).join(users, posts.c.user_id == users.c.id)
        result = conn.execute(stmt).fetchall()
        return result
    
def raw_sql_insert():
  with engine.connect() as conn:
    stmt = text("""
                INSERT INTO users (name, email, phone)
                VALUES (:name, :email, :phone)
                """)
    conn.execute(stmt, {"name": "John", "email":"john@gmail.com", "phone": "9011145678"})
    conn.commit() 

def raw_sql_example():
    with engine.connect() as conn:
        stmt = text("SELECT * FROM users WHERE email = :email")
        result = conn.execute(stmt, {"email": "john@gmail.com"}).first()
        return result 