class Counter:
    count = 0
    
    @classmethod
    def add(cls, count: int):
        cls.count += count

    @classmethod
    def subtract(cls, count: int):
        cls.count -= count

    @classmethod
    def set(cls, count: int):
        cls.count = count

    @classmethod
    def reset(cls):
        cls.count = 0

    @classmethod
    def pp(cls) -> str:
        return f"Meow has been redeemed {cls.count} times"
