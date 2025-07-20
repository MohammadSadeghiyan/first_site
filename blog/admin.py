from django.contrib import admin

# Register your models here.
from blog.models import Post,Category

class PostAdmin(admin.ModelAdmin):
    date_hierarchy="created_date"
    list_display=('title','counted_views','status','published_date','created_date')
    list_filter=('status',)
    search_fields=['title','content']
admin.site.register(Category)
admin.site.register(Post,PostAdmin)

