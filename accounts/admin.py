from django.contrib import admin
from accounts.models import (
    Account,
    ShoppingCart,
    CartItem,
    Coupon,
    Ticket,
)


admin.site.register(Account)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Ticket)
