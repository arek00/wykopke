class Optional:

    def __init__(self, value):
        self.value = value

    @staticmethod
    def of(value):
        return Optional(value)

    def map(self, func):
        if (self.value):
            self.value = func(self.value)
        return self

    def get(self):
        return self.value
