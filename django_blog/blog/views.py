from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import UserUpdateForm

class ProfileView(LoginRequiredMixin, View):
    template_name = 'blog/profile.html'

    def get(self,request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

        return render(request, self.template_name, {'form':form})