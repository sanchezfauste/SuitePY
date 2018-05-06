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

import ConfigParser
import os.path


class Config:
    """
    This class is used to read from a file the access credentials of a SuiteCRM API.

    This avoids the need of hard-code the credentials in the code.
    """

    def __init__(self, config_file="suitepy.ini"):
        """
        Creates a Config instance loading settings from specified file.

        :param str config_file: file from which the configuration will be read.
        """
        if os.path.isabs(config_file):
            abs_path = config_file
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.join(base_dir, config_file)
        if os.path.isfile(abs_path):
            print("Loading config from file: " + abs_path)
            self._load_config_file(abs_path)
        else:
            print("Creating new config file on: " + abs_path)
            print("Please edit config file and rerun the application.")
            self._create_config_file(abs_path)
            exit(0)

    def _load_config_file(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self._url = config.get("SuiteCRM API Credentials", "url")
        self._username = config.get("SuiteCRM API Credentials", "username")
        self._password = config.get("SuiteCRM API Credentials", "password")
        self._application_name = config.get("SuiteCRM API Credentials", "application_name")
        self._verify_ssl = bool(config.get("SuiteCRM API Credentials", "verify_ssl"))

    def _create_config_file(self, config_file):
        config_file = open(config_file, "w")
        config = ConfigParser.ConfigParser()
        config.add_section("SuiteCRM API Credentials")
        config.set("SuiteCRM API Credentials", "url", "https://example.org/service/v4_1/rest.php")
        config.set("SuiteCRM API Credentials", "username", "api")
        config.set("SuiteCRM API Credentials", "password", "123456")
        config.set("SuiteCRM API Credentials", "application_name", "SuitePY")
        config.set("SuiteCRM API Credentials", "verify_ssl", True)
        config.write(config_file)
        config_file.close()

    @property
    def url(self):
        """
        Get SuiteCRM REST API URL.

        :return: SuiteCRM REST API URL
        :rtype: str
        """
        return self._url

    @property
    def username(self):
        """
        Get login username.

        :return: login username.
        :rtype: str
        """
        return self._username

    @property
    def password(self):
        """
        Get login password.

        :return: login password.
        :rtype: str
        """
        return self._password

    @property
    def application_name(self):
        """
        Get application name used when login to SuiteCRM API.

        :return: application name.
        :rtype: str
        """
        return self._application_name

    @property
    def verify_ssl(self):
        """
        Specifies whether the SSL certificate should be verified.

        :return: True if SSL certificate must be verified, False otherwise.
        :rtype: bool
        """
        return self._verify_ssl
