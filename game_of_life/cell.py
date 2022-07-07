import random


class Cell:
    def __init__(self, pos, status=0):
        """
        :param pos:
        :param status:
        """
        self.pos = pos
        self.neighbours = []
        self.status = status
        self._living_neighbours = 0

    def change_status(self):
        if self.status == 0:
            self.status = 1
        else:
            self.status = 0

    def update_status(self):
        if self:
            if self._living_neighbours > 3:
                self.status = 0
            elif self._living_neighbours < 2:
                self.status = 0
        elif self._living_neighbours == 3:
            self.status = 1

        self._living_neighbours = 0

    def neighbour_count(self):
        self._living_neighbours += 1

    def update_neighbours(self):
        updated = [self]
        if self:
            for neighbour in self.neighbours:
                neighbour.neighbour_count()
                updated.append(neighbour)

        return updated

    def randomise_status(self, alive_chance):
        rand = random.random()
        if rand <= alive_chance:
            self.status = 1
        else:
            self.status = 0

    def __bool__(self):
        if self.status == 0:
            return False

        return True
