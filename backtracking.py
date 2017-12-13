import copy

#to active debug
semestre_nao_acabar = True
#receives user input
def user_input():
    #while true
    while semestre_nao_acabar:
        #dimension
        try:
            size = int(input('What size for n queens? \n'))
            if size <= 3:
                if size == 1:
                    print("You're dumb ?")
                print("The number must be greater than 4")
                continue
            else:
                #debug
                global debug
                debug = False
                while semestre_nao_acabar:
                    debug_check = input('Do you want to enable debug? (y|n): \n')
                    if (debug_check == "S") or (debug_check == "s") or (debug_check == "Y") or (debug_check == "y"):
                        debug = True
                        print("Debug = ON")
                        break
                    elif (debug_check == "N") or (debug_check == "n"):
                        print("Debug = OFF")
                        break
                    else:
                        print("Invalid response.")
                        continue
                #print(debug)
                global all_solutions
                all_solutions = False
                while semestre_nao_acabar:
                    all_solutions_check = input("Do you want to search for all solutions? (y|n) :\n")
                    if (all_solutions_check == "S") or (all_solutions_check == "s") or (all_solutions_check == "Y") or (all_solutions_check == "y"):
                        all_solutions_check = True
                        print("search for all = ON")
                        print("u are crazzy")
                        break
                    elif (all_solutions_check == "N") or (all_solutions_check == "n"):
                        print("search for all = OFF")
                        break
                    else:
                        print("Invalid response.")
                        continue
                return size
        except ValueError:
            print("Hey, I said a NUMBER...")
#starts a matrix that represents the tray with 0's
def init_board(dimension, debug):
    if debug:
        print("initializing board " +str(dimension) + "x" + str(dimension))
    board = [[0 for x in range(dimension)] for y in range(dimension)]
    if debug:
        print("successfully initialized")
        print("board initialized")
        for row in board:
            print(row)
        print("\n")
    return board
#print the solution or all solutions finded
def show_the_solutions(solutions, unique, size):
    if all_solutions:
        if debug:            
            print("all solutions : ")
        for solution in solutions:
            for row in solution:
                print(row)
            print("\n")
        print("solutions = "+str(len(solutions)))
    else:
        if debug:            
            print("first solution : ")
        for row in unique:
            print(row)
        print("\n")

    if debug:
        print("ended, by")
#check if it's possible to put a queen in this position on the board[row][col]
def can_put_here(board, row, col, dimension):
    if debug:
        print("initializing position check on (" +str(row) + "|" +str(col) +")")
    #check if there are any queens on this row
    for aux_col in range(col):
        if board[row][aux_col] == 1:
            if debug:
                print("position not ok")            
            return False
        else:
            continue
    if debug:
        print("row ok")
    #check diagonals
    #main
    aux_row, aux_col = row, col
    while aux_row >= 0 and aux_col >= 0:
        if board[aux_row][aux_col] == 1:
            if debug:
                print("position not ok")           
            return False
        else:
            aux_row-=1
            aux_col-=1
    #secondary
    new_aux_row, new_aux_col = row,col
    while new_aux_row < dimension and new_aux_col >= 0:
        if board[new_aux_row][new_aux_col] == 1:
            if debug:
                print("position not ok")
            return False
        new_aux_row+=1
        new_aux_col-=1
    if debug:
        print("diagonals ok")
        print("position ok")
    return True
#solve with backtracking
def backtrack(board, col, dimension):
    #to stop
    if col >= dimension:
        return
    for i in range(dimension):
        if can_put_here(board, i, col, dimension):
            board[i][col] = 1
            if col == dimension-1:
                #When find a solution
                if all_solutions:
                    add_solution(board)
                else:
                    first_solution(board)
                board[i][col] = 0
                return
            #recursion
            backtrack(board, col+1, dimension)
            #backtrack
            board[i][col] = 0
#when you are enabled to search for all solutions
#add to solution vector
def add_solution(board):
    global solutions
    solutions.append(copy.deepcopy(board))
#when you are enabled to return the first solution
def first_solution(board):
    global solution_unique
    solution_unique = copy.deepcopy(board)
#'main'
dimension = user_input()
board = init_board(dimension, debug)
solution_unique = None
solutions = []
backtrack(board, 0, dimension)
show_the_solutions(solutions, solution_unique ,dimension)
