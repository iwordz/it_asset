__author__ = 'fanghouguo'
#coding=utf-8
def makeFormTable(f,is_select = False,select_f = False,select_arr = None):
    sel_html = html =  ''
    if f:
        for item in f:
            if item:
               for itm in item:
                   html += '<div class="field-wrap">'
                   html += '<input type="text" value="" name="'+itm+'" value="'+item[itm]+'"/>'
                   html += '</div>'
    return html   
            