# coding: utf8


def list_to_puzzle(lst):
    """
    Converts a one dimensional puzzle list and returns it's two dimensional representation.
    [1, 2, 3, 4, 5, 6, 7, 8, 0] --> [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    n_sqrt = int(math.sqrt(len(lst)))

    puzzle = []
    for i in range(0, len(lst), n_sqrt):
        line = []
        for j in range(0, n_sqrt):
            line.append(lst[i + j])
        puzzle.append(line)

    return puzzle


def puzzle_to_list(puzzle):
    """
    Converts a two dimensional puzzle to a one dimensional puzzle.
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]] --> [1, 2, 3, 4, 5, 6, 7, 8, 0]
    """
    lst = []
    for row in puzzle:
        lst.extend(row)

    return lst
