from enum import Enum


class PieceTypes(Enum):
    RED = (-1, -2)
    BLUE = (1, 2)


POSITION_NOTATIONS = []

index = 1
for i in range(8):
    is_even = i % 2 == 0
    for j in range(8):

        if is_even and j % 2 == 0:
            POSITION_NOTATIONS.append(None)
            continue

        if not is_even and j % 2 != 0:
            POSITION_NOTATIONS.append(None)
            continue

        POSITION_NOTATIONS.append(index)
        index += 1

del index
