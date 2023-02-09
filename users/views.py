from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import AdminOrAuthor
from chats.tasks import send_admin_email


class AddUserAsMember(generics.UpdateAPIView):
    serializer_class = UserSerializer
    #permission_classes = [AdminOrAuthor]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        chat_id = self.kwargs.get('chat_id')
    #    send_admin_email(chat_id, user_id)
        return User.objects.filter(id=user_id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_id = self.kwargs.get('pk')
        chat_id = self.kwargs.get('chat_id')
        send_admin_email(chat_id, user_id)
        chat = user.chats.filter(id=chat_id).first()
        if chat is None:
            user.chats.add(chat_id)
            return Response({'ok': True}, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': 'user already in chat'
        }, status=status.HTTP_403_FORBIDDEN)


class DeleteUserFromChat(generics.UpdateAPIView):
    serializer_class = UserSerializer
    #permission_classes = [AdminOrAuthor]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return User.objects.filter(id=user_id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        chat_id = self.kwargs.get('chat_id')
        chat = user.chats.filter(id=chat_id).first()
        if chat is None:
            return Response({
                'ok': False,
                'result': 'user already deleted'
            }, status=status.HTTP_403_FORBIDDEN)

        user.chats.remove(chat_id)
        return Response({'ok': True}, status=status.HTTP_200_OK)


class GetUserInfo(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    #permission_classes = [AdminOrAuthor]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return User.objects.filter(id=user_id)


