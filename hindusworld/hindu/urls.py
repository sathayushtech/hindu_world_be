from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrgnizationView,CountryView,GetItemByfield_InputView

router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)


urlpatterns=[

    path('',include(router.urls)),
    path('countryget/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
]
