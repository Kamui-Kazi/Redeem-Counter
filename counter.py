class Counter():
    def __init__(self):
        self.count = 0
    def add(self, count: int):
        self.count += count
    def set(self, count: int):
        self.count = count
    def reset(self):
        self.count = 0
    def pp(self) -> str:
        return f"Meow has been redeemed {self.count} times"
    
import sys
print(sys.version_info)
