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

    def __init__(self, config_file = "suitepy.ini"):
        if os.path.isabs(config_file):
            abs_path = config_file
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            abs_path = os.path.join(BASE_DIR, config_file)
        if os.path.isfile(abs_path):
            print("Loading config from file: " + abs_path)
            self.load_config_file(abs_path)
        else:
            print("Creating new config file on: " + abs_path)
            print("Please edit config file and rerun the application.")
            self.create_config_file(abs_path)
            exit(0)

    def load_config_file(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.url = config.get("SuiteCRM API Credentials", "url")
        self.username = config.get("SuiteCRM API Credentials", "username")
        self.password = config.get("SuiteCRM API Credentials", "password")
        self.application_name = config.get("SuiteCRM API Credentials", "application_name")
        self.verify_ssl = bool(config.get("SuiteCRM API Credentials", "verify_ssl"))

    def create_config_file(self, config_file):
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
