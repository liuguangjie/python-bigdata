import requests
import bs4

from bs4 import BeautifulSoup
import re
import datetime, time

def parseHtml2Dict(url):
    headers = {"user-agent": "Mizilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    li_infos = soup.select(".job-list li")
    pageInfo = []
    for t in li_infos:
        """
            定义变量存储 字典
        """
        pubJob = {}
        info_primary = t.find_all('div', 'info-primary')

        job = {}
        """
        职位
        """
        job["offer"] = info_primary[0].h3.a.div.string
        """
        薪资
        """
        job["salary"] = info_primary[0].h3.a.span.string

        p = info_primary[0].p

        """
        #print(type(k))
        # 如果是文本
        #if type(k) == bs4.element.NavigableString:

        # 如果是节点 bs4.element.Tag
        # if type(k) == bs4.element.Tag:
        """
        index = 0
        for pItem in p.children:
            if type(pItem) == bs4.element.NavigableString:
                if index == 0:
                    """
                                地点
                            """
                    job["address"] = pItem
                if index == 1:
                    """
                           工作年限
                           """
                    job["yearsIn"] = pItem
                if index == 2:
                    """
                            学历
                            """
                    job["background"] = pItem
                index += 1

        pubJob['job'] = job
        """
        获取公司信息
        """
        info_company = t.find_all('div', 'info-company')

        """
            p标签
        """
        company_p_tag = info_company[0].p

        company = {}

        """
            公司 名称
        """
        company['name'] = info_company[0].div.h3.a.string

        index = 0
        for p_tag in company_p_tag:
            if type(p_tag) == bs4.element.NavigableString:
                if index == 0:
                    """
                        行业
                    """
                    company["industry"] = p_tag
                if index == 1:
                    """
                    融资情况
                    """
                    company["financing"] = p_tag
                if index == 2:
                    """
                    公司规模
                    """
                    company["scale"] = p_tag
                index += 1

        pubJob['company'] = company

        """
            发布者的信息
        """
        info_publis = t.find_all('div', 'info-publis')

        publis = {}
        publis_h3 = info_publis[0].h3

        """
        发布者的头像
        """
        publis['img'] = publis_h3.img['src']

        index = 0
        for publis_tag in publis_h3:
            if type(publis_tag) == bs4.element.NavigableString:
                if index == 0:
                    """
                    发布者的姓名
                    """
                    publis["name"] = publis_tag
                if index == 1:
                    """
                    发布者的职位
                    """
                    publis["position"] = publis_tag
                index += 1

        publis['time'] = handler_time(info_publis[0].p.string)

        pubJob['publisher'] = publis

        pageInfo.append(pubJob)
    """
    把这些数据放在后台展示 就很简单了
    """
    return pageInfo

"""处理时间:
            1. 发布于16:48
            2. 发布于昨天
            3. 发布于07月19日
    统一输出 %Y-%m-%d %H:%M 格式
"""
def handler_time(tiem_str):
    cTime = datetime.datetime.now()
    nowTime = cTime.strftime('%Y-%m-%d')
    nowYear = cTime.strftime('%Y')

    timeLen = tiem_str.__len__()
    preTime = re.sub(r'发布于', "", tiem_str)

    final_str = ""
    if timeLen == 8:
        final_str = nowTime + " " + preTime
    if timeLen == 9:
        t = time.strptime(nowYear + "-" + preTime, "%Y-%m月%d日")
        y, m, d = t[0:3]
        final_str = datetime.datetime(y, m, d).strftime('%Y-%m-%d %H:%M')
    if timeLen == 5:
        """获取昨天 00:00 时间"""
        final_str = (cTime - datetime.timedelta(days=1)).strftime('%Y-%m-%d') + " 00:00"
    #print(final_str)

    return final_str