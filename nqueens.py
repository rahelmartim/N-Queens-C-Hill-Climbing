import queue as Q
from random import randint
import sys
import resource
from time import time

class NQueens:
    
    def __init__(self):
        
        resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
        sys.setrecursionlimit(0x100000)

        self.god_vector = []
        self.dimension = 0
        self.conflicts = 0
        self.last_conflicts = 0
        self.climbs = 0
        self.max_climbs = 0
        self.initial_time = time()
        self.reestarts = -1
        #self.colums =               list()
        #self.main_diagonals =       list()
        #self.secondary_diagonals =  list()
        #self.board_game = list(list())
        #self.attacking_total = 0
        #self.attacking_lines = 0
        #self.attacking_colums = 0
        #self.attacking_mdiag = 0
        #self.attacking_sdiag = 0

    def new_n_queens(self, dimension_user, climbs_user):
        self.dimension = dimension_user
        self.god_vector = [0 for _ in range(self.dimension)]
        self.conflicts = 0
        self.climbs = 0
        self.last_conflicts = 0
        self.max_climbs = climbs_user
        self.reestarts += 1
        #self.lines = [0 for x in range(self.dimension)]         
        #self.colums = [0 for x in range(self.dimension)]         
        #self.main_diagonals = [0 for x in range((self.dimension * 2)-1)]
        #self.secondary_diagonals = [0 for x in range((self.dimension * 2)-1)]
        #self.board_game = [[0 for x in range(self.dimension)] for y in range(self.dimension)]

        self.rand_initial_state()

    def show(self):
        print(f"Dimensão: {str(self.dimension)}")
        #print("god vector: ")
        print(f"conflicts: {str(self.conflicts)}")

    def rand_initial_state(self):
        possibles = list(range(self.dimension))
        #print(possibles)
        for line_index in range(self.dimension):
            rand_index = randint(0, len(possibles)-1)
            self.god_vector[line_index] = possibles[rand_index]
            #self.god_vector[line_index] = randint(0,self.dimension-1)
            possibles.remove(possibles[rand_index])
        #self.show()
        self.calc_atks()
        if self.check_ok():
            self.end()
            return
        else:
            self.climb()

    def calc_atks(self):
        #self.calc_lines_atk()
        self.calc_diags_atk()
        self.show()

    def calc_lines_atk(self):
        #queens = 0
        colum_checks = []
        for x in range(self.dimension):
            if self.god_vector[x] not in colum_checks:
                queens = 1 + sum(
                    x != y and self.god_vector[x] == self.god_vector[y]
                    for y in range(self.dimension)
                )

                if queens > 1:
                    atks = queens * (queens - 1)
                    self.conflicts += atks
                colum_checks.append(self.god_vector[x])
        #print("line atks: " +str(self.conflicts))

    def calc_diags_atk(self):
        #(linha1 - linha2) + (coluna1 - coluna2) = 0                     
        #queens = 0
        N = self.dimension
        confli = []
        for i in range(N - 1):
            has_queen1 = False
            has_queen2 = False
            has_queen3 = False
            has_queen4 = False
            for j in range(N - i):
                # top principal diagonals
                if self.god_vector[j] == j + i:
                    if has_queen1:
                        #h += 1
                        confli.append(1)
                    has_queen1 = True

                # top secondary diagonals
                if self.god_vector[j] == N - j - i - 1:
                    if has_queen2:
                        #h += 1
                        confli.append(1)
                    has_queen2 = True

                if i > 0:
                    # bottom principal diagonals
                    if self.god_vector[j + i] == j:
                        if has_queen3:
                            #h += 1
                            confli.append(1)
                        has_queen3 = True

                    # bottom secondary diagonals
                    if self.god_vector[j + i] == N - j - 1:
                        if has_queen4:
                            #h += 1
                            confli.append(1)
                        has_queen4 = True
        self.conflicts += len(confli)

        #for x in range(self.dimension):
        #    queens = 1
        #    for y in range(self.dimension):
                #if x == y:
                    #break
        #        if (x - y) + (self.god_vector[x] - self.god_vector[y]) == 0:
        #            queens += 1
        #    if queens > 1:
        #        atks = queens * (queens - 1)
        #        self.conflicts += atks
                  

    def check_ok(self):
        return self.conflicts == 0

    def end(self):
        print("\n\n============================================\n\n")
        print(f"ended with {str(self.climbs)} climbs")
        print(f"and {str(self.reestarts)}reestarts ")
        print("final god vector")
        print(self.god_vector)
        print("matrix:")
        m = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]
        for x in range(self.dimension):
            m[x][self.god_vector[x]] = 1
        for row in m:
            print(row)
        print("time:")
        print(time() - self.initial_time)
        print("bye")


    def climb(self):
        #self.show()
        rand_line = randint(0, self.dimension-1)
        rand_line2 = randint(0, self.dimension-1)
        while rand_line == rand_line2:
            rand_line2 = randint(0, self.dimension-1)
        #rand_colum = randint(0, self.dimension-1)
        #last_colum = self.god_vector[rand_line]
        #self.god_vector[rand_line] = rand_colum
        self.god_vector[rand_line], self.god_vector[rand_line2] = self.god_vector[rand_line2], self.god_vector[rand_line]
        self.last_conflicts = self.conflicts
        self.conflicts = 0
        self.calc_atks()
        if self.conflicts >= self.last_conflicts:
            self.god_vector[rand_line], self.god_vector[rand_line2] = self.god_vector[rand_line2], self.god_vector[rand_line]
            #self.god_vector[rand_line] = last_colum
            self.conflicts = self.last_conflicts
        if self.check_ok():
            self.end()
            return
        else:
            self.climbs += 1
            print(f"--{self.climbs} | {str(self.max_climbs)}--")
            if self.climbs >= self.max_climbs:
                self.new_n_queens(self.dimension, (self.max_climbs))
            else:
                self.climb()
        #self.show()











