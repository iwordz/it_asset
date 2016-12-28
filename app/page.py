__author__ = 'fanghouguo'
#coding=utf-8
def getPagtion(url,total,pageSize = 3):

    totalPage = (total / pageSize) + 1
    ret = '<div id="pager">'
    if totalPage:
      for page in range(1,totalPage):
        ret += '<span><a herf="/'+url+'/">'+str(page)+'</a></span>'
    ret +='</div>'
    return ret



