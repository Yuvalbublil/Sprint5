from penguin_game import *

SCARE_FACTOR = 10
# from typing import *

def send_capital_reinforcement(game):
    """
    only by distance to capital.
    :param game:
    :return:
    """
    if game.get_my_icepital_icebergs() == []:
        return
    icepital = game.get_my_icepital_icebergs()[0]
    get_distance = lambda v: v.get_turns_till_arrival(dest)
    icebergs = sort(game.get_my_icebergs(), get_distance)  # .sort(key=get_distance)
    attack_potential = future_iceberg_state(icepital, icepital.get_turns_till_arrival(icebergs[0]) + SCARE_FACTOR, game, "ally")
    if attack_potential <= 0:
        for iceberg in icebergs:
            to_send = min(iceberg.penguin_amount - 1, -attack_potential + 1)
            iceberg.send_penguins(icepital, to_send)
            attack_potential += to_send








def future_iceberg_state(iceberg, t, game, state):
    """
    Calculates the number of penguins in the iceberg after t turns.
    :param state: True if the iceberg is an ally iceberg, False if it is an enemy iceberg.
    :param iceberg: The iceberg to calculate the state of.
    :param t: Time in turns.
    :param game: Game object.
    :return: Number of penguins in the iceberg after t turns.
    """
    if state == "neutral":
        enemy_penguin_groups = game.get_enemy_penguin_groups()
        my_penguin_groups = game.get_my_penguin_groups()
        enemy_groups_to_iceberg = [group for group in enemy_penguin_groups if group.destination == iceberg
                                   and group.turns_till_arrival <= t]
        my_groups_to_iceberg = [group for group in my_penguin_groups if group.destination == iceberg
                                   and group.turns_till_arrival <= t]
        current_penguin_amount = iceberg.penguin_amount
        return current_penguin_amount + iceberg.penguins_per_turn * t - sum(
            [group.penguin_amount for group in enemy_groups_to_iceberg]) + sum(
            [group.penguin_amount for group in my_groups_to_iceberg])

    elif state == "ally":
        enemy_penguin_groups = game.get_enemy_penguin_groups()
        my_penguin_groups = game.get_my_penguin_groups()

    else:
        enemy_penguin_groups = game.get_my_penguin_groups()
        my_penguin_groups = game.get_enemy_penguin_groups()

    my_groups_from_iceberg = [group for group in my_penguin_groups if group.source == iceberg]
    my_groups_to_iceberg = [group for group in my_penguin_groups if
                            group.destination == iceberg and group.turns_till_arrival <= t]
    enemy_groups_to_iceberg = [group for group in enemy_penguin_groups if
                               group.destination == iceberg and group.turns_till_arrival <= t]
    current_penguin_amount = iceberg.penguin_amount
    number_of_penguins_arriving_from_me = sum(
        [group.penguin_amount for group in my_groups_to_iceberg])  # calculate the number of penguins arriving

    # calculate how many penguins will arrive from each enemy iceberg
    penguin_arriving_from_each_iceberg = {iceberg: 0 for iceberg in game.get_enemy_icebergs()}
    for enemy_group in enemy_groups_to_iceberg:
        try:
            penguin_arriving_from_each_iceberg[enemy_group.source] += enemy_group.penguin_amount
        except KeyError:
            pass
        for my_group in my_groups_from_iceberg:
            if my_group.destination in game.get_enemy_icebergs():
                penguin_arriving_from_each_iceberg[my_group.destination] -= my_group.penguin_amount
    number_of_penguins_arriving_from_enemy = sum([max(0, x) for x in penguin_arriving_from_each_iceberg.values()])

    # return the number of penguins in the iceberg after t turns
    return current_penguin_amount + number_of_penguins_arriving_from_me + iceberg.penguins_per_turn * t \
           - number_of_penguins_arriving_from_enemy


def get_available_penguins(game, iceberg):
    available_penguins = iceberg.penguin_amount
    for t in range(game.turn, game.max_turns + 1, 1):
        available_penguins = min(available_penguins, future_iceberg_state(iceberg, t, game, "ally"))
    print("available penguins:", available_penguins)
    return available_penguins
