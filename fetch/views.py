# -*- coding: UTF-8 -*-
from django.shortcuts import render


import requests
import bs4
from bs4 import BeautifulSoup
import json
from rplatform.list.boss import html_fetch
# Create your views here.


def fetchboss(request):
    #最新
    #url = "https://www.zhipin.com/c101010100-p100101/?sort=2&ka=new-job-list&page=1"
    #最热
    url = "https://www.zhipin.com/c101010100-p100101/?page=1"
    data = html_fetch.parseHtml2Dict(url)
    """
    往 hbase里面写入数据
    """
    return render(request, "index.html", {"data": data})
