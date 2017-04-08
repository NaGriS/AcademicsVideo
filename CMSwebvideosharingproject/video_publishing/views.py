from django.shortcuts import render
from .models import PublishVideo
from django.utils import timezone
# Create your views here.


def video_list(request):
    videos = PublishVideo.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
    return render(request, 'video_publishing/video_list.html', {'videos': videos})
