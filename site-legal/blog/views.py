from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page, User
from django.db.models import Q
from django.http import Http404

PER_PAGE = 9

def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/pages/index.html', 
                  {
                      'page_obj': page_obj,
                      'page_title': page_title,
                   })

def post(request, slug):
    post = Post.objects.get_published().filter(slug=slug).first()

    if post is None:
        raise Http404()
    
    page_title = f'{post.title} - Post '


    return render(request, 'blog/pages/post.html', 
                  {
                  'post': post,
                  'page_title': page_title,
                  }
                )

def page(request, slug):
    pages = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if pages is None:
        raise Http404()
    
    page_title = f'{pages.title} - Page '

    return render(request, 'blog/pages/page.html', 
    {
        'pages': pages,
        'page_title': page_title,
    }
    )

def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(created_by__pk=author_pk)
    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} + ' ' + {user.last_name}'
    page_title = user_full_name + ' posts -'

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/pages/index.html', 
                  {
                      'page_obj': page_obj,
                      'page_title': page_title,
                   })

def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'{page_obj[0].category.name} - Category - '


    return render(request, 'blog/pages/index.html', 
                  {
                      'page_obj': page_obj,
                      'page_title': page_title,
                   })

def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'{page_obj[0].tags.firts().name} - Tag - '

    return render(request, 'blog/pages/index.html', 
                  {
                      'page_obj': page_obj,
                      'page_title': page_title,
                   })

def search(request):
    serach_value = request.GET.get('search').strip()

    if len(posts) == 0:
        raise Http404()
    
    page_title = f'{serach_value[0:30]} - Search- '

    posts = (
        Post.objects.get_published().filter(
        Q(title__icontains=serach_value) |
        Q(content__icontains=serach_value) |
        Q(tags__name__icontains=serach_value) |
        Q(category__name__icontains=serach_value) |
        Q(created_by__first_name__icontains=serach_value) |
        Q(created_by__last_name__icontains=serach_value)
    )[0:PER_PAGE]
    )
    return render(request, 'blog/pages/index.html', 
                  {
                      'posts': posts,
                      'search_value': serach_value,
                      'page_title': page_title,
                   })