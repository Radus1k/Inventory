from django import forms
from .models import Entity, Building, Floor, Room, Element
from django.views.generic import UpdateView, DeleteView
from django_select2.forms import Select2Widget
from django.urls import reverse_lazy
from django.contrib import messages


class EntityEditView(UpdateView):
    model = Entity
    fields = ('name','is_private', )  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_entity.html'
    success_url = reverse_lazy('all_data')

class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_entity.html'
    success_url = reverse_lazy('all_data')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Entity deleted successfully.")
        return super(EntityDeleteView, self).delete(request, *args, **kwargs)


class RoomEditView(UpdateView):
    model = Room
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_room.html'
    success_url = reverse_lazy('all_data')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_room.html'
    success_url = reverse_lazy('all_data')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Room deleted successfully.")
        return super(RoomDeleteView, self).delete(request, *args, **kwargs)


class FloorEditView(UpdateView):
    model = Floor
    fields = ('number',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_floor.html'
    success_url = reverse_lazy('all_data')
    
class FloorDeleteView(DeleteView):
    model = Floor
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_floor.html'
    success_url = reverse_lazy('all_data')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Floor deleted successfully.")
        return super(FloorDeleteView, self).delete(request, *args, **kwargs)


class BuildingEditView(UpdateView):
    model = Building
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_building.html'
    success_url = reverse_lazy('all_data')
    
class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_building.html'
    success_url = reverse_lazy('all_data')    

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Building deleted successfully.")
        return super(BuildingDeleteView, self).delete(request, *args, **kwargs)


class ElementEditForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'room']
        widgets = {
            'room': Select2Widget(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; background-color: #e14eca;'  # Example styling, modify as needed
            }),
            }

class ElementDeleteView(DeleteView):
    model = Element
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_element.html'
    success_url = reverse_lazy('all_data')    

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Element deleted successfully.")
        return super(ElementDeleteView, self).delete(request, *args, **kwargs)
