import sys, os, os.path
import requests
import json
 
def load_props():
    with open(os.path.expanduser("~/.wskprops"), "r") as f:
        for line in f.readlines():
            [k, v] = line.strip().split("=")
            if k == "APIHOST": os.environ["__OW_API_HOST"] = "https://%s:443" % v
            if k == "AUTH": os.environ["__OW_API_KEY"] = v
            if k == "NAMESPACE": os.environ["__OW_NAMESPACE"] = v

def url(operation):
    return "%s/api/v1/namespaces/%s/%s" % (
        os.environ["__OW_API_HOST"],
        os.environ["__OW_NAMESPACE"],
        operation
    )

def auth():
    up = os.environ['__OW_API_KEY'].split(":")
    return (up[0], up[1])

def whisk_invoke(action, args,  
                 blocking=True, result=True):
    invoke = "actions/%s?blocking=%d&result=%d" % (
        action, blocking, result)
    resp = requests.post(
        url=url(invoke), 
        auth=auth(),
        json=args
    )
    return json.loads(resp.text)

def whisk_trigger(trigger, args):
    invoke = url("triggers/%s" % trigger)
    resp = requests.post(
        url=invoke, 
        auth=auth(),
        json=args
    )
    return json.loads(resp.text)


def whisk_get(operation):
    return requests.get(
         url=url(operation), 
         auth=auth())