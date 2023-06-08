from django import forms
from django.contrib import messages
from django_select2.forms import Select2Widget
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView

from ..models import Entity, Building, Floor, Room, Element


class EntityEditView(UpdateView):
    model = Entity
    fields = ('name', 'is_private')
    template_name = 'inventory/CRUD/UPDATE/edit_entity.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.id,))
    
    def form_valid(self, form):
        messages.success(self.request, "Entity updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating entity.")
        return super().form_invalid(form)


class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'inventory/CRUD/DELETE/confirm_delete_entity.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Entity deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('data', args=(self.object.id,)) 


class RoomEditView(UpdateView):
    model = Room
    fields = ('name',)
    template_name = 'inventory/CRUD/UPDATE/edit_room.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.floor.building.entity.id,)) 
    
    def form_valid(self, form):
        messages.success(self.request, "Room updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating room.")
        return super().form_invalid(form)


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'inventory/CRUD/DELETE/confirm_delete_room.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.floor.building.entity.id,)) 
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Room deleted successfully.")
        return super().delete(request, *args, **kwargs)


class FloorEditView(UpdateView):
    model = Floor
    fields = ('number',)
    template_name = 'inventory/CRUD/UPDATE/edit_floor.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.building.entity.id,)) 
    
    def form_valid(self, form):
        messages.success(self.request, "Floor updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating floor.")
        return super().form_invalid(form)


class FloorDeleteView(DeleteView):
    model = Floor
    template_name = 'inventory/CRUD/DELETE/confirm_delete_floor.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.building.entity.id,)) 
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Floor deleted successfully.")
        return super().delete(request, *args, **kwargs)

class BuildingEditView(UpdateView):
    model = Building
    fields = ('name',)
    template_name = 'inventory/CRUD/UPDATE/edit_building.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.entity.id,)) 
    
    def form_valid(self, form):
        messages.success(self.request, "Building updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating building.")
        return super().form_invalid(form)
    
class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'inventory/CRUD/DELETE/confirm_delete_building.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.entity.id,)) 

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Building deleted successfully.")
        return super(BuildingDeleteView, self).delete(request, *args, **kwargs)


class ElementEditForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'room','category']
        widgets = {
            'room': Select2Widget(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; background-color: #e14eca;'  # Example styling, modify as needed
            }),
             'category': Select2Widget(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; background-color: #e14eca;'  # Example styling, modify as needed
            }),
            }

class ElementDeleteView(DeleteView):
    model = Element
    template_name = 'inventory/CRUD/DELETE/confirm_delete_element.html'
    
    def get_success_url(self):
        return reverse('data', args=(self.object.room.floor.building.entity.id,)) 
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Element deleted successfully.")
        return super(ElementDeleteView, self).delete(request, *args, **kwargs)
