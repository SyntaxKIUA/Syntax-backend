from django.contrib import admin
from accounts.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # delete password in django admin site
    exclude = ('password',)

admin.site.register(Profile)