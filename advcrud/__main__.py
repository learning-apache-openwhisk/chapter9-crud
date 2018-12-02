import control
import model
def main(args):
    """
>>> import model, control, rest
>>> rest.load_props()
>>> model.init("advcruddb", "test", 2)
>>> _ = model.clean()
>>> body = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3DQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9InBob3RvIjsgZmlsZW5hbWU9ImhlbGxvLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpoZWxsbwoNCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tOTU3NDJhMGJiZDhhOTI1Nw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJuYW1lIg0KDQpoZWxsbw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3DQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImVtYWlsIg0KDQpoQGwubw0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTc0MmEwYmJkOGE5MjU3LS0NCg=="
>>> ctype = "multipart/form-data; boundary=------------------------95742a0bbd8a9257"
>>> args = { "__ow_body": body, "__ow_headers": { "content-type": ctype}, "__ow_method": "post" }
>>> _ = control.main(args)
>>> _id = model.find()["docs"][0]["_id"]
>>> args = { "__ow_path": "/"+_id}
>>> control.main(args)
{'body': 'aGVsbG8K', 'headers': {'Content-Type': 'text/plain'}}
    """
    model.init(args["db"], "contact", 2)
    return control.main(args)
 

if __name__ == "__main__":
    import doctest
    doctest.testmod()
