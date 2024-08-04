from typing import Any
from django.shortcuts import render, redirect
from blog.models import Post, Page, User
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView

PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home -',
        })
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post -'
        context.update({
            'page_title': page_title,
        })
        return context


class PageDatailView(DetailView):
    template_name = 'blog/pages/page.html'
    model = Page
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - Page '

        context.update({
            'page_title': page_title,
        })

        return context
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    

class CreateByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} + {user.last_name}'
        page_title = user_full_name + ' posts -'

        context.update({
            'page_title': page_title,
        })

        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk)

        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })
        
        return super().get(request, *args, **kwargs)
    
class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Category - '
        context.update({
            'page_title': page_title,
            })
        return context
    
class TagListViews(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - Tags - '
        context.update({
            'page_title': page_title,
            })
        return context


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args, **kwargs):
        self._search_value = request.GET.get('search').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().filter(
        Q(title__icontains=self.search_value) |
        Q(content__icontains=self.search_value) |
        Q(tags__name__icontains=self.search_value) |
        Q(category__name__icontains=self.search_value) |
        Q(created_by__first_name__icontains=self.search_value) |
        Q(created_by__last_name__icontains=self.search_value)
    )[0:PER_PAGE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': f'Search results for "{self.search_value}"',
            'search_value': self._search_value
        })

        return context
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.search_value:
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
    
    
