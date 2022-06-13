# Every model represents a table in our database.

from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base


class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(length=50), index=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)

    role_id = Column(
        Integer,
        ForeignKey("role.role_id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    role = relationship(
        "Role",
        foreign_keys=[role_id]
    )


class Topic(Base):
    __tablename__ = "topic"

    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(length=100), index=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    created_by = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    updated_by = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])


class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(
        Integer,
        ForeignKey("topic.topic_id", ondelete="CASCADE"),
        nullable=False
    )

    question_text = Column(Text, index=True, nullable=False)
    option_a = Column(String(length=100), nullable=False)
    option_b = Column(String(length=100), nullable=False)
    option_c = Column(String(length=100), nullable=False)
    option_d = Column(String(length=100), nullable=False)
    correct_option = Column(String(length=10), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    created_by = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    updated_by = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )

    topic = relationship("Topic", foreign_keys=[topic_id])
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])


class TopicPlayed(Base):
    __tablename__ = "topic_played"

    topic_played_id = Column(Integer, primary_key=True, index=True)
    played_by = Column(
        Integer,
        ForeignKey("user.user_id", ondelete="CASCADE"),
        nullable=False
    )
    topic_id = Column(
        Integer,
        ForeignKey("topic.topic_id", ondelete="CASCADE"),
        nullable=False
    )
    topic_score = Column(Integer,nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    topic = relationship("Topic", foreign_keys=[topic_id])
    player = relationship("User", foreign_keys=[played_by])
