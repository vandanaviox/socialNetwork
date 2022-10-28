from rest_framework.views import APIView
from rest_framework.response import Response
from post.serializer import PostSerializer, LikesSerializer
from rest_framework import status
from post.models import Likes, Posts
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.utils import exception_handling


class PostListing(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]

    @exception_handling
    def get(self, request):
        posts = Posts.objects.filter(user=request.user)
        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)
        
        serializer = PostSerializer(posts, many=True)
        return Response({
            'Data':serializer.data,
            'Message':"Posts fetched sucessfuly",
            'Status': True
        }, status=status.HTTP_200_OK)

    @exception_handling
    def post(self, request):

        data = request.data
        data['user'] = request.user.id
        serializer = PostSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    'Data': serializer.errors,
                    'Message':'Something went wrong',
                    'Status': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({
            'Data': serializer.data,
            'Message': 'Your post is created',
            'Status': True
        }, status=status.HTTP_201_CREATED)


class PostDetail(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]

    @exception_handling
    def get(self, request, pk):

        posts = Posts.objects.get(id=pk)
        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)

        serializer = PostSerializer(posts)
        return Response({
            'Data': serializer.data,
            'Message': "Posts fetched sucessfuly",
            'Status': True
        }, status=status.HTTP_200_OK)

    @exception_handling
    def patch(self, request, pk):

        post = Posts.objects.get(id = pk)
        serializer = PostSerializer(post, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {
                    'Data': serializer.errors,
                    'Message':'Something went wrong',
                    'Status': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({
            'Data': serializer.data,
            'Message': 'Your post is updated sucessfuly',
            'Status': True
        }, status=status.HTTP_201_CREATED)

    @exception_handling
    def delete(self, request, pk):

        post = Posts.objects.get(id = pk)
        post.delete()
        return Response(
                {
                    'Data': {},
                    'Message': 'Post Deleted Successfully',
                    'Status': True
                },
                status=status.HTTP_200_OK
            )


class AllPostListing(APIView):

    @exception_handling
    def get(self, request):
        posts = Posts.objects.all()
        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)
        serializer = PostSerializer(posts, many=True)
        return Response({
            'Data': serializer.data,
            'Message': "Posts fetched sucessfullly",
            'Status': True
        }, status=status.HTTP_200_OK)


class OthersPostListing(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]

    @exception_handling
    def get(self, request):
        posts = Posts.objects.exclude(user=request.user)
        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)
        
        serializer = PostSerializer(posts, many=True)
        return Response({
            'Data': serializer.data,
            'Message': "Posts fetched sucessfuly",
            'Status': True
        }, status=status.HTTP_200_OK)


class LikeView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]

    @exception_handling
    def post(self, request, pk):
        data={'post': pk,'user': request.user.id}

        try:
            posts = Likes.objects.get(user = request.user, post = pk)
            if posts:
                posts.delete()
                return Response({
                    'Data': {},
                    'Message': 'Your Like is removed',
                    'Status': True
                }, status=status.HTTP_200_OK)
        except:
            pass 
        serializer = LikesSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    'Data': serializer.errors,
                    'Message':'Something went wrong',
                    'Status': False
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({
            'Data': serializer.data,
            'Message': 'Your Like is added',
            'Status': True
        }, status=status.HTTP_201_CREATED)


class LikeCount(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]

    @exception_handling
    def get(self, request, pk):
        posts = Posts.objects.get(id=pk)
        search = request.GET.get('search')
        if search:
            posts = posts.filter(title__icontains=search)
        serializer = PostSerializer(posts)
        post_obj = Posts()
        likes = post_obj.get_likes(pk)
        output_dict = {
            "id": pk,
            "title": posts.title,
            "content": posts.content,
            "Liked By": likes
        }
        return Response({
            'Message': f"{posts}  Detail",
            'Data': output_dict,
            'Status': True
        }, status=status.HTTP_200_OK)
