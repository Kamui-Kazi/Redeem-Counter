# creating the class that is used to keep track of the number of meows
class Counter():
    def __init__(self):
        self.count = 0
        self.write()
    def add(self, count: int):
        self.count += count
        self.write()
    def set(self, count: int):
        self.count = count
        self.write()
    def reset(self):
        self.count = 0
        self.write()
    def write(self):
        file = open("count.txt", 'w')
        file.write(str(self.count))
        file.close()
    def pp(self) -> str:
        return f"Meow has been redeemed {self.count} times"