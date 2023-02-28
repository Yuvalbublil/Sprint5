from penguin_game import *
# from typing import *

def send_capital_reinforcement(game):
    """
    only by distance to capital.
    :param game:
    :return:
    """
    dest = game.get_my_icepital_icebergs()[0]
    nearest = get_closest_icebergs(game, dest)
    need = 0
    for t in range(game.max_turns):
        need = max(need, future_state(game, t, nearest) * (-1))

    for i in nearest: #send from the nearests icebergs the need.
        i.send_penguins(dest, min(need, i.penguin_amount))
        need -= i.penguin_amount



def get_closest_icebergs(game, dest):
    """

    :param dest:
    :return:
    """
    closest = game.get_my_icepital_icebergs()[0]
    get_distance = lambda v : v.get_turns_till_arrival(dest)
    return game.get_my_icebergs().sort(key=get_distance)


def future_state(game, t, iceberg):
    """
    :param game:
    :param t:
    :param iceberg:
    :return:
    """
    pass
