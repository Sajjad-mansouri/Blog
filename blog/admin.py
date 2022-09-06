from django.contrib import admin
from .models import BlogModel,IPAddressModel
class BlogAdmin(admin.ModelAdmin):
	list_display = ('id','title','author','is_publish','published')
	list_display_links = ('id', 'title')
	list_filter = ('author','published')
	search_fields = ('title','description')
	prepopulated_fields = {'slug':('title',)}


admin.site.register(BlogModel,BlogAdmin)

admin.site.register(IPAddressModel)