#######################################################################
# Suite PY is a simple Python client for SuiteCRM API.

# Copyright (C) 2017 Marc Sanchez Fauste
# Copyright (C) 2017 BTACTIC, SCCL

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

import requests
import hashlib
import json
from collections import OrderedDict
from suite_exceptions import *
from bean import Bean
from bean_exceptions import *
from config import Config

class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class SuiteCRM(Singleton):

    conf = Config()
    _session_id = None

    def __init__(self):
        if not self._session_id: self._login()

    def _call(self, method, parameters):
        data = {
            'method' : method,
            'input_type' : 'JSON',
            'response_type' : 'JSON',
            'rest_data' : json.dumps(parameters),
        }
        r = requests.post(self.conf.url, data = data, verify = self.conf.verify_ssl)
        r.raise_for_status()
        response = json.loads(r.text, object_pairs_hook=OrderedDict)
        if (self._call_failed(response)):
            raise SuiteException.get_suite_exception(response)
        return response

    def _request(self, method, parameters):
        try:
            return self._call(method, parameters)
        except InvalidSessionIDException:
            self._login()
            parameters['session'] = self._session_id
            return self._call(method, parameters)

    @staticmethod
    def _call_failed(result):
        return not result or (len(result) == 3 and 'name' in result \
                and 'description' in result and 'number' in result)

    def _login(self):
        login_parameters = OrderedDict()
        login_parameters['user_auth'] = {
            'user_name' : self.conf.username,
            'password' : self._md5(self.conf.password)
        }
        login_parameters['application_name'] = self.conf.application_name
        login_result = self._call('login', login_parameters)
        self._session_id = login_result['id']

    @staticmethod
    def _md5(input):
        return hashlib.md5(input.encode('utf8')).hexdigest()

    @staticmethod
    def _get_bean_failed(result):
        try:
            return result['entry_list'][0]['name_value_list'][0]['name'] == 'warning'
        except:
            return False

    def get_bean(self, module_name, id, select_fields = '',
            link_name_to_fields_array = '', track_view = ''):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['id'] = id
        parameters['select_fields'] = select_fields
        parameters['link_name_to_fields_array'] = link_name_to_fields_array
        parameters['track_view'] = track_view
        result = self._request('get_entry', parameters)
        if (self._get_bean_failed(result)):
            error_msg = result['entry_list'][0]['name_value_list'][0]['value']
            raise BeanNotFoundException(error_msg)
        return Bean(
            module_name,
            result['entry_list'][0]['name_value_list'],
            result['relationship_list'][0] if len(result['relationship_list']) > 0 else []
        )

    def save_bean(self, bean):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = bean.module
        parameters['name_value_list'] = bean.name_value_list
        result = self._request('set_entry', parameters)
        bean._set_name_value_list(result['entry_list'])
        bean['id'] = result['id']

    def get_bean_list(self, module_name, query = '', order_by = '',
            offset = '', select_fields = '', link_name_to_fields_array = '',
            max_results = '', deleted = '', favorites = ''):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['query'] = query
        parameters['order_by'] = order_by
        parameters['offset'] = offset
        parameters['select_fields'] = select_fields
        parameters['link_name_to_fields_array'] = link_name_to_fields_array
        parameters['max_results'] = max_results
        parameters['deleted'] = deleted
        parameters['favorites'] = favorites
        result = self._request('get_entry_list', parameters)
        bean_list = []
        for entry in result['entry_list']:
            bean_list.append(Bean(module_name, entry['name_value_list']))
        previous_offset = None
        if offset and max_results and offset - max_results >= 0:
            previous_offset = offset - max_results
        next_offset = None
        try:
            if int(result['next_offset']) < int(result['total_count']):
                next_offset = result['next_offset']
        except:
            pass
        return {
            "result_count" : result['result_count'],
            "total_count" : result['total_count'],
            "previous_offset" : previous_offset,
            "current_offset" : offset if offset else 0,
            "next_offset" : next_offset,
            "current_limit" : max_results,
            "entry_list" : bean_list
        }

    def get_available_modules(self, filter = 'default'):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['filter'] = filter
        result = self._request('get_available_modules', parameters)
        return result

    def get_module_fields(self, module_name, fields = ''):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['fields'] = fields
        result = self._request('get_module_fields', parameters)
        return result

    def get_relationships(self, module_name, module_id, link_field_name,
            related_module_query = '', related_fields = [], 
            related_module_link_name_to_fields_array = [], deleted = False, 
            order_by = '', offset = '', limit = ''):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['module_id'] = module_id
        parameters['link_field_name'] = link_field_name
        parameters['related_module_query'] = related_module_query
        parameters['related_fields'] = related_fields
        parameters['related_module_link_name_to_fields_array'] = related_module_link_name_to_fields_array
        parameters['deleted'] = deleted
        parameters['order_by'] = order_by
        parameters['offset'] = offset
        parameters['limit'] = limit
        result = self._request('get_relationships', parameters)
        bean_list = []
        for i, entry in enumerate(result['entry_list']):
            bean_list.append(
                Bean(
                    entry['module_name'],
                    entry['name_value_list'],
                    result['relationship_list'][i] if len(result['relationship_list']) > i else []
                )
            )
        previous_offset = None
        if offset and limit and offset - limit >= 0:
            previous_offset = offset - limit
        return {
            "entry_list" : bean_list,
            "previous_offset" : previous_offset,
            "current_offset" : offset if offset else 0,
            "current_limit" : limit
        }

    def get_note_attachment(self, note_id):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['id'] = note_id
        return self._request('get_note_attachment', parameters)

    def set_note_attachment(self, note_id, filename, file):
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['note'] = {
            'id' : note_id,
            'filename' : filename,
            'file' : file
        }
        return self._request('set_note_attachment', parameters)
