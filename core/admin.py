from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'image_', 'is_active')
    readonly_fields = ('image_', 'last_login', 'date_joined')
    exclude = ['password', ]
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_active', 'is_superuser', )
    list_per_page = 10
    list_max_show_all = 100

# admin.site.register(User)
