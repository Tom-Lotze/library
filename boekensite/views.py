# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-10 08:59
# @Last Modified by:   TomLotze
# @Last Modified time: 2020-08-11 17:12

from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


