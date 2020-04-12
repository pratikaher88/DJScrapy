from django.contrib import admin
# from main.models import Quote
from main.models import URL_Details

# class QuoteAdmin(admin.ModelAdmin):
#     list_display = ('text', )

# Register your models here.
admin.site.register(URL_Details)