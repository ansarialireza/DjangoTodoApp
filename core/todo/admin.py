from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "is_completed", "created_at", "updated_at")
    list_filter = ("is_completed", "created_at")
    search_fields = ("title",)
    list_editable = ("is_completed",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "is_completed")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Task, TaskAdmin)
