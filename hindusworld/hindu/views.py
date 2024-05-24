from django.shortcuts import render
from rest_framework import viewsets
from .models import organization,Country
from .serializers import OrgnisationSerializer,countrySerializer
from .utils import save_image_to_folder
from rest_framework.response import Response
from rest_framework import generics



class OrgnizationView(viewsets.ModelViewSet):
    queryset = organization.objects.all()
    serializer_class=OrgnisationSerializer

    def create(self, request, *args, **kwargs):
        # Extract image_location from request data
        org_images = request.data.get('org_images')
        # Add the image_location back to the request data
        request.data['org_images'] = "null"
        # Serialize data and save
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if org_images and org_images != "null":
            saved_location = save_image_to_folder(org_images,serializer.instance._id,serializer.instance.organization_name)
            print(saved_location,"=================================")
            if saved_location:
                serializer.instance.image_location = saved_location
                serializer.instance.save()
                return Response({
                "message": "success",
                "result": serializer.data
            })

class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class=countrySerializer

class GetItemByfield_InputView(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer
    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Country._meta.get_fields()]
            print("@@@@@@@@@@@@",field_names)
            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                print("#######",filter_kwargs)
                queryset = organization.objects.filter(**filter_kwargs)
                print("33333333333",queryset)
                serialized_data = OrgnisationSerializer(queryset, many=True)
                return Response(serialized_data.data)
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })
        except organization.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })    



