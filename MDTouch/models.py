# imports
from django.db import models
from datetime import date,datetime
from django.utils import timezone
from django.db import models


# This module contains the Hospital model.
# D
class Hospital(models.Model):
    name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    city = models.CharField(max_length = 40,default = '')
    state = models.CharField(max_length = 20, default = '')
    pin = models.IntegerField(default = 0)
    contact = models.IntegerField(default = 0)
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    def __str__(self):
        return self.name

#to contain what are the diffrent kinds of tests
# D
class TestServices(models.Model):
    name = models.CharField(max_length=80,default='')
    def __str__(self):
        return self.name

# D
class TestCentre(models.Model):
    name = models.CharField(max_length = 20,default = '')
    address = models.CharField(max_length = 40,default ='')
    city = models.CharField(max_length = 20,default='')
    state = models.CharField(max_length = 15,default ='')
    tests = models.ForeignKey(TestServices,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name
# This module contains the Emergency Contact model.
# D
class EmergencyContact(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName


# This module contains the Patient model.
# D
class Patient(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True,on_delete = models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    username = models.CharField(max_length=30, default='')
    hospital = models.ForeignKey(Hospital, default=None, blank=True, null=True,on_delete = models.CASCADE)
    password = models.CharField(max_length=25,default='Password123!')
    dept = models.CharField(max_length=2,default='PA')
    def __str__(self):
        return self.firstName + " " + self.lastName

    def getEmergencyContact(self, patient):
        return patient.contact

    def getHospital(self, patient):
        return patient.hospital
# D
class Specialization(models.Model):
    skill = models.CharField(max_length=70,default='')
    def __str__(self):
        return self.skill
# D
class Qualification(models.Model):
    degree = models.CharField(max_length=60,default='')
    def __str__(self):
        return self.degree

# This module contains the Doctor model.
# D
class Doctor(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE,null=True)
    qualification = models.ForeignKey(Qualification,on_delete=models.CASCADE,null=True)
    workplace = models.ForeignKey(Hospital, null=True,on_delete = models.CASCADE)
    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, doctor):
        return doctor.workplace

# This module contains the Nurse model.
class Nurse(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True,on_delete = models.CASCADE)
    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, nurse):
        return nurse.workplace


# This module contains the Administrator model.
# D
class Administrator(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True,on_delete = models.CASCADE)
    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, admin):
        return admin.workplace


# This module contains the Prescription model.
# D
class Prescription(models.Model):
    name = models.CharField(max_length=50, default='')
    patient = models.ForeignKey(Patient, null=True,on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True,on_delete = models.CASCADE)
    dosage = models.CharField(max_length=100)
    prescription = models.CharField(max_length=800,null=True,default='')

    def __str__(self):
        return self.name

    def getPatient(self, pre):
        return pre.patient

    def getDoctor(self, pre):
        return pre.doctor


# This module contains the Test model.
# D
class Test(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500)
    released = models.BooleanField(default=False)
    testResults = models.FileField(upload_to='tests', null=True, blank=True)
    centre = models.ForeignKey(TestCentre,null=True,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, null=True,on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True,on_delete = models.CASCADE)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.name

    def getPatient(self, test):
        return test.patient

    def getDoctor(self, test):
        return test.doctor


# This module contains the Appointment model.
# D
class Appointment(models.Model):
    appttime = models.CharField(max_length=5, default='')  # '05:30'
    phase = models.CharField(max_length=10, default='')     # 'AM' or 'PM'
    appointmentdate = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient, null=True,on_delete = models.CASCADE)
    location = models.ForeignKey(Hospital, null=True,on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True,on_delete = models.CASCADE)
    message = models.TextField(max_length=200,default='')
    dateofrequest = models.DateField(default=timezone.now)

    def __str__(self):
        return self.patient

    def getPatient(self, appoint):
        return appoint.patient

    def getLocation(self, appoint):
        return appoint.location

    def getDoctor(self, appoint):
        return appoint.doctor


# This module contains the messaging model
# D
class Message(models.Model):
    senderName = models.CharField(max_length=50, default='')
    senderType = models.CharField(max_length=50, default='')
    receiverName = models.CharField(max_length=50, default='')
    viewed = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    subjectLine = models.CharField(max_length=50, default='')
    message = models.TextField(max_length=500, default='')
    senderDelete = models.BooleanField(default=False)
    receiverDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.subjectLine

    def getSenderType(self, message):
        return message.senderType


# This module contains the LogInInfo model.
# D
class LogInInfo(models.Model):
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.username

# D
class EmergencyService(models.Model):
    name = models.CharField(max_length=30,default='')
    city = models.CharField(max_length=25,default='new city')
    address = models.TextField(max_length=80,default='')
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    contact_number = models.CharField(max_length = 12,default = "")

# D
class Ambulance(models.Model):
    number = models.CharField(max_length=15,default="ECNALUBMA")
    driver = models.CharField(max_length=25,default='')
    capacity = models.CharField(max_length = 2,default = '2')
    contact = models.CharField(max_length=12,default = "")
    type = models.CharField(max_length = 10,default = 'van')
    active = models.BooleanField(default=True)
    service = models.ForeignKey(EmergencyService,null=True,on_delete = models.CASCADE)
    def __str__(self):
        return self.type

# D
class Login(models.Model):      #for software
    username = models.CharField(max_length=30,default="")
    password = models.CharField(max_length=30,default="Password123!")
    dept = models.CharField(max_length=2,default='NA')
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    def __str__(self):
        return self.username

#class ServiceAdmin(models.Model):
#    username = models.CharField(max_length=25, default='')
#    password = models.CharField(max_length=35, default='')

# D
class BloodBankCenter(models.Model):
    username = models.ForeignKey(Login,default='',on_delete=models.CASCADE)
    name = models.CharField(max_length = 30, default= '')
    address = models.TextField(max_length = 200,default = '')
    city = models.CharField(max_length = 40,default = '')
    contact = models.IntegerField(default = 0)
    email = models.EmailField(max_length=70,blank=True, null= True, unique= True)
    quantityAp = models.IntegerField(default = 0)
    quantityAm = models.IntegerField( default=0)
    quantityBp = models.IntegerField( default=0)
    quantityBm = models.IntegerField( default=0)
    quantityABp = models.IntegerField( default=0)
    quantityABm = models.IntegerField( default=0)
    quantityOp = models.IntegerField(default=0)
    quantityOm = models.IntegerField( default=0)
    def __str__(self):
        return self.name

# D
class Dispensaries(models.Model):
    name = models.ForeignKey(Login,default='',on_delete=models.CASCADE)
    regno = models.CharField(max_length = 10,default = '')
    address = models.TextField(max_length=100,default='')
    city = models.CharField(max_length=25,default='')
    state = models.CharField(max_length=20,default='')
    def __str__(self):
        return self.name

# D
class Event(models.Model):
    eventlocation = models.TextField(max_length=100,default='')
    city = models.CharField(max_length=25,default='')
    hospitalid = models.ForeignKey(Hospital,null=True,blank=True,on_delete=models.SET_NULL)
    bloodbankid = models.ForeignKey(BloodBankCenter,null=True,blank=True,on_delete=models.SET_NULL)
    dispensaryid = models.ForeignKey(Dispensaries,null=True,blank=True,on_delete=models.SET_NULL)
    testcentreid = models.ForeignKey(TestCentre,null=True,blank=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length = 40,default= '')
    description = models.TextField(max_length = 600,default = '')
    pic = models.CharField(max_length=2000,default='',null=True)
    dateofcreation = models.DateField(default=timezone.now)
    dateofevent = models.DateField(default=timezone.now)
    totalregistered = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# D
class BloodBilling(models.Model):
    patid = models.ForeignKey(Patient,on_delete=models.CASCADE)
    Eventid = models.ForeignKey(Event,null = True,on_delete=models.CASCADE)
    bbcid = models.ForeignKey(BloodBankCenter,null = True,on_delete=models.CASCADE)
    bloodtype = models.CharField(max_length=3,default='')
    bloodquantity = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.date

# D
class BloodWaste(models.Model):
    quantity = models.IntegerField(default=0)
    bloodgrp = models.CharField(max_length=5,default='')
    bbcid = models.ForeignKey(BloodBankCenter,on_delete=models.CASCADE)
    reason = models.TextField(max_length=200,default='')
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.quantity)

# D
class Medicine(models.Model):
    name = models.CharField(max_length = 40,default = '')
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default = 0)
    dispensary = models.ForeignKey(Dispensaries,null=True,blank=True,on_delete=models.SET_NULL)
    batch = models.IntegerField(default = 0)
    manufacturedate = models.DateField(default = timezone.now)
    expirydate = models.DateField(default = timezone.now)


# D
class DispensaryBilling(models.Model):
    dispensaryid = models.ForeignKey(Dispensaries,on_delete=models.CASCADE)
    patientid = models.ForeignKey(Patient,on_delete=models.CASCADE)
    medicineid = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    eventid = models.ForeignKey(Event,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

# D
class AmbulanceBilling(models.Model):
    ambulance_id = models.ForeignKey(Ambulance,on_delete=models.CASCADE)
    patientid = models.ForeignKey(Patient,on_delete=models.CASCADE)
    destination = models.TextField(max_length=100,default='')
    kilometers = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=datetime.now())


class WebCarousel(models.Model):
    banner = models.CharField(default='Welcome',max_length=30)
    url = models.CharField(default='img not found',max_length=800)
    slug = models.CharField(default='HealthCare',max_length=15)

class Notice(models.Model):
    host = models.CharField(default="Health Ministry",max_length=100)
    notice = models.TextField(default='Important notice',max_length=400)
    date = models.DateTimeField(default=datetime.now())
