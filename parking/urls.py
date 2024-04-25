
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from management.api.views import ParkingViewSet, ParkingSpaceViewSet, TicketViewSet, ReservationViewSet

router = SimpleRouter()

router.register("api/parking", ParkingViewSet, basename="parking")
router.register("api/parkingspaces", ParkingSpaceViewSet, basename="parking-spaces")
router.register("api/ticket", TicketViewSet, basename="tickets")
router.register("api/reservation", ReservationViewSet, basename="reservations")


urlpatterns = [
    path("admin/", admin.site.urls),
    path('parking/<uuid:pk>/list-parking-spaces/', ParkingViewSet.as_view({'get': 'list_parking_spaces'}), name='list-parking-spaces'),
    path("api/token-auth/", views.obtain_auth_token),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]+router.urls
