function (doc, old, ctx) {
    if(doc.type && doc.type == "contact") {
        if(!doc.name) {
            throw({forbidden: "name required"})
        }
        if(!doc.email) {
            throw({forbidden: "email required"})           
        }
        var re = /\S+@\S+\.\S+/;
        if(!re.test(doc.email)) {
            throw({forbidden: "not an email"})        
        }
    }
}