# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image
from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView, CreateView, ListView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.contrib import messages

from ..models import Student, Group

#Views for Students

def students_list(request):
	students = Student.objects.all()
	#try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket', 'id'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	else:
		students = students.order_by('last_name')

	#paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page not an integer, deliver first page
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', 
		{'students': students})

'''
def students_add(request):
	# was form posted?
	if request.method == 'POST':

		#was form add button clicked?:
		if request.POST.get('add_button') is not None:
			#errors collection
			errors = {}
			#validate student data will go here
			data = {'middle_name': request.POST.get('middle_name'),
			'notes': request.POST.get('notes')}

			#validate user input
			first_name = request.POST.get('first_name', '').strip()  #Обрезаем пробелы по краям, если юзер введет их
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-03-25)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов'язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу для студента"
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коректну групу"

				else:
					data['student_group'] = groups[0]

			photo = request.FILES.get('photo')
			if photo:
				try:
					image = Image.open(photo)
				except Exception:
					errors['photo'] = u'Файл не є зображенням або пошкоджений'
				else:
					if photo.size > 2 * 1024 * 1024:
						errors['photo'] = u'Розмір файлу має бути менше 2Мб'
					else:
						data['photo'] = photo

			if not errors:
				#save student
				student = Student(**data)
				student.save()

				#redirect user to students list
				return HttpResponseRedirect(
					#u'%s?status_message=Студента %s успішно додано!' % (reverse('home'), student))
					u'%s?%s' % (reverse('home'), messages.add_message(request, messages.SUCCESS,
						u'Студент {0} {1} був успішно доданий!'.format(first_name, last_name))))
			else:
				#render form with errors and previous user input
				return render(request, 'students/students_add.html', 
					{'groups': Group.objects.all().order_by('title'),
					 'errors': errors})
		elif request.POST.get('cancel_button') is not None:
				#redirect to home page on cancel button
				return HttpResponseRedirect(
					#u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
					u'%s?%s' % (reverse('home'), messages.add_message(request, messages.INFO, 
						u'Додавання студента скасовано!')))
	else:
		#initial form render
		return render(request, 'students/students_add.html', 
		{'groups': Group.objects.all().order_by('title')})
'''


class StudentCreateForm(ModelForm):
	class Meta:
		model = Student
		fields ='__all__'
		#exclude = ("",)

	def __init__(self, *args, **kwargs):
		super(StudentCreateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		#set form tag attributes
		#set form tag attributes
		self.helper.form_action = reverse('students_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.attrs = {'novalidate': ''} #off browser validation, when click cancel_button

		#set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		#add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
		))


class StudentCreateView(CreateView):
	model = Student
	template_name = 'students/students_add.html'
	form_class = StudentCreateForm

	def get_success_url(self):
		#return u'%s?status_message=Студента успішно створено!' % reverse('home')
		messages.success(self.request, u'Студента створено!')
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			#return HttpResponseRedirect(u'%s?status_message=Створення відмінено!' % reverse('home'))
			messages.info(self.request, u'Створення відмінено!')
			return HttpResponseRedirect(reverse('home'))
		else:
			#Use post method from UpdateView
			return super(StudentCreateView, self).post(request, *args, **kwargs)



#def students_edit(request, sid):
	#return HttpResponse('<h1>Edit Student %s</h1>' % sid)

class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields ='__all__'

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
			Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
		))

	def clean_student_group(self):
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')

		return self.cleaned_data['student_group']


class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm

	def get_success_url(self):
		#return u'%s?status_message=Студента успішно збережено!' % reverse('home')
		messages.success(self.request, u'Студента відредаговано!')
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(self.request, u'Редагування відмінено!')
			return HttpResponseRedirect(reverse('home'))
				#u'%s?status_message=Редагування студента відмінено!' % reverse('home'))

		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

#def students_delete(request, sid):
	#return HttpResponse('<h1>Delete Student %s</h1>' % sid)

class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'

	def get_success_url(self):
		#return u'%s?status_message=Студента успішно видалено!' % reverse('home')
		messages.success(self.request, u'Студента видалено!')
		return reverse('home')