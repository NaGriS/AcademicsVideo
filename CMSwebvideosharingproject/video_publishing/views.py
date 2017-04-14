from django.shortcuts import render
from .models import Course_Create
from .models import Video_Create
from .forms import CourseForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
# Create your views here.


def video_list(request, pk):
    course = Course_Create.objects.get(id__exact=pk)
    videos = Video_Create.objects.filter(course__exact=pk).order_by('pub_date')
    return render(request, 'video_publishing/video_list.html', {'videos': videos, 'course': course})


def course_list(request):
    courses = Course_Create.objects.all()
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