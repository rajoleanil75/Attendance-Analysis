from django.shortcuts import render
from django.http import HttpResponse
from .models import teacher
from .models import admin
from .models import student
from .models import course

from django.shortcuts import render_to_response

def addcourse(request):
	return render(request,'sample/addcourse.html')

def aviewcourse(request):
	return render_to_response('sample/aviewcourse.html', {'obj': course.objects.all()})

def aviewstudent(request):
	return render_to_response('sample/aviewstudent.html', {'obj': student.objects.all()})

def aviewteacher(request):
	return render_to_response('sample/aviewteacher.html', {'obj': teacher.objects.all()})
#	data = teacher.objects.all()
#	thu = {
 #   "teacher": data
#	}
#    return render_to_response('sample/aviewteacher.html',thu)

def adashboard(request):
	return render(request,'sample/adashboard.html')

def login_check(request):
	lid=request.POST.get('lid','')
	lpass=request.POST.get('lpass','')
	role=request.POST.get('role','')
	if role=="admin":
		#a=admin.objects.all()
		#b=admin.objects.get(uid=1)
		#print(b)
		#a=admin.objects.filter(uname=lid)
		#for i in a:
		#	print(i.uid)
		#	print(i.uname)
		#	print(i.upass)
		#	p=i.upass
		#		if p==lpass :
		if lid=="admin":
			if lpass=="password":
				return render(request,'sample/adashboard.html')
		else:
			html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
			return HttpResponse(html)
			#return render(request,'sample/login.html')
		
	elif role=="hod":
		return render(request,'sample/index.html')
	elif role=="techer":
		return render(request,'sample/home1.html')

def home(request):
	return render(request,'sample/home.html')

def login(request):
	return render(request,'sample/login.html')

def index(request):
    return render(request, 'sample/index.html')

def coursesubmit(request):
		coname=request.POST.get('coname','')
		pattern=request.POST.get('pattern','')
		n=course.objects.count()
		p=course(n+1,coname,pattern)
		p.save()

		return render(request, 'sample/coursesubmit.html')
	
def submit(request):
	tid=request.POST.get('tid','')
	tname=request.POST.get('tname','')
	designation=request.POST.get('designation','')
	mobileno=request.POST.get('mobileno','')
	emailid=request.POST.get('emailid','')
	password=request.POST.get('pass1','')
	
#	q = Question(question_text="What's new?", pub_date=timezone.now())
	q=teacher(tid,tname,designation,mobileno,emailid,password);
	q.save()
	#email = EmailMessage('Subject', 'Body', to=[emailid])
	#email.send()
#	return HttpResponse('Make sure all fields are entered and valid.')	
	return render(request, 'sample/submit.html')
#    template = loader.get_template('sample/submit.html')
#   return HttpResponse(template.render(request))
	
