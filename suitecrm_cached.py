#######################################################################
# Suite PY is a simple Python client for SuiteCRM API.

# Copyright (C) 2017-2018 BTACTIC, SCCL
# Copyright (C) 2017-2018 Marc Sanchez Fauste

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

import json
import time
import requests
from suitecrm import SuiteCRM
from suite_exceptions import *
from collections import OrderedDict

class SuiteCRMCached(SuiteCRM):

    _cache = {}
    _cache_accessed = {}
    _max_cached_requests = 100

    def _login(self):
        login_parameters = OrderedDict()
        login_parameters['user_auth'] = {
            'user_name' : self.conf.username,
            'password' : self._md5(self.conf.password)
        }
        login_parameters['application_name'] = self.conf.application_name
        login_result = super(SuiteCRMCached, self)._call('login', login_parameters)
        self._session_id = login_result['id']

    def _call(self, method, parameters):
        cached_call = self._get_cached_call(method, parameters)
        if cached_call:
            return cached_call
        else:
            response = super(SuiteCRMCached, self)._call(method, parameters)
            self._add_call_to_cache(method, parameters, response)
            return response

    def _get_time(self):
        return time.time()

    def _get_oldest_accessed_cache_key(self):
        try:
            oldest_accessed = None
            for key, timestamp in self._cache_accessed.items():
                if oldest_accessed and oldest_accessed[1] > timestamp:
                    oldest_accessed = (key, timestamp)
                else:
                    oldest_accessed = (key, timestamp)
            return oldest_accessed[0]
        except:
            return None

    def _remove_oldest_cached_requests(self):
        if len(self._cache) > self._max_cached_requests:
            oldest_accessed = self._get_oldest_accessed_cache_key()
            if oldest_accessed:
                del self._cache[oldest_accessed]
                del self._cache_accessed[oldest_accessed]

    def _add_call_to_cache(self, method, parameters, response):
        try:
            key = (method, json.dumps(parameters))
            self._cache[key] = response
            self._cache_accessed[key] = self._get_time()
            self._remove_oldest_cached_requests()
            return True
        except:
            return False

    def _get_cached_call(self, method, parameters):
        try:
            key = (method, json.dumps(parameters))
            cached_response = self._cache[key]
            self._cache_accessed[key] = self._get_time()
            return cached_response
        except:
            return None

    def clear_cache(self):
        self._cache.clear()
        self._cache_accessed.clear()
