from django.shortcuts import render
from django.shortcuts import render, redirect
from Sunbeam.tasks import test_task


def index(request):
    return render(request, 'about.html')


def run_task(request):
    test_task()
    return redirect(index)
