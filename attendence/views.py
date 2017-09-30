from django.shortcuts import render
from django.http import HttpResponse
from .models import teacher
from .models import admin
from .models import student
from .models import course
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def aview(request, username=None, errmsg=None):
	a=request.POST.get('cid','')
	return render_to_response('attendence/aviewclasses.html',{'obj':a})
	#return render(request,'attendence/aviewclasses.html')

def aupdatepass1(request):
	return render(request,'attendence/aupdatepass.html')

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
   return render(request,'attendence/logout.html')
   
def addcourse(request):
	if  'lid' in request.session:
		return render(request,'attendence/addcourse.html')
	else:
	   return render(request,'attendence/home.html')

def aviewcourse(request):
	if 'lid' in request.session:
		return render_to_response('attendence/aviewcourse.html', {'obj': course.objects.all()})
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


def adashboard(request):
	if 'lid' in request.session:
		return render(request,'attendence/adashboard.html')
	else:
	   return render(request,'attendence/home.html')

def login_check(request):
	lid=request.POST.get('lid','')
	lpass=request.POST.get('lpass','')
	role=request.POST.get('role','')
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
				return render(request,'attendence/adashboard.html')
			else:
				html = "<script>alert(\"Invalid Username or Passwords\");window.history.go(-1);</script>"
				return HttpResponse(html)
			#return render(request,'attendence/login.html')
		
	elif role=="hod":
		return render(request,'attendence/index.html')
	elif role=="techer":
		return render(request,'attendence/home1.html')

def home(request):
	return render(request,'attendence/home.html')

def login(request):
	return render(request,'attendence/login.html')

def index(request):
		return render(request, 'attendence/index.html')

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
	if 'lid' in request.session:
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
		return render(request, 'attendence/submit.html')
	#    template = loader.get_template('attendence/submit.html')
	#   return HttpResponse(template.render(request))
	else:
	   return render(request,'attendence/home.html')
	
