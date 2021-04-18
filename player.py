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
            square = self.minimax(game, self.letter)['position']# ... use minimax for square choice. Note that it's recursive.
        return square

    def minimax(self, state, player): # 'state' (not 'game') b/c it's a snapshot of the game at that moment (presumably not the game as an entirety).
        max_player = self.letter # IOW, you as the X want to maximize yourself.
        other_player = 'O' if player == 'X' else 'X'    # makes sure other_player and you aren't the same. 'else X' means: "well, what if "player" *isn't* X? Then "other_player" *definitely* is!!" 
        
        # check if the previous move won the game 
        # recursion requires a base case: have any previous states produced a winner?
        # we need to keep track of position AND score for minimax to work
        if state.current_winner == other_player: # return it as a dictionary
            return {'position': None,                 # <- "None" because nobody is moving (or just to initiaize?)
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
                    } # <- the minimax score function. Don't understand her explanation.

        elif not state.empty_squares(): # if nobody has won AND there are no empty squares, then it's a tie
            return {'position':None, 'score': 0} # none because nobody is moving (or because we're just initializing?)

        # now the algorithm:
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # a dictionary that preserves the best postiion and score
                                                            # initialize the score to negative infinity so that one iteration beats that score; by definition it is higher.
        else: 
            best = {'position': None, 'score': math.inf} # here, we're trying to minimize, so start at positive infinity.
        
        for possible_move in state.available_moves():
            # step 1: make a move and try that spot.
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after making that move.
            sim_score = self.minimax(state, other_player) # then, alternate the players.
            # question: how does that alternating take place in the above code?
            
            # step 3: undo that move (so we could try the next one in a future iteration)
            state.board[possible_move] = ' ' # we reset that point on the board to an empty space.
            state.current_winner = None      # this undoes whatever move you just did. 
            sim_score['position'] = possible_move # otherwise, gets messed up from recursion (???)
            
            # step 4: update the dictionary if necessary (meaning, if you produced a better move, thus beating the current best score).
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score # then replace that score with the new one if it's better
            else: # meaning, your player is the min player
                if sim_score['score'] < best['score']:
                    best = sim_score  # we're trying to maximize the max player and minimize the min
        
        return best
            # after we've tired all of these, the 'best' dictionary will contain the
            # best possible next move and the score that would arise from it.
            # she added [position] to get_move() to index that dictionary. No explanation as to how that works.
        