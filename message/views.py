import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.templatetags.static import static

from .models import MessageDialog, MessageRoom
from .service import hashsum_dialog
from custom_user.models import User


@login_required()
def index(request):
    rooms = MessageRoom.objects.filter(user__in=[request.user.id])
    result = list()
    if rooms:
        for room in rooms:
            for user in room.user.all().exclude(id=request.user.id):
                res = {'room': room.layer, "user": {'username': user.username, 'image': user.image, 'id': user.id}}
                result.append(res)
    return render(request, 'message/chat.html', context={'users': result})


def SearchUser(request, user_name):
    result = MessageRoom.objects.filter(user__in=[request.user.id])
    rooms = list([request.user.id])
    for room in result:
        for user in room.user.all().exclude(id=request.user.id):
            resurce = user.id
            rooms.append(resurce)
    userlist = list()
    if user_name:
        hash = hashsum_dialog()
        user_name = user_name.strip(' ')
        result = User.objects.filter(username__icontains=user_name).exclude(id__in=rooms)
        for user in result:
            if user.image:
                item = {'username': user.username, 'image': user.image.url, 'room': hash }
            else:
                item = {'username': user.username, 'image': static(), 'room': hash}
            userlist.append(item)
    return JsonResponse(userlist, safe=False)


def create_dialog(request):
    data = json.loads(request.body)
    room = data['room']
    user_to = data['userto']
    user_too = User.objects.get(username=user_to)

    result = MessageRoom.objects.create(layer=room)
    result.user.add(request.user)
    result.user.add(user_too)

    return JsonResponse({'result': 'ok'})



def OpenDialogUser(request, room):
    resource = MessageRoom.objects.get(layer=room)
    user = list()
    for item in resource.user.all().exclude(id=request.user.id):
        if item.image:
            image = item.image.url
        else:
            image = static('images/users/avatar-2.jpg')
        res = {'username': item.username, 'email': item.email, 'image': image, 'location': item.location.name, 'country': item.country.name, 'lang': item.language}
        user.append(res)
    return JsonResponse(user, safe=False)
