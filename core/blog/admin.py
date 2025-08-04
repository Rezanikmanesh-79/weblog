from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from blog.models import User, Post, Category, Tag, Comment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Role detail", {"fields": ("role", "is_verified")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_verified", "is_active", "is_staff"),
        }),
    )
    list_display = ("username", "email", "role", "is_active", "is_staff", "is_verified")
    list_filter = ("role", "is_active", "is_staff", "is_verified")
    search_fields = ("username", "email")
    ordering = ("email",)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at", "updated_at")
    list_filter = ("status", "author", "categories", "tags", "created_at")
    search_fields = ("title", "body", "author__username")
    filter_horizontal = ("categories", "tags")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    autocomplete_fields = ["author"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "email", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "body")
    autocomplete_fields = ["post"]
