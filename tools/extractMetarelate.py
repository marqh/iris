
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

CFname = collections.namedtuple('CFname', ['cfname', 'unit'])


'''

enddict = '''
}
'''

def line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort()
    lineb = '\n'
    st = lineb.join(sort_st)
    return st
    

with fuseki.FusekiServer(3333) as fu_p:
    '''connect to the local metarelate project via the
    Fuseki SPARQL interface and retrieve all of the current mappings'''
    mappings = moq.fast_mapping_by_link(fu_p, False, False)
    cflinks = moq.get_cflinks(fu_p, None)
    cflinks = {cflink['s']:cflink for cflink in cflinks}
    for amap in mappings:
        for key in amap.keys():
            if key in ['cflinks','griblinks','umlinks']:
                amap[key] = amap[key].split('&')
            if key == 'cflinks':
                amap['cflinks'] = [cflinks[cflink] for cflink in amap['cflinks']]


#loop through mappings and place translations in the appropriate dictionary 
stash_string = ''
fc_string = ''
cf_string = ''

for amap in mappings:
    if amap.has_key('umlinks') and amap.has_key('cflinks'):
        umlinks = amap['umlinks']
        #there should be one or zero STASH codes in a mapping entry (never lots)
        stashlinks = [umlink for umlink in umlinks if umlink.startswith('http://reference.metoffice.gov.uk/def/um/stash/concept/')]
        fclinks = [umlink for umlink in umlinks if umlink.startswith('http://reference.metoffice.gov.uk/def/um/fieldcode/')]
        if len(stashlinks) == 1:
            stashcode = stashlinks[0].split('/')[-1]
        elif len(fclinks) == 1:
            fcode = fclinks[0].split('/')[-1]
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
            if len(stashlinks) == 1 and amap['cfex'] == 'True' and amap['umim'] == 'True':
                stash_string += '''    "%s" : CFname(cfname="%s", unit="%s"),\n''' % (stashcode, s_n, units) 
            elif len(fclinks) == 1 and amap['cfex'] == 'True' and amap['umim'] == 'True':
                fc_string += '''    %s : CFname(cfname="%s", unit="%s"),\n''' % (fcode, s_n, units)
            elif len(fclinks) == 1 and amap['cfim'] == 'True' and amap['umex'] == 'True':
                cf_string += '''    CFname(cfname="%s", unit="%s") : %s,\n''' % (s_n, units, fcode)

stash_string = line_sort(stash_string)
fc_string = line_sort(fc_string)
cf_string = line_sort(cf_string)


#create dict strings as python source
stash_string = 'STASH_TO_CF = {\n' + stash_string + enddict
fc_string = 'LBFC_TO_CF = {\n' + fc_string + enddict
cf_string = 'CF_TO_LBFC = {\n' + cf_string + enddict



with open('../lib/iris/fileformats/um_cf_map.py', 'w') as umcf:
    umcf.write(header)
    umcf.write(stash_string)
    umcf.write('\n')
    umcf.write(fc_string)
    umcf.write('\n')
    umcf.write(cf_string)
    umcf.write('\n')
    
    










