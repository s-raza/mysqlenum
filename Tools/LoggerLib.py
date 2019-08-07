#!/usr/bin/python
# 
# Enumerate details of a MySQL database through a form field that is vulnerable to SQL injection 
# Copyright (C) 2019
# Salman Raza <raza.salman@gmail.com>
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

import colorlog
import logging

formatter = colorlog.ColoredFormatter(
    #"%(asctime)s %(log_color)s%(levelname)-8s %(name)s %(funcName)s()-%(lineno)s %(reset)s %(message)s",
    "%(asctime)s %(log_color)s%(levelname)-1s %(name)s %(reset)s %(message)s",
    datefmt='%d%b%y %I:%M:%S%p',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'white,bg_red',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

logger = colorlog.getLogger()

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


##Root logger logging level
logger.setLevel(logging.INFO)


