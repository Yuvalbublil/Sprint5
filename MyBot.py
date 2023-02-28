"""
This is an example for a bot.
"""
from penguin_game import *

from Attack import spend_penguins
def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    # Go over all of my icepitals and conquer icebergs
    spend_penguins(game, 50)
    # for my_iceberg in game.get_my_icepital_icebergs():
    # # The amount of penguins in my iceberg.
    #     my_penguin_amount = my_iceberg.penguin_amount  # type: int


