class Cup:
    def __init__(self, cup_h, cup_w):
        self.width, self.height = cup_w, cup_h
        self.gridList = [[0] * self.width for _ in range(self.height)]


    def clear(self):
        for line in range(len(self.gridList)):
            for col in range(len(self.gridList[line])):
                if self.gridList[line][col] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    self.gridList[line][col] = 0

    def delete_lines(self):
        lines = []
        # flag = False
        for x in range(len(self.gridList) - 1, -1, -1):
            if 0 not in self.gridList[x]:
                # if not flag:
                #     [print(x) for x in self.gridList]
                flag = True
                lines.append(x)

        if lines:
            print(f"--->{len(lines)}<---")

            for m in lines:
                del self.gridList[m]

            for _ in lines:
                self.gridList.insert(0, [0] * self.width)
        return len(lines)
