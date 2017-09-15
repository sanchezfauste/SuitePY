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

class Bean(object):

    def __init__(self, module, name_value_list = {}):
        self.module = module
        self._fields = {}
        self._set_name_value_list(name_value_list)

    def _set_name_value_list(self, name_value_list):
        for key, value in name_value_list.items():
            self._fields[value['name']] = value['value']

    def __getitem__(self, field_name):
        if field_name in self._fields:
            return self._fields[field_name]
        else:
            return ''

    def __setitem__(self, field_name, value):
        self._fields[field_name] = value

    @property
    def name_value_list(self):
        name_value_list = []
        for name, value in self._fields.items():
            name_value_list.append({'name' : name, 'value' : value})
        return name_value_list

    def __str__(self):
        string = self.module + '\n'
        for key, value in self._fields.items():
            string += '\t' + str(key) + ': ' + str(value) + '\n'
        return string
