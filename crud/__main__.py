import crud
import website

def main(args):
    crud.init("demodb", "contact")
    return website.main(args)

if __name__ == "__main__":
    import json, sys, rest
    rest.load_props()
    args = json.loads(sys.argv[1]) if len(sys.argv)>1 else {}   
    print(json.dumps(main(args)))           
