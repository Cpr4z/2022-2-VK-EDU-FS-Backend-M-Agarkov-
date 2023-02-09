from rest_framework import generics
from rest_framework.response import Response
from .models import Chat, Message
from django.db.models import Q
from .serializers import ChatSerializer, MessageSerializer
from .tasks import send_admin_email
from users.permissions import AdminOrAuthor
from .utils import publish_message_to_websocket
from messenger.views import my_login_required


#{"user_id": 2} GET POST
class UserChats(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    #permission_classes = [AdminOrAuthor]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        #   print(user_id)
        return Chat.objects.filter(members=user_id)


class ChatDetails(generics.RetrieveUpdateDestroyAPIView):
    ''' обрабатывает get, put, patch, delete запросы '''
    serializer_class = ChatSerializer
    #permission_classes = [AdminOrAuthor]

    #def get_permissions(self):
    #    if self.request.method in ["PUT", "PATCH"]:
    #        permission_classes = [IsChatAdmin]
    #    elif self.request.method == "DELETE":
    #        permission_classes = [IsChatOwner]
    #    else:
    #        permission_classes = []
    #    return [permission() for permission in permission_classes]
    #@my_login_required
    def get_queryset(self):
        user_id = self.request.user.id
        chat_id = self.kwargs.get('pk')
        send_admin_email(chat_id, user_id)
        return Chat.objects.filter(Q(members=user_id) & Q(id=chat_id))


class ChatMessages(generics.ListCreateAPIView):
    ''' обрабатывает get и post запросы '''
    serializer_class = MessageSerializer
    #permission_classes = [AdminOrAuthor]

    #@my_login_required
    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return Message.objects.filter(chat_id=chat_id)

    #@my_login_required
    def create(self, request, *args, **kwargs):
        text = request.data.get('text')
        author_id = request.data.get('author_id')
        chat_id = request.data.get('chat_id')
        location = request.data.get('location')
        file = request.data.get('file')
        audio = request.data.get('audio')
        print(f'msg: {text} | from id {chat_id}')
        publish_message_to_websocket({'msg': text, 'chat_id': chat_id})
        Message.objects.create(chat_id=chat_id, author_id=author_id, text=text, location=location, file=file, audio=audio)
        return Response({})


class MessageDetails(generics.RetrieveUpdateDestroyAPIView):
    ''' обрабатывает get, put, patch, delete запросы '''
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    #permission_classes = [AdminOrAuthor]


