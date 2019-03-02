# for class-based view
# from django.views import generic

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,DetailView
from django.shortcuts import render,get_object_or_404
from dems.models import Photo,MyDocs,Patient,Stocks,Hompath,BioChemic,Miasum,MedicineList
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User, Group
from dems.forms import PatientForm

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dems.serializers import PatientSerializer


@csrf_exempt
def patientlist_view(request):
	if request.method == 'GET':
		snippets = Patient.objects.all()
		serializer = PatientSerializer(snippets, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = PatientSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
		return JsonResponse(serializer.data, status=201)
	return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def patient_detail(request, pk):

	try:
		snippet = Patient.objects.get(pk=pk)
	except Patient.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = PatientSerializer(snippet)
		return JsonResponse(serializer.data)

def patient_view(request):
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/dems/patientform/')
	else:
		form = PatientForm()
		context= {
				'form':form
				}
	return render(request,'dems/patient_form.html',context)	


def stocksearch_view(request):
	if request.method == 'POST':
		srch = request.POST['stocks']

		if srch:
			match = Stocks.objects.filter(Q(name__istartswith=srch))

			if match:
				return render(request,'dems/stocksearch.html',{'honey': match})
			else:
				return HttpResponseRedirect('/dems/stocksearch/')

	return render(request,'dems/stocksearch.html')

def psearch_view(request):
	if request.method == 'POST':
		srch = request.POST['srhav']

		if srch:
			match = Patient.objects.filter(Q(name__istartswith=srch))

			if match:
				return render(request,'dems/psearch.html',{'srp': match})
			else:
				return HttpResponseRedirect("/dems/search/")

	return render(request,'dems/psearch.html')

def photo_view(request):
	obj = Photo.objects.all()	
	my_dict= {
		'photos':obj
		}
	return render(request,'dems/photo.html',my_dict)


def creative_photo_view(request):
	obj = Photo.objects.all()	
	my_dict = {
			'photos': obj
				}
	return render(request,'dems/portfolio.html', my_dict)


def miasum_view(request):
	if request.method == 'POST':
		serch = request.POST['mtodo']	
		
		if serch:			
			obj = Miasum.objects.filter(Q(name__istartswith=serch))
			
			if obj:
				return render(request,'dems/miasum.html',{'miasums': obj})
			
			else:
				return HttpResponseRedirect('/dems/miasum/')

	return render(request,'dems/miasum.html')
	

class MiasumDetailView(DetailView):
	template_name='dems/miasum_detail.html'
	context_object_name='mms'
	
	def get_object(self):
		id_= self.kwargs.get("id")
		return get_object_or_404(Miasum,id=id_)


class PhotoListView(ListView):
	template_name='dems/photo_list.html'
	context_object_name='pho'
	queryset= Photo.objects.all()

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['todo']= Photo.objects.all()
		return context

class PhotoDetailView(DetailView):
	template_name='dems/photo_detail.html'
	context_object_name='pts'
	
	def get_object(self):
		id_= self.kwargs.get("id")
		return get_object_or_404(Photo,id=id_)


def mydocs_view(request):
	ob = MyDocs.objects.all()
	dicts = {
		'images':ob
		}
	return render(request,'dems/docs.html',dicts)

class DocListView(ListView):
	model = MyDocs
	context_object_name='ods' #here 2 key ods,doclist 
	template_name = 'dems/mydocs_list.html'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['doclist']= MyDocs.objects.all()
		return context

class DocDetailView(DetailView):
	template_name='dems/mydocs_detail.html'
	context_object_name='pc'	
	def get_object(self):
		id_= self.kwargs.get("id")
		return get_object_or_404(MyDocs,id=id_)

class PatientDetailView(DetailView):
	model = Patient
	template_name = 'dems/patient_detail.html'
	context_object_name = 'mydoc'
	
	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Patient,id=id_)

class PatientListView(ListView):
	model = Patient
	template_name = 'dems/patient_list.html'
	context_object_name = 'pals'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['obj']= Patient.objects.all()
		return context	

#def patient_list_view(request):
#	if request.method == 'POST':
#		sh = request.POST['ptoda']	
#		
#		if sh:			
#			obc = Patient.objects.filter(Q(name__istartswith=sh))
#			
#			if obc:
#				return render(request,'dems/patient_list.html',{'pals': obc})
#			else:
#				return HttpResponseRedirect('/dems/patients/')
#
#	return render(request,'dems/patient_list.html')


class StocksListView(ListView):
	model = Stocks
	template_name = 'dems/stocks_list.html'
	context_object_name = 'pls'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['obj']= Stocks.objects.all()
		return context	

class StocksDetailView(DetailView):
	model = Stocks
	template_name = 'dems/stocks_detail.html'
	context_object_name = 'p'
	
	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Stocks,id=id_)

class HompathDetailView(DetailView):
	model = Hompath
	template_name = 'dems/hompath_detail.html'
	context_object_name = 'h'
	
	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Hompath,id=id_)


def hompathsearch_view(request):
	if request.method == 'POST':
		srch = request.POST['homopa']

		if srch:
			match = Hompath.objects.filter(Q(name__istartswith=srch))

			if match:
				return render(request,'dems/hompath_search.html',{'hompat': match})
			else:
				return HttpResponseRedirect('/dems/hompathsearch/')

	return render(request,'dems/hompath_search.html')


class BioChemicDetailView(DetailView):
	template_name='dems/biochemic_detail.html'
	context_object_name='bic'
	
	def get_object(self):
		id_= self.kwargs.get("id")
		return get_object_or_404(BioChemic,id=id_)

def biochemic_search_view(request):
	if request.method == 'POST':
		srch = request.POST['bios']

		if srch:
			match = BioChemic.objects.filter(Q(name__istartswith=srch))

			if match:
				return render(request,'dems/biochemicsearch.html',{'bo': match})
			else:
				return HttpResponseRedirect("/dems/biosearch/")

	return render(request,'dems/biochemicsearch.html')


class MedicineListDetail_view(DetailView):
	template_name='dems/medicinelist_detail.html'
	context_object_name='medicd'
	
	def get_object(self):
		id_= self.kwargs.get("id")
		return get_object_or_404(MedicineList,id=id_)

class MedicineList_view(ListView):
	model = MedicineList
	context_object_name='medlist' #here 2 key ods,doclist 
	template_name = 'dems/medicinelist_list.html'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['listm']= MedicineList.objects.all()
		return context

def medicinelist_search_view(request):
	if request.method == 'POST':
		srch = request.POST['medico']

		if srch:
			match = MedicineList.objects.filter(Q(name__istartswith=srch))

			if match:
				return render(request,'dems/medicinelist_search.html',{'medo': match})
			else:
				return HttpResponseRedirect("/dems/medosearch/")

	return render(request,'dems/medicinelist_search.html')


def third_view(request):
   return render(request,'dems/third.html')
def navbar_view(request):
    return render(request,'dems/navbar.html')
def fifth_view(request):
    return render(request,'dems/fifth.html')

def home_view(request):
    return render(request,'dems/home.html')


