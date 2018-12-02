def main(args):
  import os
  args["env"] = { k: os.environ[k] for k in os.environ.keys() }
  return {
    "body": args,                            
    "status": "200",                        
    "headers": {                             
      "Content-Type": "application/json"    
    }
  }

