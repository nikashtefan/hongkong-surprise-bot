"""
SQLAlchemy модели для Quest Bot.
"""

from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


class QuestDay(Base):
    """Модель дня квеста."""

    __tablename__ = "quest_days"

    id = Column(Integer, primary_key=True)
    day_number = Column(Integer, nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    questions = relationship("Question", back_populates="day", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<QuestDay(id={self.id}, day_number={self.day_number}, title={self.title})>"


class Question(Base):
    """Модель вопроса квеста."""

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("quest_days.id", ondelete="CASCADE"), nullable=False)
    question_order = Column(Integer, nullable=False)
    question_type = Column(String(50), nullable=False)
    question_text = Column(Text, nullable=False)
    hint = Column(Text, nullable=True)

    options = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    correct_answers = Column(Text, nullable=True)

    success_message = Column(Text, nullable=True)
    fail_message = Column(Text, nullable=True)

    is_required = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    day = relationship("QuestDay", back_populates="questions")

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, day_id={self.day_id}, order={self.question_order})>"


class User(Base):
    """Модель пользователя бота."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)

    current_day = Column(Integer, default=1)
    current_question = Column(Integer, default=1)
    quest_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    answers = relationship("UserAnswer", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"


class UserAnswer(Base):
    """Модель ответа пользователя на вопрос."""

    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    attempts = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="answers")

    def __repr__(self) -> str:
        return f"<UserAnswer(id={self.id}, user_id={self.user_id}, question_id={self.question_id})>"
