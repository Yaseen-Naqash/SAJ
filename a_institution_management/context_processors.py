from .models import Branch

def branches_context(request):
    return {
        'branches': Branch.objects.all()
    }