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


class SeznamVnosovHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.izbrisan == False).order(Guestbook.priimek).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil.html", params=params)


class PosamezenVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)


class UrediVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("uredi_vnos.html", params=params)

    def post(self, guestbook_id):
        ime = self.request.get("ime")
        priimek = self.request.get("priimek")
        email = self.request.get("email")
        message = self.request.get("message")
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        sporocilo.ime = ime
        sporocilo.priimek = priimek
        sporocilo.email = email
        sporocilo.message = message
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")


class IzbrisiVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("izbrisi_vnos.html", params=params)

    def post(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        sporocilo.izbrisan = True
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")


class SeznamIzbrisanihVnosovHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.izbrisan == True).order(Guestbook.priimek).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_izbrisanih_vnosov.html", params=params)


class PonovnoIzpisiVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("restore_vnos.html", params=params)

    def post(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        sporocilo.izbrisan = False
        sporocilo.put()
        return self.redirect_to("seznam-sporocil")


class DokoncnoIzpisiVnosHandler(BaseHandler):
    def get(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("dokoncni_delete_vnosa.html", params=params)

    def post(self, guestbook_id):
        sporocilo = Guestbook.get_by_id(int(guestbook_id))
        sporocilo.key.delete()
        return self.redirect_to("seznam-izbrisanih-vnosov")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos', VnosHandler),
    webapp2.Route('/seznam-sporocil', SeznamVnosovHandler, name="seznam-sporocil"),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>', PosamezenVnosHandler),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>/uredi', UrediVnosHandler),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>/izbrisi', IzbrisiVnosHandler),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>/restore', PonovnoIzpisiVnosHandler),
    webapp2.Route('/sporocilo/<guestbook_id:\d+>/delete', DokoncnoIzpisiVnosHandler),
    webapp2.Route('/seznam-izbrisanih-sporocil', SeznamIzbrisanihVnosovHandler, name="seznam-izbrisanih-vnosov"),
], debug=True)
