#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render
from booking.models import Location, Activity, Company, TimeTable
from django.http import HttpResponse
import json
from django.core import serializers
from util.excel_writer import write_booking_from
from django.conf import settings
from threading import Thread
import uniout



from util.logger import get_logger

log = get_logger('KateTravel')
# Create your views here.

def activity_booking_page(request):

    locations = Location.objects.all()
    return render(request, 'booking/activity.html', {'locations': locations})


def get_activities(request):
    activities = list()
    location_id = request.GET.get('location_id')
    tmp_list = Activity.objects.filter(location_id=location_id)
    for act in tmp_list:
        act_dict = dict()
        act_dict['id'] = act.id
        act_dict['name'] = act.name+' ('+act.during_time+')'
        act_dict['company'] = act.company.name+' '+act.company.website+' '+act.company.comment
        activities.append(act_dict)
    return HttpResponse(json.dumps(activities), content_type="application/json")


def get_activity(request):

    activity_id = request.GET.get('id')
    activity = Activity.objects.get(id=activity_id)
    activity = serializers.serialize("json", list([activity]))
    return HttpResponse(activity, content_type="application/json")

def get_time_table(request):

    activity = request.GET.get('id')
    res = TimeTable.objects.filter(activity_id=activity)
    table = [] if not res else res[0].timeslot.split(',')
    for item in table: item = item.strip()
    return HttpResponse(json.dumps(table), content_type='application/json')

def receive_booking(request):

    log.info(json.loads(request.body))
    data = json.loads(request.body)
    detail = data['detail']
    activities = data['activities']
    status = write_booking_from(detail, activities)
    t = Thread(target=send_email, args=(detail,))
    t.start()
    return HttpResponse(json.dumps('Success.'), status=status, content_type='application/json')

def send_email(detail):
    from django.core.mail import EmailMessage

    subject = 'booking from katetravel website'
    to = [settings.DEFAULT_TO_EMAIL, detail['email']]

    text_content = u'''Hi %s %s,\n\n    附件為您的活動預定單，請核對內容並盡快向您的旅遊經紀人確認付款方式.\n\nKateTravel工作團隊 預祝您旅途愉快
                    '''% (detail['first_name'], detail['last_name'])

    msg = EmailMessage(subject, text_content, settings.DEFAULT_FROM_EMAIL, to)
    msg.attach_file('booking_result/KateTravel_%s %s.xlsx' % (detail['first_name'], detail['last_name']))
    msg.send()

