import json
import tensorflow
import numpy as np
import tensorflow.compat.v1 as tf
from keras.models import load_model
from django.shortcuts import render
from tensorflow import Graph
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
tf.compat.v1.disable_v2_behavior()
import pymysql
import traceback2 as traceback
import gc
pymysql.install_as_MySQLdb()

# img_height, img_width = 150, 150
img_height, img_width = 120, 120
# with open('./models/data.json', 'r') as fp:
with open('./models/json.json', 'r') as fp:
    labelInfo = fp.read()

labelInfo = json.loads(labelInfo)

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        # model = load_model('./models/archive.h5')
        model = load_model('./models/final.h5')

def index(request):
    context = {'a':1}
    return render(request, 'index.html', context)

def predictImage(request):
    print (request)
    print (request.POST.dict())
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name,fileObj)
    filePathName = fs.url(filePathName)
    testimage='.' + filePathName

    img = image.load_img(testimage, target_size=(img_height, img_width))
    x = image.img_to_array(img)
    x = x/255
    x = x.reshape(1, img_height, img_width, 3)
    with model_graph.as_default():
        with tf_session.as_default():
            predi = model.predict(x)
            pred = predi.copy()
            pred = np.amax(pred)
            pred2f = str(pred)[2:4]

    #print(predi[0])
    k = list(predi[0])
    k.sort(reverse=True)
    pk = 100
    pk1 = str(round(k[1], 2))[2:4]
    pk2 = str(round(k[2], 2))[3:4]
    pk3 = str(round(k[3], 2))[3:4]
    if pk1=="":
        pk1="0"
    if pk2=="":
        pk2="0"
    if pk3=="":
        pk3="0"

    print(k)
    print(predi,"wwwwwwwww")
    print(labelInfo,"kkkkk")
    where1=np.argmax(predi[0])
    predictedLabel = labelInfo[str(where1)]
    predi[0][where1]=0
    where2=np.argmax(predi[0])
    k1 = labelInfo[str(where2)]
    predi[0][where2]=0
    where3=np.argmax(predi[0])
    k2 = labelInfo[str(where3)]
    predi[0][where3]=0
    where4=np.argmax(predi[0])
    k3 = labelInfo[str(where4)]

    context = {'filePathName':filePathName,
               'predictedLabel':predictedLabel,
               'k1':k1,
               'k2':k2,
               'k3':k3,
               'pred2f':pred2f,
               'pk':pk,
               'pk1':pk1,
               'pk2':pk2,
               'pk3':pk3
               }
    return render(request, 'index.html', context)

@csrf_exempt
def map(request):

    db = pymysql.connect(host="localhost", user="root", password="0000", database="scankin")
    # db = pymysql.connect(host="localhost", user="root", password="0000", database="scankin")
    
    cursor = db.cursor()
    area = request.POST.get('district')
    #print(area)
    #district = district
    sql = "SELECT * FROM hospital WHERE district = '%s'" % (area)

    try:
        # Execute the SQL command
        cursor.execute(sql)
         # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        json_data = json.dumps(results, ensure_ascii=False).replace(' ', '').replace('[', '').replace(']', '').replace('\\n', '<br>').replace('\\t', '')
        json_data2 = ""

        for i in range(len(json_data)):
            if json_data[i] == ',' and json_data[i-1].isdigit() == True:
                continue
            else:
                json_data2 += json_data[i]
        print(json_data)
        #info = []
        # if (results.__len__() > 0):
        #     info = ''
        #     for row in results:
        #         info += '{'
        #         #print (row)
        #         name = row[0]
        #         #info.append(name)
        #         info += 'name : ' + name + ","
        #         add = row[3]
        #         info += 'add : ' + add + ","
        #         #info.append(add)
        #         phone = row[4]
        #         info += 'phone : ' + phone + ","
        #         #info.append(phone)
        #         time = row[5]
        #         info += 'time : ' + time + "},"
        #         #info.append(time)
        #         # Now print fetched result
        #         #print ("name = %s, add = %s, phone = %s, time = %s" % (name, add, phone, time))
        #     print(info)
        #     return info
        # else:
        #     print("null")
        #     return 'null'

    except:
        traceback.print_exc()
        print ("Error: unable to fetch data")


    # disconnect from server
    db.close()
    #context = {'name':name,'add':add,'phone':phone,'time':time,}
    #data = JsonResponse(info)
    return JsonResponse(json_data2, encoder=DjangoJSONEncoder, content_type="application/json", safe=False, json_dumps_params={'ensure_ascii':False})


@csrf_exempt
def graph(request):
    db = pymysql.connect(host="localhost", user="root", password="0000", database="scankin")

    cursor = db.cursor()
    month = request.POST.get('month')
    #print(month)
    sql = "SELECT * FROM statistics WHERE month = %s" % (month)
    #print(sql)

    try:
        # Execute the SQL command
        cursor.execute(sql)
         # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        json_mon = json.dumps(results, ensure_ascii=False).replace(' ', '').replace('[', '').replace(']', '')
        print(json_mon)

    except:
        traceback.print_exc()
        print ("Error: unable to fetch data")

    # disconnect from server
    db.close()
    gc.collect()

    return JsonResponse(json_mon, encoder=DjangoJSONEncoder, content_type="application/json", safe=False, json_dumps_params={'ensure_ascii':False})


@csrf_exempt
def scan(request):
    db = pymysql.connect(host="localhost", user="root", password="0000", database="scankin")

    cursor = db.cursor()
    disease = request.POST.get('detailedProcessNum')
    name = '%'+disease+'%'
    #print(month)
    sql = "SELECT * FROM disease WHERE disease LIKE '%s'" % (name)
    #print(sql)

    try:
        # Execute the SQL command
        cursor.execute(sql)
         # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        json_dis = json.dumps(results, ensure_ascii=False).replace(' ', '').replace('[', '').replace(']', '')
        print(json_dis)

    except:
        traceback.print_exc()
        print ("Error: unable to fetch data")

    # disconnect from server
    db.close()
    gc.collect()

    return JsonResponse(json_dis, encoder=DjangoJSONEncoder, content_type="application/json", safe=False, json_dumps_params={'ensure_ascii':False})