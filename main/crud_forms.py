from django import forms
from .models import Entity, Building, Floor, Room, Element
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy


class EntityEditView(UpdateView):
    model = Entity
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_entity.html'
    success_url = reverse_lazy('all_data')

class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_entity.html'
    success_url = reverse_lazy('all_data')


class RoomEditView(UpdateView):
    model = Room
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_room.html'
    success_url = reverse_lazy('all_data')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_room.html'
    success_url = reverse_lazy('all_data')

class FloorEditView(UpdateView):
    model = Floor
    fields = ('number',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_floor.html'
    success_url = reverse_lazy('all_data')
    
class FloorDeleteView(DeleteView):
    model = Floor
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_floor.html'
    success_url = reverse_lazy('all_data')

class BuildingEditView(UpdateView):
    model = Building
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_floor.html'
    success_url = reverse_lazy('all_data')
    
class BuildingDeleteView(DeleteView):
    model = Building
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_floor.html'
    success_url = reverse_lazy('all_data')    

class ElementEditView(UpdateView):
    model = Element
    fields = ('name',)  # list all fields you want to edit
    template_name = 'inventory_app/CRUD/UPDATE/edit_element.html'
    success_url = reverse_lazy('all_data')
    
class ElementDeleteView(DeleteView):
    model = Element
    template_name = 'inventory_app/CRUD/DELETE/confirm_delete_element.html'
    success_url = reverse_lazy('all_data')    
