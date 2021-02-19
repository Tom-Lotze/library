# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-10 08:59
# @Last Modified by:   Tom Lotze
# @Last Modified time: 2021-01-05 22:00

from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')





