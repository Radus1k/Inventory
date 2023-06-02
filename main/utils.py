
from .models import Element, Entity

def get_last_5_elements(user):
    entities = Entity.objects.filter(users=user)
    elements = Element.objects.filter(room__floor__building__entity__in=entities).order_by('-inserted_at')[:5]
    return elements

# Usage example
