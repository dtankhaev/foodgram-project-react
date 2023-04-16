from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'first_name']
    list_filter = ['email', 'username', ]
    search_fields = ['first_name', ]


admin.site.register(Subscribe)
