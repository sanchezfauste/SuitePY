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
    """
    This class represents a SuiteCRM Bean.
    """

    def __init__(self, module, name_value_list=None, relationship_list=None):
        self.module = module
        self._fields = {}
        if name_value_list:
            self._set_name_value_list(name_value_list)
        self._relationship_list = {}
        if relationship_list:
            self._set_relationship_list(relationship_list)

    def _set_name_value_list(self, name_value_list):
        for key, value in name_value_list.items():
            self._fields[value['name']] = value['value']

    def _set_relationship_list(self, relationship_list):
        for relationship in relationship_list:
            records = []
            for record in relationship['records']:
                record_map = {}
                for key, value in record.items():
                    record_map[key] = value['value']
                records.append(record_map)
            self._relationship_list[relationship['name']] = records

    def __getitem__(self, field_name):
        if field_name in self._fields:
            return self._fields[field_name]
        elif field_name in self._relationship_list:
            return self._relationship_list[field_name]
        else:
            return ''

    def __setitem__(self, field_name, value):
        self._fields[field_name] = value

    @property
    def name_value_list(self):
        """
        Get name value list of bean fields.

        :return: name value list of bean fields.
        :rtype: list[dict]
        """
        name_value_list = []
        for name, value in self._fields.items():
            name_value_list.append({'name': name, 'value': value})
        return name_value_list

    @property
    def fields(self):
        """
        Get list of bean fields.

        :return: list with bean fields.
        :rtype: list[str]
        """
        return self._fields.keys()

    @property
    def json(self):
        """
        Get JSON representation of bean.

        :return: key value dictionary containing all bean fields.
        :rtype: dict[str, object]
        """
        return self._fields.copy()

    def __str__(self):
        string = self.module + '\n'
        for key, value in self._fields.items():
            string += '\t' + str(key) + ': ' + str(value) + '\n'
        return string

    def show(self):
        """Prints a representation of bean information."""
        print self.module
        for key, value in self._fields.items():
            print '\t', key, ':', value
        for relationship, records in self._relationship_list.items():
            print '\t', relationship, ':'
            for record in records:
                for key, value in record.items():
                    print '\t\t', key, ':', value
                print '\t\t---- ---- ---- ---- ---- ---- ---- ----'
