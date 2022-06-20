from doctest import DocFileSuite
from turtle import pos
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

from .postSerializer import PostSerializer
from .permissions import IsOwnerOrReadOnly

from .models import Post

class PostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all() 
    
    def get_queryset(self):
        return Post.objects.all()

    def get_objects(self, id):
        return Post.objects.filter(pk=id).first()
        # if non post:
            # raise DocFileSuite
    def list(self, request):
        serializer = PostSerializer(self.get_queryset(), many = True)
        return Response(serializer.data)
        
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           post = serializer.save(owner=request.user)
           return Response({'message':f'Post has created successfully! {request.user}'})

    def update(self, request, pk=None):

        serializer = PostSerializer(self.get_objects(pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':f'Post has updated successfully! {request.user}'})