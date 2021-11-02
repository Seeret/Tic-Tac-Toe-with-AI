from random import choice
from copy import deepcopy


def show_table(table):
    print("---------")
    for row in table:
        print("| " + " ".join(row) + " |")
    print("---------")


def player_turn(table, free_cells, smb, win_cond):
    while True:
        try:
            x, y = map(lambda f: int(f) - 1, input("Enter the coordinates: ").split())
            if x not in (0, 1, 2) or y not in (0, 1, 2):
                print("Coordinates should be from 1 to 3!")
            elif (x, y) not in free_cells:
                print("This cell is occupied! Choose another one!")
            else:
                table[x][y] = smb
                free_cells.remove((x, y))
                show_table(table)
                return state_game(table, win_cond)
        except ValueError:
            print("You should enter numbers!")


def good_turn(table, smb1, smb2, win_cond, free_cells):
    for win in win_cond:
        if table[win[0][0]][win[0][1]] == table[win[1][0]][win[1][1]] == smb1 and table[win[2][0]][win[2][1]] == " ":
            table[win[2][0]][win[2][1]] = smb2
            free_cells.remove(win[2])
            print('Making move level "medium"')
            show_table(table)
            return state_game(table, win_cond)
        elif table[win[0][0]][win[0][1]] == table[win[2][0]][win[2][1]] == smb1 and table[win[1][0]][win[1][1]] == " ":
            table[win[1][0]][win[1][1]] = smb2
            free_cells.remove(win[1])
            print('Making move level "medium"')
            show_table(table)
            return state_game(table, win_cond)
        elif table[win[1][0]][win[1][1]] == table[win[2][0]][win[2][1]] == smb1 and table[win[0][0]][win[0][1]] == " ":
            table[win[0][0]][win[0][1]] = smb2
            free_cells.remove(win[0])
            print('Making move level "medium"')
            show_table(table)
            return state_game(table, win_cond)
    return "Not"


def minimax(table, smb1, smb2, move, win_cond, free_cells):
    free_cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    table1 = deepcopy(table)
    moves = {x: 0 for x in free_cells}
    for i1, k in enumerate(table1):
        for i2, cell in enumerate(k):
            table1 = deepcopy(table)
            if cell != " ":
                del moves[(i1, i2)]
                continue
            table1[i1][i2] = smb1
            res = state_game(table1, win_cond)
            if not res:
                en_smb = "X" if smb1 == "O" else "O"
                moves[(i1, i2)] = minimax(table1, en_smb, smb2, move + 1, win_cond, free_cells)[0]
            elif res == "Draw":
                pass
            elif res == smb2 + " wins!":
                moves[(i1, i2)] += 10
            else:
                moves[(i1, i2)] -= 10
    if move % 2 == 1:
        maximum = -1000
        c = None
        for k, v in moves.items():
            if v > maximum:
                maximum = v
                c = k
        return maximum, c
    else:
        minimum = 1000
        c = None
        for k, v in moves.items():
            if v < minimum:
                minimum = v
                c = k
        return minimum, c


def easy_turn(table, free_cells, smb, win_cond):
    x, y = choice(free_cells)
    table[x][y] = smb
    free_cells.remove((x, y))
    print('Making move level "easy"')
    show_table(table)
    return state_game(table, win_cond)


def medium_turn(table, free_cells, smb, win_cond):
    res = good_turn(table, smb, smb, win_cond, free_cells)
    if res == "Not":
        en_smb = "X" if smb == "O" else "O"
        res = good_turn(table, en_smb, smb, win_cond, free_cells)
        if res == "Not":
            x, y = choice(free_cells)
            table[x][y] = smb
            free_cells.remove((x, y))
            print('Making move level "medium"')
            show_table(table)
            return state_game(table, win_cond)
        else:
            return res
    else:
        return res


def hard_turn(table, free_cells, smb, win_cond):
    if table == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]:
        x, y = choice([(0, 0), (0, 2), (2, 0), (2, 2)])
    else:
        x, y = minimax(table, smb, smb, 1, win_cond, free_cells)[1]
    table[x][y] = smb
    print('Making move level "hard"')
    show_table(table)
    return state_game(table, win_cond)


def state_game(table, win_cond):
    for cond in win_cond:
        if table[cond[0][0]][cond[0][1]] == table[cond[1][0]][cond[1][1]] == table[cond[2][0]][cond[2][1]] and \
                table[cond[0][0]][cond[0][1]] != " ":
            return table[cond[0][0]][cond[0][1]] + " wins!"
    for row in table:
        if " " in row:
            return False
    return "Draw"


cond = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)), ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]
field = [[" ", " ", " "] for _ in range(3)]
cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
dct = {"user": player_turn, "easy": easy_turn, "medium": medium_turn, "hard": hard_turn}
while True:
    inp = input("Input command: ")
    if inp == "exit":
        exit()
    try:
        command, first_p, second_p = inp.split()
    except ValueError:
        print("Bad parameters!")
        continue
    if command != "start" or first_p not in dct or second_p not in dct:
        print("Bad parameters!")
        continue
    show_table(field)
    while True:
        result = dct[first_p](field, cells, "X", cond)
        if result:
            print(result)
            break
        result = dct[second_p](field, cells, "O", cond)
        if result:
            print(result)
            break
    field = [[" ", " ", " "] for _ in range(3)]
    cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
