from django.contrib import admin
from .models import Category
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id','title','subcategory','created','active')
	list_display_links = ('id','title')
	list_filter = ('active',)
	prepopulated_fields = {'slug':('title',)}

admin.site.register(Category,CategoryAdmin)