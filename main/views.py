from django.shortcuts import render, redirect
from .models import Entity, Building, Floor, Room, Element, Task
from .forms import EntityForm, BuildingForm, FloorForm, RoomForm, ElementForm
from .crud_forms import ElementEditForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import models
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from .utils import get_last_5_elements, get_top_buildings, get_top_5_categories, element_access_count_chart, sum_verified_elements_access_count, elements_count_per_month, get_total_elements


@login_required
def dashboard_view(request):
    user_entities = Entity.objects.filter(users=request.user)
    is_any_antity = user_entities.exists()
    last_5_elements = get_last_5_elements(request.user)

    rooms = Room.objects.filter(floor__building__entity__in=user_entities)

    total_elements = get_total_elements(request.user)

    elements_per_month = elements_count_per_month(user_entities=user_entities)

    total_verified_elements = sum_verified_elements_access_count(request.user)

    top_buildings = get_top_buildings(request.user)

    top_elements_per_category = get_top_5_categories(request.user)

    access_count = element_access_count_chart(request.user)

    total_tasks = Task.objects.filter(user=request.user)

    return render(request, 'inventory_app/dashboard.html', context={"is_any_entity": is_any_antity,
                                                                     'last_5_elements': last_5_elements, 'total_elements': total_elements, 'total_tasks': total_tasks,
                                                                     'total_rooms': rooms.count(), 'element_data_by_month': elements_per_month, 'top_buildings': top_buildings,
                                                                     'total_elements_per_category': top_elements_per_category, 'access_count': access_count,
                                                                     'total_verified_elements': total_verified_elements})


@login_required
def data_view(request, entity_id):
    entities = Entity.objects.filter(users=request.user)
    elements = Element.objects.filter(room__floor__building__entity__id=entity_id)
    rooms = Room.objects.filter(floor__building__entity__id=entity_id)
    floors = Floor.objects.filter(building__entity__id=entity_id)
    buildings = Building.objects.filter(entity__id=entity_id)
    entity = Entity.objects.get(id=entity_id)
    return render(request, 'inventory_app/data.html', {'entity': entity, 'entity_id': entity.id, 'rooms':rooms, 'elements': elements,
                                                       'buildings': buildings,'floors': floors, 'all_entities': entities},)


@login_required
def all_data_view(request):
    entities = Entity.objects.filter(users=request.user)
    entity_with_most_elements = entities.annotate(num_elements=models.Count('building__floor__room__element')).order_by('-num_elements').first()
    entity_id = entity_with_most_elements.id
    elements = Element.objects.filter(room__floor__building__entity__id=entity_id)
    rooms = Room.objects.filter(floor__building__entity__id=entity_id)
    floors = Floor.objects.filter(building__entity__id=entity_id)
    buildings = Building.objects.filter(entity__id=entity_id)
    entity = Entity.objects.get(id=entity_id)
    return render(request, 'inventory_app/data.html', {'all_entities': entities, 'entity_with_most_elements': entity_with_most_elements,
                                                       'rooms':rooms, 'elements': elements,
                                                       'buildings': buildings,'floors': floors,'entity':entity})


@login_required
def add_inv_entity_view(request):
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.save()
            entity.users.add(request.user)
            entity.save()
            messages.success(request, 'Entity added successfully.')
            return redirect('add_building', entity_id=entity.id)
    else:
        form = EntityForm()
    return render(request, 'inventory_app/CRUD/CREATE/add_inv_entity.html', {'form': form})


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
    return render(request, 'inventory_app/CRUD/CREATE/add_building.html', {'form': form, 'buildings': buildings,  'entity_id': entity_id,})


@login_required
def add_floor(request, entity_id):
    if request.method == 'POST':
        form = FloorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Floor added successfully.')
        else:
            messages.error(request, 'Error adding floor.')
            form = FloorForm()
        return redirect('add_floor', entity_id=entity_id)    
    else:
        form = FloorForm()
    form.fields['building'].queryset = Building.objects.filter(entity__id=entity_id) 
    floors = Floor.objects.filter(building__entity__id=entity_id) # Set the queryset for the room field
    return render(request, 'inventory_app/CRUD/CREATE/add_floor.html', {'form': form, 'floors': floors, 'entity_id': entity_id })


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
    
    return render(request, 'inventory_app/CRUD/CREATE/add_room.html', {'form': form, 'entity_id': entity_id, 'rooms': rooms} )


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
    return render(request, 'inventory_app/CRUD/CREATE/add_element.html', {'form': form, 'entity_id': entity_id, 'elements':elements})


@login_required
def edit_element_view(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    if request.method == 'POST':
        form = ElementEditForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            messages.success(request, 'Element updated successfully.')
            return redirect('all_data')
        else:
            messages.error(request, 'Error updating element.')
    else:
        form = ElementEditForm(instance=element)

    return render(request, 'inventory_app/CRUD/UPDATE/edit_element.html', {'form': form, 'element_id':element_id})

@login_required
def entity_settings_view(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
   
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entity updated successfully.')
            return redirect('entity_settings', entity_id)
    else:
        form = EntityForm(instance=entity)
    
    return render(request, 'inventory_app/entity_settings.html', {'form': form, 'entity_id': entity_id, 'entity':entity, 'SITE_URL': settings.SITE_URL}, )


@login_required
def delete_element_view(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    element.delete()
    messages.success(request, 'Element deleted successfully.')
    return redirect('data')  # Replace 'element_list' with the URL pattern name for your element list view


@login_required
def add_user_to_entity(request, share_link):
    entity = get_object_or_404(Entity, share_link=share_link)
    entity.users.add(request.user)
    messages.success(request, 'You have been added to the entity.')
    return redirect('data', entity_id=entity.id)


def export_data_view(request, entity_id):
    import pytz
    entity = get_object_or_404(Entity, pk=entity_id)
    data = []
    buildings = Building.objects.filter(entity=entity)
    for building in buildings:
        floors = Floor.objects.filter(building=building)
        for floor in floors:
            rooms = Room.objects.filter(floor=floor)
            for room in rooms:
                elements = Element.objects.filter(room=room)
                for element in elements:
                    data.append({
                        'Entity': entity.name,
                        'Building': building.name,
                        'Floor': floor.number,
                        'Room': room.name,
                        'Element': element.name,
                        'Inserted_at': element.inserted_at.astimezone(pytz.UTC).replace(tzinfo=None),
                    })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ExportedData.xlsx'
    df.to_excel(response, index=False)

    return response

