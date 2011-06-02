#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson as json

import logging

from google.appengine.ext import db
from receivedata import DataPoint
import time

class MainHandler(webapp.RequestHandler):
	def get(self):
		q = db.GqlQuery("SELECT * FROM DataPoint WHERE pin = 0 AND time > DATETIME('2011-06-02 00:00:00')")
		poop = []
		for d in q:
			tupled = d.time.timetuple()
			timestamp = time.mktime(tupled)
			poop.append((timestamp,d.value))
		jsonresponse=json.dumps(poop)
		self.response.out.write(jsonresponse)

def main():
	application = webapp.WSGIApplication([('/tellmemore', MainHandler)],
                                         debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
