from django.contrib import admin
from .models import User

# Register your models here.

admin.site.site_url = "/"


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "account_type", "verified")
    list_editable = ("verified",)
    search_fields = ("username", "email")
    list_filter = ("verified",)
