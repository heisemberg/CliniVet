from django.contrib import admin
from .models.user import User
from .models.admin import Admin
from .models.client import Client
from .models.pet import Pet
from .models.medical_record import MedicalRecord
from .models.appointment import Appointment
from .models.doctor import Doctor
from .models.availability import Availability
from .models.inventory_item import InventoryItem
from .models.invoice import Invoice, InvoiceItem

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(MedicalRecord)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Availability)
admin.site.register(InventoryItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)


# Register your models here.
