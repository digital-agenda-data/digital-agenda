from datetime import timedelta

import pytest

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone

pytestmark = [pytest.mark.django_db]

User = get_user_model()  # noqa


def test_create_user():
    user = User.objects.create_user(email="normal@example.com", password="foo")
    assert user.email == "normal@example.com"
    assert user.is_active
    assert user.is_staff
    assert not user.is_superuser

    with pytest.raises(AttributeError):
        assert user.username is None

    with pytest.raises(TypeError):
        User.objects.create_user()

    with pytest.raises(TypeError):
        User.objects.create_user(email="")

    with pytest.raises(TypeError):
        User.objects.create_user(email="normal@example.com")

    with pytest.raises(ValueError):
        User.objects.create_user(email="", password="foo")

    with pytest.raises(ValueError):
        User.objects.create_user(email="normal@example.com", password="")


def test_create_superuser():
    user = User.objects.create_superuser(email="super@example.com", password="foo")
    assert user.email == "super@example.com"
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser


def test_disable_inactive_user():
    user1 = User.objects.create_superuser(email="super1@example.com", password="foo")
    user2 = User.objects.create_superuser(email="super2@example.com", password="foo")

    user1.last_login = timezone.now() - timedelta(days=179)
    user1.save()
    user2.last_login = timezone.now() - timedelta(days=180)
    user2.save()

    with pytest.raises(AssertionError):
        call_command("disable_inactive_accounts", "--days=-1")
    user1.refresh_from_db()
    assert user1.is_active
    user2.refresh_from_db()
    assert user2.is_active

    call_command("disable_inactive_accounts", "--days=0")
    user1.refresh_from_db()
    assert user1.is_active
    user2.refresh_from_db()
    assert user2.is_active

    call_command("disable_inactive_accounts", "--days=180")

    user1.refresh_from_db()
    assert user1.is_active
    user2.refresh_from_db()
    assert not user2.is_active
