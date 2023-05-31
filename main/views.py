from django.shortcuts import render, redirect
from .models import Institute, Building, Floor, Room, Element
from .forms import EntityForm, BuildingForm, FloorForm, RoomForm, ElementForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


@login_required
def dashboard_view(request):
    user_entities = Institute.objects.filter(user=request.user)
    is_any_antity = user_entities.exists()
    # The queryset is not empty
    return render(request, 'inventory_app/dashboard.html', context={"is_any_entity": is_any_antity})


@login_required
def add_entity_view(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.user = request.user
            entity.save()
            messages.success(request, 'Entity added successfully.')
            return redirect('add_building', entity_id=entity.id)
    else:
        form = EntityForm()
    return render(request, 'inventory_app/register_entity.html', {'form': form})


@login_required
def add_building(request, entity_id):
    buildings = Building.objects.filter(institute__id=entity_id)
    entity = Institute.objects.get(id=entity_id)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        print("Form: ", form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building added successfully.')
            return redirect('add_building', entity_id=entity_id)
        else:
            messages.error(request, 'Error adding building.')
            form = BuildingForm()
    else:
        form = BuildingForm()
    form.fields['institute'].queryset = Institute.objects.filter(user=request.user)    
    return render(request, 'inventory_app/add_building.html', {'form': form, 'buildings': buildings,  'entity_id': entity_id,})


@login_required
def add_floor(request, entity_id):
    if request.method == 'POST':
        form = FloorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data')
    else:
        form = FloorForm()
    form.fields['building'].queryset = Building.objects.filter(institute__id=entity_id)  # Set the queryset for the room field
    return render(request, 'inventory_app/add_floor.html', {'form': form})


@login_required
def add_room(request, entity_id):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_room', entity_id=entity_id)
    else:
        form = RoomForm()
        form.fields['floor'].queryset = Floor.objects.filter(building__institute__id=entity_id)  
    return render(request, 'inventory_app/add_room.html', {'form': form})


@login_required
def add_element(request, entity_id):
    if request.method == 'POST':
        form = ElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data')
    else:
        form = ElementForm()
    return render(request, 'inventory_app/add_element.html', {'form': form})


@login_required
def data_view(request):
    institutes = Institute.objects.prefetch_related('building_set__floor_set__room_set').all()
    return render(request, 'inventory_app/data.html', {'institutes': institutes})


@login_required
def delete_element_view(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    element.delete()
    messages.success(request, 'Element deleted successfully.')
    return redirect('data')  # Replace 'element_list' with the URL pattern name for your element list view