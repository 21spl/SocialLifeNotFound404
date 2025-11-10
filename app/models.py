from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql import relationship


class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__="post"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False, server_default="TRUE")
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped["User"] = relationship("User")



class User(Base):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default="now()")


class Vote(Base):
    __tablename__="vote"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCASE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)




    


