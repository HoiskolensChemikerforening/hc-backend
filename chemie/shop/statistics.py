from .models import Order, Item
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz


def get_bought_items(user):
    orders = Order.objects.filter(buyer=user)
    item_history = {}
    for order in orders:
        for order_item in order.items.all():
            if order_item.item.name in item_history:
                item_history[order_item.item.name][0] += order_item.quantity
                item_history[order_item.item.name][1] += float(
                    order_item.quantity * order_item.total_price
                )
            else:
                item_history[order_item.item.name] = [
                    order_item.quantity,
                    order_item.quantity * float(order_item.total_price),
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


def get_plot_item(user, item_name):
    try:
        orders = Order.objects.filter(buyer=user)
        now = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        plot_time = [now.date()]
        plot_quantity = [0]
        for order in orders:
            for order_item in order.items.all():
                if order_item.item.name == item_name:
                    if order.created.date() in plot_time:
                        plot_quantity[
                            plot_time.index(order.created.date())
                        ] += order_item.quantity
                    else:
                        for i in range(
                            (plot_time[-1] - order.created.date()).days
                        ):
                            plot_quantity.append(0)
                            plot_time.append(
                                plot_time[-1] - datetime.timedelta(days=1)
                            )
                        plot_quantity[-1] = order_item.quantity
    except ObjectDoesNotExist:
        return None, None
    plot_time = [str(time) for time in plot_time]
    return plot_time, plot_quantity
