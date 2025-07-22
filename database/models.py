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

    __table_args__ = (UniqueConstraint('username', name='uq_user_name'),
                      UniqueConstraint('telegram_id', name='uq_telegram_id'),
                      )
