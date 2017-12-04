from django.shortcuts import render
from django.http import HttpResponse
from .models import teacher
from .models import admin
from .models import student
from .models import course
from .models import division
from .models import subject
from .models import classes
from .models import attendence
from .models import lattendence
from .models import mail
from .models import lab
from .models import lab1
from django.db.models import Max
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from xlrd import open_workbook
import dateutil.parser
from datetime import datetime
from django.db.models import Count
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from graphos.renderers.gchart import GaugeChart
from graphos.renderers.gchart import BarChart
from graphos.renderers.gchart import ColumnChart
from graphos.renderers.gchart import AreaChart
from django.views.decorators.csrf import csrf_exempt
import os
from django.core import management
from django.core.management.commands import loaddata
import sys
from django.core.management import call_command
from wsgiref.util import FileWrapper 
from django.core.files.storage import FileSystemStorage

@csrf_exempt
def aview(request, username=None, errmsg=None):
	a=request.POST.get('cid','')
	return render_to_response('attendence/aviewclasses.html',{'obj':a})
	#return render(request,'attendence/aviewclasses.html')
	
def backup(request):
	if  'lid' in request.session:
		dir = os.path.dirname(__file__)  # get current directory
		#print(dir)
		file_path = os.path.join(dir, 'backup.json')
		#print(file_path)
		#f1 = open( file_path, 'w+')
		#with open(f1) as f:
	#		management.call_command('dumpdata', stdout=f)
		#management.call_command('dumpdata', use_natural_foreign_keys=True)
		#f.close()
		
		sysout = sys.stdout
		sys.stdout = open(file_path, 'w')
		call_command('dumpdata')
		sys.stdout = sysout
		
		f = open(file_path, "r")
		response = HttpResponse(FileWrapper(f), content_type='application/json')
		response['Content-Disposition'] = 'attachment; filename=backup.json'
		f.close()
		m=mail()
		n=request.session.get('lid', '')
		sub="Backup Successful"
		msg= "Backup Successful.."
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		return response
		
		#html = "<script>alert(\"Backup Successful..!!\");window.history.go(-1);</script>"
		#return HttpResponse(html)
		#return render(request,'attendence/tview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def restore(request):
	if  'lid' in request.session:
		return render(request,'attendence/restore.html')
	else:
	   return render(request,'attendence/home.html')
	
def handle_uploaded_file(f):
	dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(dir, 'backup.json')
	with open(file_path,'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	
	
def restore1(request):
	if  'lid' in request.session:
		myfile = request.FILES['efile']
	#	fs = FileSystemStorage()
	#	filename = fs.save(myfile.name, myfile)
	#	uploaded_file_url = fs.url(filename)
	#	print(uploaded_file_url)
		#print(myfile)
		#handle_uploaded_file(request.FILES['efile'])
		handle_uploaded_file(request.FILES['efile'])
		dir = os.path.dirname(__file__)  # get current directory
		file_path = os.path.join(dir, 'backup.json')
		#f = open(file_path, "r")
		call_command('loaddata',file_path, app_label='attendence')
		html = "<script>alert(\"Restore Successful..!!\");window.history.go(-1);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def tview(request):
	if  'lid' in request.session:
		obj1=subject.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/tview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def tlview(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/tlview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def alview(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter()
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/alview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def atview(request):
	if  'lid' in request.session:
		obj1=teacher.objects.all()
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/atview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def hlview(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter()
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/hlview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def htview(request):
	if  'lid' in request.session:
		obj1=teacher.objects.all()
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/htview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def hview(request):
	if  'lid' in request.session:
		obj1=classes.objects.all()
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/hview.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
class DynamicList(list):

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))
    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)
    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))

    def _resize(self, index):
        n = len(self)
        if isinstance(index, slice):
            m = max(abs(index.start), abs(index.stop))
        else:
            m = index + 1
        if m > n:
            self.extend([self.__class__() for i in range(m - n)])

    def __getitem__(self, index):
        self._resize(index)
        return list.__getitem__(self, index)

    def __setitem__(self, index, item):
        self._resize(index)
        if isinstance(item, list):
            item = self.__class__(item)
        list.__setitem__(self, index, item)
	   
def tview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			direct=request.POST.get('direct','')
			obj1=attendence.objects.filter(subject_id=category1,division_id=sub1category).order_by('student')
			obj2=student.objects.filter(division_id=sub1category)
			obj3=subject.objects.get(sid=category1)
			obj4=attendence.objects.values('student').filter(subject_id=category1,division_id=sub1category).order_by('student').annotate(Count('student'))
			obj5=obj4.aggregate(n=Max('student__count'))
			max=obj5.get('n')
			obj6=division.objects.get(did=sub1category)
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Roll No','Attendence']
				i=1
				for a in obj2:
					cnt=0
					for b in obj1:
						if b.student.roll==a.roll:
							cnt+=1
					mat[i] = [a.roll,cnt]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = LineChart(data_source,height=700, width=865, options={'title': 'Attendence Graph'})
				context = {'chart': chart , 'max': max , 'obj1':obj3 , 'obj2': obj6 }
				return render(request, 'attendence/tview1.html', context)
			else:
				mat = DynamicList()
				i=0
				for a in obj2:
					cnt=0
					for b in obj1:
						if b.student.roll==a.roll:
							cnt+=1
					per=cnt/max
					per1=per*100
					mat[i] = [a.roll,a.sname,cnt,per1]
					i=i+1
					context = {'mat': mat , 'max': max , 'obj1':obj3 , 'obj2': obj6 }
				return render(request, 'attendence/tview2.html', context)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	
def tlview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			direct=request.POST.get('direct','')
			obj3=lab.objects.get(lid=category1)
			obj1=lab1.objects.filter(lab_id=category1).order_by('student')
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Roll No','Attendence']
				i=1		
				for b in obj1:	
					obj2=lattendence.objects.filter(lid_id=b.lid)
					cnt=0
					for c in obj2:
							cnt+=1
					mat[i] = [b.student.roll,cnt]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = LineChart(data_source,height=700, width=865, options={'title': 'Lab Attendence Graph'})
				context = {'chart': chart, 'obj1' : obj3 }
				return render(request, 'attendence/tlview1.html', context)
			else:
				mat = DynamicList()
				i=0		
				for b in obj1:	
					obj2=lattendence.objects.filter(lid_id=b.lid)
					cnt=0
					for c in obj2:
						cnt+=1
					mat[i] = [b.student.roll,b.student.sname,cnt]
					i=i+1
				context = {'mat': mat , 'obj1' : obj3 }
				return render(request, 'attendence/tlview2.html', context)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def alview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			direct=request.POST.get('direct','')
			obj1=lab1.objects.filter(lab_id=category1).order_by('student')
			obj3=lab.objects.filter(lid=category1)
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Roll No','Attendence']
				i=1
				for b in obj1:
					obj2=lattendence.objects.filter(lid_id=b.lid)
					cnt=0
					for c in obj2:
						cnt+=1
					mat[i] = [b.student.roll,cnt]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = LineChart(data_source,height=700, width=865, options={'title': 'Lab Attendence Graph'})
				context = {'chart': chart , 'obj3' : obj3}
				return render(request, 'attendence/alview1.html', context)
			else:
				obj4=lattendence.objects.all()
				context_dict = { 'obj1' : obj1, 'obj3' : obj3 , 'obj4' : obj4 }
				return render(request, 'attendence/alview2.html', context_dict)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def atview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			direct=request.POST.get('direct','')
			obj1=subject.objects.filter(teacher_id=category1)
			obj2=lab.objects.filter(teacher_id=category1)
			obj5=teacher.objects.get(tid=category1)
			nme=obj5.tname
			
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Subject','Average Attendance','Total Lecture']
				i=1
				for a in obj1:
					obj3=attendence.objects.filter(subject_id=a.sid)
					obj8=attendence.objects.values('student').filter(subject_id=a.sid).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt=0
					for c in obj3:
						cnt+=1
					obj4=student.objects.all()
					cnt1=0
					for d in obj4:
						if d.division.classes_id == a.classes_id:
							cnt1=cnt1+1
					n=cnt/cnt1
					mat[i] = [a.sname,n,o1]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = ColumnChart(data_source,height=700, width=865, options={'title': 'Subject Attendence Graph'})
				context = {'chart': chart , 'name' : nme }
				return render(request, 'attendence/atview1.html', context)
			else:
				mat = DynamicList()
				i=0
				for a in obj1:
					obj3=attendence.objects.filter(subject_id=a.sid)
					obj8=attendence.objects.values('student').filter(subject_id=a.sid).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					cnt=0
					for c in obj3:
						cnt+=1
					obj4=student.objects.all()
					cnt1=0
					for d in obj4:
						if d.division.classes_id == a.classes_id:
							cnt1=cnt1+1
					n=cnt/cnt1
					mat[i] = [a.sname,a.classes.clname,n,o1]
					i=i+1
				context = {'mat': mat , 'name' : nme }
				return render(request, 'attendence/atview2.html',context)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def htview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			direct=request.POST.get('direct','')
			obj1=subject.objects.filter(teacher_id=category1)
			obj2=lab.objects.filter(teacher_id=category1)
			obj5=teacher.objects.get(tid=category1)
			nme=obj5.tname
			
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Subject','Average Attendance','Total Lecture']
				i=1
				for a in obj1:
					obj3=attendence.objects.filter(subject_id=a.sid)
					obj8=attendence.objects.values('student').filter(subject_id=a.sid).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt=0
					for c in obj3:
						cnt+=1
					obj4=student.objects.all()
					cnt1=0
					for d in obj4:
						if d.division.classes_id == a.classes_id:
							cnt1=cnt1+1
					n=cnt/cnt1
					mat[i] = [a.sname,n,o1]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = ColumnChart(data_source,height=700, width=865, options={'title': 'Subject Attendence Graph'})
				context = {'chart': chart , 'name' : nme }
				return render(request, 'attendence/htview1.html', context)
			else:
				mat = DynamicList()
				i=0
				for a in obj1:
					obj3=attendence.objects.filter(subject_id=a.sid)
					obj8=attendence.objects.values('student').filter(subject_id=a.sid).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					cnt=0
					for c in obj3:
						cnt+=1
					obj4=student.objects.all()
					cnt1=0
					for d in obj4:
						if d.division.classes_id == a.classes_id:
							cnt1=cnt1+1
					n=cnt/cnt1
					mat[i] = [a.sname,a.classes.clname,n,o1]
					i=i+1
				context = {'mat': mat , 'name' : nme }
				return render(request, 'attendence/htview2.html',context)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def hlview1(request):
	if  'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			direct=request.POST.get('direct','')
			obj1=lab1.objects.filter(lab_id=category1).order_by('student')
			obj3=lab.objects.filter(lid=category1)
			if direct == "1":
				mat = DynamicList()
				mat[0] = ['Roll No','Attendence']
				i=1
				for b in obj1:
					obj2=lattendence.objects.filter(lid_id=b.lid)
					cnt=0
					for c in obj2:
						cnt+=1
					mat[i] = [b.student.roll,cnt]
					i=i+1
				data_source = SimpleDataSource(data=mat)
				chart = LineChart(data_source,height=700, width=865, options={'title': 'Lab Attendence Graph'})
				context = {'chart': chart , 'obj3' : obj3}
				return render(request, 'attendence/hlview1.html', context)
			else:
				obj4=lattendence.objects.all()
				context_dict = { 'obj1' : obj1, 'obj3' : obj3 , 'obj4' : obj4 }
				return render(request, 'attendence/hlview2.html', context_dict)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def hview1(request):
	if  'lid' in request.session:
		try:
			#category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			#print(category1)
			#print(sub1category)
			#print(subcategory)
			# obj1=attendence.objects.values('student_id').order_by().annotate(Count('student_id'))
		#	obj1=attendence.objects.values(student).filter(subject_id=category1,division_id=sub1category).order_by('student').annotate(Count('student'))
		#	print(obj1)
			obj1=attendence.objects.filter(division_id=sub1category).order_by('student')
			#print(obj1)
			obj2=subject.objects.filter(classes_id=subcategory)
			obj3=student.objects.filter(division_id=sub1category)
			n=subject.objects.filter(classes_id=subcategory).count()
			n=n+2
			obj4=division.objects.filter(did=sub1category)
			context_dict = { 'obj1' : obj1, 'obj2': obj2, 'obj3': obj3, 'obj4': obj4, 'n':n }
			return render(request, 'attendence/hview1.html', context_dict)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def sview1(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '')
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		i=0
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				per=cnt/o1
				per1=per*100
				mat[i] = [b.sname,cnt,o1,per1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,"-","-"]
				i=i+1
		context = {'mat': mat , 'obj' : obj7 }
		return render(request,'attendence/sview1.html', context)
	else:
	   return render(request,'attendence/student1.html')

def sview2(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '') 
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		mat[0] = ['Subject','Attendence','Total Lecture']
		i=1
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				mat[i] = [b.sname,cnt,o1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,0]
				i=i+1
		data_source = SimpleDataSource(data=mat)
		chart = ColumnChart(data_source,height=700, width=865, options={'title': 'Attendence Graph'})
		context = {'chart': chart , 'obj' : obj7 }
		return render(request, 'attendence/sview2.html', context)
	else:
	   return render(request,'attendence/student1.html')	   

def asview(request):
	if  'lid' in request.session:
		n=request.COOKIES.get('sid') 
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		i=0
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				mat[i] = [b.sname,cnt,o1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,"-"]
				i=i+1
		context = {'mat': mat , 'obj' : obj7 }
		return render(request,'attendence/asview.html', context)
	else:
	   return render(request,'attendence/home.html')
	
def asview1(request):
	if  'lid' in request.session:
		n=request.COOKIES.get('sid') 
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		mat[0] = ['Subject','Attendence','Total Lecture']
		i=1
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				mat[i] = [b.sname,cnt,o1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,0]
				i=i+1
		data_source = SimpleDataSource(data=mat)
		chart = ColumnChart(data_source,height=700, width=865, options={'title': 'Attendence Graph'})
		context = {'chart': chart , 'obj' : obj7 }
		return render(request, 'attendence/asview1.html', context)
	else:
	   return render(request,'attendence/home.html')
	   
def aview1(request):
	if  'lid' in request.session:
		try:
			#category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			#print(category1)
			#print(sub1category)
			#print(subcategory)
			# obj1=attendence.objects.values('student_id').order_by().annotate(Count('student_id'))
		#	obj1=attendence.objects.values(student).filter(subject_id=category1,division_id=sub1category).order_by('student').annotate(Count('student'))
		#	print(obj1)
			obj1=attendence.objects.filter(division_id=sub1category).order_by('student')
			#print(obj1)
			obj2=subject.objects.filter(classes_id=subcategory)
			obj3=student.objects.filter(division_id=sub1category)
			n=subject.objects.filter(classes_id=subcategory).count()
			n=n+2
			obj4=division.objects.filter(did=sub1category)
			context_dict = { 'obj1' : obj1, 'obj2': obj2, 'obj3': obj3, 'obj4': obj4, 'n':n }
			return render(request, 'attendence/aview1.html', context_dict)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   

	
def amail(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '')
		obj1=mail.objects.filter(sender=n).order_by('-mid')[:30]
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/amail.html', context_dict)
		#return render(request,'attendence/amail.html')
	else:
	   return render(request,'attendence/home.html')

def tmail(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '')
		obj1=mail.objects.filter(sender=n).order_by('-mid')[:30]
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/tmail.html', context_dict)
		#return render(request,'attendence/tmail.html')
	else:
	   return render(request,'attendence/home.html')

def hmail(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '')
		obj1=mail.objects.filter(sender=n).order_by('-mid')[:30]
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/hmail.html', context_dict)
		#return render(request,'attendence/tmail.html')
	else:
	   return render(request,'attendence/home.html')
	   
def addteacher(request):
	return render(request,'attendence/addteacher.html')

def addlab(request):
	return render(request,'attendence/addlab.html', {'obj': teacher.objects.all()})

def addsubject(request):
	return render(request,'attendence/addsubject.html', {'obj': teacher.objects.all()})
	#return render_to_response('attendence/addsubject.html', {'obj': teacher.objects.all()})

def tattendence(request):
	if  'lid' in request.session:
		obj1=subject.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/tattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')	
	  
def tlattendence(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/tlattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def hlattendence(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/hlattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')	   
	   
def ultattendence(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/ultattendance.html', context_dict)
	else:
	   return render(request,'attendence/home.html')	

def ulhattendence(request):
	if  'lid' in request.session:
		obj1=lab.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/ulhattendance.html', context_dict)
	else:
	   return render(request,'attendence/home.html')	
	   
def tattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=student.objects.filter(division_id=sub1category)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/tattendence2.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def tlattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=lab1.objects.filter(lab_id=category1)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/tlattendence2.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def hlattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=lab1.objects.filter(lab_id=category1)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/hlattendence2.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def ultattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=lab1.objects.filter(lab_id=category1)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/ultattendance1.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def ulhattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=lab1.objects.filter(lab_id=category1)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/ulhattendance1.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def tattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=subject.objects.get(sid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=student.objects.get(sid=i)
			#print(st.sname)
			atd=attendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.student=st
			atd.division=d
			atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Attendence Added"
		msg=s.sname+" attendece added for division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Attendence Added..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def tlattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=lab.objects.get(lid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=lab1.objects.get(lid=i)
			#print(st.sname)
			atd=lattendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.lid=st
			#atd.division=d
			#atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Lab Attendence Added"
		msg=s.lname+" attendece added of division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Lab Attendence Added..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def hlattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=lab.objects.get(lid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=lab1.objects.get(lid=i)
			#print(st.sname)
			atd=lattendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.lid=st
			#atd.division=d
			#atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Lab Attendence Added"
		msg=s.lname+" attendece added of division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Lab Attendence Added..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def ultattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=lab.objects.get(lid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		obj1=lab1.objects.filter(lab_id=sub)
		for i in obj1:
			lattendence.objects.filter(adate=date,lid_id=i.lid).delete()
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=lab1.objects.get(lid=i)
			#print(st.sname)
			atd=lattendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.lid=st
			#atd.division=d
			#atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Lab Attendence Updated"
		msg=s.lname+" attendece updated of division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Lab Attendence Updated..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def ulhattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=lab.objects.get(lid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		obj1=lab1.objects.filter(lab_id=sub)
		for i in obj1:
			lattendence.objects.filter(adate=date,lid_id=i.lid).delete()
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=lab1.objects.get(lid=i)
			#print(st.sname)
			atd=lattendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.lid=st
			#atd.division=d
			#atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Lab Attendence Updated"
		msg=s.lname+" attendece updated of division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Lab Attendence Updated..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def hattendence(request):
	if  'lid' in request.session:
		obj1=subject.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/hattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')	

def hattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=student.objects.filter(division_id=sub1category)
			#print(obj1)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/hattendence2.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def hattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=subject.objects.get(sid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=student.objects.get(sid=i)
			#print(st.sname)
			atd=attendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.student=st
			atd.division=d
			atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)

		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		m=mail()
		n=request.session.get('lid', '')
		sub="Attendence Added"
		msg=s.sname+" attendece added for division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		html = "<script>alert(\"Attendence Added..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def utattendence(request):
	if 'lid' in request.session:
		obj1=subject.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/utattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def utattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=attendence.objects.filter(adate=date,subject_id=category1,division_id=sub1category)
			obj2=student.objects.filter(division_id=sub1category)
			context_dict = { 'obj1' : obj1, 'obj2': obj2}
			return render(request,'attendence/utattendence1.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def utattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=subject.objects.get(sid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		attendence.objects.filter(adate=date,subject_id=sub,division_id=div).delete()
		#for r in rows:
		#	r.delete()
		#attendence.objects.all().delete()
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=student.objects.get(sid=i)
			#print(st.sname)
			atd=attendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.student=st
			atd.division=d
			atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)
		m=mail()
		n=request.session.get('lid', '')
		sub="Attendence Updated"
		msg=s.sname+" attendece updated for division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		
		html = "<script>alert(\"Attendence Updated..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def uhattendence(request):
	if 'lid' in request.session:
		obj1=subject.objects.filter(teacher_id=request.session['lid'])
		#obj2=student.objects.all()
		#context_dict = { 'obj1' : obj1, 'obj2': obj2}
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/uhattendence.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def uhattendence1(request):
	if 'lid' in request.session:
		try:
			category1=request.POST.get('category1','')
			subcategory=request.POST.get('subcategory','')
			sub1category=request.POST.get('sub1category','')
			date=request.POST.get('date','')
			#print(request.POST)
			request.session['subject'] = category1
			request.session['division'] = sub1category
			request.session['date'] = date
			obj1=attendence.objects.filter(adate=date,subject_id=category1,division_id=sub1category)
			#print(obj)
			#obj2=student.objects.filter(sid=obj)
			#print(obj2)
			obj2=student.objects.filter(division_id=sub1category)
			#print(obj1)
			context_dict = { 'obj1' : obj1, 'obj2': obj2}
			return render(request,'attendence/uhattendence1.html', context_dict)
			#html = "<script>alert(\"Attendence Added..!!\");window.history.go(-1);</script>"
			#return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def uhattendence2(request):
	if 'lid' in request.session:
		#form = NameForm(request.POST)
		#subject = form.cleaned_data['chk1']
		#print(subject)
		chk1=request.POST.getlist('chk')
		#print(chk1)
		sub=request.session.get('subject', '')
		#print(sub)
		s=subject.objects.get(sid=sub)
		#print(s.sname)
		div=request.session.get('division', '')
		#print(div)
		date=request.session.get('date', '')
		#print(date)
		d=division.objects.get(did=div)
		attendence.objects.filter(adate=date,subject_id=sub,division_id=div).delete()
		#for r in rows:
		#	r.delete()
		#attendence.objects.all().delete()
		for i in chk1:
			#n=attendence.objects.count()
			#n+=1
			st=student.objects.get(sid=i)
			#print(st.sname)
			atd=attendence()
			#atd.aid=n
			atd.adate=date
			atd.atime=datetime.now()
			atd.student=st
			atd.division=d
			atd.subject=s
			atd.save()
			#print(i)
		#print(request.POST)
		m=mail()
		n=request.session.get('lid', '')
		sub="Attendence Updated"
		msg=s.sname+" attendece updated for division "+d.dname+", Date:"+date
		m.sender=n
		m.subject=sub
		m.message=msg
		m.mdate=datetime.now().date()
		m.mtime=datetime.now()
		m.save()
		#choices = request.POST.MultipleChoiceField('chk')
		#print(choices)
		
		html = "<script>alert(\"Attendence Updated..!!\");window.history.go(-2);</script>"
		return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def addsubject1(request):
	if 'lid' in request.session:
		try:
			scode=request.POST.get('scode','')
			sname=request.POST.get('sname','')
			maxlec=request.POST.get('maxlec','')
			thid=request.POST.get('teacher','')
			clas=request.POST.get('classes','')
			d=teacher.objects.get(tid=thid)
			e=classes.objects.get(clid=clas)
			n=subject.objects.count()
			q=subject(1,0,'',0,d,e)
			q.sid=n+1
			q.scode=scode
			q.sname=sname
			q.max_lacture=maxlec
			q.teacher=d
			q.classes=e
			q.save();
			m=mail()
			n=request.session.get('lid', '')
			sub="Subject Added"
			msg= sname+" subject added to "+e.clname
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			return render(request, 'attendence/subjectsubmit.html')
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def addlab1(request):
	if 'lid' in request.session:
		lname=request.POST.get('lname','')
		div=request.POST.get('sub1category','')
		teach=request.POST.get('teacher','')
		try:
			d=teacher.objects.get(tid=teach)
			div1=division.objects.get(did=div)
			fromr=request.POST.get('from','')
			tor=request.POST.get('to','')
			fromr1=int(fromr)
			tor1=int(tor)
			if fromr1>=tor1:
				html = "<script>alert(\"From Roll No. is must be less than To Roll No.\");window.history.go(-2);</script>"
				return HttpResponse(html)
			q=lab()
			q.lname=lname
			q.teacher=d
			q.division=div1
			q.save()
			
			#ssid=101
			#s2=student.objects.get(sid=ssid)
			while fromr1<=tor1:
				s=student.objects.filter(division_id=div)
				for s1 in s:
					if s1.roll==fromr1 :
						s2=student.objects.get(sid=s1.sid)
						l1=lab1()
						l1.lab=q
						l1.student=s2
						l1.save()
				fromr1+=1
			m=mail()
			n=request.session.get('lid', '')
			sub="Lab Added"
			msg= lname+" lab added to "+div1.classes.clname
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Lab Added..!!\");window.history.go(-2);</script>"
			return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')

def addteacher1(request):
	if 'lid' in request.session:
		try:
			tid=request.POST.get('tid','')
			tname=request.POST.get('tname','')
			designation=request.POST.get('designation','')
			mobileno=request.POST.get('mobileno','')
			emailid=request.POST.get('emailid','')
			password=""	
			q=teacher(tid,tname,designation,mobileno,emailid,password);
			q.save()
			m=mail()
			n=request.session.get('lid', '')
			sub="Teacher Added"
			msg= "Prof. "+tname+" teacher added."
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()		
			return render(request, 'attendence/teachersubmit.html')
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
	   return render(request,'attendence/home.html')
	   
def aupdatepass1(request):
	return render(request,'attendence/aupdatepass.html')
	
def tupdatepass1(request):
	return render(request,'attendence/tupdatepass.html')
	
def hupdatepass1(request):
	return render(request,'attendence/hupdatepass.html')
	
def supdatepass1(request):
	return render(request,'attendence/supdatepass.html')

def addstudent(request):
	return render(request,'attendence/addstudent.html')

def addstudent1(request):
	if  'lid' in request.session:
		try:
			c1=request.POST.get('category1','') 
			c2=request.POST.get('subcategory',None) 
			c3=request.POST.get('sub1category','sub1category') 
			if c1=="BSc (Computer Science)":
				if c2=="FYBsc":
					if c3=="Div A":
						divid=1
					elif c3=="Div B":
						divid=2
				elif c2=="SYBsc":
					if c3=="Div A":
						divid=3
					elif c3=="Div B":
						divid=4
				elif c2=="TYBsc":
					if c3=="Div A":
						divid=5
					elif c3=="Div B":
						divid=6
			elif c1=="MSc (Computer Science)":
				if c2=="FYMsc":
					if c3=="Div A":
						divid=7
				elif c2=="SYMsc":
					if c3=="Div A":
						divid=8
			myfile = request.FILES['efile']
			arr=myfile.get_array(sheet_name=None)
			d=division.objects.get(did=divid)
			for a in arr:
				t1=a[0]
				t2=str(a[1])
				t4=a[2]
				#n=student.objects.count()
				t3=student()
				#t3.sid=n+1
				t3.division=d
				t3.roll=t1
				t3.sname=t2
				t3.smobile=t4
				t3.save()
			m=mail()
			n=request.session.get('lid', '')
			sub="Students Added"
			msg="Students added to course "+c1+" of class "+c2+" of division "+c3
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Students Added..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		except Exception as e:
			html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
		return render(request,'attendence/home.html')
	
def aupdatepass(request):
	curp=request.POST.get('curp','')
	password=request.POST.get('pass','')
	cpassword=request.POST.get('cpass','')	
	if password==cpassword:
		name=request.session.get('lid', '')
		c=admin.objects.get(uid=request.session['lid'])
		#print(c.len())
		#b = admin(uname=name, upass=curp)
		if c.upass==curp:
			adm=admin.objects.select_for_update().filter(uid=request.session['lid']).update(upass=password)
			#print(adm)
			#print(adm.uname)
			#print(adm.upass)
			#adm.update(upass=password)
			#adm.save();
		#	b.upass=password;
		#	b.save()
			m=mail()
			n=request.session.get('lid', '')
			sub="Password Updated"
			msg="Password Updated"
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Passwords Updated..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		else:
			html = "<script>alert(\"Please enter valid passwrod..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
		html = "<script>alert(\"Passwords Not Match..!!\");window.history.go(-1);</script>"
		return HttpResponse(html)
		
def tupdatepass(request):
	curp=request.POST.get('curp','')
	password=request.POST.get('pass','')
	cpassword=request.POST.get('cpass','')	
	if password==cpassword:
		name=request.session.get('lid', '')
		c=teacher.objects.get(tid=request.session['lid'])
		if c.tpassword==curp:
			adm=teacher.objects.select_for_update().filter(tid=request.session['lid']).update(tpassword=password)
			m=mail()
			n=request.session.get('lid', '')
			sub="Password Updated"
			msg="Password Updated"
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Passwords Updated..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		else:
			html = "<script>alert(\"Please enter valid passwrod..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
		html = "<script>alert(\"Passwords Not Match..!!\");window.history.go(-1);</script>"
		return HttpResponse(html)
		
def hupdatepass(request):
	curp=request.POST.get('curp','')
	password=request.POST.get('pass','')
	cpassword=request.POST.get('cpass','')	
	if password==cpassword:
		name=request.session.get('lid', '')
		c=teacher.objects.get(tid=request.session['lid'])
		if c.tpassword==curp:
			adm=teacher.objects.select_for_update().filter(tid=request.session['lid']).update(tpassword=password)
			m=mail()
			n=request.session.get('lid', '')
			sub="Password Updated"
			msg="Password Updated"
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Passwords Updated..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		else:
			html = "<script>alert(\"Please enter valid passwrod..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
		html = "<script>alert(\"Passwords Not Match..!!\");window.history.go(-1);</script>"
		return HttpResponse(html)

def supdatepass(request):
	curp=request.POST.get('curp','')
	password=request.POST.get('pass','')
	cpassword=request.POST.get('cpass','')	
	if password==cpassword:
		name=request.session.get('lid', '')
		c=student.objects.get(sid=request.session['lid'])
		if c.spassword==curp:
			adm=student.objects.select_for_update().filter(sid=request.session['lid']).update(spassword=password)
			m=mail()
			n=request.session.get('lid', '')
			sub="Password Updated"
			msg="Password Updated"
			m.sender=n
			m.subject=sub
			m.message=msg
			m.mdate=datetime.now().date()
			m.mtime=datetime.now()
			m.save()
			html = "<script>alert(\"Passwords Updated..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		else:
			html = "<script>alert(\"Please enter valid passwrod..!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
	else:
		html = "<script>alert(\"Passwords Not Match..!!\");window.history.go(-1);</script>"
		return HttpResponse(html)

def adminreg(request):
	return render(request,'attendence/adminreg.html')

def adminsubmit(request):
	name=request.POST.get('name','')
	password=request.POST.get('pass','')
	n=admin.objects.count()
	p=admin(n+1,name,password)
	p.save()
	return render(request,'attendence/adminsubmit.html')
  
def logout(request):
   del request.session['lid']
   return render(request,'attendence/home.html')
   
def slogout(request):
   del request.session['lid']
   return render(request,'attendence/student.html')
   
def addcourse(request):
	if  'lid' in request.session:
		return render(request,'attendence/addcourse.html')
	else:
	   return render(request,'attendence/home.html')

def aviewcourse(request):
	if 'lid' in request.session:
		obj1=classes.objects.all()
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/aviewcourse.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def aviewsubject(request):
	if 'lid' in request.session:
		return render_to_response('attendence/aviewsubject.html', {'obj': subject.objects.all()})
	else:
	   return render(request,'attendence/home.html')
	   
def aviewstudent(request):
	if 'lid' in request.session:
		return render_to_response('attendence/aviewstudent.html', {'obj': student.objects.all()})
	else:
	   return render(request,'attendence/home.html')

def aviewteacher(request):
	if 'lid' in request.session:
		return render_to_response('attendence/aviewteacher.html', {'obj': teacher.objects.all()})
#	data = teacher.objects.all()
#	thu = {
 #   "teacher": data
#	}
#    return render_to_response('attendence/aviewteacher.html',thu)
	else:
	   return render(request,'attendence/home.html')
	   
def aviewlab(request):
	if 'lid' in request.session:
		return render_to_response('attendence/aviewlab.html', {'obj': lab.objects.all()})
#	data = teacher.objects.all()
#	thu = {
 #   "teacher": data
#	}
#    return render_to_response('attendence/aviewteacher.html',thu)
	else:
	   return render(request,'attendence/home.html')

def tdashboard(request):
	if 'lid' in request.session:
		n=request.session.get('lid', '') 
		obj1=subject.objects.filter(teacher_id=n)
		obj3=teacher.objects.get(tid=n)
		cnt=0
		for a in obj1:
			cnt=cnt+1
		obj2=lab.objects.filter(teacher_id=n)
		cnt1=0
		for b in obj2:
			cnt1=cnt1+1
		context_dict = { 'cnt' : cnt, 'cnt1': cnt1 , 'obj3': obj3 }
		return render(request,'attendence/tdashboard.html', context_dict)
	else:
	   return render(request,'attendence/home.html')

def adashboard(request):
	if 'lid' in request.session:
		obj1=teacher.objects.count()
		obj2=subject.objects.count()
		obj3=lab.objects.count()
		obj4=student.objects.count()
		n=request.session.get('lid', '') 
		obj5=admin.objects.get(uid=n)
		context_dict = { 'obj1' : obj1, 'obj2': obj2 ,'obj3': obj3 , 'obj4': obj4,'obj5': obj5 }
		return render(request,'attendence/adashboard.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
  
def hdashboard(request):
	if 'lid' in request.session:
		obj1=teacher.objects.count()
		obj2=subject.objects.count()
		obj3=lab.objects.count()
		obj4=student.objects.count()
		n=request.session.get('lid', '') 
		obj5=teacher.objects.get(tid=n)
		context_dict = { 'obj1' : obj1, 'obj2': obj2 ,'obj3': obj3 , 'obj4': obj4,'obj5': obj5 }
		return render(request,'attendence/hdashboard.html', context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def sdashboard(request):
	if 'lid' in request.session:
		n=request.session.get('lid', '') 
		obj1=student.objects.get(sid=n)
		context_dict = { 'obj1' : obj1 }
		return render(request,'attendence/sdashboard.html' , context_dict)
	else:
	   return render(request,'attendence/home.html')
	   
def login_check(request):
	lid=request.POST.get('lid','')
	lpass=request.POST.get('lpass','')
	role=request.POST.get('role','')
	#print(lid)
	if role=="admin":
	#	a=admin.objects.all()
		#b=admin.objects.get(uid=1)
		#print(b)
		a=admin.objects.filter(uname=lid)
		for i in a:
		#	print(i.uid)
		#	print(i.uname)
		#	print(i.upass)
			p=i.upass
			if p==lpass :
				uid=i.uid
	#	if lid=="admin":
	#		if lpass=="password":
				request.session['lid'] = uid
				d=admin.objects.select_for_update().filter(uid=uid).update(lastlogin=datetime.now())
				return render(request,'attendence/adashboard.html')
			else:
				html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
				return HttpResponse(html)
		html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
		return HttpResponse(html)
			#return render(request,'attendence/login.html')
		
	elif role=="hod":
		if lid == "1001" :
			a=teacher.objects.filter(tid=lid)
			for i in a:
				p=i.tpassword
				if p==lpass :
					uid=i.tid
					request.session['lid'] = uid
					d=teacher.objects.select_for_update().filter(tid=uid).update(lastlogin=datetime.now())
					return render(request,'attendence/hdashboard.html')
				else:
					html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
					return HttpResponse(html)
			html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
		else :
			html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
	elif role=="teacher":
		try:
			a=teacher.objects.filter(tid=lid)
		except Exception as e:
			html = "<script>alert(\"InvalidUsername or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
		for i in a:
			p=i.tpassword
			if p==lpass :
				uid=i.tid
				request.session['lid'] = uid
				#creationDate = timezone.now()
				d=teacher.objects.select_for_update().filter(tid=uid).update(lastlogin=datetime.now())
				return render(request,'attendence/tdashboard.html')
			else:
				html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
				return HttpResponse(html)
		html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
		return HttpResponse(html)

def slogin_check(request):
	lid=request.POST.get('lid','')
	lpass=request.POST.get('lpass','')
	#print(lid)
	#if role=="admin":
	#	a=admin.objects.all()
		#b=admin.objects.get(uid=1)
		#print(b)
	a=student.objects.filter(suname=lid)
	for i in a:
		#	print(i.uid)
		#	print(i.uname)
		#	print(i.upass)
		p=i.spassword
		if p==lpass :
			uid=i.sid
	#	if lid=="admin":
	#		if lpass=="password":
			request.session['lid'] = uid
			#e=student.objects.get(sid=uid)
			#request.session['llogin']=e.lastlogin
			d=student.objects.select_for_update().filter(sid=uid).update(lastlogin=datetime.now())
			return render(request,'attendence/sdashboard.html')
		else:
			html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
	html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
	return HttpResponse(html)
			#return render(request,'attendence/login.html')
	
	
def home(request):
	return render(request,'attendence/home.html')
	
def student1(request):
	return render(request,'attendence/student.html')

def login(request):
	return render(request,'attendence/login.html')
	
def slogin(request):
	return render(request,'attendence/slogin.html')

def index(request):
		return render(request, 'attendence/index.html')
		
def sindex(request):
		return render(request, 'attendence/sreg.html')

def coursesubmit(request):
	if 'lid' in request.session:
		coname=request.POST.get('coname','')
		pattern=request.POST.get('pattern','')
		n=course.objects.count()
		p=course(n+1,coname,pattern)
		p.save()

		return render(request, 'attendence/coursesubmit.html')
	else:
	   return render(request,'attendence/home.html')

def aviewclasses(request):
	if  'lid' in request.session:
		#render(request, 'index.html', {params})
		#a=request.POST.get('a','')
		#ans=request.POST.get('ans','')
		#print(p);
		#return render_to_response('attendence/aviewclasses.html', {'ans': p})
		#return render_to_response('attendence/aviewclasses.html', context_instance=RequestContext(request))
		#return render_to_response('attendence/aviewclasses.html', {'answer': p}, context_instance=RequestContext(request))
		return render(request,'attendence/aviewclasses.html')
	else:
	   return render(request,'attendence/home.html')

def submit(request):
	#if 'lid' in request.session:
		tid1=request.POST.get('tid','')
		#tname=request.POST.get('tname','')
		#designation=request.POST.get('designation','')
		#mobileno=request.POST.get('mobileno','')
		emailid=request.POST.get('emailid','')
		password=request.POST.get('pass1','')
		
		try:
			c=teacher.objects.get(tid=tid1)
		except teacher.DoesNotExist:
			html = "<script>alert(\"Invalid Teacher ID...!!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		#print(c.tid)
		#print(c.contact_mob)
		#print(tid1)
		#print(mobileno)
		#print(emailid)
		#if c.contact_mob==mobileno:
		if c.email==emailid:
			d=teacher.objects.select_for_update().filter(tid=tid1).update(tpassword=password)
			return render(request, 'attendence/submit.html')
		else:
			html = "<script>alert(\"Invalid email ID or Teacher ID...!!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		#else:
		#	html = "<script>alert(\"Invalid Mobile Number or Teacher ID\");window.history.go(-1);</script>"
		#	return HttpResponse(html)
	#	q = Question(question_text="What's new?", pub_date=timezone.now())
		#q=teacher(tid,tname,designation,mobileno,emailid,password);
		#q.save()
		#email = EmailMessage('Subject', 'Body', to=[emailid])
		#email.send()
	#	return HttpResponse('Make sure all fields are entered and valid.')	
		
	#    template = loader.get_template('attendence/submit.html')
	#   return HttpResponse(template.render(request))
	#else:
	 #  return render(request,'attendence/home.html')
def ssubmit(request):
	try:
		#if 'lid' in request.session:
		sid1=request.POST.get('sid','')
		uname=request.POST.get('uname','')
		email=request.POST.get('email','')
		#tname=request.POST.get('tname','')
		#designation=request.POST.get('designation','')
		#mobileno=request.POST.get('mobileno','')
		c3=request.POST.get('sub1category','')
		#print(c3)
		mob=request.POST.get('mob','')
		#print(mob)
		password=request.POST.get('pass1','')
		try:
			c=student.objects.get(smobile=mob,division_id=c3)
		except Exception as e:
			html = "<script>alert(\"Invalid Mobile Number...!!!\");window.history.go(-1);</script>"
			return HttpResponse(html)	
		#print(c.tid)
		#print(c.contact_mob)
		#print(tid1)
		#print(mobileno)
		#print(emailid)
		#if c.contact_mob==mobileno:
		sid2=c.sid
		if c.roll==int(sid1):
			d=student.objects.select_for_update().filter(sid=sid2).update(spassword=password,suname=uname,semail=email)
			return render(request, 'attendence/submit.html')
		else:
			html = "<script>alert(\"Invalid Mobile Number or Roll Number...!!!\");window.history.go(-1);</script>"
			return HttpResponse(html)
		#else:
	except Exception as e:
		html = "<script>alert(\"Oops! Something went wrong\");window.history.go(-1);</script>"
		return HttpResponse(html)
		
def m_student(request):
	if 'lid' in request.session:
		n=request.session.get('lid', '') 
		obj1=student.objects.get(sid=n)
		context_dict = { 'obj1' : obj1}
		return render(request,'attendence/m_student.html', context_dict)
	else:
	   return render(request,'attendence/m_slogin.html')
		
def m_slogin(request):
		return render(request, 'attendence/m_slogin.html')
		
def m_slogout(request):
   del request.session['lid']
   return render(request,'attendence/m_slogin.html')
   
def m_slogin_check(request):
	lid=request.POST.get('lid','')
	lpass=request.POST.get('lpass','')
	#print(lid)
	#if role=="admin":
	#	a=admin.objects.all()
		#b=admin.objects.get(uid=1)
		#print(b)
	a=student.objects.filter(suname=lid)
	for i in a:
		#	print(i.uid)
		#	print(i.uname)
		#	print(i.upass)
		p=i.spassword
		if p==lpass :
			uid=i.sid
	#	if lid=="admin":
	#		if lpass=="password":
			request.session['lid'] = uid
			#e=student.objects.get(sid=uid)
			#request.session['llogin']=e.lastlogin
			d=student.objects.select_for_update().filter(sid=uid).update(lastlogin=datetime.now())
			obj1=student.objects.get(sid=uid)
			context_dict = { 'obj1' : obj1}
			return render(request,'attendence/m_student.html', context_dict)
		else:
			html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
	html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
	return HttpResponse(html)
			#return render(request,'attendence/login.html')

def m_sview1(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '')
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		i=0
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				per=cnt/o1
				per1=per*100
				mat[i] = [b.sname,cnt,o1,per1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,"-","-"]
				i=i+1
		context = {'mat': mat , 'obj' : obj7 }
		return render(request,'attendence/m_sview1.html', context)
	else:
	   return render(request,'attendence/m_slogin.html')

def m_sview2(request):
	if  'lid' in request.session:
		n=request.session.get('lid', '') 
		obj7=student.objects.get(sid=n)
		obj1=attendence.objects.filter(student_id=n).order_by('subject')
		obj2=subject.objects.all()
		context_dict = { 'obj1' : obj1}
		mat = DynamicList()
		mat[0] = ['Subject','Attendence','Total Lecture']
		i=1
		for b in obj2:
			cnt=0
			o1=0
			for c in obj1:
				if b.sid==c.subject.sid:
					obj8=attendence.objects.values('student').filter(subject_id=c.subject.sid,division_id=c.division.did).order_by('student').annotate(Count('student'))
					obj9=obj8.aggregate(n=Max('student__count'))
					o1=obj9.get('n')
					#print(o1)
					cnt+=1
			if cnt > 0: 
				mat[i] = [b.sname,cnt,o1]
				i=i+1
	
		obj5=lab1.objects.filter(student_id=n).order_by('lab')
		obj6= lattendence.objects.all()
		for b in obj5:
			cnt=0
			for c in obj6:
				if b.lid==c.lid_id:
					cnt+=1
			if cnt>0:
				mat[i] = [b.lab.lname,cnt,0]
				i=i+1
		data_source = SimpleDataSource(data=mat)
		chart = BarChart(data_source,height=700, width=865, options={'title': 'Attendence Graph'})
		context = {'chart': chart , 'obj' : obj7 }
		return render(request, 'attendence/m_sview2.html', context)
	else:
	   return render(request,'attendence/m_slogin.html')	