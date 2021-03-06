import model
import rest
db = "cruddb"
dtype = "test"

def init(_db, _dtype):
  global db, dtype
  db = _db
  dtype = _dtype

def insert(args, id=None):
  doc = args.copy()
  doc["type"] = dtype
  if id:
    doc["_id"] = id
  ret = rest.whisk_invoke("%s/create-document" % db, {"doc": doc})
  if "ok" in ret:
    return "%s:%s" % (ret["id"], ret["rev"])
  return None

def find(id=None):
  query = { "selector": {"type": dtype} }
  if id:
    query["selector"]["_id"] = id.split(":")[0]
  ret = rest.whisk_invoke("%s/exec-query-find" % db, {"query": query})
  for rec in ret["docs"]:
    rec["id"] = "%s:%s" % (rec["_id"], rec["_rev"])
  return ret

def update(args):
  doc = args.copy()
  a = doc["id"].split(":")
  del doc["id"]
  doc["_id"] = a[0]
  doc["_rev"] = a[1]
  doc["type"] = dtype
  ret = rest.whisk_invoke("%s/update-document" % db, {"doc": doc})
  if "ok" in ret:
    return "%s:%s" % (ret["id"], ret["rev"])
  return None

def delete(id):
  a = id.split(":")
  if len(a) == 1:                                 
    res = find(id) 
    if res["docs"]:
      a = res["docs"][0]["id"].split(":")
    else:
     return {"error": "not found" }
  params = { 
    "docid": a[0],
    "docrev": a[1]
  }
  ret = rest.whisk_invoke("%s/delete-document" % db, params)
  return ret

# import importlib ; importlib.reload(rest);importlib.reload(crud) ; crud.init("demodb","test")
def test():
    """
    >>> import rest,model,json
    >>> rest.load_props()
    >>> model.init("cruddb","test")
    >>> args = {"name": "Mike", "email":"msciab@gmail.com"}
    >>> x = model.insert(args)
    >>> res = model.find()
    >>> rec = res["docs"][0]
    >>> print(rec["name"])
    Mike
    >>> rec["name"] = "Michele"
    >>> id1 = model.update(rec)
    >>> res = model.find()
    >>> fnd = res["docs"][0]
    >>> print(fnd["name"])
    Michele
    >>> args = {"name":"Miri","email":"miri@sc.com"}
    >>> nid = "test-miri"
    >>> x = model.insert(args, nid)
    >>> res = model.find(nid)
    >>> snd = res["docs"][0]
    >>> print(snd["name"])
    Miri
    >>> x = model.delete(id1) 
    >>> x = model.delete(nid)
    >>> res = model.find()
    >>> print(res["docs"])
    []
    """
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
