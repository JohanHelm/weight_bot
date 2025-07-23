import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    text,
    Float,
    Index,
)
from sqlalchemy.orm import relationship

from database.connection import Base


class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    telegram_id = Column(Integer, nullable=False, index=True)
    role = Column(
        Enum(RoleEnum),
        nullable=False,
        default=RoleEnum.user,
        server_default=text("'user'")
    )

    weighins = relationship("Weights", back_populates="user")

    __table_args__ = (UniqueConstraint('username', name='uq_user_name'),
                      UniqueConstraint('telegram_id', name='uq_telegram_id'),
                      )


class Weights(Base):
    __tablename__ = "weighins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="weighins")
    __table_args__ = (
        Index("ix_weighins_user_id", "user_id"),
        Index("ix_weighins_date_time", "date_time"),
    )
