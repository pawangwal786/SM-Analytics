import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.auth.app.models.rbac import Permission, Role, RolePermission, UserRole
from backend.services.auth.app.models.user import User, UserStatus


@pytest.mark.asyncio
async def test_user_creation_and_defaults(db_session: AsyncSession):
    user = User(email="test@example.com", password_hash="hashed")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.status == UserStatus.PENDING_VERIFICATION
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_user_email_unique_constraint(db_session: AsyncSession):
    user1 = User(email="unique@example.com", password_hash="hashed")
    db_session.add(user1)
    await db_session.commit()

    user2 = User(email="unique@example.com", password_hash="hashed")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_rbac_cascade_deletes(db_session: AsyncSession):
    user = User(email="cascade@example.com", password_hash="hashed")
    role = Role(name="admin")
    permission = Permission(name="read:all")

    db_session.add_all([user, role, permission])
    await db_session.commit()

    user_role = UserRole(user_id=user.id, role_id=role.id)
    role_permission = RolePermission(role_id=role.id, permission_id=permission.id)

    db_session.add_all([user_role, role_permission])
    await db_session.commit()

    # Delete the user, should cascade to user_roles
    await db_session.delete(user)
    await db_session.commit()

    result = await db_session.execute(select(UserRole).where(UserRole.role_id == role.id))
    assert result.scalar_one_or_none() is None

    # Delete the role, should cascade to role_permissions
    await db_session.delete(role)
    await db_session.commit()

    result = await db_session.execute(select(RolePermission).where(RolePermission.permission_id == permission.id))
    assert result.scalar_one_or_none() is None
