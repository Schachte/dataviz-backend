from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection
from bson import json_util
import unicodedata
import json, ast
import os
import requests
import httplib2
import simplejson
import eventful
from django.views.decorators.csrf import csrf_exempt

def Uptime(request):
    return HttpResponse("Up!")


def CityReviews(request, city):
    """
    @Description:
    Calendar Summary will retrieve 365 days of average pricing data and events for a particular city
    """
    print("doing a query on the database for %s"%(city))

    cursor = connection.cursor()
    cursor.execute('SELECT city_name, comments FROM reviews WHERE city_name like "%s"'%(city))
    rows = cursor.fetchall()
    #Store return data from the SQL query
    result = []

    #Column values in the summary table
    keys = ('city_name', 'comments')

    for row in rows:
        row = list(row)
        row[1] = unicodedata.normalize('NFKD', row[1]).encode('ascii','ignore')
        row[1] = row[1].replace('\n', ' ').replace('\r', '')
        result.append(dict(zip(keys,row)))

    json_data = json.dumps(result, indent=4, sort_keys=True, default=str)

    #Get the city information for 1 year
    return HttpResponse(json_data, content_type="application/json")


def CalendarSummary(request, city):
    """
    @Table Structure:
    +------------+------------+---------------+------------------------------------------------------+
    | city_name  | date       | average_price | happenings                                           |
    +------------+------------+---------------+------------------------------------------------------+

    @Description:
    Calendar Summary will retrieve 365 days of average pricing data and events for a particular city
    """

    print("doing a query on the database for %s"%(city))


    cursor = connection.cursor()
    cursor.execute('SELECT calendar_summary.city_name, calendar_summary.date, calendar_summary.average_price, holiday_event.holiday, holiday_event.event FROM calendar_summary left JOIN holiday_event ON (calendar_summary.city_name = holiday_event.city and calendar_summary.date = holiday_event.date) where calendar_summary.city_name = "%s" order by calendar_summary.date'%(city) )
    # 'SELECT * FROM calendar_summary WHERE city_name="%s"'%(city))

    rows = cursor.fetchall()

    #Store return data from the SQL query
    result = []

    #Column values in the summary table
    keys = ('city_name','date', 'average_price', 'holiday', 'event')

    for row in rows:
        result.append(dict(zip(keys,row)))

    json_data = json.dumps(result, indent=4, sort_keys=True, default=str)

    print(json_data)
    #Get the city information for 1 year
    return HttpResponse(json_data, status=200, content_type="application/json")
