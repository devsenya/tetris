import abc


class Shape(abc.ABC):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.variationNum = 0
        self.variations = self.get_variations()

    def set_XY(self, X, Y):
        self.X = X
        self.Y = Y
        self.update_variations()
        self.update_massBlocks()

    def rotate(self):
        self.variationNum = (self.variationNum + 1) % len(self.variations)
        self.update_massBlocks()

    # обновить блоки после изменений
    def update_massBlocks(self):
        self.massBlocks = self.variations[self.variationNum]

     # Пересчитываем все вариации
    def update_variations(self):
        self.variations = self.get_variations()
        self.update_massBlocks()  # Обновляем текущие блоки после изменения вариаций

    # свойство-геттер
    @property
    def nextRotate(self):
        return self.variations[(self.variationNum + 1) % len(self.variations)]

    @abc.abstractmethod
    def get_variations(self):
        pass


class I_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 1

    def get_variations(self):
        return [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X, self.Y + 2)],
                [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X + 2, self.Y)]]


class O_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 2

    def get_variations(self):
        return [[(self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)]]


class S_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 3

    def get_variations(self):
        return [[(self.X - 1, self.Y + 1), (self.X, self.Y + 1), (self.X, self.Y), (self.X + 1, self.Y)],
                [(self.X - 1, self.Y - 1), (self.X - 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]


class Z_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 4

    def get_variations(self):
        return [[(self.X - 1, self.Y - 1), (self.X, self.Y - 1), (self.X, self.Y), (self.X + 1, self.Y)],
                [(self.X + 1, self.Y - 1), (self.X + 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]


class L_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 5

    def get_variations(self):
        return [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)],
                [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y + 1)],
                [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y - 1)],
                [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y - 1)]]


class J_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 6

    def get_variations(self):
        return [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y + 1)],
                [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y - 1)],
                [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y - 1)],
                [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y + 1)]]


class T_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 7

    def get_variations(self):
        return [[(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1)],
                [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y)],
                [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y - 1)],
                [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y)]]
