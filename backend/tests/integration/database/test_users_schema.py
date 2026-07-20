import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.users.app.models.preference import Preference, Theme
from backend.services.users.app.models.profile import Profile


@pytest.mark.asyncio
async def test_profile_and_preference_creation(db_session: AsyncSession):
    user_id = uuid.uuid4()

    profile = Profile(
        user_id=user_id,
        username="testuser",
        display_name="Test User",
        bio="Hello world",
        avatar_url="https://example.com/avatar.png",
    )

    preference = Preference(user_id=user_id, timezone="America/New_York", language="en-US", theme=Theme.DARK)

    db_session.add_all([profile, preference])
    await db_session.commit()
    await db_session.refresh(profile)
    await db_session.refresh(preference)

    assert profile.user_id == user_id
    assert profile.username == "testuser"
    assert profile.created_at is not None
    assert profile.updated_at is not None

    assert preference.user_id == user_id
    assert preference.theme == Theme.DARK
    assert preference.timezone == "America/New_York"
    assert preference.language == "en-US"


@pytest.mark.asyncio
async def test_profile_username_unique_constraint(db_session: AsyncSession):
    user_id_1 = uuid.uuid4()
    user_id_2 = uuid.uuid4()

    profile1 = Profile(user_id=user_id_1, username="uniqueuser")
    db_session.add(profile1)
    await db_session.commit()

    profile2 = Profile(user_id=user_id_2, username="uniqueuser")
    db_session.add(profile2)

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()
