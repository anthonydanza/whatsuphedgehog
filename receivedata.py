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
from datetime import datetime

import logging

from google.appengine.ext import db

class DataPoint(db.Model):
	pin = db.IntegerProperty(required=True)
	isDigital = db.BooleanProperty(required=True)
	time = db.DateTimeProperty(required=True)
	value = db.FloatProperty(required=True) #speed, for wheel

class MainHandler(webapp.RequestHandler):
	def post(self):
		logging.info('At pin!')
		data=json.loads(self.request.get('data'))
		logging.info(str(data))
		for pininfo,vals in data['pins']:
			try:
				oldtime,oldval=vals[0]
				for t,v in vals[2::2]:
					newspeed=0.88/(t-oldtime) #0.14m * 2pi = 0.88
					oldtime=t
					d = DataPoint(pin=pininfo[0],isDigital=bool(pininfo[1]),time=datetime.fromtimestamp(t),value=newspeed)
					logging.info(str(newspeed))
					d.put()
			except:
				logging.error('list of data received had no data!')
		# 1: low-high
		# 0: high-low
		
		#e = Employee(name="",
		#	role="manager",
		#	account=users.get_current_user())
		#e.hire_date = datetime.datetime.now().date()
		#e.put()
    	

def main():
    application = webapp.WSGIApplication([('/pin', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
