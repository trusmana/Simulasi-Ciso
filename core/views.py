from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime

@login_required
def home(request):
    ipaddr = request.META.get("REMOTE_ADDR")
    user = request.user
    return render(request,'core/base.html',{'ip':ipaddr})

