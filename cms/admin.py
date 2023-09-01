from django.contrib import admin

# Register your models here.

from .models import ContentItem

admin.site.register(ContentItem)