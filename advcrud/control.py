import model
import view

# fill a form with values from args
def fill(args):
  res = { }
  if "id" in args: res["id"]=args["id"]
  res["name"] = args.get("name", "")
  res["email"] = args.get("email", "")
  return res


def main(args):
    r"""
  >>> import model
  >>> import control
  >>> from bs4 import BeautifulSoup as BS
  >>> docs = [{"id":"test-mike","name":"Mike","email":"m@s.c"}]
  >>> model.find = lambda x=None: {"docs":docs}
  >>> res = control.main({})
  >>> html = BS(res["body"], "lxml")
  >>> print(html.find("tbody"))
  <tbody>
  <tr>
  <td scope="row">
  <input name="id" type="radio" value="1"/>
  </td>
  <td>Mike</td>
  <td>m@s.c</td>
  </tr>
  </tbody>
  >>> res = control.main({"op":"new"})
  >>> inp = BS(res["body"], "lxml").find_all("input")
  >>> print(*inp, sep="\n")
  <input name="op" type="hidden" value="save"/>
  <input class="form-control" id="name" name="name" type="text" value=""/>
  <input class="form-control" id="email" name="email" type="email" value=""/>
  >>> res = control.main({"op":"edit", "id":"1"})
  >>> inp = BS(res["body"], "lxml").find_all("input")
  >>> print(*inp, sep="\n")
  <input name="id" type="hidden" value="1"/>
  <input name="op" type="hidden" value="save"/>
  <input class="form-control" id="name" name="name" type="text" value="Mike"/>
  <input class="form-control" id="email" name="email" type="email" value="m@s.c"/>
  >>> model.insert = control.inspect
  >>> args = {"op":"save", "name":"Miri","email":"m@d.g"}
  >>> x = control.main(args)
  >>> print(control.spy)
  {'name': 'Miri', 'email': 'm@d.g'}
  >>> model.update = control.inspect
  >>> args = {"op":"save", "id": "1", "name":"Mike","email":"m@s.c"}
  >>> x = control.main(args)
  >>> print(control.spy)
  {'id': '1', 'name': 'Mike', 'email': 'm@s.c'}
    """
    op = args.get("op")
    if  op == "new":
        body = view.form(fill({}))
        return { "body": view.wrap(body) }
    if op == "edit" and "id" in args:
      res = model.find(args["id"])
      rec = res["docs"][0]
      body = view.form(rec)
      return { "body": view.wrap(body) }
    if op == "save":
      if "id" in args:
        model.update(fill(args))
      else:
        model.insert(fill(args))
    if op == "delete" and "id" in args: 
        model.delete(args["id"]) 
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
