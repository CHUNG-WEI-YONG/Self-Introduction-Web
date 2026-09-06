from django.shortcuts import render,get_object_or_404,redirect
from .models import Post , Tags,PostImage
from .forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def is_admin_user(user):
    return user.is_authenticated and user.is_superuser

#for the list of post
def post_list_view(request):
    post=Post.objects.filter(status=Post.Status.PUBLISHED ).select_related('author').prefetch_related('tags','images')
    context={
        'posts':post
    }
    return render(request,'blog/post_list.html',context)


def post_detail_view(request,slug):
    post=get_object_or_404(
        Post.objects.select_related('author').prefetch_related('tags'),
        slug=slug,
        status=Post.Status.PUBLISHED
    )

    context={
        'post':post
    }
    return render(request,'blog/post_detail.html',context)


@user_passes_test(is_admin_user, login_url='/admin/login/')
def post_create_view(request):
    if request.method == 'POST':
        # 1. 必须同时绑定 POST 与 FILES
        form = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()          # 触发 models.py 中的自动生成 slug 逻辑
            form.save_m2m()      # 保存 tags 关联

            for image in images:
                PostImage.objects.create(post=post, image=image)
                
            return redirect('blog:post_detail', slug=post.slug)
        else:
            # 调试：控制台打印表单未能通过的原因
            print("Post Form Validation Failed:", form.errors)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form,
        'action_title': 'Create New Article'
    })

@user_passes_test(is_admin_user, login_url='/admin/login/')
def post_edit_view(request,slug):
    post=get_object_or_404(Post,slug=slug)
    if request.user!=post.author:
        return HttpResponseForbidden("You are not allowed to change this post")
    if request.method=='POST':
        form = PostForm(request.POST, instance=post)
        images=request.FILES.getlist("images")
        if form.is_valid():
            form.save()

            for img in images:
                PostImage.objects.create(post=post,image=img)
            return redirect('blog:post_detail', slug=post.slug)
    return render(request, 'blog/post_form.html', {'form': form, 'action_title': 'Edit Article', 'post': post})

@user_passes_test(is_admin_user, login_url='/admin/login/')
def delete_post_view(request,slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user!=post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})
    

    
    