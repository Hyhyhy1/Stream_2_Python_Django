from .views import ArtistViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/artists', ArtistViewSet, basename='artists')
urlpatterns = router.urls