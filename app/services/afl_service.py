from app.models import user

class FuzzService:
    def __init__(self):
        self.john = user.User('John', 30)
        self.jane = user.User('Jane', 25)
        self.jclin = user.User('Jclin', 24)

    # Test method
    def users(self): 
        return [self.john, self.jane, self.jclin]

    def uploadFuzzTarget(self) -> bool:
        pass

    def transferRunningTarget(self) -> bool:
        pass

    def replayFuzzTarget(self) -> None:
        pass