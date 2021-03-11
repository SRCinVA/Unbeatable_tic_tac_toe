import math
import random

class Player: # this is a "base" player for use later on.
    def __init__(self, letter):   # "letter" is x or o
        self.letter = letter
    
    #we want all players to get their next move given a game (??)
    def get_move(self, game):
        pass  # just a placeholder in code.

class RandomComputerPlayer(Player): # notice we take in the Player class
    def __init__(self,letter):
        super().__init__(letter)    # we initialize the super class here as well 
                                    # 'super' gives access to methods and properties in the parent or sibling class, or makes that easier
                                    # b/c of inheritance here, you dont use 'self' (I guess?)
    def get_move(self,game):
        square = random.choice(game.available_moves())    # the computer can randomly start anywhere
                                                        # then we pass in game.available_moves (in game.py)
                                                        # remember that 'game' is our board.
        return square                                   # this just gives us a random valid spot


class HumanPlayer(Player):
    def __init__(self,letter):
        super().__init__(letter)

    def get_move(self, game):
        # before the player has input a letter to play
        valid_square = False     # lets the human input through the terminal. Starts 'False' because there is no input yet.
        val = None
        while not valid_square:  # meaning, "not False," so the square is in fact valid ...
            square = input(self.letter + '\'s turn. Input move (0-8):')  # square will be set to the input received.
                                                                        # looks like that input will be called "letter"
            # now we have to make sure that the input is valid
            try:
                val = int(square)   # to make sure the player actually put in an integer into "square" above.
                                    # if it can't be cast to an int, it will throw an error.
                if val not in game.available_moves():   # also, if it's not in the set of available moves, it will also be invalid.
                    raise ValueError     

                # if we pass both of those conditions, then we can go to the condition below:
                valid_square = True    
            except ValueError:  # next, if we don't get to "True," we "catch" the ValueError outside of the "try" block:
                print('Invalid square; try again!')   
        #after all of this, and we've gotten a valid square, we return it and it becomes the human player's next move.
        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # it will randomly choose a spot
        else:  # for each subsequent move ...
            square = self.minimax(game, self.letter) # ... use minimax for square choice
        return square

    def minimax(self, state, player): # 'state' (not 'game') b/c it's a screenshot of the game at that moment.
        max_player = self.letter # IOW, you as the X want to maximize yourself.
        other_player = 'O' if player == 'X' else 'X' # makes sure other player is *not* you. ('Else" is probably not necessary)

        # check if the previous move won the game 
        # with recursion, we need a base case
        # have any of the states we passed in produced a winner?
        if state.current_winner == other_player: # return it as a dictionary
            return {'position': None,                 # <- why is this 'None'?
                    'score': 1 * (state.num_empty_squares())
                    } # <- the minimax score