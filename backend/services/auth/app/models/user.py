import enum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.libs.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    SUSPENDED = "SUSPENDED"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents an identity within the system.
    Only security-critical information is stored here.
    Presentation data (like username, bio, avatar) belongs in the Users service.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.PENDING_VERIFICATION, index=True, nullable=False)
