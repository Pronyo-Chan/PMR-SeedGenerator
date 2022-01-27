import random

from db.item import Item
from worldgraph import get_node_identifier

def get_alpha_prices(
    placed_items
):
    """alpha test function for item pricing"""
    if False:
        for node in placed_items:
            node.current_item.base_price = 1
    else:
        for node in placed_items:
            node_identifier = get_node_identifier(node)
            if "Shop" in node_identifier:
                item_type = Item.get_type(node.current_item.value)
                if "HOS_06" in node_identifier:
                    # Merlow's StarPiece trade
                    if item_type == "COIN":
                        buy_price = 0
                    else:
                        buy_price = 2
                else:
                    # Regular shop
                    if item_type == "ITEM":
                        sell_price = node.current_item.base_price
                        buy_price = round(sell_price * 1.5)

                        # Randomly adjust price a bit
                        rnd_factor = random.choice([0.75,0.9,1,1.1,1.25])

                        buy_price = round(buy_price * rnd_factor)

                        if buy_price == 0:
                            buy_price = 1

                        # If below 5, let value stay, else round to nearest 5
                        if (buy_price - (buy_price % 5)) != 0:
                            buy_price = round(buy_price/5) * 5
                    
                    #    print(f"{node.current_item.item_name=}: {sell_price=} -> {buy_price=}")

                    elif item_type in ["BADGE", "KEYITEM", "PARTNER"]:
                        buy_price = random.choice([10,15,20,25,30])

                    elif item_type == "COIN":
                        buy_price = 1

                    elif item_type == "STARPIECE":
                        buy_price = random.choice([2,4,6,8,10])

                    else:
                        buy_price = 35

                node.current_item.base_price = buy_price

    return placed_items
