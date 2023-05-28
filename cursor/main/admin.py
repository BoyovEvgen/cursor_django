from django.contrib import admin
from .models import MenuItem, SliderItem, OrderItems, Order


class SliderItemAdmin(admin.ModelAdmin):
    exclude = ('link',)  # виключає відображення цього пункту в адмін панелі. автозаповнення прописав в models.py


admin.site.register(MenuItem)
admin.site.register(SliderItem, SliderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = fields = ['id', 'first_name', "last_name", "address", "email"]

    def queryset(self, request):
        qs = super(Order, self).queryset(request)
        return qs.all()


admin.site.register(Order, OrderAdmin)