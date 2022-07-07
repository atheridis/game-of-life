import json
import sys
from math import floor

import pygame

from .board import Board

pygame.init()


class GameOfLife:
    def __init__(
        self, resolution, cell_width, dead_colour, alive_colour, frame_limit, save_path
    ):
        self._resolution = resolution
        self._cell_width = cell_width
        self._dead_colour = dead_colour
        self._alive_colour = alive_colour
        self._frame_limit = frame_limit
        self._save_path = save_path

        # Required due to MOUSEBUTTONDOWN sometimes activating after get_pressed
        self._changing = False

        self.rows = int(round(self._resolution[1] / self._cell_width))
        self.cols = int(round(self._resolution[0] / self._cell_width))
        self.cell_width = self._resolution[0] / self.cols

        self._save_game_keys = (
            pygame.K_F1,
            pygame.K_F2,
            pygame.K_F3,
            pygame.K_F4,
            pygame.K_F5,
            pygame.K_F6,
            pygame.K_F7,
            pygame.K_F8,
            pygame.K_F9,
        )

        self._load_game_keys = (
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
            pygame.K_0,
        )

        self._screen = pygame.display.set_mode(self._resolution)
        pygame.display.set_caption("Game of Life")
        self.fpsClock = pygame.time.Clock()

        self.board = Board((self.rows, self.cols))
        self.board.create()
        self.load()

        self.paused = False
        self.changing = False
        self.lock_x = False
        self.lock_y = False

    @classmethod
    def fromjsonfile(cls, settings_path, save_path):
        with open(settings_path) as f:
            file = json.loads(f.read())["settings"]
        return cls.fromdict(file, save_path)

    @classmethod
    def fromdict(cls, dict, save_path):
        resolution = dict["resolution"]
        cell_width = dict["cell_width"]
        dead_colour = dict["colour"]["dead"]
        alive_colour = dict["colour"]["alive"]
        frame_limit = dict["frame_limit"]
        return cls(
            resolution, cell_width, dead_colour, alive_colour, frame_limit, save_path
        )

    def save(self, code):
        save = []
        for cell in self.board.living_cells:
            save.append(cell.pos)

        with open(self._save_path) as rf:
            try:
                save_data = json.loads(rf.read())
            except ValueError:
                save_data = {}
                print("Save File Empty")

        print(self._save_game_keys.index(code) + 1)
        save_data[f"save_{self._save_game_keys.index(code) + 1}"] = save
        with open(self._save_path, "w") as wf:
            wf.write(json.dumps(save_data))

    def load(self, code="0"):
        try:
            if code == "0":
                with open(self._save_path) as f:
                    save = json.loads(f.read())["starting_position"]
            else:
                with open(self._save_path) as f:
                    save = json.loads(f.read())[f"save_{code}"]
        except KeyError:
            print("save not found")
        else:
            self.board.create(save)

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            self._quit()
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key in self._save_game_keys:
            self.save(event.key)
        elif event.key in self._load_game_keys:
            self.load(event.unicode)
        elif event.key == pygame.K_r:
            self.board.randomise_grid(0.1)
        elif event.key == pygame.K_c:
            self.board.create()
        elif self.paused and event.key == pygame.K_RIGHT:
            self.board.update_grid()
        elif event.key == pygame.K_UP and self._frame_limit < 1000:
            self._frame_limit += 10
        elif event.key == pygame.K_DOWN:
            if self._frame_limit > 10:
                self._frame_limit -= 10
            else:
                self._frame_limit = 1
        elif pygame.KMOD_SHIFT:
            self.original_posx = int(floor(pygame.mouse.get_pos()[1] / self.cell_width))
            self.original_posy = int(floor(pygame.mouse.get_pos()[0] / self.cell_width))

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._changing = True
                self.original_posx = int(
                    floor(pygame.mouse.get_pos()[1] / self.cell_width)
                )
                self.original_posy = int(
                    floor(pygame.mouse.get_pos()[0] / self.cell_width)
                )
                self.original_cell_status = self.board.grid[self.original_posx][
                    self.original_posy
                ].status
                self.board.change_cell_status((self.original_posx, self.original_posy))
            elif pygame.mouse.get_pressed()[0] & self._changing:
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     self._changing = True
                #     self.original_posx = int(
                #         floor(pygame.mouse.get_pos()[1] / self.cell_width)
                #     )
                #     self.original_posy = int(
                #         floor(pygame.mouse.get_pos()[0] / self.cell_width)
                #     )
                #     self.original_cell_status = self.board.grid[self.original_posx][
                #         self.original_posy
                #     ].status
                #     self.board.change_cell_status(
                #         (self.original_posx, self.original_posy)
                #     )
                self.posx = int(floor(pygame.mouse.get_pos()[1] / self.cell_width))
                self.posy = int(floor(pygame.mouse.get_pos()[0] / self.cell_width))
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if self.posx != self.original_posx and not self.lock_x:
                        self.lock_y = True
                        if (
                            self.board.grid[self.posx][self.original_posy].status
                            == self.original_cell_status
                        ):
                            self.board.change_cell_status(
                                (self.posx, self.original_posy)
                            )
                    if self.posy != self.original_posy and not self.lock_y:
                        self.lock_x = True
                        if (
                            self.board.grid[self.original_posx][self.posy].status
                            == self.original_cell_status
                        ):
                            self.board.change_cell_status(
                                (self.original_posx, self.posy)
                            )
                elif (
                    self.board.grid[self.posx][self.posy].status
                    == self.original_cell_status
                ):
                    self.board.change_cell_status((self.posx, self.posy))
            elif event.type == pygame.MOUSEBUTTONUP:
                self._changing = False
                self.lock_x = False
                self.lock_y = False

    def _draw_screen(self):
        self._empty_space()

        for cell in self.board.living_cells:
            if cell:
                pygame.draw.rect(
                    self._screen,
                    self._alive_colour,
                    (
                        cell.pos[1] * self.cell_width,
                        cell.pos[0] * self.cell_width,
                        self.cell_width,
                        self.cell_width,
                    ),
                )

        pygame.display.flip()

    def _empty_space(self):
        self._screen.fill(self._dead_colour)

    def run(self):
        while True:
            self._draw_screen()
            self._handle_events()
            if not self.paused:
                self.board.update_grid()
                self.fpsClock.tick(self._frame_limit)
