from django.shortcuts import render, redirect
from .models import Entity, Building, Floor, Room, Element, Task, Category, EntityUserRequest
from .forms import EntityForm, BuildingForm, FloorForm, RoomForm, ElementForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db import models
from .forms import CategoryForm
import pandas as pd
from django.conf import settings
from django.http import HttpResponse, Http404
from .utils import get_last_5_elements, get_top_buildings, get_top_5_categories, element_access_count_chart, sum_verified_elements_access_count, elements_count_per_month, get_total_elements, ElementFilter


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

    return render(request, 'inventory/dashboard.html', context={"is_any_entity": is_any_antity,
                                                                     'last_5_elements': last_5_elements, 'total_elements': total_elements, 'total_tasks': total_tasks,
                                                                     'total_rooms': rooms.count(), 'element_data_by_month': elements_per_month, 'top_buildings': top_buildings,
                                                                     'total_elements_per_category': top_elements_per_category, 'access_count': access_count,
                                                                     'total_verified_elements': total_verified_elements})


@login_required
def data_view(request, entity_id):
    user = request.user
    entities = Entity.objects.filter(users=user)
    elements = Element.objects.filter(room__floor__building__entity__id=entity_id)
    rooms = Room.objects.filter(floor__building__entity__id=entity_id)
    floors = Floor.objects.filter(building__entity__id=entity_id)
    buildings = Building.objects.filter(entity__id=entity_id)
    entity = Entity.objects.get(id=entity_id)
    is_entity_owner = entity.is_owner(user)
    filter_set = ElementFilter(request.GET, queryset=elements)

    return render(request, 'inventory/entity/entity_data.html', {'entity': entity, 'entity_id': entity.id, 'rooms':rooms, 'elements': filter_set.qs,
                                                       'buildings': buildings,'floors': floors, 'all_entities': entities, 'filter': filter_set, 'is_entity_owner': is_entity_owner},)




@login_required
def entity_settings_view(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    is_entity_owner = entity.is_owner(request.user)
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entity updated successfully.')
            return redirect('entity_settings', entity_id)
    else:
        form = EntityForm(instance=entity)
    
    return render(request, 'inventory/entity/entity_settings.html', {'form': form, 'entity_id': entity_id, 'entity':entity, 'SITE_URL': settings.SITE_URL, 'is_entity_owner': is_entity_owner}, )

@login_required
def add_user_to_entity_view(request, share_link):
    entity = get_object_or_404(Entity, share_link=share_link)
    EntityUserRequest.objects.get_or_create(user=request.user, entity=entity)
    messages.success(request, 'Your request has been sent to the entity owner.')
    return redirect('data', entity_id=entity.id)


def category_list_view(request, entity_id):
    categories = Category.objects.all()
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally add a success message or redirect to another page

    context = {
        'categories': categories,
        'form': form,
        'entity_id': entity_id,
    }

    return render(request, 'inventory/categories.html', context)


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

@login_required
def users_entity_view(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    users = entity.users.all()
    is_entity_owner = entity.is_owner(request.user)
    requests = EntityUserRequest.objects.filter(entity=entity) if is_entity_owner else None
    return render(request,'inventory/entity/all_entity_users.html', context={'users':users, 'entity': entity, 'is_entity_owner': is_entity_owner, 'requests': requests})

@login_required
def accept_request_view(request, request_id):
    entity_user_request = get_object_or_404(EntityUserRequest, id=request_id)

    # Ensure the current user is the owner of the entity
    if not entity_user_request.entity.is_owner(request.user):
        raise Http404("You do not have permission to accept this request.")

    entity = entity_user_request.entity
    user = entity_user_request.user
    entity.users.add(user)
    entity_user_request.delete()

    messages.success(request, f'{user.username} has been added to the entity.')
    return redirect('users_entity', entity_id=entity.id)

@login_required
def deny_request_view(request, request_id):
    entity_user_request = get_object_or_404(EntityUserRequest, id=request_id)

    # Ensure the current user is the owner of the entity
    if not entity_user_request.entity.is_owner(request.user):
        raise Http404("You do not have permission to deny this request.")

    entity = entity_user_request.entity
    user = entity_user_request.user
    entity_user_request.delete()

    messages.success(request, f'Request from {user.username} has been denied.')
    return redirect('users_entity', entity_id=entity.id)

def map_view(request, entity_id):
    entity = get_object_or_404(Entity, id=entity_id)
    context = {
        'latitude': entity.latitude,
        'longitude': entity.longitude,
        'entity': entity,
    }
    return render(request, 'inventory/entity/map.html', context)

    