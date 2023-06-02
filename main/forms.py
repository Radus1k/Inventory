from django import forms
from .models import Entity, Building, Floor, Room, Element
from django_select2.forms import Select2Widget
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Entity

### Base Form Classes 
class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['name']
        # Add other fields specific to the entity model

class BuildingForm(forms.ModelForm):
  class Meta:
        model = Building
        fields = ['name','description', 'entity']
        # Add other fields specific to the Building model
        widgets = {
            'entity': Select2Widget(attrs={
                'class': 'form-control',
                'style': 'background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['number','building']
        # Add other fields specific to the Floor model
        widgets = {
            'building': Select2Widget(attrs={
                'class': 'form-control',
                'style': 'background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }        

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'floor']
        # Add other fields specific to the Room model
        widgets = {
            'floor': Select2Widget(attrs={
                'class': 'form-control',
                'style': 'background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }

class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'room']
        widgets = {
            'room': Select2Widget(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }




