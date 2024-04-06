class User:
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age

    def toStr(self):
        return f'{self.name} is {self.age} years old'
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, age):
        if(age < 0 or age > 150):
            raise ValueError('Age cannot be negative')
        self._age = age