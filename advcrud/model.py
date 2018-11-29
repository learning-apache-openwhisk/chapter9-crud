import model
import rest
db = "demodb"
dtype = "contact"
last_error = None
find_limit = 10

def init(_db, _dtype, _find_limit):
  global db, dtype, find_limit
  db = _db
  dtype = _dtype
  find_limit = _find_limit

def insert(args, id=None):
  doc = args.copy()
  doc["type"] = dtype
  if id:
    doc["_id"] = id
  ret = rest.whisk_invoke("%s/create-document" % db, {"doc": doc})
  global last_error
  if "ok" in ret:
    last_error = None
    return "%s:%s" % (ret["id"], ret["rev"])
  if "error" in ret:
    last_error = ret["error"]["message"]
  return None

def find(id=None, bookmark=None):
  query = { 
    "selector": {"type": dtype}, 
    "limit": find_limit,
    "sort": [{"name": "asc"}]  
  }
  if bookmark:
    query["bookmark"] = bookmark
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
  global last_error
  if "ok" in ret:
    last_error = None
    return "%s:%s" % (ret["id"], ret["rev"])
  if "error" in ret:
    last_error = ret["error"]["message"]
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
    >>> model.init("advcruddb","test", 2)
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

    >>> args = {"name":"Vin","email":"v@i.n"}
    >>> model.insert(args, "test-vin")
    >>> bk = model.find()["bookmark"]
    >>> model.find(bookmark=bk)["docs"][0]["name"]
    Vin

    args = {"name":"Vin1","email":"v1@i.n"}
    model.insert(args, "test-vin1")
    args = {"name":"Zen","email":"z@e.n"}
    model.insert(args, "test-zen")

    
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
