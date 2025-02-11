from django.contrib import admin
from accounts.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # این بخش برای مخفی کردن فیلد پسورد در پنل ادمین است
    readonly_fields = ('password',)


