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

class SuiteCRM(object):

    def __init__(self, url, username, password, application_name = 'Suite PY'):
        self._url = url
        self._username = username
        self._password = password
        self._application_name = application_name
        self._verify_ssl = True

    def _call(self, method, parameters):
        data = {
            'method' : method,
            'input_type' : 'JSON',
            'response_type' : 'JSON',
            'rest_data' : json.dumps(parameters),
        }
        r = requests.post(self._url, data = data, verify = self._verify_ssl)
        r.raise_for_status()
        response = json.loads(r.text)
        if (self._call_failed(response)):
            raise SuiteException.get_suite_exception(response)
        return response

    @staticmethod
    def _call_failed(result):
        return len(result) == 3 and 'name' in result \
                and 'description' in result and 'number' in result

    def _login(self):
        login_parameters = OrderedDict()
        login_parameters['user_auth'] = {
            'user_name' : self._username,
            'password' : self._md5(self._password)
        }
        login_parameters['application_name'] = self._application_name
        login_result = self._call('login', login_parameters)
        self._session_id = login_result['id']

    @staticmethod
    def _md5(input):
        return hashlib.md5(input.encode('utf8')).hexdigest()
