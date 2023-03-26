from django.contrib import admin
from pproducts.models import *
from django.contrib import admin

from superuseractions.models import *




# from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

# class ProductAdmin(SummernoteModelAdmin):
#     empty_value_display = '-empty-'
#     search_fields = ['name',]
#     list_display = ('name',)
#     summernote_fields = ()



admin.register(QuickInviteLogs)
admin.register(UserHistoryTable)
admin.site.register([Product,Physician,ProductTags,LinkedProductTags,ProductImages])
# admin.site.register(Product, ProductAdmin)
