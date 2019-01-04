from rest_framework import serializers
from .models import *

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class LoginInInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInInfo
        fields = '__all__'

class EmergencyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyService
        fields = '__all__'

class AmbulanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambulance
        fields = '__all__'

class LoginSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class BloodBankCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBankCenter
        fields = '__all__'

class DispensariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispensaries
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class BloodBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBilling
        fields = '__all__'

class BloodWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodWaste
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class DispensaryBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispensaryBilling
        fields = '__all__'

class AmbulanceBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceBilling
        fields = '__all__'


class TestServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestServices
        fields = '__all__'

class TestCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCentre
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class WebCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebCarousel
        fields = '__all__'

class AmbulanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceRequest
        fields = '__all__'

class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'

class BedBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedBilling
        fields = '__all__'

class HospitalBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalBilling
        fields = '__all__'

class MaintainenceBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintainenceBed
        fields = '__all__'

class HospitalFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalFacilities
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class DiseaseSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseSearch
        fields = '__all__'

class DiseaseCuredSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseCured
        fields = '__all__'

