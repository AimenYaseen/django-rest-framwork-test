from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .postSerializer import PostSerializer
from .permissions import IsOwnerOrReadOnly

from .models import Post

class PostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all() 
    
    def get_queryset(self):
        return Post.objects.all()

    # def get_objects(self, id):
    #     return Post.objects.filter(pk=id).first()
        # if non post:
            # raise DocFileSuite

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def list(self, request):
        serializer = PostSerializer(self.get_queryset(), many = True)
        return Response(serializer.data)
        
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           post = serializer.save(owner=request.user)
           return Response({'message':f'Post has created successfully! {request.user}'})

    def update(self, request, pk=None):
        post = self.get_object()
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':f'Post has updated successfully! {request.user}'})

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.get_queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)