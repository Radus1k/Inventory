from django.shortcuts import render, redirect
from .models import Institute, Building, Floor, Room
from .forms import EntityForm, BuildingForm, FloorForm, RoomForm, ElementForm
from django.contrib.auth.decorators import login_required


@login_required
def register_entity(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save()
            return redirect('add_building', entity_id=entity.id)
    else:
        form = EntityForm()
    return render(request, 'inventory_app/register_entity.html', {'form': form})

@login_required
def add_building(request, entity_id):
    entity = Institute.objects.get(id=entity_id)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.institute = entity
            building.save()
            return redirect('add_floor', entity_id=entity_id, building_id=building.id)
    else:
        form = BuildingForm()
    return render(request, 'inventory_app/add_building.html', {'form': form})

@login_required
def add_floor(request, entity_id, building_id):
    building = Building.objects.get(id=building_id)
    if request.method == 'POST':
        form = FloorForm(request.POST)
        if form.is_valid():
            floor = form.save(commit=False)
            floor.building = building
            floor.save()
            return redirect('add_room', entity_id=entity_id, building_id=building_id, floor_id=floor.id)
    else:
        form = FloorForm()
    return render(request, 'inventory_app/add_floor.html', {'form': form})

@login_required
def add_room(request, entity_id, building_id, floor_id):
    floor = Floor.objects.get(id=floor_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.floor = floor
            room.save()
            return redirect('add_element', entity_id=entity_id, building_id=building_id, floor_id=floor_id, room_id=room.id)
    else:
        form = RoomForm()
    return render(request, 'inventory_app/add_room.html', {'form': form})

@login_required
def add_element(request, entity_id, building_id, floor_id, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        form = ElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.room = room
            element.save()
            return redirect('add_element', entity_id=entity_id, building_id=building_id, floor_id=floor_id, room_id=room_id)
    else:
        form = ElementForm()
    return render(request, 'inventory_app/add_element.html', {'form': form})

@login_required
def home_view(request):
     return render(request, 'inventory_app/home.html', context={})