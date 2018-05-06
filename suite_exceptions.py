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


class SuiteException(Exception):
    """
    Base class for SuiteCRM requests exceptions.
    """

    def __init__(self, data):
        """
        Creates an exception with the provided data.

        :param dict[str, str] data: data that specifies the exception.
        """
        if data:
            self.name = data['name']
            self.description = data['description']
            self.number = data['number']
        else:
            self.name = "UnknownSuiteException"
            self.description = "Unknown error"
            self.number = 1012

    def __str__(self):
        return self.name + ': ' + self.description

    @staticmethod
    def get_suite_exception(result):
        """
        Get a SuiteException from the error specified in the result of a failed API call.

        :param ict[str, str] result: result of a failed API call.
        :return: the SuiteException that represents the error of result.
        :rtype: SuiteException
        """
        if not result:
            return UnknownSuiteException(result)
        if result['number'] == 0:
            return NoErrorException(result)
        if result['number'] == 10:
            return InvalidLoginException(result)
        if result['number'] == 11:
            return InvalidSessionIDException(result)
        if result['number'] == 12:
            return UserNotConfiguredException(result)
        if result['number'] == 20:
            return ModuleDoesNotExistException(result)
        if result['number'] == 21:
            return FileDoesNotExistException(result)
        if result['number'] == 30:
            return ModuleNotSupportedException(result)
        if result['number'] == 31:
            return RelationshipNotSupportedException(result)
        if result['number'] == 40:
            return AccessDeniedException(result)
        if result['number'] == 50:
            return DuplicateRecordsException(result)
        if result['number'] == 51:
            return NoRecordsException(result)
        if result['number'] == 52:
            return CannotAddOfflineClientException(result)
        if result['number'] == 53:
            return ClientDeactivatedException(result)
        if result['number'] == 60:
            return NumberOfSessionsExceededException(result)
        if result['number'] == 61:
            return UpgradeClientException(result)
        if result['number'] == 70:
            return AdminCredentialsRequiredException(result)
        if result['number'] == 80:
            return CustomFieldTypeNotSupportedException(result)
        if result['number'] == 81:
            return CustomFieldPropertyNotSuppliedException(result)
        if result['number'] == 90:
            return ResourceManagementErrorException(result)
        if result['number'] == 1000:
            return InvalidCallErrorException(result)
        if result['number'] == 1001:
            return InvalidDataFormatException(result)
        if result['number'] == 1005:
            return InvalidSetCampaignMergeDataException(result)
        if result['number'] == 1009:
            return PasswordExpiredException(result)
        if result['number'] == 1012:
            return LDAPAuthenticationFailedException(result)
        return UnknownSuiteException(result)


class NoErrorException(SuiteException):  # Number 0
    """
    Exception raised when no error is specified.
    """
    pass


class InvalidLoginException(SuiteException):  # Number 10
    """
    Exception raised when login is invalid.
    """
    pass


class InvalidSessionIDException(SuiteException):  # Number 11
    """
    Exception raised when session is not valid.
    """
    pass


class UserNotConfiguredException(SuiteException):  # Number 12
    """
    Exception raised when the authenticated user is not configured.
    """
    pass


class InvalidPortalClientException(SuiteException):  # Number 13
    """
    Exception raised when portal client does not have authorized access.
    """
    pass


class ModuleDoesNotExistException(SuiteException):  # Number 20
    """
    Exception raised when requested module is not available.
    """
    pass


class FileDoesNotExistException(SuiteException):  # Number 21
    """
    Exception raised when the requested file does not exist on the server.
    """
    pass


class ModuleNotSupportedException(SuiteException):  # Number 30
    """
    Exception raised when the requested action is not supported on a module.
    """
    pass


class RelationshipNotSupportedException(SuiteException):  # Number 31
    """
    Exception raised when a relationship is not supported on a module.
    """
    pass


class AccessDeniedException(SuiteException):  # Number 40
    """
    Exception raised when logged user does not have
    permission to perform the requested action.
    """
    pass


class DuplicateRecordsException(SuiteException):  # Number 50
    """
    Exception raised when duplicated records are found.
    """
    pass


class NoRecordsException(SuiteException):  # Number 51
    """
    Exception raised when no records are found.
    """
    pass


class CannotAddOfflineClientException(SuiteException):  # Number 52
    """
    Exception raised when is not possible to add offline client.
    """
    pass


class ClientDeactivatedException(SuiteException):  # Number 53
    """
    Exception raised when a client offline instance has been deactivated.
    """
    pass


class NumberOfSessionsExceededException(SuiteException):  # Number 60
    """
    Exception raised when max number of sessions is reached.
    """
    pass


class UpgradeClientException(SuiteException):  # Number 61
    """
    Exception raised when upgrading an offline client.
    """
    pass


class AdminCredentialsRequiredException(SuiteException):  # Number 70
    """
    Exception raised when the requested action can only be
    performed by an account with administrator rights.
    """
    pass


class CustomFieldTypeNotSupportedException(SuiteException):  # Number 80
    """
    Exception raised when a custom type is not supported.
    """
    pass


class CustomFieldPropertyNotSuppliedException(SuiteException):  # Number 81
    """
    Exception raised when one or more properties are
    missing for the supplied custom field type.
    """
    pass


class ResourceManagementErrorException(SuiteException):  # Number 90
    """
    Exception raised when the resource query limit specified in config.php
    has been exceeded during execution of the request.
    """
    pass


class InvalidCallErrorException(SuiteException):  # Number 1000
    """
    Exception raised when the requested call is invalid for the given module.
    """
    pass


class InvalidDataFormatException(SuiteException):  # Number 1001
    """
    Exception raised when the data of a request is invalid.
    """
    pass


class InvalidSetCampaignMergeDataException(SuiteException):  # Number 1005
    """
    Exception raised when merge action status will not be updated,
    because, campaign_id is null or no targets were selected.
    """
    pass


class LockoutReachedException(SuiteException):  # Number 1008
    """
    Exception raised when you have been locked out of the Sugar
    application and cannot log in using existing password.
    """
    pass


class PasswordExpiredException(SuiteException):  # Number 1009
    """
    Exception raised when password of logged user is expired.
    """
    pass


class LDAPAuthenticationFailedException(SuiteException):  # Number 1012
    """
    Exception raised when LDAP Authentication failed
    but supplied password was already encrypted.
    """
    pass


class UnknownSuiteException(SuiteException):
    """
    Exception raised when the request error is unknown.
    """
    pass
