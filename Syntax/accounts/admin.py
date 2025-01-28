from django.contrib import admin
from accounts.models import Comment, Like , User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email' ,'first_name' ,'last_name')

admin.site.register(Comment)
admin.site.register(Like)
