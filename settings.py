BOARD_OFFSET = 30
BOARD_SIZE = 640
CELL_SIZE = BOARD_SIZE // 8
BOARD_BORDER_THICKNESS = 20

NUM_SQUARES_TO_EDGE = [(0, 0, 0, 0) for _ in range(64)]
DIRECTIONAL_OFFSET = (7, 9, -7, -9)

for row in range(8):
    for column in range(8):
        index = column * 8 + row

        dist_north: int = 7 - column
        dist_south: int = column
        dist_east: int = 7 - row
        dist_west: int = row

        NUM_SQUARES_TO_EDGE[index] = (  # type: ignore
            min(dist_north, dist_west),
            min(dist_north, dist_east),
            min(dist_south, dist_east),
            min(dist_south, dist_west),
        )

        del index
