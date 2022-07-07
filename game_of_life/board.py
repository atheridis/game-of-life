from itertools import product

from .cell import Cell


class Board:
    def __init__(self, size):
        """
        :param size:
        """
        self.size = size
        self._cells = []
        self.living_cells = []
        self.grid = []
        self._altered = set()

    def create(self, state=None):
        """
        :param start_state:
        """
        state = [] if state is None else state

        self.grid = []
        self._cells = []
        self.living_cells = []
        self._altered = set()

        for i in range(self.size[0]):
            self.grid.append([])
            for j in range(self.size[1]):
                if [i, j] in state:
                    c = Cell((i, j), 1)
                    self.living_cells.append(c)
                else:
                    c = Cell((i, j), 0)
                self._cells.append(c)
                self.grid[i].append(c)

        self._assign_neighbours()

    def update_grid(self):
        self._altered = set()
        for living_cell in self.living_cells:
            altered_cells = living_cell.update_neighbours()
            self._altered.update(altered_cells)

        self.living_cells = []

        for altered_cell in self._altered:
            altered_cell.update_status()
            if altered_cell:
                self.living_cells.append(altered_cell)

    def change_cell_status(self, pos):
        self.grid[pos[0]][pos[1]].change_status()

        if self.grid[pos[0]][pos[1]]:
            self.living_cells.append(self.grid[pos[0]][pos[1]])
        else:
            self.living_cells.remove(self.grid[pos[0]][pos[1]])

    def randomise_grid(self, alive_chance):
        self.living_cells = []
        for c in self._cells:
            c.randomise_status(alive_chance)
            if c:
                self.living_cells.append(c)

    def _assign_neighbours(self):
        for (n, m) in product(range(self.size[0]), range(self.size[1])):
            for (i, j) in product(range(3), range(3)):
                if (
                    0 <= n - i + 1 < self.size[0]
                    and 0 <= m - j + 1 < self.size[1]
                    and (i, j) != (1, 1)
                ):
                    self.grid[n][m].neighbours.append(self.grid[n - i + 1][m - j + 1])
