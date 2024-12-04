# -*- coding: utf-8 -*-

from django.http import HttpResponse

from TestModel.models import hospital

# 数据库操作
def testdb(request):
    test1 = hospital(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")