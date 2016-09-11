# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse



#Views for Groups

def groups_list(request):
	groups = (
		{'id': 1,
		 'name': 'МтМ-21',
		 'leader': {'id': '1', 'name': 'Ячменєв Олег'}},

		 {'id': 2,
		  'name': 'МтМ-22',
		  'leader': {'id': '2', 'name': 'Віталій Подоба'}},

		  {'id': 3,
		   'name': 'МтМ-23',
		   'leader': {'id': '3', 'name': 'Іванов Андрій'}},
		)
		
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)