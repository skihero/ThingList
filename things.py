things/things.py
#!/usr/bin/env python
# Kish
# Task list keeper
#
import cgi
import datetime
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Task(db.Model):
        author = db.UserProperty()
        subject = db.StringProperty(multiline=True)
        content = db.StringProperty(multiline=True)
        status = db.StringProperty(multiline=True)
        date = db.DateTimeProperty(auto_now_add=True)
        def prints(self):
           print self.author
           print self.subject
           print self.content
           print self.date

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""<html><head>
                             <script type="text/css">
                             body{
                                 background-color: #FF0000;
                                 }
                             </script>
                             </head>
                             <body>""")
    tasks = db.GqlQuery("SELECT * "
                        "FROM Task "
                        "ORDER BY date DESC LIMIT 50 ")
    #print tasks
    suc = "id=body "
    for task in tasks:
      self.response.out.write("""<div %s >What %s  Stat %s  </div> <div>More %s </div>
                                """ % (suc,
                                       cgi.escape(task.subject),
                                       cgi.escape(task.status),
                                       cgi.escape(task.content)
                                   ))
      if task.author:
         self.response.out.write(' <div><h6>Who %s</h6></div>' % task.author.nickname())
      else:
         self.response.out.write('<div><h6>Master</h6></div>')
    self.response.out.write("""
          <form action="/sign" method="post">
            <div>   <LABEL for="subject">Sub </LABEL> <textarea name="subject" rows="1" cols="60"></textarea></div>
            <div>   <LABEL for="content">Con </LABEL> <textarea name="content" rows="3" cols="60"></textarea></div>
            <div>   <LABEL for="status">Stat </LABEL><textarea name="status" rows="1" cols="20"></textarea></div>
            <div><input type="submit" value="Add a task"></div>
          </form>
        </body>
      </html>""")

class TaskList(webapp.RequestHandler):
  def post(self):
    task = Task()
    if users.get_current_user():
      task.author = users.get_current_user()
    task.content = self.request.get('content')
    task.subject = self.request.get('subject')
    task.status= self.request.get('status')
    task.put()
    self.redirect('/')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/sign', TaskList)
], debug=True)

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
 

