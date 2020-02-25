from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse

from django.views import View

class RegisterView(View):
    def get(self, request):
        return render(request, 'survey/register.html', {'form': UserCreationForm() })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))
        return render(request, 'survey/register.html', {'form': form})
    

# class LoginView(View):
#     def get(self, request):
#         return render(request,'survey/login.html', { 'form': AuthenticationForm })
    
#     def post(self, request):
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = authenticate( request, username=form.cleaned_data.get('username'),
#             password=form.cleaned_data.get('password'))
#             if user is None:
#                 return render(request, 'survery/login.html', {'form' : form, 'invalidd_creds' : True })

#             try:
#                 form.confirm_login_allowed(user)
#             except validationError:
#                 return render(
#                     request, 'survey/login.html', {'form': form, 'invalid_creds': True}
#                 )
#             login(request, user)

#             return redirect(reverse('profile'))


class LoginView(View):
    def get(self, request):
        return render (request, 'survey/login.html', {'form': AuthenticationForm})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(request, 'survey/login.html', {'form': form, 'invalid_creds': True})
            login(request, form.get_user())

            return redirect (reverse('profile'))
        return render(request, 'survey/login.html', {'form': form})
    

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        surveys = Survey.objects.filter(created_by=request.user).all()
        assigned_surveys =  SurveyAssignment.objects.filter(assigned_to=request.user).all()

        context = {
            'surveys': surveys,
            'assigned_surveys': assigned_surveys
        }

        return render(request, 'survey/profile.html', context)