from django import forms
from .models import Hospital, HospitalFacilities

class HospitalFacilitiesForm(forms.ModelForm):
    class Meta:
        model = HospitalFacilities
        fields = ('facilities')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.none()