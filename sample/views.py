from django.shortcuts import render

from .models import teacher
from django.core.mail import EmailMessage

def index(request):
    return render(request, 'sample/index.html')

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
	email = EmailMessage('Subject', 'Body', to=[emailid])
	email.send()
#	return HttpResponse('Make sure all fields are entered and valid.')	
	return render(request, 'sample/submit.html')
#    template = loader.get_template('sample/submit.html')
#   return HttpResponse(template.render(request))
	
