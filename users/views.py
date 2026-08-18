from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# ✅ YOUR MISSING LOGIN VIEW — NOW ADDED!
class LoginView(APIView):
    print("hey")
    permission_classes = []  # Allow anyone to login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print("Request data:", request.data)


        # ✅ THIS IS THE MAGIC LINE — Django handles password hashing!
        user = authenticate(username=username, password=password)

        if user:
            # ✅ Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'phone': getattr(user, 'phone', ''),
                }
            })
        else:
            # ❌ This only triggers if authenticate() actually fails!
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user