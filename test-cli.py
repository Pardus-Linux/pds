#!/usr/bin/python
# -*- coding: utf-8 -*-

from pds import Pds
import time

a=time.time()
b=Pds()

print 'Current Desktop Environment         :', b.session.Name
print 'Current Desktop Environment Version :', b.session.Version
print 'I18n test result                    :',b.i18n('test')
print 'It took                             :',time.time()-a

