from django.shortcuts import render
from .models import Course_Create
from .models import Video_Create
from .forms import CourseForm
from .forms import VideoForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
# Create your views here.


def video_list(request, pk):
    course = Course_Create.objects.get(id__exact=pk)
    videos = Video_Create.objects.filter(course__exact=pk).order_by('id')
    return render(request, 'video_publishing/video_list.html', {'videos': videos, 'course': course})


def course_list(request):
    courses = Course_Create.objects.all().order_by('id')
    return render(request, 'video_publishing/course_list.html', {'courses': courses})


def course_new(request):
    if request.method == "POST":
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.author = request.user
                course.save()
                return redirect('video_list', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'video_publishing/course_edit.html', {'form': form})


def course_edit(request, pk):
    course = get_object_or_404(Course_Create, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('video_list', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'video_publishing/course_edit.html', {'form': form})


def video_new(request, pk):
    if request.method == "POST":
            form = VideoForm(request.POST)
            if form.is_valid():
                video = form.save(commit=False)
                video.course_id = pk
                video.pub_date = timezone.now()
                video.save()
                return redirect('video_list', pk)
    else:
        form = VideoForm()
    return render(request, 'video_publishing/video_edit.html', {'form': form})

def video(request, course_pk, video_pk):
    course = get_object_or_404(Course_Create, pk=course_pk)
    video_d = get_object_or_404(Video_Create, pk=video_pk)
    return render(request, 'video_publishing/video.html', {'video_d': video_d, 'course': course})


def video_edit(request, course_pk, video_pk):
    video_d = get_object_or_404(Video_Create, pk=video_pk)
    if request.method == "POST":
        form = VideoForm(request.POST, instance=video_d)
        if form.is_valid():
            video_d = form.save(commit=False)
            video_d.course_id = course_pk
            video_d.pub_date = timezone.now()
            video_d.save()
            return redirect('video', course_pk=course_pk, video_pk=video_pk)
    else:
        form = VideoForm(instance=video_d)
    return render(request, 'video_publishing/course_edit.html', {'form': form})

def video_delete(request, course_pk, video_pk):
    video_d = get_object_or_404(Video_Create, pk=video_pk)
    if request.method == "POST":
        if 'yes' in request.POST.getlist('yes'):
            video_d.delete()
            return redirect('video_list', pk=course_pk)
        elif 'no' in request.POST.getlist('no'):
            return redirect('video', course_pk=course_pk, video_pk=video_pk)
    return render(request, 'video_publishing/video_delete.html', {'video_d': video_d})

def course_delete(request, course_pk):
    course_d = get_object_or_404(Course_Create, pk=course_pk)
    if request.method == "POST":
        if 'yes' in request.POST.getlist('yes'):
            course_d.delete()
            return redirect('course_list')
        elif 'no' in request.POST.getlist('no'):
            return redirect('video_list', pk=course_pk)
    return render(request, 'video_publishing/course_delete.html', {'course_d': course_d})