from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method=='POST':
        respone=HttpResponse()
        respone.write("<h1> Thanks for registering<h1></br>")
        respone.write("Your user name:"+request.POST['username']+"</br>")
        return respone
    return render(request,'user_auth/register.html',{'form':UserCreationForm})
