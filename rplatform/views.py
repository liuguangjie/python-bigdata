#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
import re
# Create your views here.


def test1():
    str = '发布于昨天'
    print(re.sub('发布于', '', str))
test1()