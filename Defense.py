def future_iceberg_state(iceberg, t, game, state):
    """
    Calculates the number of penguins in the iceberg after t turns.
    :param state: "ally" or "enemy" or "neutral"
    :param iceberg: The iceberg to calculate the state of.
    :param t: Time in turns.
    :param game: Game object.
    :return: Number of penguins in the iceberg after t turns.
    """
    if state == "netural":
        enemy_penguin_groups = game.get_enemy_penguin_groups()
        my_penguin_groups = game.get_my_penguin_groups()
        my_group_to_iceberg = [group for group in my_penguin_groups if group.destination == iceberg
                               and group.turns_till_arrival <= t]
        enemy_group_to_iceberg = [group for group in enemy_penguin_groups if group.destination == iceberg
                                  and group.turns_till_arrival <= t]
        current_penguin_amount = iceberg.penguin_amount
        number_of_penguins_arriving_from_me = sum([group.penguin_amount for group in my_group_to_iceberg])
        number_of_penguins_arriving_from_enemy = sum([group.penguin_amount for group in enemy_group_to_iceberg])
        return current_penguin_amount + number_of_penguins_arriving_from_me - number_of_penguins_arriving_from_enemy

    if state == "ally":
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
        penguin_arriving_from_each_iceberg[enemy_group.source] += enemy_group.penguin_amount
        for my_group in my_groups_from_iceberg:
            if my_group.destination in game.get_enemy_icebergs():
                penguin_arriving_from_each_iceberg[my_group.destination] -= my_group.penguin_amount
    number_of_penguins_arriving_from_enemy = sum([max(0, x) for x in penguin_arriving_from_each_iceberg.values()])

    # return the number of penguins in the iceberg after t turns
    return current_penguin_amount + number_of_penguins_arriving_from_me + iceberg.penguins_per_turn * t \
           - number_of_penguins_arriving_from_enemy



