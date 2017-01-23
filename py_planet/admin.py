from django.contrib import admin
from py_planet.models import TgGroup, TgUser, UserGroupModel

# Register your models here.

class BaseMaterialAdmin(admin.ModelAdmin):
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save(auto_change_updated_at=False)


@admin.register(TgGroup)
class TgGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


@admin.register(UserGroupModel)
class UserGroupModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    raw_id_fields = ('user', 'group')
