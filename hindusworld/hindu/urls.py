from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrgnizationView,CountryView,GetItemByfield_InputView,continentsView,AddOrgnization,CountsView,countries_by_Continent

router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)
router.register(r'continents',continentsView)


urlpatterns=[

    path('',include(router.urls)),
    path('countryget/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    path('OrgnizationViewpost',AddOrgnization.as_view()),
    # path('count/<str:country_id>',CountsView.as_view()),
    path('count/',CountsView.as_view()),
    # path('continents/<str:pk>',continentsView.as_view())
    path('get-countriesBycontinent/<str:continent>', countries_by_Continent.as_view(), name='get-items-by-field'),




]


