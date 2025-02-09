#!/usr/bin/env python3

import sys
import time
from typing import Tuple, List, Optional

ROWS = 8
COLS = 8
OPEN_SLOT = "_ "
LIVE_SLOT = "☺ "


class Board:
    def __init__(self, rows: int, cols: int, seed: List[Tuple[int, int]]):
        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.board = []
        self.is_over = False

        for _ in range(rows):
            self.board.append([OPEN_SLOT for _ in range(cols)])

        for coords in self.seed:
            self.set_coords(coords)

    def __repr__(self):
        s = ""
        for row in self.board:
            s += "".join(row) + "\n"

        return s

    # TODO(team): Do we need this method?
    def set_coords(self, coords: Tuple[int, int]) -> None:
        """Sets coords on the game board."""
        i, j = coords
        self.board[i][j] = LIVE_SLOT

    def get_neighbors(self, coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Looks at neighbors in 9x9 grid and returns i, j coords for non-null neighbors"""
        neighbors = []
        for direction in ["nw", "n", "ne", "w", "e", "sw", "s", "se"]:
            neighbor = self.get_inbound_coords(coords, direction)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def get_inbound_coords(
        self, coords: Tuple[int, int], directional: str
    ) -> Optional[Tuple[int, int]]:
    #    nw 0,  0 | n 0, 1 | ne  0, 2
    #     -1,  -1 |  -1, 0 |    -1, 1
    #    ---------------------------
    #     w 1,  0 | c 1, 1 |  e  1, 2
    #       0, -1 |        |     0, 1
    #    ---------------------------
    #    sw 2,  0 | s 2, 1 | se  2, 2
    #       1, -1 |   1, 0 |     1, 1
        mp = {
            "nw": (-1, -1),
            "n": (-1, 0),
            "ne": (-1, 1),
            "w": (0, -1),
            "e": (0, 1),
            "sw": (1, -1),
            "s": (1, 0),
            "se": (1, 1),
        }

        i_mod, j_mod = mp[directional]
        i, j = coords
        neighbor_coords = (i + i_mod, j + j_mod)

        if any(
            [
                neighbor_coords[0] < 0,
                neighbor_coords[1] < 0,
                neighbor_coords[0] > ROWS - 1,
                neighbor_coords[1] > COLS - 1,
            ]
        ):
            return None
        else:
            return neighbor_coords

    def is_living(self, coords):
        i, j = coords
        return self.board[i][j] == LIVE_SLOT


# TODO(team): How can the seed elements be an input parameter from CLI?
# add `--random` param to CLI to randomize board population.
def seed_elements() -> List[Tuple[int, int]]:
    return [
        (0, 0),
        (0, 1),
        (0, 5),
        (1, 1),
        (1, 4),
        (1, 6),
        (2, 1),
        (2, 2),
        (2, 4),
        (2, 6),
        (3, 2),
        (3, 4),
        (4, 4),
        (4, 5),
        (5, 6),
        (6, 0),
        (6, 1),
        (7, 3),
        (7, 4),
        (7, 7),
    ]


def init_board():
    """Build an initial board based on ROWS / COLS"""
    return Board(ROWS, COLS, seed_elements())


def main():
    counter = 0
    game = init_board()
    # TODO(team): Does game.is_alive ever change to False?
    while not game.is_over:
        counter += 1
        game.is_over = True
        print(game)
        for i, row in enumerate(game.board):
            for j, item in enumerate(row):
                neighbors = [
                    game.board[x][y]
                    for x, y in game.get_neighbors((i, j))
                    if game.board[x][y] == LIVE_SLOT
                ]
                # A dead cell has exactly 3 neighbors => toggle to alive
                if item == OPEN_SLOT and len(neighbors) == 3:
                    game.board[i][j] = LIVE_SLOT
                    game.is_over = False
                # A living cell has 4 or more neighbors => toggle to dead
                elif item == LIVE_SLOT and len(neighbors) >= 4:
                    game.board[i][j] = OPEN_SLOT
                    game.is_over = False
                # When a living cell has 1 or fewer neighbors => toggle to dead
                elif item == LIVE_SLOT and len(neighbors) <= 1:
                    game.board[i][j] = OPEN_SLOT
                    game.is_over = False

        time.sleep(2)
        print("============================================================")
    
    print("Game exited. Your score is {}.".format(counter))
    sys.exit(0)            

if __name__ == "__main__":
    main()
