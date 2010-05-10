#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
a=time.time()
from pds import Pds

b=Pds('package-manager')

print 'Current Desktop Environment         :', b.session.Name
print 'Current Desktop Environment Version :', b.session.Version
print 'I18n test result for session        :', b.session.i18n('Package Manager')
print 'I18n test result for gettext        :', b.i18n('Package Manager')
print 'It took                             :', time.time()-a

