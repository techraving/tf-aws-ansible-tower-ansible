#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from ansible import errors
from datetime import datetime, timedelta
import requests, time
import urllib3, json
urllib3.disable_warnings()


# Required for Python 3 compatibility
try:
    basestring
except NameError:
    basestring = str


class FilterModule(object):
    """Ansible encoder Jinja2 filters."""

    def filters(self):
        """Expose filters to ansible."""

        return {
            'get_attribute_by_name': self.get_attribute_by_name,
            'get_instance_attribute': self.get_instance_attribute,
            'get_role_instances': self.get_role_instances,
            'get_group_instances': self.get_group_instances,
            'get_instance_name_by_private_ip': self.get_instance_name_by_private_ip
        }

    def get_attribute_by_name(self, jsonStr, name):
        jsonObj = json.loads(jsonStr)
        for k,v in jsonObj['values']['root_module']['resources'][0]['values'].items():
            if k == name:
                return v

    def get_instance_attribute(self, jsonStr, name):
        jsonObj = json.loads(jsonStr)
        for resource in jsonObj['values']['root_module']['resources']:
            if resource['type'] == 'aws_instance':
                for k,v in resource['values'].items():
                    if k == name:
                        return v

    def get_role_instances(self, jsonStr, type):
        data = []
        jsonObj = json.loads(jsonStr)
        for resource in jsonObj['values']['root_module']['resources']:
            if resource['type'] == 'aws_instance':
                for k,v in resource['values']['tags'].items():
                    if k == "Role" and v == type:
                        data.append(resource['values']['private_ip'])

    def get_group_instances(self, jsonStr, type):
        data = []
        jsonObj = json.loads(jsonStr)
        for resource in jsonObj['values']['root_module']['resources']:
            if resource['type'] == 'aws_instance':
                for k,v in resource['values']['tags'].items():
                    if k == "Group" and v == type:
                        data.append(resource['values']['private_ip'])
        return data

    def get_instance_name_by_private_ip(self, jsonStr, private_ip):
        data = []
        jsonObj = json.loads(jsonStr)
        for resource in jsonObj['values']['root_module']['resources']:
            if resource['type'] == 'aws_instance' and resource['values']['private_ip'] == private_ip:
                for k,v in resource['values']['tags'].items():
                    if k == "Name":
                        return v
