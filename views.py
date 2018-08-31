from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.template import loader
from django.template.response import TemplateResponse
from django.utils.timezone import datetime
from re import compile
from medium.models import Medium

from .models import Tug
from blog.models import Title

class TugMediaDelete(View):
	def post(self, request):
		midinfo=eval(request.body)
		mid=midinfo['mid']
		media=Medium.objects.get(id=mid)
		media.delete()
		return JsonResponse({'TugMediaDeleted':True})

class Address2LatLng(View):
	def post(self, request):
		addrInfo=eval(request.body)
		coordinate=addrInfo['coordinate']
		from geocoder import osm
		rslt=osm(coordinate)
		print(rslt.lat, rslt.lng)
		return JsonResponse(dict(addr2LatLng=True, Lat=rslt.lat, Lng=rslt.lng))
	
class TugDelete(View):
	def post(self, request):
		tidInfo=eval(request.body)
		tid=tidInfo['tid']
		Tug.objects.get(id=tid).delete()
		return JsonResponse({'TugDeleted':True})

class TugEdit(View):
	'''
	def get(self, request):
		rqstPst=request.POST
		tid=rqstPst['tid']
		tug=Tug.objects.get(id=tid)
		return render(request, 'tug-edit.html', {'tug':tug, 'tid':tid})
		return TemplateResponse(request, 'tug-edit.html', {'tug':tug})
	'''
	def post(self, request, tid=None):
		me, rqstPst=request.user, request.POST
		tid, title, coordinate, description, date, time=rqstPst['tid'], rqstPst['title'], rqstPst['coordinate'], rqstPst['description'], rqstPst['date'], rqstPst['time']
		tug=Tug.objects.get(id=tid)
		for media in request.FILES.getlist('attached'):
			mdm=me.user_medium.create(media=media)
			tug.media.add(mdm)
		dtime, tugTitle, pttrn=' '.join([date, time]), tug.title, compile(r'[-:]')
		dtime=pttrn.sub(' ', dtime)	#dtime=dtime.replace('-', ' ').replace(':', ' ')
		a, b, c, d, e, f=map(int, dtime.split())
		dtime=datetime(a, b, c, d, e, f)
		if tug.datetime!=dtime:
			tug.datetime=dtime
			tug.save()
		if title!=tugTitle.title:
			tugTitle.title=title
			tugTitle.save()
		if description!=tug.description:
			tug.description=description
			tug.save()
		if coordinate!=tug.coordinate:
			tug.coordinate=coordinate
			tug.save()
		return JsonResponse({'tugUpdated':True})
		return render(request, 'tug-edit.html', {'tug':tug})

class TugJoin(View):
	def post(self, request):
		me, tugInfo=request.user, eval(request.body)
		tid=tugInfo['tid']
		tug=Tug.objects.get(id=tid)
		if me not in tug.tuggers: tug.tugger.add(me)
		return JsonResponse(dict(tugJoined=True))

class TugAdd(View):
	def post(self, request):
		me, rqstPst=request.user, request.POST
		max, title, coordinate, date, time, description=rqstPst['max'], rqstPst['title'], rqstPst['coordinate'], rqstPst['date'], rqstPst['time'], rqstPst['description']
		datetime=' '.join([date, time])
		#print(loads(request.body))	#__dict__)	#._body)
		#bodyinfo=dump(request.body)	#eval(request._body)
		#print(bodyinfo['textareaData'], bodyinfo['title'], )
		title=Title.objects.create(title=title)
		tug=Tug.objects.create(title=title, description=description, max=max, coordinate=coordinate, datetime=datetime)
		tug.tugger.add(me)
		#tug=Tug.objects.create(body='kdjlkfjd\n', title='BLOG TITLE', post_ptr=post, author=u)
		#medium=tug.post_ptr.media.create()
		for media in request.FILES.getlist('attached'):
			mdm=me.user_medium.create(media=media)
			tug.media.add(mdm)
		tmpl=loader.get_template('tug-template.html')
		ctx=tmpl.render({'tug':tug})
		return JsonResponse(dict(tugAdded=True, ctx=ctx))

class TugDetail(View):
	def get(self, request, tid=None):
			data, tug={}, Tug.objects.get(id=tid)
			userID, iid=request.user.id, tug.initiator.id
			perm=iid==userID
			time=tug.datetime.time().strftime("%H:%M:%S")
			#tug_initiator
			#comments=tug.tug_commenttug.filter(commenttug__isnull=True).all()
			#data['tug'], data['comments']=tug, comments
			return render(request, 'tug-detail.html', {'tug':tug, 'tid':tug.id, 'iid':tug.initiator.id, 'medium':tug.media.all(), 'tuggers':tug.tuggers, 'title':tug.title.title, 'time':time, 'date':tug.datetime.date(), 'max':tug.max, 'coordinate':tug.coordinate, 'datetime':tug.datetime, 'description':tug.description, 'timestamp':tug.timestamp, 'perm':perm})

def fetchData(tid, idRange):
		qsFunc, tugs, count=Tug.objects.filter, tuple(), 0
		while count<idRange:
			tid-=1
			querySet=qsFunc(id=tid)
			if querySet.exists():
				tugs+=(querySet.get(), )
				idRange-=1
			count+=1
		return tid, tugs

class Tugs(View):
	def get(self, request):
		tugQueryset=Tug.objects.filter(id__isnull=False)
		if not tugQueryset.exists():return render(request, 'tugs.html')
		latest_tug, idRange, count=tugQueryset.latest('timestamp'), 5, 0
		tid, tugs=latest_tug.id, tuple()
		while not tugs:
			tid, tugs=fetchData(tid, idRange)
			idRange+=5
			if tid<2:break
		tugs=(latest_tug, )+tugs
		return render(request, 'tugs.html', {'tugs':tugs})

class TugPagination(View):
	def post(self, request, pid=None):
		tid=eval(request.body)['tid']
		tid, tugs, idRange=int(tid), tuple(), 5
		while not tugs:
			tid, tugs=fetchData(tid, idRange)
			idRange+=5
			if tid<2:break
		tmpl=loader.get_template('tug-pagination.html')
		ctx=tmpl.render({'tugs':tugs}, request)
		return JsonResponse({'newData':ctx})
		#posts=[Post.objects.get(id=pid) for pid in range(latestID-idRange, latestID)]
