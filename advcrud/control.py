import model
import view


def form_parse(args):
    """
>>> import control
>>> body = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1mNDNkYjAzNTQyNmQzYmZjDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InBob3RvIjsgZmlsZW5hbWU9ImhlbGxvLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpoZWxsbwoNCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tZjQzZGIwMzU0MjZkM2JmYw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJuYW1lIg0KDQpoZWxsbw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1mNDNkYjAzNTQyNmQzYmZjDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImVtYWlsIg0KDQpoQGwubw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1mNDNkYjAzNTQyNmQzYmZjLS0NCg=="
>>> ctype = "multipart/form-data; boundary=------------------------f43db035426d3bfc"
>>> args = { "__ow_body": body, "__ow_headers": { "content-type": ctype}, "__ow_method": "post" }
>>> fields, files = control.form_parse(args)
>>> print("%s %s" % (fields["name"], fields["email"]))
hello h@l.o
>>> photo = files["photo"].file.read()
>>> photo_type = files["photo"].content_type
>>> print("%s %s" % (photo, photo_type))
b'hello\n' text/plain
"""
    import io, base64, multipart
    body = args.get("__ow_body")
    method = args["__ow_method"]
    ctype = args["__ow_headers"]["content-type"]
    input = io.BytesIO(base64.b64decode(body))
    env = {
        'REQUEST_METHOD': method, 
        'CONTENT_TYPE': ctype, 
        'wsgi.input': input
    }
    return multipart.parse_form_data(env, strict=True, charset='utf-8')

# fill a form with values from args
def fill(fields, files):
  res = { }
  if "id" in fields: res["id"]=fields["id"]
  res["name"] = fields.get("name", "")
  res["email"] = fields.get("email", "")
  if "photo" in files:
      from base64 import b64encode
      photo = files["photo"].file.read()
      res["photo"] = b64encode(photo).decode('ascii') 
      res["photo_mime"] = files["photo"].content_type
  return res


def main(args):
    r"""
  >>> import model, control, rest
  >>> rest.load_props()
  >>> from bs4 import BeautifulSoup as BS
  >>> docs = [{"id":"1","name":"Mike","email":"m@s.c"}]
  >>> model.find = lambda bookmark=None: {"docs":docs}
  >>> res = control.main({"__ow_method":"get"})
  >>> html = BS(res["body"], "lxml")
  >>> print(html.find("tbody"))
  <tbody>
  <tr>
  <td scope="row">
  <input name="id" type="radio" value="1"/>
  </td>
  <td>Mike</td>
  <td>m@s.c</td>
  <td></td>
  </tr>
  </tbody>
  >>> res = control.main({"__ow_method":"get", "op":"new"})
  >>> inp = BS(res["body"], "lxml").find_all("input")
  >>> print(*inp, sep="\n")
  <input class="form-control" id="photo" name="photo" type="file"/>
  <input class="form-control" id="name" name="name" type="text" value=""/>
  <input class="form-control" id="email" name="email" type="email" value=""/>
  >>> res = control.main({"__ow_method":"get", "op":"edit", "id":"1"})
  >>> inp = BS(res["body"], "lxml").find_all("input")
  >>> print(*inp, sep="\n")
  <input name="id" type="hidden" value="1"/>
  <input class="form-control" id="photo" name="photo" type="file"/>
  <input class="form-control" id="name" name="name" type="text" value="Mike"/>
  <input class="form-control" id="email" name="email" type="email" value="m@s.c"/>
  >>> model.insert = control.inspect
  >>> ctype = "multipart/form-data; boundary=------------------------ff26122a2a4ed25b"
  >>> body = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1mZjI2MTIyYTJhNGVkMjViDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9Im5hbWUiDQoNCmhlbGxvDQotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLWZmMjYxMjJhMmE0ZWQyNWINCkNvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsgbmFtZT0iZW1haWwiDQoNCmhAbC5vDQotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLWZmMjYxMjJhMmE0ZWQyNWItLQ0K"
  >>> args = {"__ow_method":"post", "__ow_body":body, "__ow_headers": {"content-type": ctype} }
  >>> _ = control.main(args)
  >>> print(control.spy)
  {'name': 'Miri', 'email': 'm@d.g'}
  >>> model.update = control.inspect
  >>> args = {"op":"save", "id": "1", "name":"Mike","email":"m@s.c"}
  >>> x = control.main(args)
  >>> print(control.spy)
  {'id': '1', 'name': 'Mike', 'email': 'm@s.c'}
    """
    # extract photo
    if "__ow_path" in args:
      path = args["__ow_path"]
      if len(path) > 1:
        doc = model.find(path[1:])["docs"][0]
        return {
          "body": doc["photo"],
          "headers": {
            "Content-Type": doc["photo_mime"]
          } 
        }
    # post data
    if "__ow_body" in args:
      fields, files = form_parse(args)
      if "id" in fields:
        model.update(fill(fields, files))
      else:
        model.insert(fill(fields, files))
    
    # handle other ops
    op = ""
    if args["__ow_method"] == "get":
      op = args.get("op")
    if  op == "new":
        body = view.form(fill({},{}))
        return { "body": view.wrap(body) }
    if op == "edit" and "id" in args:
      res = model.find(args["id"])
      rec = res["docs"][0]
      body = view.form(rec)
      return { "body": view.wrap(body) }
    if op == "delete" and "id" in args: 
        model.delete(args["id"])
    
    # paginated rendering 
    curr = args.get("bookmark")
    query = model.find(bookmark=curr)
    data = query["docs"]
    next = ""
    if len(data) == model.find_limit:
      next = query.get("bookmark")
    body = view.table(data, next, model.last_error)
    if model.last_error:
      model.last_error = None
    return { "body": view.wrap(body) }

# test support
spy = {}
def inspect(x): 
   global spy 
   spy = x.copy()

# integration test
def test_save_load():
  """
>>> import model, control, rest
>>> model.init("advcruddb", "test", 2)
>>> rest.load_props()
>>> model.clean()
>>> body = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3DQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InBob3RvIjsgZmlsZW5hbWU9ImhlbGxvLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpoZWxsbwoNCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tOTU3NDJhMGJiZDhhOTI1Nw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJuYW1lIg0KDQpoZWxsbw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3DQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImVtYWlsIg0KDQpoQGwubw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3LS0NCg=="
>>> ctype = "multipart/form-data; boundary=------------------------95742a0bbd8a9257"
>>> args = { "__ow_body": body, "__ow_headers": { "content-type": ctype}, "__ow_method": "post" }
>>> _ = control.main(args)
>>> _id = model.find()["docs"][0]["_id"]
>>> args = { "__ow_path": "/"+_id}
>>> control.main(args)
{'body': 'aGVsbG8K', 'headers': {'Content-Type': 'text/plain'}}
  """
  pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
