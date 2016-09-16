import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


# /blog will display 5 newest blog posts
# /newpost will submit a new blog - after submitting you go back to main page
# 	- Errors for blank title or blog

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **parems):
		t = jinja_env.get_template(template)
		return t.render(parems)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
	title = db.StringProperty(required = True)
	blog = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **parems):
		t = jinja_env.get_template(template)
		return t.render(parems)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def get(self, id):
		blog_id = int(id)
		test = Blog.get_by_id(blog_id)
		self.render("display.html", title = test.title, blog = test.blog)


    	# if blog_post:
     #        self.render("b.html", blog=blog_post)
     #    else:
     #        error= "No blog found!"
     #        self.render("b.html", error=error)

class MainPage(Handler):
	def render_front(self,title="",blog="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

		self.render("ba.html", title = title, blog = blog, error = error, blogs = blogs)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		blog = self.request.get("blog")

		if title and blog:
			a = Blog(title = title, blog = blog)
			a.put()

			aID = str(a.key().id())

			self.redirect("/blog/" + aID)

		elif not title and blog:
			error = "We need a title!"
			self.render_front(title, blog, error)
		elif not blog and title:
			error = "We need a blog!"
			self.render_front(title, blog, error)
		else:
			error = "We need a title and blog!"
			self.render_front(title, blog, error)

class BlogPage(Handler):
	def render_front(self,title="",blog="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")

		self.render("b.html", blogs = blogs)

	def get(self):
		self.render_front()


class NewPost(Handler):
	def render_front(self,title="",blog="", error=""):

		self.render("ba.html", title = title, blog = blog, error = error)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		blog = self.request.get("blog")

		if title and blog:
			a = Blog(title = title, blog = blog)
			a.put()

			self.redirect("/")
		elif not title and blog:
			error = "We need a title!"
			self.render_front(title, blog, error)
		elif not blog and title:
			error = "We need a blog!"
			self.render_front(title, blog, error)
		else:
			error = "We need a title and blog!"
			self.render_front(title, blog, error)

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/blog', BlogPage),
	('/newpost', NewPost),
	webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
	], debug = True)