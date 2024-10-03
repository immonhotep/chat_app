from .models import  FriendRequest
from rooms.models import Message
def navbar_context(request):
    if request.user.is_authenticated:
        
        return {'pending_request': FriendRequest.objects.filter(sent_from=request.user,status=1),'pending_inivitation':FriendRequest.objects.filter(sent_to=request.user,status=1),'last_message':Message.objects.filter(checked=False,room__participant=request.user,room__private=True).exclude(user=request.user).count()}
    
    else:    
        return {}