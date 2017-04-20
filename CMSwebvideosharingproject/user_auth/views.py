from django.shortcuts import render,redirect

# Create your views here.
from django.http import  HttpResponse
from django.contrib.auth import (authenticate,login)
from .forms import UserForm
from django.views.generic import View
from django.db.models import Q

#Registration
class UserFormView(View):
    form_class=UserForm
    template_name = 'user_auth/registration_form.html'

    #display blank form

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form =self.form_class(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            #cleaned normalized data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            #returns User objects if credentials are correct
            user=authenticate(username=username,password=password)



            if user is not None:
                if user.is_active:
                    login(request,user)
            return render(request, 'user_auth/login.html',{'error_message': 'Thank for registration. Now you can login to site'})
        return render(request,self.template_name,{'form':form})

 #login user
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # returns User objects if credentials are correct
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                #login sucessfull
                login(request, user)
                return render(request, 'video_publishing/course_list.html', {'error_message': 'Thank for registration'})
            else:
                return render(request, 'user_auth/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'user_auth/login.html', {'error_message': 'Invalid login'})
    return render(request, 'user_auth/login.html')

    #funtion search
    query=request.GET.get("query")
    if query:
        queryset_list=queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        )

