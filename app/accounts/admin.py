from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Admin, Customer

# Register your models here.


@admin.register(Admin)
class CustomAdmin(UserAdmin):
    list_display = ("id", "email", "name", "created_at")
    list_filter = ()
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "created_at",
    )
    add_form_template = "admin/accounts/customer/change_form.html"
    list_filter = ()
    search_fields = ("email", "name")
    ordering = ("email",)
    readonly_fields = ["agreed_at", "agreed_agent", "agreed_ip"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "last_name",
                    "email",
                    "password",
                    "phone",
                    "birth_date",
                    "photo",
                )
            },
        ),
        (
            _("Endereço"),
            {
                "fields": (
                    "city",
                    "state",
                    "zipcode",
                    "address",
                    "number",
                    "district",
                    "complement",
                )
            },
        ),
        (
            _("Permissões"),
            {
                "fields": (
                    "is_active",
                    "agreed_at",
                    "agreed_agent",
                    "agreed_ip",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "password1", "password2"),
            },
        ),
    )


admin.site.unregister(Group)
