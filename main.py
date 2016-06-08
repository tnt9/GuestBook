#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Guestbook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class VnosHandler(BaseHandler):
    def get(self):
        error = {"error": "Please fill in the message form."}
        return self.render_template("index.html", params=error)

    def post(self):
        ime = self.request.get("ime")
        if ime == "":
            ime = "N/A"
        priimek = self.request.get("priimek")
        if priimek == "":
            priimek = "N/A"
        email = self.request.get("email")
        message = self.request.get("message")

        if message:
            guestbook = Guestbook(ime=ime, priimek=priimek, email=email, message=message)
            guestbook.put()
            return self.write(guestbook)
        else:
            error = True
            return self.get()


class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query().fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil.html", params=params)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos', VnosHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>', PosameznoSporociloHandler),
], debug=True)
