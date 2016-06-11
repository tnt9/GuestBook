from google.appengine.ext import ndb


class Guestbook(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.TextProperty(required=True)
    nastanek =ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)
