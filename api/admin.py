
# Register your models here.
from django.contrib import admin
from .models import Vendor,purchaseOrder

admin.site.register(Vendor)
admin.site.register(purchaseOrder)