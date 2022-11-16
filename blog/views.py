# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag


# Create your views here.
def home_view(request):
    return render(request, 'index.html')


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    # list all posts tagged ith a specific tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'posts': posts, 'tag': tag})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # form for user to comment
    form = CommentForm()
    return render(request, 'detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f" {cd['نام']}  به شما پیشنهاد میکند که پست  {post.title} را بخوانید "
            message = f" پست{post.title} در ادرس {post_url} مطالعه کنید {cd['نام']} کامنت :{cd['نظر']}"
            send_mail(subject, message, 'work.moshavereh@gmail.com', [cd['گیرنده']])
            sent = True
            # send email
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the comment to database
        comment.save()
    return render(request, 'comment.html', {'post': post, 'form': form, 'comment': comment})
