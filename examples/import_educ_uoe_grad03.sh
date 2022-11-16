#!/usr/bin/env bash

./manage.py estat-import-bulk-meta educ_uoe_grad03 --indicator=~ict_grad --breakdown=sex --unit=unit --country=geo --period=time --delete-existing
./manage.py estat-enable-dim-values examples/educ_uoe_grad03.json
./manage.py estat-import-bulk-data educ_uoe_grad03
./manage.py import-with-query educ_uoe_grad03
