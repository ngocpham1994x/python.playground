import math
import random as rd

class Player:
    def __init__(self, letter):
        self.letter = letter    # player x or o

    def get_move(self, game):   # get next move given a name
        pass

class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for our next move
        square = rd.choice(game.available_moves())  # square = []
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = false
        val = None
        while not valid_square:
            square = input (self. letter + '\'s turn. Input move (0-9): ')
            # we're going to check that this is a correct value by trying to cast it to an integer,
            # and if it's not, then we say it's invalid.
            # if that spot is not available on the board, we also say it's invalid
            
        # return super().get_move(game)

