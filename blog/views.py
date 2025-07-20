from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from django.shortcuts import render,get_object_or_404
from blog.models import Post
import datetime
from blog.serilizes import PostSerializer,UserSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import generics
from blog.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework import viewsets

# Create your views here.
def blog_view(request,cat_name=None):
    posts=Post.objects.filter(published_date__lte=datetime.datetime.now(),status=1)
    if cat_name:
            posts=posts.filter(category__name=cat_name)

    context={'posts':posts}
    return render(request,"blog/blog-home.html",context=context)
def blog_single(request,pid):
    post=get_object_or_404(Post,pk=pid)
    post.counted_views+=1
    post.save()
    published_post=Post.objects.filter(published_date__lte=datetime.datetime.now(),status=1)
    next_post = published_post.filter(id__gt=post.id).order_by('id').first() 
    prev_post = published_post.filter(id__lt=post.id).order_by('-id').first()

    if prev_post is None:
        prev_post = None
    if next_post is None:
        next_post = None
    context={'post':post,'prev_post':prev_post,'next_post':next_post}
    return render(request,"blog/blog-single.html",context=context)

def blog_writer(request,author_username):
    posts=Post.objects.filter(published_date__lte=datetime.datetime.now(),status=1)
    author_posts=posts.filter(author__username=author_username)
    context={'posts':author_posts}
    return render(request,"blog/blog-home.html",context=context)

@csrf_exempt
def Post_list(request):
     if request.method=="GET":
        post=Post.objects.all()
        serializer=PostSerializer(post,many=True)
        return JsonResponse(serializer.data,safe=False)
     elif request.method=="POST":
        data=JSONParser.parse(request)
        serializer=PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.data,status=400)

@api_view(['GET','POST'])   
def Post_list_main(request,format=None):

    if request.method=="GET":
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class Post_main(APIView):
    def get(self,request,format=None):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        post=Post(request.data)
        serializer=PostSerializer(post)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Post_detail(APIView):
    def get_object(self,title):
        try:
            return Post.objects.get(title=title)
        except Post.DoesNotExist:
            raise Http404

    def get(self,request,title,format=None):
        post=self.get_object(title)
        serializer=PostSerializer(post)
        return Response(serializer.data)
    
    def put(self,request,title,format=None):
        post=self.get_object(title)
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Post_great(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class post_detail_great(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    lookup_field = 'pk' 


class UserList(generics.ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='pk'


    
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('blog:user-list', request=request, format=format),
        'posts': reverse('blog:post-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)