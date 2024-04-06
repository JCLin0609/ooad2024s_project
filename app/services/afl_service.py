from app.models import user

def users():
    john = user.User('John', 30)
    jane = user.User('Jane', 25)
    jclin = user.User('Jclin', 24)
    
    return [john, jane, jclin]