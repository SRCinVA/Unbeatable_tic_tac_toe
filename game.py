import time
from player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer # related to __name__ statement below

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]    # a single list of length 9 to rep 3*3 board
                                                # the indexes we assign to this list will represent the board
        self.current_winner = None  # to keep track of winner
    
    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]: 
        # the large bracketed statement is indexing into the len 9 list defined above
        # the result of each of those iterations (for i in range (3)) is a row "chunk" of the final board
        # the innermost is a slice (i.e., 'start':'end'); 'range(3)' is for each row, meaning indices of 0, 1, and 2 (upper-bound exclusive)
        # the range bracket creates three "self-contained" chunks of indices, like this:
                # 0:3    (0,1,2) <-index positions
                # 3:6    (3,4,5) <-index positions
                # 6:8    (6,7,8) <-index positions
        
            print('| ' + ' | '.join(row) + ' |')
            # 1.) print the first pipe; 
            # 2.) the join() method intersperses the pipe(s or however many required?) 
            #     between the iterables present in [row] from above; 
            # 3.) print the last pipe.
    
    @staticmethod # static methods are methods bound to the class, not the object
    def print_board_nums(): # this doesn't relate to any specific board, so we don't have to pass in self (makes sense).
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        # iterating over 'j' feeds in exactly like printing the board, to manufacture all of the row "chunks"
        # "this is saying 'give me the indices of the rows, for all of the rows'."
        # "i" is the "x" or "o" String that gets dropped into the (0,1,2) or (3,4,5) or (6,7,8)
        # that is created by the iteration over 'j'
        
        # now, we concatenate the strings and print the board, like above:
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # the long way to do it:
        # moves = []  # initialize moves to an empty list.
        # for (i,spot) in enumerate(self.board): # basically, it attaches a value ("x" or "o") to its index place as a tuple.
        #     # ['x','x','o'] --> [(0,'x'),(1,'x'),(2,'o')]
        #     if spot == ' ':      # meaning that it's empty and available for use.
        #         moves.append(i)  # we append that index to know that it's been taken. 
        #         return moves
    
        # the same thing, using list comprehension:
        return [i for i, spot in enumerate(self.board) if spot == ' ']
        # basically, this says: "when enumerating through the tuples of (i, spot),
        # if 'spot' is empty, put it into this list (which is what enumerate() creates for us)."
        # it then returns this list (makes it available outside of this function)
    
    def empty_squares(self):
        return ' ' in self.board     # returns a boolean if the selection is an empty space

        # to count the number of empty squares
    def num_empty_squares(self):
        return self.board.count(' ')# returns the available_moves list, so we can count the available spaces

    # to actually make a move
    def make_move(self, square, letter):
        # to make a move, be sure it's valid. If valid, returns True; if not, then False.
        if self.board[square] == ' ': # if that square is empty ...
            self.board[square] = letter # ... then the letter goes in that space.
            # now you need to check if you actually won (we'll do this later):
            if self.winner(square, letter): # passes in last move ("we'll come back to the winner function")
                self.current_winner = letter # if that's true, then we can assign current_winner to that letter (X or O)
            return True
        return False

    def winner(self, square, letter):
        # we have to check all possibilities of three in a row.
        # check rows
        row_ind = square//3  # divide by three and then round down. Ex: if square = 5, divide by 3 = 1.67 (row 1)
        row = self.board[row_ind*3 : (row_ind + 1) * 3] # this just highlights the three possible rows
        if all([spot == letter for spot in row]):   # "if all spots (or whatever) equal the same letter for spots in this row ...
            return True
        
        # check columns
        col_ind = square % 3   # the modulus of 8 is 2 (making it the third column, according to index)
        column = [self.board[col_ind+i*3] for i in range(3)]  # Ex.: [1 + (2*3)] = spot 7; tells us all spot indexes on the board by column.
        if all([spot == letter for spot in column]): # same reason as above.
            return True

        # check diagonals (we basically hard code these)
        if square % 2 == 0: # these are the only spots possible for either diagonal
            diagonal1 = [self.board[i] for i in [0,4,8]] # <i> is just spot holder as the "for" statement traverses 0,4, and 8 and puts them in a list.
            if all([spot == letter for spot in diagonal1]): # a similar checker to above
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all of these checks fail, then there's no winner, so it returns False
        return False

# notice that this function exists outside of the TicTacToe class
def play(game, x_player, o_player, print_game=True): # if a human is playing, show the board
    if print_game: #meaning, if we want to see it
        game.print_board_nums() # put print_board_nums against 'game' (but where is 'game' coming from?)

    letter = 'X' # a starting letter
    # iterate while the game has empty squares
    # don't worry about a winner; because we'll just return whatever breaks the loop). (I guess we'll see)

    # she calls this "the play loop" (which makes sense):
    while game.empty_squares(): #to check if the game has empty squares
        # while there are empty spaces, get the next move from the appropriate player:
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

    # define a function to actually make a move
        if game.make_move(square, letter): # meaning, "is valid":
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board() # so that we can see what the user just did
                print('')          # just an empty next line.

            if game.current_winner: # implies "if True" and no longer set to None, then this is our checker
                if print_game: # not sure why this line is needed
                    print(letter + ' wins!')
                return letter

            # after making a single move, we need to alternate letters
            # here, we assign the letter to 'O' if it's currently 'X',
            # otherwise, we just assign 'letter' to 'X' (don't even need the rest of the statement)
            letter = 'O' if letter == 'X' else 'X'
            # another way to do this is below (probably what I would have done):
            # if letter == 'X':
            #   letter = 'O'
            # else:
            #   letter = 'X' 
        # let's introduce a pause of 0.8 seconds
        time.sleep(.8)

    if print_game: # here, if we fall out of the while loop, then there was no winner (it was a tie)
        print('It\'s a tie!')

if __name__ == '__main__': # it seems (?) that this sets 'game.py' as the main file.
    x_player = HumanPlayer('X')    # not clear what's going on with these importations.
    o_player = GeniusComputerPlayer('O')
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
