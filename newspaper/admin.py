from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "featured_image", "author", "status", "category", "views_count"]

admin.site.register(Post, PostAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject']
admin.site.register(Contact, ContactAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["id", "email"]
admin.site.register(Newsletter, NewsletterAdmin)

admin.site.register(Comment)