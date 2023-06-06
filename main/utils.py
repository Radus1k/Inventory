
from django.db import models
from .models import Element, Entity, Building
from django.utils import timezone


def elements_count_per_month(user_entities):
    elements = Element.objects.filter(room__floor__building__entity__in=user_entities)

    now = timezone.now()
    data = []
    for i in range(12):
        month = now.month - i
        year = now.year
        if month <= 0:
            month += 12
            year -= 1
        count = elements.filter(inserted_at__year=year, inserted_at__month=month).count()
        data.insert(0, count)  # We insert at the beginning to get the oldest month first
    return data

def get_last_5_elements(user):
    entities = Entity.objects.filter(users=user)
    elements = Element.objects.filter(room__floor__building__entity__in=entities).order_by('-inserted_at')[:5]
    return elements


def get_top_buildings(user):
    # Get all entities associated with the user
    user_entities = Entity.objects.filter(users__in=[user])
    
    # Get buildings of these entities
    buildings = Building.objects.filter(entity__in=user_entities)
    
    # Annotate each building with the count of its rooms
    buildings = buildings.annotate(room_count=models.Count('floor__room'))

    buildings = buildings.filter(room_count__gt=0)

    # Order by the room count and limit to top 6
    top_buildings = buildings.order_by('-room_count')[:6]

    # Manually construct the JSON data
    data = [{'name': b.name, 'room_count': b.room_count} for b in top_buildings]

    return data 

def get_top_5_categories(user):
    # Get all entities associated with the user
    user_entities = Entity.objects.filter(users__in=[user])
    
    # Get elements of these entities
    elements = Element.objects.filter(room__floor__building__entity__in=user_entities)

     # Group by category and count the elements
    category_counts = elements.values('category__name').annotate(element_count=models.Count('id'))

    # Exclude elements with count values of 0
    category_counts = category_counts.exclude(element_count=0)

    # Order by the count and limit to top 5
    top_categories = category_counts.order_by('-element_count')[:5]

    # Manually construct the JSON data
    data = [{'name': c['category__name'], 'element_count': c['element_count']} for c in top_categories]
    
    return data


def element_access_count_chart(user):
    # Retrieve the entities associated with the user
    user_entities = Entity.objects.filter(users=user)

    # Retrieve the top 5 elements based on their access counts filtered by the user's entities
    elements = Element.objects.filter(room__floor__building__entity__in=user_entities).order_by('-access_count')[:5]
    access_count_data = [{'name': element.name, 'access_count': element.access_count} for element in elements]

    return access_count_data

def get_total_elements(user):
    # Get all entities associated with the user
    user_entities = Entity.objects.filter(users__in=[user])
    
    # Get elements of these entities
    elements = Element.objects.filter(room__floor__building__entity__in=user_entities)
    return elements.count()


def sum_verified_elements_access_count(user):
    user_entities = Entity.objects.filter(users=user)

    sum_access_count = Element.objects.filter(
        room__floor__building__entity__in=user_entities,
        access_count__gt=0,
        category__isnull=False
    ).aggregate(sum_access_count=models.Sum('access_count'))['sum_access_count']

    return sum_access_count or 0