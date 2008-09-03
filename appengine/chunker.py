import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from gae import chunker

application = webapp.WSGIApplication([('.*', chunker.GaeChunkerHandler)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
    main()

