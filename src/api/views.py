from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView  # Missing import added
from rest_framework.response import Response  # Optional but recommended
from django.http import JsonResponse  # Missing import added

from api.serializers import TodoListSerializer, TodoSerializer, UserSerializer
from lists.models import Todo, TodoList

from django.http import HttpResponse
from django.utils import timezone
import time



_START_TIME = time.time()

class LivenessView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return JsonResponse({'status': 'OK'}, status=200)


class ReadinessView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        if time.time() < _START_TIME + 60:
            return JsonResponse(
                {'status': 'initializing', 'seconds_remaining': int(60 - (time.time() - _START_TIME))}, 
                status=503
            )
        return JsonResponse({'status': 'READY'}, status=200)


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `creator` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # If the object doesn't have a creator (i.e. anon) allow all methods.
        if not obj.creator:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class TodoListViewSet(viewsets.ModelViewSet):

    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)

class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        creator = user if user.is_authenticated else None
        serializer.save(creator=creator)