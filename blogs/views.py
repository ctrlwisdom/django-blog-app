from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .models import Post, Comment, Category
from .forms import CommentForm



def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blogs/tag.html', context)

def category_list(request):
    context = {}
    category_list = Category.objects.all()
    context['category_list'] = category_list
    return render(request, 'blogs/category.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blogs/category-detail.html', context)


def home(request):
    context = {}
    post_list = Post.objects.all().filter(published=True)
    # set pagination
    p = Paginator(post_list, 1)
    page = request.GET.get('page')
    posts = p.get_page(page)
    context['posts'] = posts

    return render(request, 'blogs/index.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.all().filter(post=post)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'blogs/post-detail.html', {'post': post, 'comments': comments, 'form': form})


def search(request):
    search = request.GET.get('q')
    if search:     
        posts_list = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        # set pagination
        p = Paginator(posts_list, 1)
        page = request.GET.get('page')
        # posts = p.get_page(page)
        try:
            posts = p.page(page)
        except PageNotAnInteger:
            posts = p.page(1)
        except EmptyPage:
            posts = p.page(p.num_pages)
    return render(request, 'blogs/search-result.html', {'search':search, 'posts':posts})

