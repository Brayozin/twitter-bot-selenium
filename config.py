# coding: utf-8
# TwitterSpottedPoster
# This file is part of the TwitterSpottedPosterSelenium distribution
# (https://github.com/Brayozin/TwitterSpottedPosterSelenium).
# Copyright (C) 2018 Matheus Horstmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
TWITTER_USERNAME = None
TWITTER_PASSWORD = None

try:
    with open('tweet_info.txt', 'r') as f:
        TWITTER_USERNAME = f.readline().rstrip()
        TWITTER_PASSWORD = f.readline().rstrip()

except FileNotFoundError:
    loger.error("File not found")
