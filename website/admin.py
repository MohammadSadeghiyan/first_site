from django.contrib import admin
from website.models import contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy="created_date"
    list_display=('name','email','subject','created_date','created_date')
    list_filter=('email',)
    search_fields=['name','subject']

admin.site.register(contact,ContactAdmin)
