import random


class TemporaryPassword():
    def __init__(self):
        self.words = ["chocolate", "popcycle", "marshmallow"]

    def generate_temporary_password(self):
        word = random.choice(self.words)

        numbers = ''.join(str(random.randint(1, 9)) for i in range(3))

        password = word + numbers

        return password
