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
        if 'ver' not in request.session:
            print("here")
            request.session['ver'] = []
        ver = request.session['ver']
        if filtered_data.exists():
            pk = None
            random_object = filtered_data.order_by('?').first()
            for pk in ver:
                random_object = filtered_data.order_by('?').first()
                pk = random_object.pk
            return JsonResponse({'pk':random_object.pk, 'malayalam': random_object.malayalam, 'english': random_object.english})
        else:
            return JsonResponse({'message': 'Now more data available', 'status': 100})


@login_required
def yon(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        rating = request.POST.get('rating')

        ver = request.session['ver']
        ver.append(pk)

        request.session['ver'] = ver
        
        print(request.session['ver'])
        print(pk)

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
        pk = request.POST.get('pk')
        text = request.POST.get('edit')
        object = Dataset.objects.get(pk=pk)
        object.malayalam = text
        object.save()
        return JsonResponse({'status': "success"})