#!/usr/bin/env python3
import bsddb3
db = bsddb3.hashopen('berkeley.db', 'c')

key = b'test'
db[key] = 'testing'

print(db.get(key))


