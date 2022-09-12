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
        square = rd.choice(game.available_moves())  # square = []
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        return super().get_move(game)

