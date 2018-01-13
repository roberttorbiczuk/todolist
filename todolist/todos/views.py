from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Todo


def index(request):
    todos = [i for i in enumerate(Todo.objects.all())]
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

        todo = Todo(title=title, text=text)
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
