# Create your views here.up
import keys


def update_available_item(invoice_order_item, type):
    order_item = invoice_order_item.order_items
    if type == keys.IN:
        order_item.available_qty = float(order_item.available_qty) + float(invoice_order_item.quantity)
    else:
        order_item.available_qty = float(order_item.available_qty) - float(invoice_order_item.quantity)

    order_item.save()
