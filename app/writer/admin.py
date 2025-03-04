from django.contrib import admin

from writer.models import Article

@admin.register(Article)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified', 'is_premium')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_premium',)
