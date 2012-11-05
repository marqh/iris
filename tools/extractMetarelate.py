# (C) British Crown Copyright 2010 - 2012, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.

import metocean.queries as moq
import metocean.fuseki as fuseki

header = '''# (C) British Crown Copyright 2010 - 2012, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.

# DO NOT EDIT: AUTO-GENERATED RULES

import collections

CFname = collections.namedtuple('CFname', ['cfname', 'units'])

STASH_TO_CF = {
'''

footer = '''
}
'''

with fuseki.FusekiServer() as fu:

    mappings = moq.fast_mapping_by_link(False,False,True)
    cflinks = moq.get_cflinks(None,True)
    cflinks = {cflink['s']:cflink for cflink in cflinks}
    for amap in mappings:
        for key in amap.keys():
            if key in ['cflinks','griblinks','umlinks']:
                amap[key] = amap[key].split('&')
            if key == 'cflinks':
                amap['cflinks'] = [cflinks[cflink] for cflink in amap['cflinks']]


with open('../lib/iris/fileformats/um_cf_map.py', 'w') as umcf:
    umcf.write(header)
    #write STASH_TO_CF
    for amap in mappings:
        if amap.has_key('umlinks') and amap.has_key('cflinks'):
            umlinks = amap['umlinks']
            #there should be one or zero STASH codes in a mapping entry (never lots)
            stashlinks = [umlink for umlink in umlinks if umlink.startswith('http://reference.metoffice.gov.uk/data/stash/')]
            if len(stashlinks) == 1:
                stashcode = stashlinks[0].split('/')[-2]
                version = stashlinks[0].split('/')[-1]
            #there should always be one or zero Fields in a mapping entry
            cflinks = amap['cflinks']
            cffield = [cflink for cflink in cflinks if cflink.has_key('type') and cflink['type'] == 'Field']
            if len(cffield) == 1:
                cffield = cffield[0]
                s_n = cffield.get('standard_name', None)
                if s_n:
                    s_n = s_n.split('/')[-1]
                units = cffield.get('units',None)
                l_n = cffield.get('long_name', None)
                umcf.write('''    "%s/%s" : CFname(cfname="%s", units="%s"),''' % (stashcode, version, s_n, units) + '\n' )
                
    umcf.write(footer)




