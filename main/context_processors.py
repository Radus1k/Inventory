from .models import Entity

def entities_processor(request):
    if not request.user.is_anonymous:
        entities = Entity.objects.filter(users=request.user)
    else:
        entities = Entity.objects.none()
    return {'entities': entities}