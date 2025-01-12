"""
This module is used for modifying BP costs of badges, FP costs of both badge
and partner moves and SP costs for star power moves.
"""
import random

from db.move import Move


def _get_shuffled_costs(movetype, costtype):
    """
    Returns a list of tuples where the first value holds the dbkey for a move
    cost and the second value holds the shuffled cost depending on which
    move type and cost type are given as parameters.
    """
    shuffled_costs = []
    db_keys = []
    db_values = []

    for move in Move \
                .select() \
                .where(Move.move_type == movetype) \
                .where(Move.cost_type == costtype):
        db_keys.append(move.get_key())
        db_values.append(move.cost_value)

    random.shuffle(db_values)

    for db_key, db_value in zip(db_keys, db_values):
        shuffled_costs.append((db_key, db_value))

    return shuffled_costs


def _get_rnd_bp_costs() -> list:
    """
    Returns a list of tuples where the first value holds the dbkey for a badge
    BP cost and the second value holds its randomized BP cost.
    """
    random_costs = []

    for move in Move \
                .select() \
                .where(Move.move_type == "BADGE") \
                .where(Move.cost_type == "BP"):
        default_cost = move.cost_value

        # 10% Chance to pick randomly between 1 and 8, else randomly choose
        # from -2 to +2, clamping to 1-8
        if random.randint(1, 10) == 10:
            new_cost = random.randint(1, 8)
        else:
            new_cost = default_cost + random.choice([-2, -1, 0, 1, 2])
            if new_cost < 1:
                new_cost = 1
            if new_cost > 8:
                new_cost = 8

        random_costs.append((move.get_key(), new_cost))
        print(f"BP: {move.move_name}: {new_cost}")

    return random_costs


def get_randomized_moves(
    shuffle_badges_bp:bool,
    shuffle_badges_fp:bool,
    shuffle_partner_fp:bool,
    shuffle_starpower_sp:bool
):
    """
    Returns a list of tuples where the first value holds the dbkey for a move
    cost and the second value holds the shuffled FP,BP,SP cost.
    """
    move_costs = []

    if shuffle_badges_bp:
        move_costs.extend(_get_rnd_bp_costs())

    if shuffle_badges_fp:
        move_costs.extend(_get_shuffled_costs("BADGE", "FP"))

    if shuffle_partner_fp:
        move_costs.extend(_get_shuffled_costs("PARTNER", "FP"))

    if shuffle_starpower_sp:
        move_costs.extend(_get_shuffled_costs("STARPOWER", "FP"))

    return move_costs
