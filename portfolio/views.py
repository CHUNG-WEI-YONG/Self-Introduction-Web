from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import TechCategory, Project,Technology
from .forms import ProjectForm, TechnologyForm


def is_admin_user(user):
    return user.is_authenticated and user.is_superuser


def tech_stack_view(request):
    categories = TechCategory.objects.prefetch_related('technologies').all()
    return render(request, 'portfolio/tech_stack.html', {'categories': categories})


def project_list_view(request):
    projects = Project.objects.prefetch_related('technologies').all()
    return render(request, 'portfolio/project_list.html', {'projects': projects})


@user_passes_test(is_admin_user, login_url='/admin/login/')
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio:project_list')
    else:
        form = ProjectForm()

    # 无论是 GET 还是 POST 校验失败，统一在这里渲染并回显错误提示
    return render(request, 'portfolio/project_form.html', {
        'form': form,
        'action_title': 'Add New Project'
    })


@user_passes_test(is_admin_user, login_url='/admin/login/')
def tech_create_view(request):
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio:tech_stack')
    else:
        form = TechnologyForm()

    # 保证 GET 和校验失败时都能正确返回响应
    return render(request, 'portfolio/tech_form.html', {
        'form': form,
        'action_title': 'Add New Technology'
    })

@user_passes_test(is_admin_user,login_url='/admin/login/')
def project_update_view(request,pk):
    project=get_object_or_404(Project,pk=pk)
    if request.method=='POST':
        form=ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('portfolio:project_list')
    else:
        form=ProjectForm(instance=project)

    return render(request,'portfolio/project_form.html',{'form': form, 'action_title': f'Edit Project: {project.title}'})

@user_passes_test(is_admin_user, login_url='/admin/login/')
def project_delete_view(request, pk):
  project = get_object_or_404(Project, pk=pk)
  if request.method == 'POST':
    project.delete()
    return redirect('portfolio:project_list')

  return render(
      request,
      'portfolio/confirm_delete.html',
      {'object': project, 'cancel_url': 'portfolio:project_list'},
  )


# --- Technology: Update & Delete ---
@user_passes_test(is_admin_user, login_url='/admin/login/')
def tech_update_view(request, pk):
  tech = get_object_or_404(Technology, pk=pk)
  if request.method == 'POST':
    form = TechnologyForm(request.POST, instance=tech)
    if form.is_valid():
      form.save()
      return redirect('portfolio:tech_stack')
  else:
    form = TechnologyForm(instance=tech)

  return render(
      request,
      'portfolio/tech_form.html',
      {'form': form, 'action_title': f'Edit Technology: {tech.name}'},
  )


@user_passes_test(is_admin_user, login_url='/admin/login/')
def tech_delete_view(request, pk):
  tech = get_object_or_404(Technology, pk=pk)
  if request.method == 'POST':
    tech.delete()
    return redirect('portfolio:tech_stack')

  return render(
      request,
      'portfolio/confirm_delete.html',
      {'object': tech, 'cancel_url': 'portfolio:tech_stack'},
  )

    


    