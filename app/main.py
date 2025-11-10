from fastapi import FastAPI
from .database import create_db_and_tables


from contextlib import asynccontextmanager




# Creating lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield create_db_and_tables()

# Create the FastAPI instance
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}




@app.get("/sqlalchemy")
def test_posts(Post, db):
    posts = db.query(Post).all()
    return {"posts": posts}

@app.get("/posts")
def get_posts(Post, db):
    posts = db.query(Post).all()
    return {"posts": posts}


