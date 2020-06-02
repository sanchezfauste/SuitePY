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

import requests
import hashlib
import json
from collections import OrderedDict
from .suite_exceptions import *
from .bean import Bean
from .bean_exceptions import *
from .config import Config
from .singleton import Singleton


class SuiteCRM(Singleton):
    """
    This class contains methods to interact with a SuiteCRM instance.
    """

    conf = Config()
    _session_id = None

    def __init__(self):
        if not self._session_id:
            self._login()

    def _call(self, method, parameters):
        data = {
            'method': method,
            'input_type': 'JSON',
            'response_type': 'JSON',
            'rest_data': json.dumps(parameters),
        }
        r = requests.post(
            self.conf.url,
            data=data,
            verify=self.conf.verify_ssl
        )
        r.raise_for_status()
        response = json.loads(r.text, object_pairs_hook=OrderedDict)
        if self._call_failed(response):
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
        return not result or (len(result) == 3 and 'name' in result
                              and 'description' in result and 'number' in result)

    def _login(self):
        login_parameters = OrderedDict()
        login_parameters['user_auth'] = {
            'user_name': self.conf.username,
            'password': self._md5(self.conf.password)
        }
        login_parameters['application_name'] = self.conf.application_name
        login_result = self._call('login', login_parameters)
        self._session_id = login_result['id']

    @staticmethod
    def _md5(text):
        return hashlib.md5(text.encode('utf8')).hexdigest()

    @staticmethod
    def _get_bean_failed(result):
        try:
            return result['entry_list'][0]['name_value_list'][0]['name'] == 'warning'
        except Exception:
            return False

    def get_bean(self, module_name, id, select_fields='',
                 link_name_to_fields_array='', track_view=''):
        """
        Retrieve a single Bean based on ID.

        :param str module_name: name of the module to return record from.
        :param str id: bean id.
        :param list[str] select_fields: list of the fields to be included in the results.
            This optional parameter allows for only needed fields to be retrieved.
        :param list[dict] link_name_to_fields_array: a list of link_names and for each link_name,
            what fields value to be returned.
        :param bool track_view: should we track the record accessed.
        :return: Bean object matching the selection criteria.
        :rtype: Bean
        :raises BeanNotFoundException: if the Bean is not found.
        :raises SuiteException: if error when retrieving bean from SuiteCRM instance.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['id'] = id
        parameters['select_fields'] = select_fields
        parameters['link_name_to_fields_array'] = link_name_to_fields_array
        parameters['track_view'] = track_view
        result = self._request('get_entry', parameters)
        if self._get_bean_failed(result):
            error_msg = result['entry_list'][0]['name_value_list'][0]['value']
            raise BeanNotFoundException(error_msg)
        return Bean(
            module_name,
            result['entry_list'][0]['name_value_list'],
            result['relationship_list'][0] if len(
                result['relationship_list']) > 0 else []
        )

    def save_bean(self, bean):
        """
        Saves a Bean object to SuiteCRM.

        :param Bean bean: Bean object.
        :raises SuiteException: if error when saving Bean to SuiteCRM instance.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = bean.module
        parameters['name_value_list'] = bean.name_value_list
        result = self._request('set_entry', parameters)
        bean._set_name_value_list(result['entry_list'])
        bean['id'] = result['id']

    def get_bean_list(self, module_name, query='', order_by='',
                      offset='', select_fields='', link_name_to_fields_array='',
                      max_results='', deleted='', favorites=''):
        """
        Get list of beans matching criteria.

        :param str module_name: name of the module to return records from.
        :param str query: SQL WHERE clause without the word 'WHERE'.
        :param str order_by: SQL ORDER BY clause without the phrase 'ORDER BY'.
        :param int offset: the record offset to start from.
        :param list[str] select_fields: a list of the fields to be included in the results.
            This optional parameter allows for only needed fields to be retrieved.
        :param list[dict] link_name_to_fields_array: a list of link_names and for each link_name,
            what fields value to be returned.
        :param int max_results: the maximum number of records to return.
            The default is the sugar configuration value for 'list_max_entries_per_page'.
        :param bool deleted: False if deleted records should not be include,
            True if deleted records should be included.
        :param bool favorites: True if only favorites should be included, False otherwise.
        :return: dict containing results matching criteria.
        :rtype: dict[str, object]
        :raises SuiteException: if error when retrieving beans from SuiteCRM instance.
        """
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
        except Exception:
            pass
        return {
            "result_count": result['result_count'],
            "total_count": result['total_count'],
            "previous_offset": previous_offset,
            "current_offset": offset if offset else 0,
            "next_offset": next_offset,
            "current_limit": max_results,
            "entry_list": bean_list
        }

    def get_available_modules(self, filter='default'):
        """
        Retrieve the list of available modules on the system available to the currently logged in user.

        :param str filter: valid values are: [all, default, mobile].
        :return: dictionary containing information about modules.
        :rtype: dict[str, object]
        :raises SuiteException: if error when retrieving modules from SuiteCRM.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['filter'] = filter
        result = self._request('get_available_modules', parameters)
        return result

    def get_module_fields(self, module_name, fields=''):
        """
        Retrieve field definitions of a module.

        :param str module_name: the name of the module to return records from.
        :param list[str] fields: if specified then retrieve definition of specified fields only.
        :return: field definitions of the specified module.
        :rtype: dict[str, object]
        :raises SuiteException: if error when retrieving field definitions from SuiteCRM.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['fields'] = fields
        result = self._request('get_module_fields', parameters)
        return result

    def get_relationships(self, module_name, module_id, link_field_name,
                          related_module_query='', related_fields=None,
                          related_module_link_name_to_fields_array=None, deleted=False,
                          order_by='', offset='', limit=''):
        """
        Retrieve a collection of beans that are related to the specified bean
        and optionally return relationship data for those related beans.

        :param str module_name: name of the module that the primary record is from.
        :param str module_id: ID of the bean in the specified module.
        :param str link_field_name: name of the link field to return records from.
        :param str related_module_query: a portion of the where clause of the SQL statement to find the related items.
            The SQL query will already be filtered to only include the beans that are related to the specified bean.
        :param list[str] related_fields: list of related bean fields to be returned.
        :param list[dict] related_module_link_name_to_fields_array: for every related bean returned,
            specify link fields name to fields info for that bean to be returned.
        :param bool deleted: False if deleted records should not be include,
            True if deleted records should be included.
        :param str order_by: SQL ORDER BY clause without the phrase 'ORDER BY'.
        :param int offset: the result offset to start from.
        :param int limit: the maximum number of records to return.
        :return: dict containing results matching criteria.
        :rtype: dict[str, object]
        :raises SuiteException: if error when retrieving beans from SuiteCRM instance.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['module_id'] = module_id
        parameters['link_field_name'] = link_field_name
        parameters['related_module_query'] = related_module_query
        parameters['related_fields'] = related_fields or []
        parameters['related_module_link_name_to_fields_array'] = \
            related_module_link_name_to_fields_array or []
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
                    result['relationship_list'][i] if len(
                        result['relationship_list']) > i else []
                )
            )
        previous_offset = None
        result_count = len(bean_list)
        if offset and limit and offset - limit >= 0:
            previous_offset = offset - limit
        next_offset = None
        if limit and result_count == limit:
            if offset:
                next_offset = offset + limit
            else:
                next_offset = limit
        return {
            "entry_list": bean_list,
            "result_count": result_count,
            "previous_offset": previous_offset,
            "current_offset": offset if offset else 0,
            "next_offset": next_offset,
            "current_limit": limit
        }

    def set_relationship(self, module_name, module_id, link_field_name,
                         related_ids, name_value_list=None, delete=False):
        """
        Set a single relationship between two beans. The items are related by module name and id.

        :param str module_name: name of the module that the primary record is from.
        :param str module_id: ID of the bean in the specified module_name.
        :param str link_field_name: name of the link field which relates to the other
            module for which the relationship needs to be generated.
        :param list[str] related_ids: list of related record ids for which relationships needs to be generated.
        :param dict[str, str] name_value_list: the keys of the array are the SugarBean attributes,
            the values of the array are the values the attributes should have.
        :param bool delete: if True delete the relationship and if False add the relationship.
        :return: how many relationships are deleted, created and failed.
        :rtype: dict[str, int]
        :raises SuiteException: if error when relating beans.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['module_name'] = module_name
        parameters['module_id'] = module_id
        parameters['link_field_name'] = link_field_name
        parameters['related_ids'] = related_ids
        parameters['name_value_list'] = name_value_list or []
        parameters['delete'] = delete
        return self._request('set_relationship', parameters)

    def get_note_attachment(self, note_id):
        """
        Retrieve an attachment from a note.

        :param str note_id: ID of the appropriate Note.
        :return: the requested attachment.
        :rtype: dict[str, object]
        :raises SuiteException: if error when retrieving the attachment from SuiteCRM instance.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['id'] = note_id
        return self._request('get_note_attachment', parameters)

    def set_note_attachment(self, note_id, filename, file):
        """
        Add or replace the attachment on a Note.

        :param str note_id: ID of the Note containing the attachment.
        :param str filename: the file name of the attachment.
        :param str file: the binary contents of the file.
        :return: the ID of the note.
        :rtype: dict[str, str]
        :raises SuiteException: if error when setting the note attachment.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['note'] = {
            'id': note_id,
            'filename': filename,
            'file': file
        }
        return self._request('set_note_attachment', parameters)

    def get_pdf_template(self, template_id, bean_module, bean_id):
        """
        Retrieve PDF Template for a given module record.

        :param str template_id: template ID used to generate PDF.
        :param str bean_module: module name of the bean that will be used to populate PDF.
        :param str bean_id: ID of the bean record.
        :return: the generated PDF.
        :rtype: dict[str, str]
        :raises SuiteException: if error when retrieving PDF.
        """
        parameters = OrderedDict()
        parameters['session'] = self._session_id
        parameters['template_id'] = template_id
        parameters['bean_module'] = bean_module
        parameters['bean_id'] = bean_id
        return self._request('get_pdf_template', parameters)
