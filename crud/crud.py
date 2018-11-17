import crud
import rest

db = "demodb"
dtype = "contact"

def init(_db, _dtype):
  global db, dtype
  db = _db
  dtype = _dtype

def delete(id):
  a = id.split(":")
  if len(a) == 1:
    res = find(id)
    if res["docs"]:
      a = res["docs"][0]["id"].split(":")
  params = {
    "docid": a[0],
    "docrev": a[1]
  }
  ret = rest.whisk_invoke("%s/delete-document" % db, params)
  return ret

def update(args):
  doc = args.copy()
  a = doc["id"].split(":")
  del doc["id"]
  doc["_id"] = a[0]
  doc["_rev"] = a[1]
  doc["type"] = dtype
  ret = rest.whisk_invoke("%s/update-document" % db, {"doc": doc})
  return ret

def insert(args, id=None):
  doc = args.copy()
  doc["type"] = dtype
  if id:
    doc["_id"] = id
  ret = rest.whisk_invoke("%s/create-document" % db, {"doc": doc})
  return ret

def find(id=None):
  query = { "selector": {"type": dtype} }
  if id:
    query["selector"]["_id"] = id.split(":")[0]
  ret = rest.whisk_invoke("%s/exec-query-find" % db, {"query": query})
  for rec in ret["docs"]:
    rec["id"] = "%s:%s" % (rec["_id"], rec["_rev"])
  return ret

# import importlib ; importlib.reload(rest);importlib.reload(crud) ; crud.init("demodb","test")
def test():
    """
    >>> import rest,crud,json
    >>> rest.load_props()
    >>> crud.init("demodb","test")
    >>> args = {"name": "Mike", "email":"msciab@gmail.com"}
    >>> x = crud.insert(args)
    >>> res = crud.find()
    >>> rec = res["docs"][0]
    >>> print(rec["name"])
    Mike
    >>> id = rec["id"]
    >>> rec["name"] = "Michele"
    >>> x = crud.update(rec)
    >>> res = crud.find()
    >>> fnd = res["docs"][0]
    >>> id = fnd["id"]
    >>> print(fnd["name"])
    Michele
    >>> args = {"name":"Miri","email":"miri@sc.com"}
    >>> nid = "test-miri"
    >>> x = crud.insert(args, nid)
    >>> res = crud.find(nid)
    >>> snd = res["docs"][0]
    >>> print(snd["name"])
    Miri
    >>> x = crud.delete(id) 
    >>> x = crud.delete(nid)
    >>> res = crud.find()
    >>> print(res["docs"])
    []
    """
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
