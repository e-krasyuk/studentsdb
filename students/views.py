# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#Views for Students

def students_list(request):
		students = (
			{'id': 1,
			 'first_name': u'Корост',
			 'last_name': u'Андрій',
			 'ticket': 2123,
			 'image': 'img/me.jpeg'},

			{'id': 2,
			 'first_name': u'Шевченко',
			 'last_name': u'Сергій',
			 'ticket': 3862,
			 'image': 'img/podoba3.jpg'},

			{'id': 3,
			 'first_name': u'Левченко',
			 'last_name': u'Олексій',
			 'ticket': 1363,
			 'image': 'img/piv.png'},
		)
			
		return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

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
