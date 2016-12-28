#coding=utf-8
__author__ = 'fanghouguo'

import  time
def utcToString(utctime,formation = "%Y-%m-%d %H:%M:%S"):
    if utctime:
       ltime = time.localtime(utctime)
       timeStr = time.strftime(formation, ltime)
       return timeStr


def stringToUtc(strtime):
    if strtime:
         strtime = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
         strtime = time.mktime(strtime)
         return strtime