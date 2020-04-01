#!/usr/bin/env python
from copy import deepcopy

def solve_puzzle (clues):
    p = Puzzle(clues)
    result = solve(p)
#     result.print_proven()
    formatted = result.proven
    for i in range(result.size):
        formatted[i] = tuple(formatted[i])
    
    return tuple(formatted)

class Puzzle(object):
    
    def __init__(self, clues):
        self.size = len(clues) // 4
        
        self.situation_changed = True
        
        # Ключи в удобном порядке
        self.clues = {'left' : [int(clues[i + 3 * self.size]) for i in range(self.size - 1, -1, -1)],
                     'right' : [int(clues[i + self.size]) for i in range(self.size)],
                     'upper' : [int(clues[i]) for i in range(self.size)],
                    'bottom' : [int(clues[i + 2 * self.size]) for i in range(self.size - 1, -1, -1)]}
        
        # Множество всех возможных значений
        self.full = set([x + 1 for x in range(self.size)])
        
        # Однозначное значение для каждой ячейки
        self.proven = [[None for _x in range(self.size)] for _y in range(self.size)]
        
        # Множество невозможных значений для каждой ячейки        
        self.excluded = [[set([]) for _x in range(self.size)] for _y in range(self.size)]
        
        
        """
        На основе ключей сразу определяем значения, которые
        точно не могут находиться в ячейках, и заполняем
        ячейки, которые однозначно определены.
        """
        for key, value in self.clues.items():
            if key == 'left':
                for i in range(self.size):
                    if value[i] == 1:
                        self.set_cell_to(i, 0, self.size)
                    for j in range(value[i] - 1):
                        self.excluded[i][j] |= set(range(self.size - (value[i] - 1) + 1 + j, self.size + 1))

            if key == 'right':
                for i in range(self.size):
                    if value[i] == 1:
                        self.set_cell_to(i, self.size - 1, self.size)
                    for j in range(value[i] - 1):
                        self.excluded[i][self.size - 1 - j] |= set(range(self.size - (value[i] - 1) + 1 + j, self.size + 1))

            if key == 'upper':
                for i in range(self.size):
                    if value[i] == 1:
                        self.set_cell_to(0, i, self.size)
                    for j in range(value[i] - 1):
                        self.excluded[j][i] |= set(range(self.size - (value[i] - 1) + 1 + j, self.size + 1))

            if key == 'bottom':
                for i in range(self.size):
                    if value[i] == 1:
                        self.set_cell_to(self.size - 1, i, self.size)
                    for j in range(value[i] - 1):
                        self.excluded[self.size - 1 - j][i] |= set(range(self.size - (value[i] - 1) + 1 + j, self.size + 1))


        # Переписать это говно
        for i in range(self.size):
            if self.clues['left'][i] == 2 and self.clues['right'][i] == 2:
                for j in range(1, self.size - 1):
                    self.excluded[i][j] |= set([5])
            if self.clues['upper'][i] == 2 and self.clues['bottom'][i] == 2:
                for j in range(1, self.size - 1):
                    self.excluded[j][i] |= set([5])
            if self.clues['left'][i] == 4 and self.clues['right'][i] == 3:
                self.set_cell_to(i, 3, self.size)
            if self.clues['left'][i] == 3 and self.clues['right'][i] == 4:
                self.set_cell_to(i, 2, self.size)
            if self.clues['upper'][i] == 4 and self.clues['bottom'][i] == 3:
                self.set_cell_to(3, i, self.size)
            if self.clues['upper'][i] == 3 and self.clues['bottom'][i] == 4:
                self.set_cell_to(2, i, self.size)
            if self.clues['left'][i] == 5 and self.clues['right'][i] == 2:
                self.set_cell_to(i, 4, self.size)
            if self.clues['left'][i] == 2 and self.clues['right'][i] == 5:
                self.set_cell_to(i, 1, self.size)
            if self.clues['upper'][i] == 5 and self.clues['bottom'][i] == 2:
                self.set_cell_to(4, i, self.size)
            if self.clues['upper'][i] == 2 and self.clues['bottom'][i] == 5:
                self.set_cell_to(1, i, self.size)
    
    
    """
    Считаем задачу решенной, если заполнены
    все гарантированные значения.
    """
    def is_solved(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.proven[i][j]:
                    return False
        return True
    
    def is_solvable(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.proven[i][j] and len(self.excluded[i][j]) == self.size:
                    return False
        return True
    
    """
    Для каждой строки и каждого столца (12 шт) проверить,
    нет ли в исключенных значениях тех, которые встречаются
    ровно size - 1 раз. Это значит, что существует одна
    ячейка, куда это самое значение и должно быть записано.
    """
    def check_and_fill(self):
        self.situation_changed = False
        for v in range(self.size):
            for i in range(self.size):
                ii = jj = -1
                found = 0
                for j in range(self.size):
                    if not self.proven[i][j] and v + 1 not in self.excluded[i][j]:
                        found += 1
                        ii = i
                        jj = j
                if found == 1:
                    self.situation_changed = True
                    self.set_cell_to(ii, jj, v + 1)
        for v in range(self.size):
            for i in range(self.size):
                ii = jj = -1
                found = 0
                for j in range(self.size):
                    if not self.proven[j][i] and v + 1 not in self.excluded[j][i]:
                        found += 1
                        ii = i
                        jj = j
                if found == 1:
                    self.situation_changed = True
                    self.set_cell_to(jj, ii, v + 1)
    
    
    """
    Записать число в ячейку, если оно единственно верное,
    для всех ячеек в данной строке/столбце записать это
    число в исключения.
    """
    def set_cell_to(self, x, y, value):
        self.proven[x][y] = value
        for i in range(self.size):
            self.excluded[i][y].add(value)
            self.excluded[x][i].add(value)


    def print_proven(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.proven[i][j], end = ' ')
            print()

    def print_excluded(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.excluded[i][j]:
                    print(self.excluded[i][j], end = '')
                else:
                    print('{}', end = '')
            print()
    
    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                if i + j:
                    print(',', end = '')
                print(self.proven[i][j], end = '')
    
    """
    Строки: 0, ..., size - 1
    Столбцы: size, ..., 2 * size - 1
    """
    def clues_defined(self, i):
        if not (i // self.size):
            if self.clues['left'][i] or self.clues['right'][i]:
                return True
        else:
            if self.clues['upper'][i - self.size] or self.clues['bottom'][i - self.size]:
                return True
        return False


    def clues_ok(self, i):
        c1 = c2 = m1 = m2 = 0
        if not (i // self.size):
            for j in range(self.size):
                if self.clues['left'][i]:
                    if self.proven[i][j] > m1:
                        m1 = self.proven[i][j]
                        c1 += 1
                if self.clues['right'][i]:
                    if self.proven[i][self.size - 1 - j] > m2:
                        m2 = self.proven[i][self.size - 1 - j]
                        c2 += 1
#             if c1 == self.clues['left'][i] and c2 == self.clues['right'][i]:
#                 print(self.clues['left'][i], self.clues['right'][i], self.proven[i])
            return c1 == self.clues['left'][i] and c2 == self.clues['right'][i]
        else:
            for j in range(self.size):
                if self.clues['upper'][i - self.size]:
                    if self.proven[j][i - self.size] > m1:
                        m1 = self.proven[j][i - self.size]
                        c1 += 1
                if self.clues['bottom'][i - self.size]:
                    if self.proven[self.size - 1 - j][i - self.size] > m2:
                        m2 = self.proven[self.size - 1 - j][i - self.size]
                        c2 += 1
#             if c1 == self.clues['upper'][i - self.size] and c2 == self.clues['bottom'][i - self.size]:
#                 print(self.clues['upper'][i - self.size], self.clues['right'][i - self.size], end = ' ')
#                 for bla in range(self.size):
#                     print(self.proven[bla][i - self.size], end = ' ')
            return c1 == self.clues['upper'][i - self.size] and c2 == self.clues['bottom'][i - self.size]
    
    def has_smth(self, i):
        if not (i // self.size):
            for j in range(self.size):
                if self.proven[i][j]:
                    return True
            return False
        else:
            for j in range(self.size):
                if self.proven[j][i - self.size]:
                    return True
            return False


    def has_no_nones(self, i):
        if not (i // self.size):
            for j in range(self.size):
                if not self.proven[i][j]:
                    return False
            return True
        else:
            for j in range(self.size):
                if not self.proven[j][i - self.size]:
                    return False
            return True


    def brute_force(self):
        self.situation_changed = False
        for i in range(self.size):
#             print(i, self.has_smth(i), self.has_no_nones(i), self.clues_defined(i))
#             self.print_proven()
            if self.has_smth(i) and not self.has_no_nones(i) and self.clues_defined(i):
                possible_values = [set([]) for x in range(self.size)]
                possible_values = try_all_combos(i, self, 0, [], possible_values)
#                 print(i, possible_values)
                for j in range(self.size):
                    for x in self.full ^ self.excluded[i][j]:
                        if x not in possible_values[j]:
                            self.excluded[i][j] |= set([x])
                    if len(possible_values[j]) == 1:
                        if not self.proven[i][j]:
                            self.situation_changed = True
                            self.set_cell_to(i, j, possible_values[j].pop())
        for i in range(self.size):
            if self.has_smth(i + self.size) and not self.has_no_nones(i + self.size) and self.clues_defined(i + self.size):
                possible_values = [set([]) for x in range(self.size)]
                possible_values = try_all_combos(i + self.size, self, 0, [], possible_values)
#                 print(i, possible_values)
                for j in range(self.size):
                    for x in self.full ^ self.excluded[j][i]:
                        if x not in possible_values[j]:
                            self.excluded[j][i] |= set([x])
                    if len(possible_values[j]) == 1:
                        if not self.proven[j][i]:
                            self.situation_changed = True
                            self.set_cell_to(j, i, possible_values[j].pop())


def try_all_combos(z, a, v, used, possible_digits):
    tmp = deepcopy(a)
    if tmp.has_no_nones(z):
        if tmp.clues_ok(z):
            for i in range(tmp.size):
                if not (z // tmp.size):
                    possible_digits[i].add(tmp.proven[z][i])
                else:
                    possible_digits[i].add(tmp.proven[i][z - tmp.size])
        return possible_digits
    if v == tmp.size:
        return [set([]) for i in range(tmp.size)]
    
    if not (z // tmp.size):
        while v < tmp.size - 1 and tmp.proven[z][v]:
            v += 1
        for i in tmp.excluded[z][v] ^ tmp.full:
            if i not in tmp.proven[z]:
                tmp.proven[z][v] = i
                used.append(i)
                result = try_all_combos(z, tmp, v + 1, used, possible_digits)
                used.pop(-1)
    else:
        while v < tmp.size - 1 and tmp.proven[v][z - tmp.size]:
            v += 1
        for i in tmp.excluded[v][z - tmp.size] ^ tmp.full:
            i_in_a_proven_z = False
            for j in range(tmp.size):
                if i == tmp.proven[j][z - tmp.size]:
                    i_in_a_proven_z = True
            if not i_in_a_proven_z:
                tmp.proven[v][z - tmp.size] = i
                used.append(i)
                result = try_all_combos(z, tmp, v + 1, used, possible_digits)
                used.pop(-1)

    return possible_digits


def solve(puzzle):
#     print('BEFORE CHANGES')
#     puzzle.print_proven()
#     puzzle.print_excluded()
    while puzzle.situation_changed and not puzzle.is_solved():
        puzzle.check_and_fill()
        puzzle.brute_force()
#     while puzzle.situation_changed and not puzzle.is_solved():
#         puzzle.check_and_fill()

#     puzzle.print_proven()
#     puzzle.print_excluded()
#     print(puzzle.is_solvable())
#     print('CHANGES DONE')
#     print()
    
    if not puzzle.is_solvable() or puzzle.is_solved():
        return puzzle
    
    possible_values = []
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            if len(puzzle.excluded[i][j]) != puzzle.size:
                possible_values.append([puzzle.size - len(puzzle.excluded[i][j]), i, j])
    possible_values.sort()
    
    for i in range(len(possible_values)):
        for x in puzzle.excluded[possible_values[i][1]][possible_values[i][2]] ^ puzzle.full:
            t = deepcopy(puzzle)
            t.situation_changed = True
            t.set_cell_to(possible_values[i][1], possible_values[i][2], x)
            assumption = solve(t)
            if assumption.is_solved():
                flag = True
                for clue in range(assumption.size * 2):
                    if not assumption.clues_ok(clue):
                        flag = False
                if flag:
                    return assumption
                else:
                    continue
            else:
                continue
    return puzzle
