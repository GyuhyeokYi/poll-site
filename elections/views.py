from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Candidate, Poll, Choice, Area
from django.db.models import Sum

import datetime

# Create your views here.

def index(request):
	areas = Area.objects.all().order_by('name')
	candidates = Candidate.objects.all().order_by('area', 'party_number')

	# str = ''

	# for candidate in candidates:
	# 	str += "<p>{} 기호{}번({})<br>".format(candidate.name,
	# 		candidate.party_number,
	# 		candidate.area)
	# 	str += candidate.introduction+ "</p>"
	# return HttpResponse(str)

	context = {
		'candidates':candidates,
		'areas': areas
		}

	return render(request, 'elections/index.html', context)

def candidates(request, name):
	areas = Area.objects.all().order_by('name')
	candidate = get_object_or_404(Candidate, name=name)
	# try:
	# 	candidate = Candidate.objects.get(name = name)
	# except:
	# 	# return HttpResponseNotFound("없는 페이지 입니다.")
	# 	return Http404

	# return HttpResponse(candidate.name+"<br>"+candidate.introduction)

	context = {'candidate': candidate,
				'areas':areas
				}
	return render(request, 'elections/detail.html', context)

def areas(request, area):
	# return HttpResponse(area)
	areas = Area.objects.all().order_by('name')
	today = datetime.datetime.now()
	area = Area.objects.get(name=area)
	try:
		# poll = Poll.objects.get(area=area, start_date__lte=today, # lte = less than equal, today >= start_date
		# end_date__ gte=today) # gte : great than equal, today <= end_date
		poll = Poll.objects.filter(area=area, start_date__lte=today, # lte = less than equal, today >= start_date
		end_date__gte=today).order_by('start_date').first() # gte : great than equal, today <= end_date

		polls = []
		polls.append(poll)
		candidates = Candidate.objects.filter(area=area)
		print('#######', polls)
	except:
		polls = None
		candidates = None
	context = {'candidates': candidates, 'area': area, 'polls': polls, 'areas':areas}
	return render(request, 'elections/area.html', context)

def polls(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	selection = request.POST['choice']
	print("selection: {}".format(selection))

	try:
		choice = Choice.objects.get(poll_id=poll.id, candidate_id=selection)
		choice.votes += 1
		choice.save()
	except:
		choice = Choice(poll_id=poll.id, candidate_id=selection, votes=1)
		choice.save()

	# return HttpResponse('finish')
	return HttpResponseRedirect("/areas/{}/results".format(poll.area))
	# return redirect("results", { 'area' : poll.area} )

def results(request, area):
	areas = Area.objects.all().order_by('name')
	area = Area.objects.get(name=area)
	candidates = Candidate.objects.filter(area=area)
	
	polls = Poll.objects.filter(area=area)

	poll_results = []
	for poll in polls:
		result = {}
		result['start_date'] = poll.start_date
		result['end_date'] = poll.end_date

		 
		total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
		result['total_votes'] = total_votes['votes__sum']

		rates = [] # 지지율

		for candidate in candidates:
			try:
				choice = Choice.objects.get(poll=poll, candidate=candidate)
				rates.append(
					round(choice.votes * 100 / result['total_votes'], 1)
					)
			except:
				rates.append(0)

		result['rates'] = rates
		poll_results.append(result)

	context = {'candidates': candidates, 'area': area, 'poll_results': poll_results, 'areas':areas}

	return render(request, 'elections/result.html', context)

