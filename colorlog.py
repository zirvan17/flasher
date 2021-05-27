class LeftShiftConcat:
    string: str

    def __init__(self, string: str):
        self.string = string

    def __lshift__(self, other):
        print(other, end="")
        return LeftShiftConcat(self.string + str(other))


class ColorLog:
    pref: str

    def __init__(self, pref: str):
        self.pref = pref

    def __str__(self):
        return self.pref

    def __repr__(self):
        return self.pref

    def __add__(self, other):
        return self.pref + other

    def __lshift__(self, other):
        print(self.pref, other, end="")

        return LeftShiftConcat(other)
