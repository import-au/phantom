# File: phantom_views.py
# Copyright (c) 2016-2020 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --

from django.http import HttpResponse
from bs4 import UnicodeDammit
import json
import sys


def find_artifacts(provides, all_results, context):

    headers = ['Container ID', 'Container', 'Artifact ID', 'Artifact Name', 'Found in field', 'Matched Value']

    context['ajax'] = True
    context['allow_links'] = [0, 1]
    if 'start' not in context['QS']:
        context['headers'] = headers
        return '/widgets/generic_table.html'

    start = int(context['QS']['start'][0])
    length = int(context['QS'].get('length', ['5'])[0])
    end = start + length
    cur_pos = 0
    rows = []
    total = 0
    for summary, action_results in all_results:
        for result in action_results:
            base = result.get_summary().get('server')
            data = result.get_data()
            total += len(data)
            for item in data:
                cur_pos += 1
                if (cur_pos - 1) < start:
                    continue
                if (cur_pos - 1) >= end:
                    break
                row = []

                c_link = base + '/mission/{}'.format(item.get('container'))
                row.append({ 'value': c_link, 'link': item.get('container') })
                row.append({ 'value': c_link, 'link': item.get('container_name') })
                row.append({ 'value': item.get('id'), 'link': item.get('id') })
                row.append({ 'value': item.get('name'), 'link': item.get('name') })
                row.append({ 'value': item.get('found in') })
                row.append({ 'value': item.get('matched') })
                rows.append(row)

    if len(rows) == 0:
        content = {
            "data": [[{"value": None}, {"value": None}, {"value": None}, {"value": None}, {"value": None}, {"value": None}]],
            "recordsTotal": 1,
            "recordsFiltered": 1
        }
    else:
        content = {
            "data": rows,
            "recordsTotal": total,
            "recordsFiltered": total,
        }
    return HttpResponse(json.dumps(content), content_type='text/javascript')


def add_artifact(provides, all_results, context):

    headers = ['Artifact ID', 'Container ID']

    context['ajax'] = True
    context['allow_links'] = [1]
    if 'start' not in context['QS']:
        context['headers'] = headers
        return '/widgets/generic_table.html'

    start = int(context['QS']['start'][0])
    length = int(context['QS'].get('length', ['5'])[0])
    end = start + length
    cur_pos = 0
    rows = []
    total = 0
    for summary, action_results in all_results:
        for result in action_results:
            summary = result.get_summary()
            base = summary.get('server')
            data = result.get_data()
            total += len(data)
            for item in data:
                cur_pos += 1
                if (cur_pos - 1) < start:
                    continue
                if (cur_pos - 1) >= end:
                    break
                row = []

                c_link = base + '/mission/{}'.format(summary.get('container id'))
                row.append({ 'value': summary.get('artifact id'), 'link': summary.get('artifact id') })
                row.append({ 'value': c_link, 'link': summary.get('container id') })
                rows.append(row)

    if len(rows) == 0:
        content = {
            "data": [[{"value": None}, {"value": None}]],
            "recordsTotal": 1,
            "recordsFiltered": 1
        }
    else:
        content = {
            "data": rows,
            "recordsTotal": total,
            "recordsFiltered": total
        }
    return HttpResponse(json.dumps(content), content_type='text/javascript')


def find_listitem(provides, all_results, context):

    # Fetching the Python major version
    python_version = 2
    try:
        python_version = int(sys.version_info[0])
    except:
        python_version = 2

    headers = ['List Name', 'Matched Row', 'Found at']

    context['ajax'] = True
    context['allow_links'] = [0, 1]
    if 'start' not in context['QS']:
        context['headers'] = headers
        return '/widgets/generic_table.html'

    start = int(context['QS']['start'][0])
    length = int(context['QS'].get('length', ['5'])[0])
    end = start + length
    cur_pos = 0
    rows = []
    total = 0
    for summary, action_results in all_results:
        for result in action_results:
            summary = result.get_summary()
            param = result.get_param()
            data = result.get_data()
            total += len(data)
            locations = summary.get('locations')
            if not locations:
                locations = 'Not Found'
            for idx, item in enumerate(data):
                cur_pos += 1
                if (cur_pos - 1) < start:
                    continue
                if (cur_pos - 1) >= end:
                    break
                row = []
                item_str = ""
                for i in item:
                    if i:
                        i = UnicodeDammit(i).unicode_markup.encode('utf-8') if python_version == 2 else i
                    item_str = '{0}"{1}",'.format(item_str, i)
                item_str = item_str[:-1]

                row.append({ 'value': param.get('list') })
                row.append({ 'value': item_str })
                len_of_list = len(locations) > idx and locations[idx] or 'Missing Data'
                if type(len_of_list) == str:
                    row.append({ 'value': len_of_list})
                else:
                    row.append({ 'value': 'Row {}, Column {}'.format(len_of_list[0], len_of_list[1])})
                rows.append(row)

    if len(rows) == 0:
        content = {
            "data": [[{"value": None}, {"value": None}, {"value": None}]],
            "recordsTotal": 1,
            "recordsFiltered": 1
        }
    else:
        content = {
            "data": rows,
            "recordsTotal": total,
            "recordsFiltered": total,
        }
    return HttpResponse(json.dumps(content), content_type='text/javascript')
