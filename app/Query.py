# coding=utf-8
__author__ = 'fanghouguo'


def fSqlResult(r, key_list):
    return r
    mlist = []
    l = len(key_list)
    if r:
        for item in r:
            tmp = {}
            for i in range(l):
                tmp[key_list[i]] = str(item[i])
            mlist.append(tmp)
    return mlist
