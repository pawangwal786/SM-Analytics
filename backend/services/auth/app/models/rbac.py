import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.libs.database import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents a system role (e.g., admin, manager, standard_user).
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents a specific fine-grained permission (e.g., users:read, users:write).
    """

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class UserRole(Base):
    """
    Association table for User <-> Role many-to-many relationship.
    Uses composite primary key (no surrogate UUID).
    """

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


class RolePermission(Base):
    """
    Association table for Role <-> Permission many-to-many relationship.
    Uses composite primary key (no surrogate UUID).
    """

    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
