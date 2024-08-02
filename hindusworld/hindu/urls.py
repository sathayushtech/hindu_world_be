from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from .views import OrgnizationView,CountryVIews,GetItemByfield_InputView,continentsView,AddOrgnization,GetOrgByStatus_Pending,GetOrgByStatus_Success,UpdateOrgStatus,Registerview,LoginApiView,GetItemByfields_InputViews,ResetPassword,ForgotOtp,ResendOtp,VerifyOtpView,BlockView,GetVillages,VillageView,DistrictVIew,StateViews,GetbyCountryLocationorganization,GetbyDistrictLocationOrganization,GetbyBlockLocationOrganization,GetItemBystatefield_location,GetIndianOrganizations,GetGlobalOrganizations
# from .views import OrgnizationView,countries_by_Continent,CountryView,GetItemByfield_InputView,continentsView,AddOrgnization,GetOrgByStatus_Pending,GetOrgByStatus_Success,UpdateOrgStatus,Register_LoginView,Validate_LoginOTPView,GetItemByfields_InputViews,MemberDetailsViews,UpdateMemberDetails,DistrictVIew,StateViews,GetOrgbyroot_map,states_by_country,districts_By_State,GetProfileById,GetProfile
from .views import *



router=DefaultRouter()
router.register(r'organizations',OrgnizationView)
router.register(r'countries',CountryView)
router.register(r'continents',continentsView)
router.register(r'state',StateViews)  
router.register(r"district",DistrictVIew)
router.register(r'category',CategoryView)
router.register(r'subcategory',SubCategoryView)
router.register(r'events', EventsViewSet, basename='events')
router.register(r'training', TrainingView, basename='training')


# router.register(r"block",BlockView)
# router.register(r"village",VillageView)
# router.register(r"allvillages",GetVillages, basename="allvillages_extra")


urlpatterns=[

    path('',include(router.urls)),
    # path('organization_get/<str:field_name>/<str:input_value>', GetItemByfield_InputView.as_view()),
    path('organizations_get/<str:field_name1>/<str:input_value1>/<str:field_name2>/<str:input_value2>', GetItemByfields_InputViews.as_view()),
    path('addOrgnization',AddOrgnization.as_view()),
    path('updateStatusOrgnization/<str:org_id>',UpdateOrgStatus.as_view()),
    
    path('get_org_by_pending',GetOrgByStatus_Pending.as_view()),
    path('get_org_by_success',GetOrgByStatus_Success.as_view()),
    # path('indian_org',GetIndianOrganizations.as_view()),
    # path('international_org',GetGlobalOrganizations.as_view()),
    # path('root_map_org/<str:input_value>/',GetOrgbyroot_map.as_view()),
    # path('root_map_org/<str:field_name>/<str:input_value>', GetOrgbyroot_map.as_view()),
  
    # path('count/<str:country_id>',CountsView.as_view()),
    # path('count/',CountsView.as_view()),
    # path('continents/<str:pk>',continentsView.as_view())
    path('get-countriesBycontinent/<str:continent>', countries_by_Continent.as_view(), name='get-items-by-field'),
    # path('register',Registerview.as_view()),
    # path('Login/',LoginApiView.as_view()),
    # path('VerifyOtp/',VerifyOtpView.as_view()),
    # path('resendOtp',ResendOTPView.as_view()),
    path('register_login',Register_LoginView.as_view(), name="register"),
    path('verify_login',Validate_LoginOTPView.as_view()),
    # path('MemberDetails',MemberDetailsViews.as_view()),
    path('updateMemberDetails/<str:id>',UpdateMemberDetails.as_view()),
    # path('ForgotOtp',ForgotOtp.as_view()),
    # path('ResetPassword',ResetPassword.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('states_by_country/<str:country>',states_by_country.as_view()),
    path('districts_by_state/<str:state>/', districts_By_State.as_view(), name='districts_by_state'),
    path('profile_get_by_id/<str:id>/',GetProfileById.as_view()),
    path('profile_get/',GetProfile.as_view()),
    # path('category', CategoryView.as_view({'get': 'list'})),
    # path('subcategory', SubCategoryView.as_view({'get': 'list'})),
    path('addevents', AddEventView.as_view(), name='add-event'),
    path('eventsupdatestatus/<uuid:event_id>/', UpdateEventStatus.as_view(), name='update-event-status'),
    path('trainingupdatestatus/<str:_id>/update-status/', UpdateTrainingStatus.as_view(), name='update-training-status'),



    
    # path('organization/state_id/<str:state_id>/', GetItemBystatefield_location.as_view()),
    # path('organization/district_id/<str:district_id>/', GetbyBlockLocationOrganization.as_view()),
    # path('organization/block_id/<str:block_id>/', GetbyDistrictLocationOrganization.as_view()),
    # path('organization/country_id/<str:country_id>/',GetbyCountryLocationorganization.as_view()),  









]


