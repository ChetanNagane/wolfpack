from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from PIL import Image
from django.conf import settings


# Create your views here.
class user(APIView):

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User added'})
        else:
            return Response(serializer.error_messages,status=400,)

    def put(self,request):
        user = User.objects.filter(email= request.data["email"]).first()
        serializer =UserSerializers(user ,data = request.data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password updated'})
        else:
            return Response(serializer.error_messages,status=400,)


class api(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response(self.imageResize(request.data['image']))
    
    def imageResize(self,imageurl):
        size = {
            "small" : (200, 300),
            "medium" : (500, 500),
            "large" : (1024, 768)
        }
        response = {}
        media_url = settings.MEDIA_URL
        
        for key in size:
            image = Image.open(imageurl)
            image.thumbnail(size[key])
            image.save(media_url[1:]+key + str(imageurl))
            response[key] = media_url[1:]+key + str(imageurl)
            

        image.convert('L').save(media_url[1:]+"grayscale" + str(imageurl))
        response["grayscale"] = media_url[1:]+"grayscale" + str(imageurl)

        return response
