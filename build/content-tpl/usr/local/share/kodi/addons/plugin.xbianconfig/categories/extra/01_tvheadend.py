from __future__ import print_function
from builtins import map

try:
    import itertools.ifilter as filter
except ImportError:
    pass

import re

from resources.lib.xbmcguie.xbmcContainer import *
from resources.lib.xbmcguie.xbmcControl import *
from resources.lib.xbmcguie.tag import Tag
from resources.lib.xbmcguie.category import Setting
from resources.lib.xbianconfig import xbianConfig

import resources.lib.translation
_ = resources.lib.translation.language.gettext

class TVHeadend(Setting):
    CONTROL = CategoryLabelControl(Tag('label','TVheadend'))

class enableTVHeadend(Setting):
    CONTROL = RadioButtonControl(Tag('label',_('Enable TVheadend')))

    def onInit(self):
        self.cfgfile = '/etc/default/tvheadend'
        self.setting = 'TVH_ENABLED'
        self.exist = False

    def getUserValue(self):
        self.DIALOGHEADER = _('Enable TVheadend')
        return str(self.getControlValue())

    def setControlValue(self,value):
        if value == '1' or value == 'True':
            value = True
        else:
            value = False
        self.control.setValue(value)

    def getXbianValue(self):
        with open(self.cfgfile,'r') as f:
            mat = list(filter(lambda x: re.match('%s=.*'%self.setting,x),f.readlines()))
        if mat:
            self.exist = True
            return re.search('[01]',mat[0]).group()[0]
        return 0

    def setXbianValue(self,value):
        if value == True or value == 'True':
            value = '1'
        elif value == False or value == 'False':
            value = '0'
        if self.exist and value in ('0','1'):
            #replace
            def replace(x):
                if re.match('%s=.*'%self.setting,x):
                    return re.sub('[01]',value,x,1)
                else:
                    return x
            with open(self.cfgfile, "r") as f:
                data = list(map(replace,open(self.cfgfile,'r').readlines()))
            with open(self.cfgfile, "w") as f:
                f.writelines(data)
        elif value in ('0','1'):
            with open(self.cfgfile, "a") as f:
                f.write('%s=%s\n'%(self.setting,value))
        else:
            return False
        xbianConfig('services', '%s' % ('start' if value == '1' else 'stop'), 'tvheadend')
        self.OKTEXT = _('TVheadend has been %s now') % (_('started') if value == '1' else _('stopped'))
        return True

settings = [TVHeadend, enableTVHeadend]
