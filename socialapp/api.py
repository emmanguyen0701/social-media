from rest_framework import generics, mixins
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *

class ImageDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        profile = Profile.objects.get(pk=request.POST['profile_id']) 
        if serializer.is_valid():
            serializer.save(profile=profile)
            redirect_url = '/profile_detail/' + str(profile.id) + '/image_gallery'
            return HttpResponseRedirect(redirect_url)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        images = super().get_queryset().filter(profile=profile)  
        return images 

