from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Organization, Country,Continent,Village,Register
from ..serializers.organization_serializer import OrgnisationSerializer,OrgnisationSerializer1,OrgnisationSerializer2,OrganizationSerializer3
from ..utils import save_image_to_folder,save_logo_to_folder
from ..pagination.org_pagination import OrganizationPagination
from ..pagination.orgbycountry_pagination import orgByCountryPagination
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
import uuid
from ..location_tree import get_location_hierarchy
from rest_framework.exceptions import ValidationError
from django.db.models import Q



class OrgnizationView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrgnisationSerializer
    pagination_class = OrganizationPagination



##############   single image for AddOrgnization #########################

# class AddOrgnization(generics.GenericAPIView):
#     serializer_class = OrgnisationSerializer1
#     permission_classes = []
    
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', ]:
#             return [IsAuthenticated()]
#         return super().get_permissions()

#     def post(self, request, *args, **kwargs):
#         org_images = request.data.get('org_images')
#         org_logo = request.data.get('org_logo')
#         print(org_images, "vfvfv")
#         print(org_logo, "vqqqqfvfv")

#         # Temporarily set these fields to "null" for initial validation and saving
#         request.data['org_images'] = "[ ]"
#         request.data['org_logo'] = "None"

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         if org_images and org_images != "null":
#             saved_location = save_image_to_folder(org_images, serializer.instance._id, serializer.instance.organization_name)
#             if saved_location:
#                 serializer.instance.org_images = saved_location
#                 print(serializer.instance.org_images, "referg")

#         if org_logo and org_logo != "null":
#             saved_logo_location = save_logo_to_folder(org_logo, serializer.instance._id, serializer.instance.organization_name)
#             if saved_logo_location:
#                 serializer.instance.org_logo = saved_logo_location
#                 print(serializer.instance.org_logo, "referg")

#         serializer.instance.save()

#         return Response({
#             "message": "success",
#             "result": serializer.data
#         }, status=status.HTTP_201_CREATED)


####################  AddOrgnization as per single register and login ########################
class AddOrgnization(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Fetch the Register instance for the logged-in user using some identifier
            username = request.user.username  # Example: Using username
            print(f"Username: {username}")
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member
            print(f"is_member: {is_member}")

            # Check if the user is a member
            if is_member == "FALSE":
                print("User is not a member")
                return Response({
                    "message": "Cannot create organization. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Proceed with organization creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Handle organization images and logo if provided
            org_images = request.data.get('org_images')
            org_logo = request.data.get('org_logo')

            if org_images and org_images != "null":
                saved_location = save_image_to_folder(org_images, serializer.instance._id, serializer.instance.organization_name)
                if saved_location:
                    serializer.instance.org_images = saved_location

            if org_logo and org_logo != "null":
                saved_logo_location = save_logo_to_folder(org_logo, serializer.instance._id, serializer.instance.organization_name)
                if saved_logo_location:
                    serializer.instance.org_logo = saved_logo_location

            serializer.instance.save()

            return Response({
                "message": "Organization created successfully.",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Register.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###############changes need to be done for uploading more than one image################
# class AddOrgnization(generics.CreateAPIView):
#     serializer_class = OrgnisationSerializer1

#     permission_classes = []
    
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', ]:
#             return [IsAuthenticated()]
#         return super().get_permissions()

#     def create(self, request, *args, **kwargs):
#         images = request.data.get('org_images', [])
#         images = request.data.get('org_logo', [])
        
#         # Temporarily remove images from request data to avoid validation errors
#         request.data['org_images'] = []
#         request.data['org_logo'] = []

#         # Serialize data and save temple
#         serializer = self.get_serializer(data=request.data)
#         print(serializer,"sssssssssssssssssssss")
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         saved_image_paths = []
#         print(saved_image_paths,"iiiiiiiiiiiiiiii")
#         for image_data in images:
#             if image_data:
#                 saved_location = save_image_to_folder(image_data, serializer.instance._id, serializer.instance.name)
#                 print(saved_location)
#                 if saved_location:
#                     saved_image_paths.append(saved_location)

#         if saved_image_paths:
#             serializer.instance.image_location = saved_image_paths
#             serializer.instance.save()

#         return Response({
#             "message": "success",
#             "result": serializer.data
#         })


from rest_framework.pagination import PageNumberPagination

class GetIndianOrganizations(APIView):
    def get(self, request):
        indian_location = Village.objects.all()
        organization_query_set = Organization.objects.all()
        indian_organization = organization_query_set.filter(object_id__in=indian_location)
       


        paginator = PageNumberPagination()
        paginator.page_size = 50 
        indian_organizations_page = paginator.paginate_queryset(indian_organization, request)


        indianorganization = OrganizationSerializer3(indian_organizations_page = paginator.paginate_queryset(indian_organization, request)
, many=True)
        
        return paginator.get_paginated_response( indianorganization.data)
    

from rest_framework.pagination import PageNumberPagination

class GetGlobalOrganizations(APIView):
    def get(self, request):
        organization_query_set = Organization.objects.all()
        global_organization = organization_query_set.exclude(geo_site__in=['S', 'D', 'B', 'V'])

        paginator = PageNumberPagination()
        paginator.page_size = 50 
        global_organization_page = paginator.paginate_queryset(global_organization, request)

        globaltemples = OrganizationSerializer3(global_organization_page, many=True)

        return paginator.get_paginated_response( globaltemples.data)















class GetItemByfield_InputView(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer
    pagination_class = orgByCountryPagination

    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Organization._meta.get_fields()]
            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Organization.objects.filter(**filter_kwargs)
                serialized_data = OrgnisationSerializer(queryset, many=True)
                return Response(serialized_data.data)
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })
        except Organization.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })
        






class GetItemByfields_InputViews(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer
    pagination_class = orgByCountryPagination

    def get(self, request, input_value1, field_name1, input_value2=None, field_name2=None):
        try:
            field_names = [field.name for field in Organization._meta.get_fields()]
            filter_kwargs = {}


            if field_name1 in field_names:
                filter_kwargs[field_name1] = input_value1

                
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })
            if field_name2 and input_value2:
                if field_name2 in field_names:
                    filter_kwargs[field_name2] = input_value2

                else:
                    return Response({
                        'message': f'Invalid field name: {field_name2}',
                        'status': 400
                    })
                
            queryset = Organization.objects.filter(**filter_kwargs)
            serialized_data = OrgnisationSerializer(queryset, many=True)
            return Response(serialized_data.data)
            
        except Organization.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })
        











class GetOrgByStatus_Pending(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1

    def get(self, request):
        orgs = Organization.objects.filter(status='PENDING')  # Filter by 'PENDING' status
        
        if not orgs.exists():
            return Response({
                'message': 'No organizations found with PENDING status',
                'result': []
            })

        serializer = self.get_serializer(orgs, many=True)
        return Response({
            'message': 'success',
            'result': serializer.data
        })
        
class GetOrgByStatus_Success(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1

    def get(self, request):
        orgs = Organization.objects.filter(status='SUCCESS')  # Filter by 'PENDING' status
        
        if not orgs.exists():
            return Response({
                'message': 'No organizations found with SUCCESS status',
                'result': []
            })

        serializer = self.get_serializer(orgs, many=True)
        return Response({
            'message': 'success',
            'result': serializer.data
        }) 




class UpdateOrgStatus(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer2

    def put(self, request, org_id):
        try:
            org = Organization.objects.get(pk=org_id, status='PENDING')
        except Organization.DoesNotExist:
            return Response({
                'message': 'Organization with PENDING status not found for the provided ID'
            }, status=http_status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        org.status = 'SUCCESS'
        org.save()

        # Serialize the updated organization
        serializer = self.get_serializer(org)

        return Response({
            'message': 'success',
            'result': serializer.data
        })












class GetbyCountryLocationorganization(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        country_id = self.kwargs.get('country_id')
        organization_in_country = Organization.objects.filter(
            object_id__block__district__state__country_id=country_id
        )
        return organization_in_country


  








class GetItemBystatefield_location(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        organizations_in_state = Organization.objects.filter(object_id__block__district__state_id=state_id)
        return organizations_in_state
    


class GetbyDistrictLocationOrganization(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        organizations_in_district = Organization.objects.filter(object_id__block__district_id=district_id)
        return organizations_in_district
    


    
class GetbyBlockLocationOrganization(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        block_id = self.kwargs.get('block_id')
        organizations_in_district = Organization.objects.filter(object_id__block_id=block_id)
        return organizations_in_district


from rest_framework import viewsets, pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000 

# class GetOrgbyroot_map(generics.GenericAPIView):
#     serializer_class = OrgnisationSerializer
#     pagination_class = CustomPagination

#     def get(self, request, input_value, field_name):
#         try:
#             field_names = [field.name for field in Organization._meta.get_fields()]

#             if field_name in field_names:
#                 if field_name == 'root_map':
#                     # Validate UUID
#                     try:
#                         input_uuid = uuid.UUID(input_value)
#                     except ValueError:
#                         return Response({
#                             'message': 'Invalid UUID format.',
#                             'status': 400
#                         })

#                     # Fetch all related UUIDs based on the hierarchy
#                     hierarchy_map = get_location_hierarchy()
#                     if input_value not in hierarchy_map:
#                         return Response({
#                             'message': 'root_map UUID not found in hierarchy.',
#                             'status': 400
#                         })
                    
#                     related_uuids = hierarchy_map[input_value]

#                     # Get the temples with the specified object_id (UUIDs)
#                     queryset = Organization.objects.filter(object_id__in=related_uuids)
                    
#                 else:
#                     filter_kwargs = {field_name: input_value}
#                     queryset = Organization.objects.filter(**filter_kwargs)
                
#                 # Paginate the queryset
#                 page = self.paginate_queryset(queryset)
#                 if page is not None:
#                     serialized_data = self.get_paginated_response(OrgnisationSerializer(page, many=True).data)
#                 else:
#                     serialized_data = OrgnisationSerializer(queryset, many=True)

#                 return Response(serialized_data.data)
#             else:
#                 return Response({
#                     'message': 'Invalid field name',
#                     'status': 400
#                 })

#         except Organization.DoesNotExist:
#             return Response({
#                 'message': 'Object not found',
#                 'status': 404
#             })
#         except Exception as e:
#             return Response({
#                 'message': str(e),
#                 'status': 500
#             })


class GetOrgbyroot_map(generics.ListAPIView):
    serializer_class = OrgnisationSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.kwargs.get('input_value')

        if not input_value:
            raise ValidationError("Input value is required")

        # Define queries for each level using the correct field lookups
        continent_query = Q(object_id__block__district__state__country__continent__pk=input_value)
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Combine queries with OR operator
        combined_query = (
            continent_query | country_query | state_query |
            district_query | block_query | village_query
        )

        queryset = Organization.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country__continent',
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id'
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)