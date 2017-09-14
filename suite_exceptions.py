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

class SuiteException(Exception):

    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.number = data['number']

    def __str__(self):
        return self.name + ': ' + self.description

    @staticmethod
    def get_suite_exception(result):
        if result['number'] == 0: return NoErrorException(result)
        if result['number'] == 10: return InvalidLoginException(result)
        if result['number'] == 11: return InvalidSessionIDException(result)
        if result['number'] == 12: return UserNotConfiguredException(result)
        if result['number'] == 20: return ModuleDoesNotExistException(result)
        if result['number'] == 21: return FileDoesNotExistException(result)
        if result['number'] == 30: return ModuleNotSupportedException(result)
        if result['number'] == 31: return RelationshipNotSupportedException(result)
        if result['number'] == 40: return AccessDeniedException(result)
        if result['number'] == 50: return DuplicateRecordsException(result)
        if result['number'] == 51: return NoRecordsException(result)
        if result['number'] == 52: return CannotAddOfflineClientException(result)
        if result['number'] == 53: return ClientDeactivatedException(result)
        if result['number'] == 60: return NumberOfSessionsExceededException(result)
        if result['number'] == 61: return UpgradeClientException(result)
        if result['number'] == 70: return AdminCredentialsRequiredException(result)
        if result['number'] == 80: return CustomFieldTypeNotSupportedException(result)
        if result['number'] == 81: return CustomFieldPropertyNotSuppliedException(result)
        if result['number'] == 90: return ResourceManagementErrorException(result)
        if result['number'] == 1000: return InvalidCallErrorException(result)
        if result['number'] == 1001: return InvalidDataFormatException(result)
        if result['number'] == 1005: return InvalidSetCampaignMergeDataException(result)
        if result['number'] == 1009: return PasswordExpiredException(result)
        if result['number'] == 1012: return LDAPAuthenticationFailedException(result)
        return UnknownSuiteException(result)

class NoErrorException(SuiteException): # Number 0
    pass

class InvalidLoginException(SuiteException): # Number 10
    pass

class InvalidSessionIDException(SuiteException): # Number 11
    pass

class UserNotConfiguredException(SuiteException): # Number 12
    pass

class InvalidPortalClientException(SuiteException): # Number 13
    pass

class ModuleDoesNotExistException(SuiteException): # Number 20
    pass

class FileDoesNotExistException(SuiteException): # Number 21
    pass

class ModuleNotSupportedException(SuiteException): # Number 30
    pass

class RelationshipNotSupportedException(SuiteException): # Number 31
    pass

class AccessDeniedException(SuiteException): # Number 40
    pass

class DuplicateRecordsException(SuiteException): # Number 50
    pass

class NoRecordsException(SuiteException): # Number 51
    pass

class CannotAddOfflineClientException(SuiteException): # Number 52
    pass

class ClientDeactivatedException(SuiteException): # Number 53
    pass

class NumberOfSessionsExceededException(SuiteException): # Number 60
    pass

class UpgradeClientException(SuiteException): # Number 61
    pass

class AdminCredentialsRequiredException(SuiteException): # Number 70
    pass

class CustomFieldTypeNotSupportedException(SuiteException): # Number 80
    pass

class CustomFieldPropertyNotSuppliedException(SuiteException): # Number 81
    pass

class ResourceManagementErrorException(SuiteException): # Number 90
    pass

class InvalidCallErrorException(SuiteException): # Number 1000
    pass

class InvalidDataFormatException(SuiteException): # Number 1001
    pass

class InvalidSetCampaignMergeDataException(SuiteException): # Number 1005
    pass

class PasswordExpiredException(SuiteException): # Number 1009
    pass

class LDAPAuthenticationFailedException(SuiteException): # Number 1012
    pass

class UnknownSuiteException(SuiteException): # Number 1012
    pass
