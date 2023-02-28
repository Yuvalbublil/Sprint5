from penguin_game import *
from Defense import *

class AttackPlan:
    def __init__(self, source, destination, penguins):
        self.source = source
        self.destination = destination
        self.penguins = penguins

    def activate(self):
        self.source.send_penguins(self.destination, self.penguins)

def get_other_icebergs(game):
    return game.get_enemy_icebergs() + game.get_neutral_icebergs()


def get_closest_netural(game, iceberg):
    closest = None
    for neutral in get_other_icebergs(game):
        if closest is None:
            closest = neutral
        elif iceberg.get_turns_till_arrival(closest) > iceberg.get_turns_till_arrival(neutral):
            closest = neutral
    return closest


def get_closest_netural_for_all(game):
    closest = None
    for my_iceberg in game.get_my_icebergs():
        if closest is None:
            if can_attack_closest_netural(game, my_iceberg):
                closest = Min_Attack_Plan(game, my_iceberg, get_closest_netural(game, my_iceberg))
        elif my_iceberg.get_turns_till_arrival(closest.destination) > my_iceberg.get_turns_till_arrival(
                get_closest_netural(game, my_iceberg)) and can_attack_closest_netural(
                game, my_iceberg):
            closest = Min_Attack_Plan(game, my_iceberg, get_closest_netural(game, my_iceberg))
    return closest, 1/closest.source.get_turns_till_arrival(closest.destination)


def Min_Attack_Plan(game, my_iceberg,target_iceberg, extra_penguins=1):
    return AttackPlan(my_iceberg, target_iceberg, predict_future_state_in_arrival(game, my_iceberg, target_iceberg) + extra_penguins)

def predict_future_state_in_arrival(game, my_iceberg, other_iceberg):
    return future_iceberg_state(other_iceberg, my_iceberg.get_turns_till_arrival(other_iceberg),game,
                                is_Ally=False)



def can_attack_closest_netural(game, my_iceberg):
    return my_iceberg.penguin_amount > get_closest_netural(game, my_iceberg).penguin_amount


def cheapest_iceberg_to_upgrade(game):
    cheapest = None
    for my_iceberg in game.get_my_icebergs():
        if cheapest is None:
            if my_iceberg.can_upgrade():
                cheapest = my_iceberg
        elif my_iceberg.upgrade_cost < cheapest.upgrade_cost and my_iceberg.can_upgrade():
            cheapest = my_iceberg
    return cheapest, 1

def get_best_clone(game):
    best = None
    cloneberg = game.get_cloneberg()
    for my_iceberg in game.get_my_icebergs():
        total_time = 2*my_iceberg.get_turns_till_arrival(cloneberg) + cloneberg.cloneberg_pause_turns
        if best is None:
            if total_time < game.turns_left:
                best = my_iceberg
        elif total_time < best.get_turns_till_arrival(cloneberg) + cloneberg.cloneberg_pause_turns:
            best = my_iceberg


def spend_penguins(game, amount_to_spend):
    optional_upgrade = cheapest_iceberg_to_upgrade(game)
    optional_attack = get_closest_netural_for_all(game)

    if optional_attack is None:
        if optional_upgrade is not None:
            optional_upgrade.upgrade()
        return None
    if optional_upgrade is None:
        return optional_attack.activate()
    if amount_to_spend< min(optional_attack.penguins, optional_upgrade.upgrade_cost):
        return None
    if optional_attack.penguins < optional_upgrade.upgrade_cost:
        optional_attack.activate()
    else:
        optional_upgrade.upgrade()


