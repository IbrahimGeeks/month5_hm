from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')