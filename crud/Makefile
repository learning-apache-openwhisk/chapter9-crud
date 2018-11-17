include ../_config.mk

deploy: crud.zip package.done bind.done
	wsk action update crud/main crud.zip -p db cruddb --kind python:3 --web true
	wsk action get crud/main --url

bind.done: 
	wsk package bind /whisk.system/cloudant cruddb \
	-p username "$(CLOUDANT_USER)" \
    -p password "$(CLOUDANT_PASS)" \
    -p host "$(CLOUDANT_USER).cloudant.com" \
    -p dbname cruddb
	wsk action invoke cruddb/create-database -r
	touch bind.done

package.done:
	wsk package create crud
	touch package.done

crud.zip: *.py
	zip crud.zip *.py

clean:
	wsk action delete crud/main
	wsk package delete crud 
	wsk package delete cruddb
	rm bind.done

test:
	wsk action invoke crud/main -r

.PHONY: deploy clean test