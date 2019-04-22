from .models import Order, Item


def get_bought_items(user):
    orders = Order.objects.filter(buyer=user)
    item_history = {}
    for order in orders:
        for order_item in order.items.all():
            if order_item.item.name in item_history:
                item_history[order_item.item.name][0] += order_item.quantity
                item_history[order_item.item.name][1] += float(
                    order_item.quantity * order_item.item.price
                )
            else:
                item_history[order_item.item.name] = [
                    order_item.quantity,
                    order_item.quantity * float(order_item.item.price),
                ]
    sorted_item_history = sorted(
        item_history.items(), reverse=True, key=lambda x: x[1]
    )
    return sorted_item_history


def get_most_bought_item(user):
    item_list = get_bought_items(user)
    if len(item_list) > 0:
        return Item.objects.get(name=item_list[0][0])
    else:
        return


def get_second_most_bought_item(user):
    item_list = get_bought_items(user)
    if len(item_list) > 1:
        return Item.objects.get(name=item_list[1][0])
    else:
        return


def get_third_most_bought_item(user):
    item_list = get_bought_items(user)
    if len(item_list) > 2:
        return Item.objects.get(name=item_list[2][0])
    else:
        return
