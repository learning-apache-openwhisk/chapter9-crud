import control
import model
def main(args):
    model.init(args["db"], "contact", 2)
    return control.main(args)
 
if __name__ == "__main__":
    import json, sys, rest
    rest.load_props()
    args = json.loads(sys.argv[1]) if len(sys.argv)>1 else {}   
    print(json.dumps(main(args)))           
