
class Helpers(object):
    @staticmethod
    def get_cells(row, col, rows, cols, move):
        short_cell = (row + move["short"][0], col + move["short"][1])
        long_cell = (row + move["long"][0], col + move["long"][1])
        if not (0 <= short_cell[0] < rows and 0 <= short_cell[1] < cols):
            short_cell = None
        if not (0 <= long_cell[0] < rows and 0 <= long_cell[1] < cols):
            long_cell = None
        return (short_cell, long_cell)

    @staticmethod
    def reverse_tuple(tuple):
        new_tup = () 
        for k in reversed(tuple): 
            new_tup = new_tup + (k,) 
        return new_tup