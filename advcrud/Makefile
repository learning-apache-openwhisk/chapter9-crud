include ../_config.mk

deploy: advcrud.zip package.done bind.done validate.done
	wsk action update advcrud/main advcrud.zip -p db advcruddb --kind python:3 --web true
	wsk action get advcrud/main --url

bind.done: 
	wsk package bind /whisk.system/cloudant advcruddb \
	-p username "$(CLOUDANT_USER)" \
    -p password "$(CLOUDANT_PASS)" \
    -p host "$(CLOUDANT_USER).cloudant.com" \
    -p dbname advcruddb
	wsk action invoke advcruddb/create-database -r
	touch bind.done

package.done:
	wsk package create advcrud
	touch package.done

advcrud.zip: *.py
	zip advcrud.zip *.py

validate.json: validate.js
	jq -n --rawfile file validate.js \
	'{ "doc":{ "_id": "_design/validate", "validate_doc_update":$$file} }' \
	>validate.json

validate.done: validate.json
	! test -e validate.done
	wsk action invoke advcruddb/create-document -P  validate.json -r | tee validate.done

index.done:
	wsk action invoke advcruddb/create-query-index -P index.json -r | tee index.done
	

clean:
	-wsk action invoke advcruddb/delete-database
	-wsk action delete advcrud/main
	-wsk package delete advcrud 
	-wsk package delete advcruddb
	-rm bind.done
	-rm package.done
	-rm validate.done
	-rm advcrud.zip

test: bind.done
	python3 model.py
	python3 view.py
	python3 control.py

.PHONY: deploy clean test