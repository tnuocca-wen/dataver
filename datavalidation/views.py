from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from data.models import Dataset

@login_required
def index(request):
    return render(request, 'datavalidation/index.html', {})

@login_required
def textpair(request):
    if request.method == 'POST':
        filtered_data = Dataset.objects.filter(again=True)
        filtered_pks = filtered_data.values_list('pk', flat=True)
        if 'first_count' not in request.session:
            request.session['first_count'] = 0
        if 'ver' not in request.session:
            request.session['ver'] = []
        ver = request.session['ver']
        print(ver)
        pks_to_exclude = set(filtered_pks) & set(ver)
        print(pks_to_exclude)
        fin_data = filtered_data.exclude(pk__in = pks_to_exclude)
        print(len(fin_data))
        if fin_data.exists():
            random_object = fin_data.order_by('?').first()
            return JsonResponse({'pk':random_object.pk, 'malayalam': random_object.malayalam, 'english': random_object.english})
        else:
            return JsonResponse({'message': 'Now more data available', 'status': 100})


@login_required
def yon(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        rating = request.POST.get('rating')

        ver = request.session['ver']
        ver.append(eval(pk))

        request.session['ver'] = ver

        dataset_object = Dataset.objects.get(pk=pk)
        
        if rating == 'true':
            dataset_object.good += 1
        else:
            dataset_object.bad += 1

        dataset_object.save()

        return JsonResponse({'message': 'Rating saved'})
    else:
        return JsonResponse({'message': 'No rating saved'})
    


@login_required
def edittext(request):
    if request.method == 'POST':
        print("entered edit")
        pk = request.POST.get('pk')
        text = request.POST.get('edit')
        eom = request.POST.get('eom')
        print(text)
        object = Dataset.objects.get(pk=pk)
        if eom == '0':
            object.malayalam = text
        else:
            object.english = text
        object.save()
        return JsonResponse({'status': "success"})