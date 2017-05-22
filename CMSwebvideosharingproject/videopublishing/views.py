from django.shortcuts import render
from .models import Course_Create,Comment
from .models import Videocreate
from .forms import CourseForm
from .forms import VideoForm,CommentForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import  HttpResponse,HttpResponseRedirect

from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from .forms import NotesSearchForm

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
    titlestring = "New course"
    return render(request, 'videopublishing/course_edit.html', {'form': form, 'titlestring': titlestring})


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
    titlestring = "Edit course"
    return render(request, 'videopublishing/course_edit.html', {'form': form, 'titlestring': titlestring})


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
                length_link=len(video.youtube_link)
                if video.youtube_link.find("watch", 0, length_link)!=-1:
                    i=video.youtube_link.find("?v=", 0, length_link)+3
                    s2=video.youtube_link[i:length_link:]
                    s1="https://www.youtube.com/embed/"
                    video.youtube_link=s1+s2
                if video.youtube_link.find("youtu.be", 0, length_link)!=-1:
                    i=video.youtube_link.find("youtu.be/", 0, length_link)+9
                    s2=video.youtube_link[i:length_link:]
                    s1="https://www.youtube.com/embed/"
                    video.youtube_link=s1+s2
                video.course_id = pk
                video.pub_date = timezone.now()
                video.save()
                return redirect('videopublishing:video_list', pk)
    else:
        form = VideoForm()
    titlestring = "New video"
    return render(request, 'videopublishing/video_edit.html', {'form': form, 'titlestring': titlestring})

def video(request, course_pk, video_pk):
    # pemission to pages
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login_user/')

    course = get_object_or_404(Course_Create, pk=course_pk)
    video_d = get_object_or_404(Videocreate, pk=video_pk)

    # comment
    # if 'q' in request.get:
    #   comment_d=get_object_or_404(Comment,pk=request.get['q'])
    post = get_object_or_404(Videocreate, pk=video_pk)
    if request.method == "POST":
        if 'send' in request.POST.getlist('send'):
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
        elif 'delete' in request.POST.getlist('delete'):
            # comment_d.delete()
            comment_id = int(request.POST.get('comment_id'))
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
    else:
        form = CommentForm()
    return render(request, 'videopublishing/video.html', {'video_d': video_d, 'course': course, 'form': form})

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
            length_link = len(video_d.youtube_link)
            if video_d.youtube_link.find("watch", 0, length_link) != -1:
                i = video_d.youtube_link.find("?v=", 0, length_link) + 3
                s2 = video_d.youtube_link[i:length_link:]
                s1 = "https://www.youtube.com/embed/"
                video_d.youtube_link = s1 + s2
            if video_d.youtube_link.find("youtu.be", 0, length_link) != -1:
                i = video_d.youtube_link.find("youtu.be/", 0, length_link) + 9
                s2 = video_d.youtube_link[i:length_link:]
                s1 = "https://www.youtube.com/embed/"
                video_d.youtube_link = s1 + s2
            video_d.course_id = course_pk
            video_d.pub_date = timezone.now()
            video_d.save()
            return redirect('videopublishing:video', course_pk=course_pk, video_pk=video_pk)
    else:
        form = VideoForm(instance=video_d)
    titlestring = "Edit video"
    return render(request, 'videopublishing/video_edit.html', {'form': form, 'titlestring': titlestring})


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

    
