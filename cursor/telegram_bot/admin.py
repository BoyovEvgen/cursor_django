from django.contrib import admin
from .models import ProfileTelegram, DiscontSetings

class ProductInline(admin.TabularInline):
    model = ProfileTelegram.like_products.through
    extra = 0
    verbose_name = 'Liked Product'
    verbose_name_plural = 'Liked Products'

@admin.register(ProfileTelegram)
class ProfileTelegramAdmin(admin.ModelAdmin):

    list_display = ['id', 'user_name', 'first_name', 'last_name', 'phone']
    exclude = ('like_products',)
    inlines = [ProductInline, ]


admin.site.register(DiscontSetings)