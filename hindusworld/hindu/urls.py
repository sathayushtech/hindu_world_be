from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrgnizationView,CountryView,GetItemByfield_InputView,continentsView,AddOrgnization,CountsView,countries_by_Continent,GetOrgByStatus_Pending,GetOrgByStatus_Success,UpdateOrgStatus,Registerview,LoginApiView,VerifyOtpView,ResendOtp,ResetPassword,ForgotOtp

router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)
router.register(r'continents',continentsView)
router.register(r'Registerview',Registerview)


urlpatterns=[

    path('',include(router.urls)),
    path('Organization_get/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    path('OrgnizationViewpost',AddOrgnization.as_view()),
    path('updateStatusOrgnization/<str:org_id>',UpdateOrgStatus.as_view()),
    
    path('get_org_by_pending',GetOrgByStatus_Pending.as_view()),
    path('get_org_by_success',GetOrgByStatus_Success.as_view()),
  
    # path('count/<str:country_id>',CountsView.as_view()),
    path('count/',CountsView.as_view()),
    # path('continents/<str:pk>',continentsView.as_view())
    path('get-countriesBycontinent/<str:continent>', countries_by_Continent.as_view(), name='get-items-by-field'),
    # path('Register/',Registerview.as_view()),
    path('Login/',LoginApiView.as_view()),
    path('VerifyOtp/',VerifyOtpView.as_view()),
    path('ResendOtp',ResendOtp.as_view()),
    path('ForgotOtp',ForgotOtp.as_view()),
    path('ResetPassword',ResetPassword.as_view())








]


