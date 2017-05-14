from django.shortcuts import render
from .models import Course_Create
from .models import Videocreate
from .forms import CourseForm
from .forms import VideoForm,CommentForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import  HttpResponse,HttpResponseRedirect

# Create your views here.

def video_list(request, pk):

    #pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    course = Course_Create.objects.get(id__exact=pk)
    videos = Videocreate.objects.filter(course__exact=pk).order_by('id')
    return render(request, 'videopublishing/video_list.html', {'videos': videos, 'course': course})


def course_list(request):

    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    courses = Course_Create.objects.all().order_by('id')
    return render(request, 'videopublishing/course_list.html', {'courses': courses})


def course_new(request):
    # permission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')
    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/')
    if request.method == "POST":
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.author = request.user
                course.save()
                return redirect('videopublishing:video_list', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'videopublishing/course_edit.html', {'form': form})


def course_edit(request, pk):
    # permission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')
    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/'+str(pk) + '/')
    course_d = get_object_or_404(Course_Create, pk=pk)
    # validate author
    if permission_validate_del_edit(request, course_d.author) != 1:
        return HttpResponseRedirect('/courses/' + str(pk) + '/')

    course = get_object_or_404(Course_Create, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('videopublishing:video_list', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'videopublishing/course_edit.html', {'form': form})


def video_new(request, pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')
    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/' + str(pk) + '/')
    course_d = get_object_or_404(Course_Create, pk=pk)
    # validate author
    if permission_validate_del_edit(request, course_d.author) != 1:
        return HttpResponseRedirect('/courses/' + str(pk) + '/')
    if request.method == "POST":
            form = VideoForm(request.POST)
            if form.is_valid():
                video = form.save(commit=False)
                video.course_id = pk
                video.pub_date = timezone.now()
                video.save()
                return redirect('videopublishing:video_list', pk)
    else:
        form = VideoForm()
    return render(request, 'videopublishing/video_edit.html', {'form': form})

def video(request, course_pk, video_pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    course = get_object_or_404(Course_Create, pk=course_pk)
    video_d = get_object_or_404(Videocreate, pk=video_pk)

    post = get_object_or_404(Videocreate, pk=video_pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author=request.user
            comment.save()
            return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
    else:
        form = CommentForm()
    return render(request, 'videopublishing/video.html', {'video_d': video_d, 'course': course,'form':form})


def video_edit(request, course_pk, video_pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/'+ str(course_pk)+'/'+str(video_pk)+'/')
    course_d = get_object_or_404(Course_Create, pk=course_pk)
    # validate author
    if permission_validate_del_edit(request, course_d.author) != 1:
        return HttpResponseRedirect('/courses/' + str(course_pk) + '/' + str(video_pk) + '/')

    video_d = get_object_or_404(Videocreate, pk=video_pk)
    if request.method == "POST":
        form = VideoForm(request.POST, instance=video_d)
        if form.is_valid():
            video_d = form.save(commit=False)
            video_d.course_id = course_pk
            video_d.pub_date = timezone.now()
            video_d.save()
            return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
    else:
        form = VideoForm(instance=video_d)
    return render(request, 'videopublishing/video_edit.html', {'form': form})


def video_delete(request, course_pk, video_pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/' + str(course_pk) + '/' + str(video_pk) + '/')
    course_d = get_object_or_404(Course_Create, pk=course_pk)
    # validate author
    if permission_validate_del_edit(request, course_d.author) != 1:
        return HttpResponseRedirect('/courses/' + str(course_pk) + '/' + str(video_pk) + '/')
    video_d = get_object_or_404(Videocreate, pk=video_pk)
    if request.method == "POST":
        if 'yes' in request.POST.getlist('yes'):
            video_d.delete()
            return redirect('videopublishing:video_list', pk=course_pk)
        elif 'no' in request.POST.getlist('no'):
            return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
    return render(request, 'videopublishing/video_delete.html', {'video_d': video_d})


def course_delete(request, course_pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')
    # validate professor
    if permission_validate(request) != 1:
        return HttpResponseRedirect('/courses/'+str(course_pk))
    course_d = get_object_or_404(Course_Create, pk=course_pk)
    # validate author
    if permission_validate_del_edit(request, course_d.author) != 1:
        return HttpResponseRedirect('/courses/'+str(course_pk))
    if request.method == "POST":
        if 'yes' in request.POST.getlist('yes'):
            course_d.delete()
            return redirect('videopublishing:course_list')
        elif 'no' in request.POST.getlist('no'):
            return redirect('videopublishing:video_list', pk=course_pk)
    return render(request, 'videopublishing/course_delete.html', {'course_d': course_d})


def permission_validate(request):
    flag = 0
    for group in request.user.groups.all():
        if group.name == 'Professor':
            flag = 1
    return flag


def permission_validate_del_edit(request, author):
    flag = 0
    for group in request.user.groups.all():
        if (group.name == 'Professor') and (str(request.user.username) == str(author)):
            flag = 1
    return flag

#def search_titles(request):
    #video = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))
    #return render_to_response('ajax_search.hlml',{'video' : video})
    #if request.method == "POST":
    #    search_text = request.POST['search_text']
    #else:
    #    search_text = ''
    #articles = Article.object.filter(title__contains=search_text)
    #articles = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))    
    #return render_to_response('ajax_search.hlml',{'articles' : articles})