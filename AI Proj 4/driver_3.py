import argparse
from copy import copy, deepcopy

rows = 'ABCDEFGHI'
columns = [x for x in range(9)]
options = [x + 1 for x in range(9)]

all_in = []
row_set = []
column_set = []
box_set = []

for row, x in zip(rows, range(len(rows))):
    temp_row = []
    for column in columns:
        temp_row.append("%s%s" % (row, column))
        all_in.append("%s%s" % (row, column))

    row_set.append(temp_row)

for column, x in zip(columns, range(len(columns))):
    temp_column = []
    for row in rows:
        temp_column.append("%s%s" % (row, column))

    column_set.append(temp_column)

for a in range(3):
    for x in range(3):
        temp_box = []
        for y in range(3):
            row = rows[y + a * 3]
            for z in range(3):
                column = columns[z+3*x]
                temp_box.append("%s%s" % (row, column))

        box_set.append(temp_box)


class sudoku:

    def __init__(self, board):
        self.state = board
        self.unresolved = []
        self.domain = self.first_domain()
        self.next_guess = []

    def first_domain(self):
        domain = {}
        for location in all_in:
            if self.state[location] == 0:
                domain[location] = copy(options)
                self.unresolved.append(location) # this can be tuple with loc, row, column, and box

        return domain


    def new_child(self):
        new_inst = deepcopy(self)
        # new_inst.state = deepcopy(self.state)

        return new_inst

    def is_solved(self):
        for thing in all_in:
            if self.state[thing] == -1:
                return 2
        for row in row_set:
            seen = set()
            for each in row:
                if self.state[each] == 0:
                    return 1
                if self.state[each] in seen:
                    return 2
                else:
                    seen.add(self.state[each])

        for column in column_set:
            seen = set()
            for each in column:
                if self.state[each] in seen:
                    return 2
                else:
                    seen.add(self.state[each])

        for box in box_set:
            seen = set()
            for each in box:
                if self.state[each] in seen:
                    return 2
                else:
                    seen.add(self.state[each])

        return 0

    def set_next(self):
        self.next_guess = []
        for key, value in self.domain.items():
            self.next_guess.append((len(value), key))

        self.next_guess.sort()


    def legal_move(self, candidate, key):
        for row in row_set:
            if key in row:
                for spot in row:
                    if candidate == self.state[spot]:
                        return False

        for column in column_set:
            if key in column:
                for spot in column:
                    if candidate == self.state[spot]:
                        return False

        for box in box_set:
            if key in box:
                for spot in box:
                    if candidate == self.state[spot]:
                        return False

        return True


    def checker(self, checks, place, changes):
        while True:
            leave = 0
            for each in checks:

                if self.state[each] != 0 and self.state[each] in self.domain[place]:
                    b = self.domain[place].index(self.state[each])
                    del self.domain[place][b]
                    leave += 1
                    changes += 1
                    if len(self.domain[place]) == 1:
                        if self.legal_move(int(self.domain[place][0]), place):
                            self.state[place] = int(self.domain[place][0])
                            self.unresolved.remove(place)
                            del self.domain[place]
                        else:
                            self.state[place] = -1
                            self.unresolved.remove(place)
                            del self.domain[place]

                        return False



            if leave == 0:
                return changes


    def acthree(self):
        while True:
            changes = 0
            for row in row_set:
                for place in row:
                    if place in self.unresolved:
                        changes = self.checker(row, place, changes)

            for column in column_set:
                for place in column:
                    if place in self.unresolved:
                        changes = self.checker(column, place, changes)

            for box in box_set:
                for place in box:
                    if place in self.unresolved:
                        changes = self.checker(box, place, changes)

            if changes == 0:
                return

    def build_tree(self):
        self.set_next()
        next = self.next_guess[0]
        del self.next_guess[0]
        key = next[1]
        haveago = self.domain[key]
        del self.domain[next[1]]
        self.unresolved.remove(key)
        for each in haveago:
            tester = self.new_child()
            tester.state[key] = each
            tester.acthree()
            tester.set_next()
            result = tester.is_solved()
            if result == 2:
                pass
            elif result == 0:
                return tester
            else:
                tester = tester.build_tree()
                if tester:
                    if tester.is_solved() == 0:
                        return tester




    def solve(self):
        self.acthree()
        result = self.is_solved()
        if result == 0:
            return result
        if result == 2:
            return result
        else:
            return self.build_tree()


    def print_int(self):
        strang = 0
        for each, i  in zip(all_in, range(len(all_in))):
            strang += self.state[each]*pow(10, (80-i))

        return strang



def allocate(board):
    allocation = {}
    for each, i in zip(all_in, range(len(all_in))):
        allocation[each] = int(board[i])

    return allocation


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    board = allocate(parser.parse_args().start)
    final = sudoku(board)
    final = final.solve()
    answer = final.print_int()
    fo = open('output.txt', 'w')
    fo.write("%i" % answer)
    fo.close()




