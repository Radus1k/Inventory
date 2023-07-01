from django import forms
from .models import Entity, Building, Floor, Room, Element, Category, Task
from django_select2.forms import Select2Widget
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Entity

### Base Form Classes 
class EntityForm(forms.ModelForm):
    is_private = forms.BooleanField(required=False, label='Public', help_text='Check this box if you want the entity to be public. It will be private by default.')

    class Meta:
        model = Entity
        fields = ['name', 'is_private', 'latitude', 'longitude']
        # Add other fields specific to the entity model

    def __init__(self, *args, **kwargs):
        super(EntityForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-control'})
        self.fields['latitude'].label = 'Latitude (Optional)'
        self.fields['longitude'].label = 'Longitude (Optional)'        

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name','description', ]
        # Add other fields specific to the Building model

class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['number','building']
        widgets = {
            'building': Select2Widget(attrs={
                'class': 'form-control',
                'style': 'background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }        
        
    def __init__(self, *args, **kwargs):
        super(FloorForm, self).__init__(*args, **kwargs)
        try:
            last_building = Building.objects.latest('id')  # Replace 'id' with your DateTime field if you have one
            self.fields['building'].initial = last_building
        except Building.DoesNotExist:
            pass


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'floor']
        widgets = {
            'floor': Select2Widget(attrs={
                'class': 'form-control',
                'style': 'background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        try:
            last_floor = Floor.objects.latest('id')  # Replace 'id' with your DateTime field if you have one
            self.fields['floor'].initial = last_floor
        except Floor.DoesNotExist:
            pass


class ElementForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        empty_label='Select a category (optional)',
        label='Category: \t',
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'style': 'width: 100%; background-color: #e14eca;'
        }),
    )
      
    class Meta:
        model = Element
        fields = ['name', 'room',]
        widgets = {
            'room': Select2Widget(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; background-color: #e14eca;'  # Example styling, modify as needed
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(ElementForm, self).__init__(*args, **kwargs)
        try:
            last_room = Room.objects.latest('id')  # Replace 'id' with your DateTime field if you have one
            self.fields['room'].initial = last_room
        except Room.DoesNotExist:
            pass

    def save(self, commit=True):
        element = super().save(commit=False)
        element.category = self.cleaned_data['category']
        if commit:
            element.save()
        return element    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Category Name'}
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', ]

    def save(self, commit=True):
        task = super().save(commit=False)
        task.user = self.instance.user  # assuming 'user' is a field in your 'Task' model
        if commit:
            task.save()
        return task 