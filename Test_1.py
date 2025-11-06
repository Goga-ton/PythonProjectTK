class Personal:
    def __init__(self, name, age):
        self.name = name  # self - ссылка на создаваемый объект
        self.age = age
    def __str__(self):
        return f'Привет {self.name}! Мне {self.age}'

    def say_hi(self, friend_name):
        # self здесь - тот же самый объект, что и в __init__!
        return f"Привет {friend_name}! Мне {self.age}"

    def get_birth_year(self, current_year):
        # self здесь - тоже тот же объект!
        return f"Привет {current_year}! Мне {self.age}"

personal1 = Personal("Антон", 20)
print(personal1)
print(personal1.say_hi("Жора"))
print(personal1.get_birth_year(50))