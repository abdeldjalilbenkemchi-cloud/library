
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class RegisterView(generics.CreateAPIView):
    permission_classes=(permissions.AllowAny,)
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
   
    def post(self,request,*arg,**kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        
        return Response({
            'user': serializer.data,
            'message':'User registration was successfull'
        },status=status.HTTP_201_CREATED)
    
class UserDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        serializer=RegisterSerializer(user)

        return Response({
            'id' : user.id,
            'username':user.username,
            'email':user.email,
            'is_authenticated' : True
        })