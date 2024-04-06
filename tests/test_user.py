import pytest
from app.models import user

def test_user():    
    john = user.User('John', 30)
    assert john.toStr() == 'John is 30 years old'

def test_user_age():
    with pytest.raises(ValueError):
        wrongAge = user.User('John', 200)