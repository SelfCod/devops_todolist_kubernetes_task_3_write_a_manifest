from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"todolists", views.TodoListViewSet)
router.register(r"todos", views.TodoViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path('health/liveness/', views.LivenessView.as_view(), name='liveness-probe'),
    path('health/readiness/', views.ReadinessView.as_view(), name='readiness-probe')
]
