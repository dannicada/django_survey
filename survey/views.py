from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
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
    