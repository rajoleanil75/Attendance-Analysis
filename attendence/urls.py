from django.conf.urls import url

from . import views

app_name = 'attendence'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^home$', views.home, name='home'),
    url(r'^index$', views.index, name='index'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^login/$', views.login, name='login'),
	url(r'^login_check/$', views.login_check, name='login_check'),
	url(r'^adashboard/$', views.adashboard, name='adashboard'),
	url(r'^aviewteacher$', views.aviewteacher, name='aviewteacher'),
	url(r'^aviewstudent$', views.aviewstudent, name='aviewstudent'),
	url(r'^aviewcourse$', views.aviewcourse, name='aviewcourse'),
	url(r'^addcourse/$', views.addcourse, name='addcourse'),
	url(r'^coursesubmit/$', views.coursesubmit, name='coursesubmit'),
	url(r'^aviewclasses/$', views.aviewclasses, name='aviewclasses'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^aview/$', views.aview, name='aview'),
	url(r'^adminreg/$', views.adminreg, name='adminreg'),
	url(r'^adminsubmit/$', views.adminsubmit, name='adminsubmit'),
	url(r'^aupdatepass/$', views.aupdatepass, name='aupdatepass'),
	url(r'^aupdatepass1/$', views.aupdatepass1, name='aupdatepass1'),
] 