from django.contrib import admin
from .models import Asset

admin.site.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    pass
