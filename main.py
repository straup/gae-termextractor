#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

import termextractor

if __name__ == '__main__' :

  handlers = [
    ('/', termextractor.Main),
    ('/terms', termextractor.Terms),    
    ]
  
  application = webapp.WSGIApplication(handlers, debug=True)
  wsgiref.handlers.CGIHandler().run(application)
