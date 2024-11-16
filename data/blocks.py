import abc


class Shape(abc.ABC):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.variationNum = 0
        self.variations = self.update()
        self.massBlocks = self.variations[self.variationNum]

    def set_XY(self, X, Y):
        self.X = X
        self.Y = Y
        self.update()

    def rotate(self):
        self.variationNum = (self.variationNum + 1) % len(self.variations)
        self.update()

    # свойство-геттер
    @property
    def nextRotate(self):
        return self.variations[(self.variationNum + 1) % len(self.variations)]

    @abc.abstractmethod
    def update(self):
        pass


class I_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 1

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X, self.Y + 2)],
                           [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X + 2, self.Y)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class O_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 2

    def update(self):
        self.variations = [[(self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class S_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 3

    def update(self):
        self.variations = [[(self.X - 1, self.Y + 1), (self.X, self.Y + 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X - 1, self.Y - 1), (self.X - 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class Z_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 4

    def update(self):
        self.variations = [[(self.X - 1, self.Y - 1), (self.X, self.Y - 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X + 1, self.Y - 1), (self.X + 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class L_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 5

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y + 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y - 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y - 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class J_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 6

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y + 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y - 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y - 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class T_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 7

    def update(self):
        self.variations = [[(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y)],
                           [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y - 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations
