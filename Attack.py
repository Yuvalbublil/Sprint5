from penguin_game import *
from Defense import *

class AttackPlan:
    def __init__(self, source, destination, penguins):
        self.source = source
        self.destination = destination
        self.penguins = penguins

    def activate(self):
        self.source.send_penguins(self.destination, self.penguins)


def check_if_have_enough_penguins_to_attack(game, my_iceberg, other_iceberg):
    if get_available_penguins(game,my_iceberg) > other_iceberg.penguin_amount:
        return True
    else:
        return False


def get_closest_netural(game, iceberg):
    closest = None
    for neutral in game.get_neutral_icebergs():
        if closest is None:
            closest = neutral
        elif iceberg.distance_to(closest) > iceberg.distance_to(neutral):
            closest = neutral
    return closest


def get_closest_netural_for_all(game):
    closest = None
    for my_iceberg in game.get_my_icebergs():
        if closest is None:
            if can_attack_closest_netural(game, my_iceberg):
                closest = Min_Attack_Plan(game, my_iceberg)
        elif my_iceberg.distance_to(closest.destination) > my_iceberg.distance_to(
                get_closest_netural(game, my_iceberg)) and can_attack_closest_netural(
                game, my_iceberg):
            closest = Min_Attack_Plan(game, my_iceberg)
    return AttackPlan


def Min_Attack_Plan(game, my_iceberg, extra_penguins=1):
    return AttackPlan(my_iceberg, get_closest_netural(game, my_iceberg), get_closest_netural(game,
                                                                                             my_iceberg).penguin_amount + extra_penguins)


def can_attack_closest_netural(game, my_iceberg):
    return get_available_penguins(game,my_iceberg) > get_closest_netural(game, my_iceberg).penguin_amount


def cheapest_iceberg_to_upgrade(game):
    cheapest = None
    for my_iceberg in game.get_my_icebergs():
        if cheapest is None:
            if my_iceberg.can_upgrade():
                cheapest = my_iceberg
        elif my_iceberg.upgrade_cost < cheapest.upgrade_cost and my_iceberg.can_upgrade():
            cheapest = my_iceberg
    return cheapest


def spend_penguins(game, amount_to_spend):
    optional_upgrade = cheapest_iceberg_to_upgrade(game)
    optional_attack = get_closest_netural_for_all(game)
    if amount_to_spend < min(optional_attack.penguins, optional_upgrade.upgrade_cost):
        return None
    if optional_attack is not None and optional_attack.penguins < optional_upgrade.upgrade_cost:
        optional_attack.activate()
    elif optional_upgrade is not None:
        optional_upgrade.upgrade()
