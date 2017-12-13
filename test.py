from nqueens import NQueens
import sys
a = NQueens()
n = int(input("A PORRA DO NUMERO DAS RAINHAS: "))
a.new_n_queens(n, 10000 * n)
