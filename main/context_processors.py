from .models import Entity

def entities_processor(request):
    entities = Entity.objects.filter(users=request.user)
    return {'entities': entities}