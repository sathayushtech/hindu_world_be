from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrgnizationView,CountryView,GetItemByfield_InputView,continentsView,AddOrgnization,CountsView

router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)
router.register(r'continents',continentsView)


urlpatterns=[

    path('',include(router.urls)),
    path('countryget/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    path('OrgnizationViewpost',AddOrgnization.as_view()),
    path('count/',CountsView.as_view())


]
