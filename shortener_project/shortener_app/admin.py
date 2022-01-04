from django.contrib import admin

from shortener_app.models import Urls


class UrlsAdmin(admin.ModelAdmin):
    list_display = (
        'short_url',
        'real_url',
        'creation_date',
        'used_count',
        'created_by_id'
    )
    ordering = ('-creation_date',)


admin.site.register(Urls, UrlsAdmin)
