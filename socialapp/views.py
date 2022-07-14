import json
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from .models import *
from .forms import *

@login_required(login_url='/account/login')
def index(request):
    form = PostForm(request.POST or None)
    followed_posts = Post.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-created_at')
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False) # not save the record in db yet
            post.user = request.user
            post.save()
            return redirect("socialapp:index")
    return render(request, 'socialapp/index.html', {
        'form': form,
        'followed_posts': followed_posts,
    })

class ProfileList(ListView):
    model = Profile
    template_name = 'socialapp/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        try:
            s = self.request.GET.get('profile')
        except KeyError:
            s = None
        if s:
            profiles = Profile.objects.filter(user__username__icontains=s)
        else:
            profiles = Profile.objects.exclude(user=self.request.user)
        return profiles


@login_required(login_url='/account/login')
def profile_detail(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        current_profile_user = request.user.profile
        action = request.POST['followBtn']
        if action == 'follow':
            current_profile_user.follows.add(profile)
        elif action == 'unfollow':
            current_profile_user.follows.remove(profile)
        current_profile_user.save()
    return render(request, 'socialapp/profile_detail.html', {
        'profile': profile,
    })


@login_required(login_url='/account/login')
def image_gallery(request, pk):
    profile = Profile.objects.get(pk=pk)
    profile_id = json.dumps(profile.id)
    return render(request, 'socialapp/image_gallery.html', {
        'profile_id': profile_id
    })

def register(request):
    user_form = UserForm(request.POST or None)
    if request.method == 'POST':
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login/')    
        else:
            return render(request, 'registration/register.html', {
                'user_form': user_form
            })        
    return render(request, 'registration/register.html', {
        'user_form': user_form
    })  

@login_required(login_url='/account/login')
def chatIndex(request):
    return render(request, 'chat/index.html')

@login_required(login_url='/account/login')
def chatRoom(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': mark_safe(json.dumps(request.user.username)),
    })

