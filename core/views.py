from django.shortcuts import render
from portfolio.models import Project ,Technology
from blog.models import Post

# Create your views here.
def home(request):
    recent_projects=Project.objects.prefetch_related('technologies').order_by('-created_at').all()[:2]
    latest_post=Post.objects.filter(status=Post.Status.PUBLISHED).prefetch_related('images','tags').select_related('author')[:3]
    featured_path=Technology.objects.select_related('category').all()[:6]
    context={
        'recent_projects':recent_projects,
        'latest_post':latest_post,
        'featured_path':featured_path,
    }
    return render(request,'core/home.html',context)

def about(request):
    return render(request,'core/about.html',
                  context={"title":"About page","content":"This is about me"})

