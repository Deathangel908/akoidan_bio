import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from akoidan_bio.forms import UserProfileReadOnlyForm, RequestsForm, UserProfileForm
from akoidan_bio.models import UserProfile, Request
from django.http import Http404

__author__ = 'andrew'


def home(request):
    if request.method == 'GET':
        # TODO remove hardcoded id
        form = UserProfileReadOnlyForm(instance=UserProfile.objects.get(id=1))
        params = {'form': form}
        params.update(csrf(request))
        return render_to_response("akoidan_bio/home.html", params)
    elif request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("form")
        else:
            message = "Login or password is wrong"
        return HttpResponse(message, content_type='text/plain')


def requests(request):
    RequestsFormSet = modelformset_factory(Request, form=RequestsForm)
    # TODO move 10 to settings
    form = RequestsFormSet(queryset=Request.objects.all().order_by('-pk')[:10])
    return render_to_response("akoidan_bio/requests.html", {'formset': form})


def change_form(request):
    user = request.user
    if user.is_authenticated():
        if request.method == 'GET':
            c = csrf(request)
            user_profile = UserProfile.objects.get(pk=1)
            c['form'] = UserProfileForm(instance=user_profile)
            return render_to_response("akoidan_bio/form.html", c)
        elif request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("sorry, form is not valid", content_type='text/plain')

    else:
        raise PermissionDenied


def auth(request):
    """
    POST only. Logs in into system.
    """


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        message = False
        if password is None or password == '':
            message = "Password can't be empty"
        if message is False:
            message = validate_user(username)
        if message is False:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            authenticate(username=username, password=password)
            return HttpResponse("you successfully registered", content_type='text/plain')
        return HttpResponse(message, content_type='text/plain')
    else:
        raise Http404


def validate_user(username):
    if username is None or username == '':
        return "User name can't be empty"
    elif len(username) > 16:
        return "User is too long. Max 16 symbols"
    if not re.match('^[A-Za-z0-9-_]*$', username):
        return "Only letters, numbers, dashes or underlines"
    try:
        # theoretically can throw returning 'more than 1' error
        User.objects.get(username=username)
        return 'This user name already used'
    except User.DoesNotExist:
        return False
