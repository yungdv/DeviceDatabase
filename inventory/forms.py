from django import forms
from .models import EquipmentType, Model, Hardware

class EquipmentTypeForm(forms.ModelForm):
    class Meta:
        model = EquipmentType
        fields = ['name']

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['name', 'equipment_type']

class HardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ['sn', 'model']
