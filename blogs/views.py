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

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts
    }
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'blogs/category-detail.html', context)


def home(request):
    context = {}
    post_list = Post.objects.all().filter(published=True)
    categories = Category.objects.all()
    context['categories'] = categories
    # set pagination
    p = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)
    context['posts'] = posts

    return render(request, 'blogs/index.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    related_posts = post.tags.similar_objects()[:10]
    comments = Comment.objects.all().filter(post=post)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return HttpResponseRedirect(request.path_info)
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'related_posts':related_posts
    }
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'blogs/post-detail.html', context)


def search(request):
    search = request.GET.get('q')
    if search:     
        posts_list = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        # set pagination
        p = Paginator(posts_list, 2)
        page = request.GET.get('page')
        # posts = p.get_page(page)
        try:
            posts = p.page(page)
        except PageNotAnInteger:
            posts = p.page(1)
        except EmptyPage:
            posts = p.page(p.num_pages)
    context = {'search':search, 'posts':posts}
    categories = Category.objects.all()
    context['categories'] = categories
    return render(request, 'blogs/search-result.html', context)

