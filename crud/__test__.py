from __future__ import print_function
import re

def extract_id(text):
    """
    from __test__ import extract_id
    text = '<input name="id" value="123">\n<input name="id" value="456">'
    print(extract_id(text))
    >>> from __test__ import extract_id
    >>> text = '<input name="id" value="123">\n<input name="id" value="456">'
    >>> print(extract_id(text))
    <input name="id" value="-id-here-">
    <input name="id" value="-id-here-">
    123
    >>> print(extract_id("nothing"))
    None
    """
    pattern = re.compile('name="id" value="(.*?)"')
    replace = 'name="id" value="-id-here-"'
    m = pattern.search(text)
    if m:
        print(re.sub(pattern, replace, text))
        return m.group(1)
    return None

  
def test_website():
    x = """
    import rest,crud,website,json
    rest.load_props()
    crud.db = "demodb"
    crud.init("demodb","contact")
    print(website.form(website.empty))
    print(website.form({"id":"abc","name":"Mike","email":"a@b.c"}))
    docs = [{"id":"1","name":"Mike", "email":"a@b.c"}]
    print(website.rows(docs))
    """

def test_main():
    x = """
    import rest,crud,website,json
    from __test__ import extract_id
    rest.load_props()
    crud.db = "demodb"
    crud.dtype = "test"
    print(website.main({})["body"])
    website.main({"op":"save","name":"Mike","email":"m@s.c"})
    id = extract_id(website.main({})["body"])
    args = {"op":"edit", "id": id}
    website.main(args)
    x = website.main({"op":"save", "id": id, "name":"Michele","email":"m2@s.c"})
    id = extract_id(website.main({})["body"])
    website.main({"op":"delete", "id": id})
    id = extract_id(website.main({})["body"])
    print(id)
    """
