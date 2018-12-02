import model
import os

BOOTSTRAP_CSS = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
BOOTSTRAP_JS = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
JQUERY = "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"

def wrap(body):
    """
    >>> import view
    >>> from bs4 import BeautifulSoup as BS
    >>> ht = BS(view.wrap("BODY"), "lxml")
    >>> print(ht.find_all("script")[0])
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    >>> print(ht.find_all("script")[1])
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    >>> print(ht.find_all("link")[0])
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
    >>> print(ht.body.div)
    <div class="container">BODY</div>
    """
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"> 
    <title>OpenWhisk Crud Demo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="%s">
    <script src="%s"></script>
    <script src="%s"></script>
  </head>
  <body>
   <div class="container">%s</div>
  </body>
</html>
""" % (BOOTSTRAP_CSS, JQUERY, BOOTSTRAP_JS, body)

def rows(docs):
  """
>>> import view, os
>>> from bs4 import BeautifulSoup as BS
>>> os.environ["__OW_ACTION_NAME"] = "/test/main"
>>> docs = [{"id":"1","name":"Mike", "email":"a@b.c"}, {"id":"2","name":"Miri", "email":"m@s.c", "photo":"xxx"}]
>>> ht = BS(view.rows(docs), "lxml")
>>> print(ht.body.tbody)
<tbody>
<tr>
<td scope="row">
<input name="id" type="radio" value="1"/>
</td>
<td>Mike</td>
<td>a@b.c</td>
<td></td>
</tr>
<tr>
<td scope="row">
<input name="id" type="radio" value="2"/>
</td>
<td>Miri</td>
<td>m@s.c</td>
<td><img src="/api/v1/web/test/main/2" width="200"/></td>
</tr>
</tbody>"""
  res = "<tbody>"
  for row in docs:
    img = ""
    if "photo" in row:
      action = os.environ["__OW_ACTION_NAME"]
      _id = row["id"].split(":")[0]
      url = "/api/v1/web%s/%s" % (action, _id)
      img = '<img width="200" src="%s">' % url
    res += """
 <tr>
  <td scope="row">
   <input name="id" value="%s" type="radio">
  </td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
 </tr>
""" % (row["id"], row["name"], row["email"], img)
  return res+"</tbody>"

def table(data, bookmark=None, error=None):
    """
    >>> from bs4 import BeautifulSoup as BS
    >>> import view
    >>> docs = [{"id":"3","name":"Max", "email":"m@a.x"}]
    >>> tb = BS(view.table(docs), "lxml")
    >>> print(tb.body.tbody)
    <tbody>
    <tr>
    <td scope="row">
    <input name="id" type="radio" value="3"/>
    </td>
    <td>Max</td>
    <td>m@a.x</td>
    <td></td>
    </tr>
    </tbody>
    >>> tb = BS(view.table([], bookmark="123", error="Error"), "lxml")
    >>> print(tb.find("div"))
    <div class="alert alert-danger" role="alert"><b>Error</b>: Error <br/>
    <a href="javascript:window.history.back()">Retry</a>
    </div>
    >>> print(tb.find_all("button")[-1])
    <button class="btn btn-default" name="bookmark" type="submit" value="123">More...</button>
    """
    res = ""
    if error:
      res += """
<div class="alert alert-danger" 
 role="alert"><b>Error</b>: %s <br>
 <a href="javascript:window.history.back()">Retry</a>
</div>""" % error
    res += """
<form method="get">
 <table class="table">
  <thead>
    <tr>
     <th scope="col">#</th>
     <th scope="col">Name</th>
     <th scope="col">Email</th>
     <th scope="col">Photo</th>
    </tr>
  </thead>"""
    res += rows(data)
    if bookmark:
      button = """
      <button name="bookmark" value="%s" type="submit" 
       class="btn btn-default">More...</button> 
       """ % bookmark
    else:
      button = """
      <button name="bookmark" value="" type="submit" 
       class="btn btn-default">Restart...</button>""" 
    res += """
  <tfoot>
    <tr>
     <td colspan="4" align="center">  
       <button name="op" value="new" type="submit" 
        class="btn btn-default">New Contact</button>
       <button name="op" value="edit" type="submit" 
       class="btn btn-default">Edit Contact</button>
       <button name="op" value="delete" type="submit" 
       class="btn btn-default">Delete Contact</button>
       %s   
     </td>
   <tr>
  </tfoot>
 </table>
</form>
""" % button
    return res

"""
>>> from bs4 import BeautifulSoup as BS
>>> import view
>>> args = { "id":"4", "name":"Laura", "email":"l@s.c"}
>>> fm = BS(view.form(args), "lxml")
>>> inp = [str(x) for x in fm.find_all("input")]
>>> print("\n".join(inp))
<input name="id" type="hidden" value="4"/>
<input class="form-control" id="name" name="name" type="text" value="Laura"/>
<input class="form-control" id="email" name="email" type="email" value="l@s.c"/>
"""
def form(args):
  id = ""
  if "id" in args:
    id = """<input type="hidden" 
      name="id" value="%s">""" % (args["id"])
  return """
<form method="post" enctype="multipart/form-data">
  %s
  <div class="form-group">
    <label for="photo">Photo (optional):</label>
    <input type="file" class="form-control" 
     id="photo" name="photo">
  </div>
  <div class="form-group">
    <label for="usr">Name:</label>
    <input type="text" class="form-control" 
     id="name" name="name" value="%s">
  </div>
  <div class="form-group">
    <label for="email">Email address:</label>
    <input type="email" class="form-control" 
     id="email" name="email" value="%s">
  </div>
  <button type="submit" 
   class="btn btn-default">Save</button>
</form>    
    """ % (id, args["name"], args["email"])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
