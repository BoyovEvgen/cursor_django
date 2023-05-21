from django.contrib import admin
from .models import MenuItem, SliderItem


class SliderItemAdmin(admin.ModelAdmin):
    exclude = ('link',)  # виключає відображення цього пункту в адмін панелі. автозаповнення прописав в models.py


admin.site.register(MenuItem)
admin.site.register(SliderItem, SliderItemAdmin)
