from django.contrib import admin
from .models import MenuItem, SliderItem, Discount_code, CustomUser
from products.models import OrderItem, Order

class SliderItemAdmin(admin.ModelAdmin):
    exclude = ('link',)  # виключає відображення цього пункту в адмін панелі. автозаповнення прописав в models.py


admin.site.register(MenuItem)
admin.site.register(SliderItem, SliderItemAdmin)
admin.site.register(Discount_code)
admin.site.register(CustomUser)


# class OrderItemsInline(admin.TabularInline):  # відображення в рядок
class OrderItemsInline(admin.StackedInline):  # в колонку
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'address', 'email', 'total_price']
    inlines = [OrderItemsInline]

admin.site.register(Order, OrderAdmin)