from django.contrib import admin
from .models import Bank , Branch
# Register your models here.
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name' , 'swift_code' , 'institution_number' , 'description' , 'owner')
    search_fields = ('name' , 'swift_code' , 'institution_number' , 'description' , 'owner__username')
    
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name' , 'transit_number' , 'address', 'email' , 'capacity' , 'last_modified' , 'bank')
    search_fields = ('name' , 'transit_number' , 'address' , 'email' , 'bank__name')
    list_filter = ('bank' , 'last_modified')