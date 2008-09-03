import datetime
import logging
import types
import os
import re

from google.appengine.ext import webapp
from google.appengine.ext import db
#from google.appengine.api import datastore_types

from django.utils import simplejson

def status_ok(handler, entity):
    handler.response.set_status(200)
    _set_entity(handler, entity)

def status_created(handler, entity):
    handler.response.set_status(201)
    _set_entity(handler, entity)

def status_accepted(handler, entity):
    handler.response.set_status(202)
    _set_entity(handler, entity)

def status_not_found(handler, message):
    handler.error(404)
    logging.debug("Status Not Found: %s" % (message,))
    _set_entity(handler, { "error": message })

def status_bad_request(handler, message):
    handler.error(400)
    logging.debug("Status Bad Request: %s" % (message,))
    _set_entity(handler, { "error": message })

def _set_entity(handler, entity):
    if entity is None:
        entity = {}
#   handler.response.headers["Content-Type"] = "application/json"
    handler.response.headers["Content-Type"] = "text/plain"
    handler.response.out.write(simplejson.dumps(entity))

def empty(value):
    return not(bool(value) or value is 0)

def default(value, default=''):
    return value if not empty(value) else default

class GaeChunkerChunkMessage(db.Model):
    length = db.IntegerProperty(required = True)

class GaeChunkerChunk(db.Model):
    message=db.ReferenceProperty(GaeChunkerChunkMessage, required = True)
    rank=db.IntegerProperty(required = True)
    payload=db.TextProperty(required = True)

class GaeChunkerHandler(webapp.RequestHandler):
    def get(self):

        message_key = self.request.get("mk", None)
        chunk_rank = self.request.get("cr", None)
        payload = self.request.get("cp", None)
        callback = self.request.get("cb")

        chunk_message = None
        if empty( message_key ):
            message_length = long(self.request.get("ml", None))
            chunk_message = GaeChunkerChunkMessage(
                length = message_length
            )
            chunk_message.put()
            chunk_rank = 0
        else:
            chunk_message = GaeChunkerChunkMessage.get_by_id(long(message_key))

        chunk = GaeChunkerChunk(
            message = chunk_message,
            rank = int(chunk_rank),
            payload = payload,
        )
        chunk.put()

        query = db.GqlQuery("""\
SELECT * FROM GaeChunkerChunk WHERE message = :1 ORDER BY rank
""", chunk_message)

        if query.count() == chunk_message.length:
            message = ""
            for chunk in query:
                message += chunk.payload
            logging.info( message )
            

        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(callback + "(" + simplejson.dumps({
            "mk": chunk_message.key().id()
        }) + ")");
