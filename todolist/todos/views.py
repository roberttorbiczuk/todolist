from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Todo

from datetime import datetime, timezone, timedelta
import pytz



def index(request):
    todos = [(i+1, el) for i, el in enumerate(Todo.objects.all())]
    textes = []
    for i in Todo.objects.all():
        textes.append(i.text[:10] + '...')

    context = {
        'todos': todos,
        'text': textes,
    }
    return render(request, 'index.html', context)


def details(request, id):
    todo = Todo.objects.get(id=id)

    context = {
        'todo': todo
    }
    return render(request, 'details.html', context)


def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        deadline_date = request.POST['date']
        deadline_time = request.POST['time']

        todo = Todo(title=title, text=text)
        todo.deadline = datetime.strptime(deadline_date + deadline_time, "%Y-%m-%d%H:%M" )
        utc_info = pytz.timezone("UTC")
        todo.deadline = utc_info.localize(todo.deadline)
        todo.save()
        return redirect('/todos')
    else:
        return render(request, 'add.html')


def delete(request):
    if request.method == 'POST':
        for todo in Todo.objects.all():
            if str(todo.id) in request.POST:
                todo.delete()
        return redirect('/todos/delete')
    else:
        todos = Todo.objects.all()

        context = {
            'todos': todos
        }
        return render(request, 'delete.html', context)


def one_day(request):
    one_day_to_deadline = []
    for todo in Todo.objects.all().order_by('-deadline'):
        if todo.deadline - datetime.now(timezone.utc) <= timedelta(days=1):
            one_day_to_deadline.append(todo)

    context = {
        'deadline': one_day_to_deadline,
    }
    return render(request, 'day.html', context)


def week(request):
    one_day_to_deadline = []
    for todo in Todo.objects.all().order_by('-deadline'):
        if todo.deadline - datetime.now(timezone.utc) <= timedelta(days=7):
            one_day_to_deadline.append(todo)

    context = {
        'deadline': one_day_to_deadline,
    }
    return render(request, 'week.html', context)
