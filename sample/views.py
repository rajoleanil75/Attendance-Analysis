from django.shortcuts import render

from .models import teacher

def index(request):
    return render(request, 'sample/index.html')

def submit(request):
	tname=request.POST.get('tname','')
	designation=request.POST.get('designation','')
	rescontact=request.POST.get('rescontact','')
	mobileno=request.POST.get('mobileno','')
	emailid=request.POST.get('emailid','')
	n=teacher.objects.count()
	n+=1
#	q = Question(question_text="What's new?", pub_date=timezone.now())
	q=teacher(n,tname,designation,rescontact,mobileno,emailid);
	q.save()
#	return HttpResponse('Make sure all fields are entered and valid.')	
	return render(request, 'sample/submit.html')
#    template = loader.get_template('sample/submit.html')
#   return HttpResponse(template.render(request))
	
