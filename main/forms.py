from django import forms
from .models import Institute, Building, Floor, Room, Element

class EntityForm(forms.ModelForm):
    class Meta:
        model = Institute
        fields = ['name']
        # Add other fields specific to the Institute model

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name']
        # Add other fields specific to the Building model

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['number']
        # Add other fields specific to the Floor model

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        # Add other fields specific to the Room model

class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name']
        # Add other fields specific to the Element model