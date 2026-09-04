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
        # 1. 绑定 POST 请求数据到表单
        form = PostForm(request.POST)
        images=request.FILES.getlist("images")
        if form.is_valid():
            # 2. 挂起保存以填充当前登录用户
            post = form.save(commit=False)
            post.author = request.user  # 修正：使用 request.user
            post.save()
            form.save_m2m()  # 保存关联的 tags

            for image in images:
                PostImage.objects.create(post=post,image=image)
            return redirect('blog:post_detail', slug=post.slug)
    else:
        # 3. GET 请求：直接实例化一个空白表单
        form = PostForm()

    # 4. 无论 GET 还是校验失败的 POST，均渲染页面并回显错误信息
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
    

    
    