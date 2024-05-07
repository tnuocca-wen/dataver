from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import csv, os
from data.models import Dataset
from django.http import HttpResponse

@login_required
@csrf_exempt
def adddata(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if not os.path.exists('data/files/' + uploaded_file.name):
            with open('data/files/' + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            with open('data/files/' + uploaded_file.name, newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                good = False
                for row in reader:
                    if len(row) == 2:
                            good = True
                    else:
                        return JsonResponse({'message': 'Not a valid file, Note the csv file should have 2 columns and each string in both the columns should be enclosed inside \" characters', 'status' : 400})
                if good:
                    csvfile.seek(0)  # Reset the file pointer to the beginning
                    # next(reader)   Skip the header row if present
                    for row in reader:
                        instance = Dataset(malayalam=row[0], english=row[1])
                        instance.save()

                    return JsonResponse({'message': 'File uploaded successfully', 'status':200})
                else:
                    # os.remove('data/files/' + uploaded_file.name)
                    return JsonResponse({'message': 'Not a valid file, Note the csv file should have 2 columns and each string in both the columns should be enclosed inside \" characters', 'status' : 400})
        else:
            return JsonResponse({'message': 'Data already exists, or was uploaded once before.', 'status':400})
    else:
        return JsonResponse({'message': 'No file uploaded'}, status=400)
    

@login_required
@csrf_exempt
def exportdata(request, file_name):
        if request.user.is_authenticated and request.user.username == 'daadmin':
            filtered_data = Dataset.objects.filter(Q(consensus='g') | Q(consensus="b"))
            print(len(filtered_data))
            data = filtered_data.values('malayalam', 'english', 'consensus')

            file_path = 'data/files/export/data.csv'

            with open(file_path, "w+", newline='', encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

                for instance in data:
                    mal = instance['malayalam']
                    eng = instance['english']
                    cons = '1' if instance['consensus'] == 'g' else '0'
                    csvwriter.writerows([[mal, eng, cons]])

            with open(file_path, 'rb') as f:
                if f.read() != '':
                    f.seek(0)
                    print("entered")
                    response = HttpResponse(f.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    return response
                else:
                    return JsonResponse({'message': 'No data available' , 'status': 400})
        else:
            return HttpResponse("Access Denied")