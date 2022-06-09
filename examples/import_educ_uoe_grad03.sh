#!/usr/bin/env bash

django-admin estat-import-bulk-meta educ_uoe_grad03 --indicator=~ict_grad --breakdown=sex --unit=unit --country=geo --period=time --delete-existing
django-admin estat-enable-dim-values examples/educ_uoe_grad03.json
django-admin estat-import-bulk-data educ_uoe_grad03
django-admin import-with-query educ_uoe_grad03
