# File: admin.py
# Description: This file contains the Django model imports for the admin console
# Author(s): Devil Corp

# imports
from django.contrib import admin
from .models import Patient
from .models import Doctor
from .models import Nurse
from .models import Administrator
from .models import Hospital
from .models import LogInInfo
from .models import Prescription
from .models import Appointment
from .models import Test
from .models import EmergencyContact
from .models import Message
from .models import EmergencyService,Event,Ambulance,BloodBankCenter,Dispensaries,Medicine,Login,BloodBilling
from .models import *

# model registers
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Administrator)
admin.site.register(Hospital)
admin.site.register(LogInInfo)
admin.site.register(Login)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Test)
admin.site.register(EmergencyContact)
admin.site.register(Message)
admin.site.register(EmergencyService)
admin.site.register(Event)
admin.site.register(Ambulance)
admin.site.register(BloodBankCenter)
admin.site.register(Dispensaries)
admin.site.register(Medicine)
admin.site.register(BloodBilling)
admin.site.register(BloodWaste)
admin.site.register(AmbulanceBilling)
admin.site.register(DispensaryBilling)
admin.site.register(TestCentre)
admin.site.register(TestServices)
admin.site.register(Specialization)
admin.site.register(Qualification)