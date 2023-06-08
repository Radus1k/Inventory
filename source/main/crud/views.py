from main.models import Entity, Building, Floor, Room, Element, Task
from django.contrib.auth.decorators import login_required
from main.forms import EntityForm, BuildingForm, FloorForm, RoomForm, ElementForm, TaskForm
from .forms import ElementDeleteView, EntityDeleteView, FloorEditView, RoomEditView, ElementEditForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden


@login_required
def add_building(request, entity_id):
    buildings = Building.objects.filter(entity__id=entity_id)
    entity= Entity.objects.get(id=entity_id)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        print("Form: ", form.errors)
        if form.is_valid():
            building = form.save(commit=False)
            building.entity = entity
            building.save()
            messages.success(request, 'Building added successfully.')
            return redirect('add_building', entity_id=entity_id)
        else:
            messages.error(request, 'Error adding building.')
            form = BuildingForm()
    else:
        form = BuildingForm()
    return render(request, 'inventory/CRUD/CREATE/add_building.html', {'form': form, 'buildings': buildings,  'entity_id': entity_id,})


@login_required
def add_floor(request, entity_id):
    if request.method == 'POST':
        form = FloorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Floor added successfully.')
        else:
            messages.error(request, 'Error adding floor.')
        return redirect('add_floor', entity_id=entity_id)    
    else:
        form = FloorForm()
    form.fields['building'].queryset = Building.objects.filter(entity__id=entity_id) 
    floors = Floor.objects.filter(building__entity__id=entity_id) # Set the queryset for the room field
    return render(request, 'inventory/CRUD/CREATE/add_floor.html', {'form': form, 'floors': floors, 'entity_id': entity_id })


@login_required
def add_room(request, entity_id):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully.')
            return redirect('add_room', entity_id=entity_id)
    else:
        form = RoomForm()
        form.fields['floor'].queryset = Floor.objects.filter(building__entity__id=entity_id)  
    rooms = Room.objects.filter(floor__building__entity__id=entity_id) # Set the queryset for the room field
    
    return render(request, 'inventory/CRUD/CREATE/add_room.html', {'form': form, 'entity_id': entity_id, 'rooms': rooms} )


@login_required
def add_element(request, entity_id):
    if request.method == 'POST':
        form = ElementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Element added successfully.')
            return redirect('add_element', entity_id)
    else:
        form = ElementForm()
    form.fields['room'].queryset = Room.objects.filter(floor__building__entity__id=entity_id)
    elements = Element.objects.filter(room__floor__building__entity__id=entity_id)
    return render(request, 'inventory/CRUD/CREATE/add_element.html', {'form': form, 'entity_id': entity_id, 'elements':elements})

@login_required
def edit_element_view(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    entity = element.room.floor.building.entity
    if request.method == 'POST':
        form = ElementEditForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            messages.success(request, 'Element updated successfully.')
            return redirect('data', entity_id=entity.id)
        else:
            messages.error(request, 'Error updating element.')
    else:
        form = ElementEditForm(instance=element)

    return render(request, 'inventory/CRUD/UPDATE/edit_element.html', {'form': form, 'element_id':element_id})


@login_required
def delete_element_view(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    element.delete()
    messages.success(request, 'Element deleted successfully.')
    return redirect('data')  # Replace 'element_list' with the URL pattern name for your element list view

@login_required
def add_entity_view(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.owner = request.user
            entity.save()
            entity.users.add(request.user)
            entity.save()
            messages.success(request, 'Entity added successfully.')
            return redirect('add_building', entity_id=entity.id)
    else:
        form = EntityForm()
    return render(request, 'inventory/CRUD/CREATE/add_entity.html', {'form': form})


@login_required
def add_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user  # set user here
            form.save()
            messages.success(request, 'Task added successfully.')
            return redirect('add_task')
    else:
        form = TaskForm()
    return render(request, 'inventory/CRUD/CREATE/add_task.html', {'form': form})

@login_required
def delete_task_view(request, task_id):
    print("kekw")
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('dashboard')

    return render(request, 'inventory/CRUD/DELETE/delete_task.html', {'task': task})

@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('edit_task', task_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'inventory/CRUD/UPDATE/edit_task.html', {'form': form})
