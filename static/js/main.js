/**
 * Created by fanghouguo on 2016/12/15.
 */


Date.prototype.format = function (format) {
        var date = {
            "M+": this.getMonth() + 1,
            "d+": this.getDate(),
            "h+": this.getHours(),
            "m+": this.getMinutes(),
            "s+": this.getSeconds(),
            "q+": Math.floor((this.getMonth() + 3) / 3),
            "S+": this.getMilliseconds()
        };
        if (/(y+)/i.test(format)) {
            format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
        }
        for (var k in date) {
            if (new RegExp("(" + k + ")").test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length == 1
                        ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
            }
        }
        return format;
    }

///////////////获取URL参数
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return unescape(r[2]);
    return 1;
}


////////////////////////make page
function getPagtion(url, total, current, lastPage) {
    var page_info = '';
    if (total > 10 && current != 1) {
        page_info += '<span><a href="/' + url + '/?p=1">第一页</a></span>&nbsp;';
    }
    //alert(total);
    for (var p = 1; p <= total; p++) {
        if (p == current) {
            page_info += '<span><a style="color:#F00;font-size:18px;" class="active" href="/' + url + '/?p=' + p + '">' + p + '</a></span>&nbsp;';
        }
        else {
            page_info += '<span><a href="/' + url + '/?p=' + p + '">' + p + '</a></span>&nbsp;';
        }
    }
    if (total > 10 && current < lastPage && lastPage != current) {
        page_info += '<span><a href="/' + url + '/?p=' + lastPage + '">最后一页</a></span>';
    }
    page_info_html = '<div id="pager">';
    page_info_html += page_info;
    page_info_html += '</div>';
    return page_info_html;
    //$("#"+id).html(page_info);
}

////////////////////make html content
function makehtml(page_url, page, head, body,is_view) {
    var page_num = getQueryString('p');
    var table_header = '<table class="table" id="myTable"><thead><tr>';
    var new_body_fields = {};
    for (var h_key in head) {
        var h_name = head[h_key].split("-");
        //var h_name_1 = h_key.split("_");
        var h_name_1 = h_key.substring(2,h_key.length);
        console.log(h_name_1);
        new_body_fields[h_name_1] = h_name_1;
        table_header += "<th>" + head[h_key] + "</th>"
    }
    console.log(new_body_fields);
    table_header += '</tr></thead>';
    var table_body = '<tbody>';
    for (var b in body) {
        table_body += '<tr>';
        //for(var bb in body[b])
        for (var bb in new_body_fields) {
            if (bb == 'oper') {
                if (is_view){
                body[b][bb] = '' +
                    '<a data-toggle="modal" data-target="#myModalView" class="btn btn-warning view" data-view="'+body[b]['id']+'" data-page="'+page_num+'" role="button">详细</a>'+
                    '&nbsp;<a data-toggle="modal" data-target="#myModal" class="btn btn-success editor" data-id="' + body[b]['id'] + '" data-page="'+page_num+'" role="button">编辑</a>' +
                    '&nbsp;<a data-toggle="modal" data-target="#myModalDel" class="btn btn-danger delete" data-deleteid="'+body[b]['id']+'" data-page="'+page_num+'" role="button">删除</a>';
                }else{
                    body[b][bb] = '' +
                    '<a data-toggle="modal" data-target="#myModal" class="btn btn-success editor" data-id="' + body[b]['id'] + '" data-page="'+page_num+'" role="button">编辑</a>' +
                    '&nbsp;<a data-toggle="modal" data-target="#myModalDel" class="btn btn-danger delete" data-deleteid="'+body[b]['id']+'" data-page="'+page_num+'" role="button">删除</a>';
                }

            }
            if (bb == 'status') {
                if (body[b][bb] == 1) {
                    body[b][bb] = '正常';
                }
                if (body[b][bb] == 0) {
                    body[b][bb] = '通电未使用';
                }
                if (body[b][bb] == 2) {
                    body[b][bb] = '停机';
                }
            }
            table_body += "<td>" + body[b][bb] + "</td>";
        }
        table_body += '</tr>';
    }
    table_body += '</tbody></table>';
    var table = table_header + table_body;
    console.log(page);
    var page_html = getPagtion(page_url, page['totalpage'], page['current'], page['lastpage']);
    table += page_html;
    $("#body").html(table);
}

function parsebodydata(bodyData) {
    console.log("start parse body data");
}

/////////////////////////common ajax function
function ajaxRequest(page_url, ajax_url, method, param,is_view) {
    ajax_url = '/' + ajax_url + '/?';
    if (param) {
        for (var p in param) {
            ajax_url += p + '=' + param[p] + '&';
        }
    }

    if(!is_view){
        is_view = false;
    }

    $.ajax({
        type: method,
        url: ajax_url,
        beforeSend: function (XMLHttpRequest) {
            //start request status
        },
        success: function (data, textStatus) {
            //make build body html
            makehtml(page_url, data['page'], data['head'], data['body'],is_view);
        },
        complete: function (XMLHttpRequest, textStatus) {
            //HideLoading();
        },
        error: function () {
            //请求出错处理
        }
    });
}
