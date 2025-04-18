import pytest
from pydantic import ValidationError
from src.models import UserModel
from bson import ObjectId


def test_valid_json_data_alias__id(valid_user_data):
    user = UserModel(**valid_user_data)

    assert user.id == valid_user_data["_id"]
    assert user.email == valid_user_data["email"]
    assert user.login == valid_user_data["login"]
    assert user.password_hash == valid_user_data["password_hash"]
    assert user.first_name == valid_user_data["first_name"]
    assert user.middle_name == valid_user_data["middle_name"]
    assert user.last_name == valid_user_data["last_name"]
    assert user.active == valid_user_data["active"]
    assert user.role == valid_user_data["role"]


def test_valid_json_data_id():
    user_data = {
        "id": ObjectId("661adfa5e13f1a1234567890"),
        "email": "petr.petrov@example.com",
        "login": "petrpetr",
        "password_hash": "$2b$10$....",
        "first_name": "Петр",
        "middle_name": "Петрович",
        "last_name": "Петров",
        "active": True,
        "role": "student",
    }

    user = UserModel(**user_data)
    assert user.id == user_data["id"]
    assert user.email == user_data["email"]
    assert user.login == user_data["login"]
    assert user.password_hash == user_data["password_hash"]
    assert user.first_name == user_data["first_name"]
    assert user.middle_name == user_data["middle_name"]
    assert user.last_name == user_data["last_name"]
    assert user.active == user_data["active"]
    assert user.role == user_data["role"]


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("_id", "not_a_valid_objectid"),  # must be ObjectId
        ("email", 123),  # must be str
        ("login", None),  # must be str
        ("password_hash", 42),  # must be str
        ("first_name", 123),  # must be str
        ("active", "yes"),  # must be bool
        ("role", None),  # must be str
    ],
)
def test_invalid_user_fields(field, invalid_value, valid_user_data):
    data = valid_user_data.copy()
    data[field] = invalid_value

    with pytest.raises(ValidationError) as exc_info:
        UserModel(**data)
    print(exc_info.value)

    assert field in str(exc_info.value)


@pytest.fixture
def valid_user_data():
    return {
        "_id": ObjectId("661adfa5e13f1a1234567890"),
        "email": "ivan.ivanov@example.com",
        "login": "ivanivan",
        "password_hash": "$2b$10$...",
        "first_name": "Иван",
        "middle_name": "Иванович",
        "last_name": "Иванов",
        "active": True,
        "role": "student",
    }
