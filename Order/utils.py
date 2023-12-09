from Cart.models import Carts


def get_order_count_in_cart(cart_id):
    order_count = Carts.objects.get(id=cart_id).orders.count()
    return order_count
