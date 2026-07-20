import enum
import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.libs.database import Base, TimestampMixin


class Theme(enum.Enum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    SYSTEM = "SYSTEM"


class Preference(TimestampMixin, Base):
    """
    User configuration preferences.
    Primary key is the user_id (soft reference to auth.users).
    """

    __tablename__ = "preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    timezone: Mapped[str] = mapped_column(String, default="UTC", nullable=False, doc="IANA timezone identifier")
    language: Mapped[str] = mapped_column(String, default="en-US", nullable=False, doc="BCP 47 language tag")
    theme: Mapped[Theme] = mapped_column(default=Theme.SYSTEM, nullable=False)
