include ../_config.mk

deploy: advcrud.zip package.done bind.done validate.done index.done
	wsk action update advcrud/main advcrud.zip -p db advcruddb --kind python:3 --web true
	wsk action get advcrud/main --url

bind.done: 
	wsk package bind /whisk.system/cloudant advcruddb \
	-p username "$(CLOUDANT_USER)" \
    -p password "$(CLOUDANT_PASS)" \
    -p host "$(CLOUDANT_USER).cloudant.com" \
    -p dbname advcruddb
	-wsk action invoke advcruddb/create-database -r
	touch bind.done

package.done:
	wsk package create advcrud
	touch package.done

advcrud.zip: *.py
	zip advcrud.zip *.py

_validate.json: validate.js
	jq -n --rawfile file validate.js \
	'{ "doc":{ "_id": "_design/validate", "validate_doc_update":$$file} }' \
	>_validate.json

_index.json: index.json
	jq -n --slurpfile index index.json '{"index": $$index[0]}' >_index.json

validate.done: _validate.json
	! test -e validate.done
	wsk action invoke advcruddb/create-document -P  _validate.json -r | tee validate.done

index.done: _index.json
	wsk action invoke advcruddb/create-query-index -P _index.json -r | tee index.done
	
clean:
	-wsk action invoke advcruddb/delete-database
	-wsk action delete advcrud/main
	-wsk package delete advcrud 
	-wsk package delete advcruddb
	-rm bind.done
	-rm package.done
	-rm validate.done
	-rm index.done
	-rm advcrud.zip


test: bind.done
	python3 view.py
	python3 control.py
	python3 model.py
	python3 __main__.py

.PHONY: deploy clean test
