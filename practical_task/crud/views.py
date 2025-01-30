from .models import User, Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication


class UserSignupAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User signup successfully!",
                    "status": status.HTTP_201_CREATED
                }
            )
        return Response(
            {
                "message": "Something wrong when user trying to signup!",
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
        )


class UserSigninAPIView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Login successful!",
                    "status": status.HTTP_200_OK,
                    "token": token.key
                }
            )
        return Response(
            {
                "message": "Invalid credentials.",
                "status": status.HTTP_400_BAD_REQUEST
            }
        )


class UserDetailsUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(
                {
                    "message": "User details fetching successfully!",
                    "details": serializer.data
                }
            )

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User details update successfully!",
                    "status": status.HTTP_200_OK
                }
            )
        return Response(
            {
                "message": "Something went wrong while user trying to update their details!",
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
        )


class AdminAPIView(APIView):

    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            {
                "message": "User details fetched successfully!",
                "users": serializer.data
            }
        )

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User details update successfully!",
                    "status": status.HTTP_200_OK
                }
            )
        return Response(
            {
                "message": "Something went wrong while user trying to update their details!",
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
        )

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(
                {
                    "message": "User deleted successfully!",
                    "status": status.HTTP_204_NO_CONTENT
                }
            )
        except User.DoesNotExist:
            return Response(
                {
                    "message": "User doesn't exist with this id!",
                    "status": status.HTTP_404_NOT_FOUND
                }
            )


class PostsAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Post created successfully!",
                    "status": status.HTTP_201_CREATED,
                }
            )
        return Response(
            {
                "message": "Something wrong when user trying to create a post!",
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
        )

    def get(self, request):
        posts = Post.objects.filter(created_by=request.user)
        if posts:
            serializer = PostSerializer(posts, many=True)
            return Response(
                {
                    "message": "Your all posts are fetched successfully!",
                    "posts": serializer.data
                }
            )
        return Response(
                {
                    "message": "You do not have any post!",
                }
            )
