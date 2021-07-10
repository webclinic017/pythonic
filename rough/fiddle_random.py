# fiddle_random.py
# This module is for testing random python codes only. 
# Do not use this for any module work


import timeit

def for_loop(seq, result_list=[]):
    for char in seq:
        result_list.append(char)
    return result_list

def list_comprehension(seq):
    return [char for char in seq]

%timeit for_loop("Hello World")  # working 
%timeit -r5 -n10 for_loop("Hello World") ### dont use: long exec time # not working as planned 


timeit.timeit(for_loop("Hello World"))

print(timeit.timeit(stmt = "for_loop(seq)",
                    setup="seq='Pylenin'",
                    number=10000))

print(timeit.timeit(stmt = "list_comprehension(seq)",
                    setup="seq='Pylenin'",
                    number=10000))