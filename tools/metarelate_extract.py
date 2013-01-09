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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris. If not, see <http://www.gnu.org/licenses/>.

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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris. If not, see <http://www.gnu.org/licenses/>.

# DO NOT EDIT: AUTO-GENERATED RULES

import collections

CFname = collections.namedtuple('CFname', ['cfname', 'unit'])

G2param = collections.namedtuple('G2param', ['edition', 'discipline', 'category', 'number'])


'''

enddict = '''
}
'''

def line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort()
    st = '\n'.join(sort_st)
    return st

def num_line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort(key=lambda str: int(str.split(':')[0].strip()))
    st = '\n'.join(sort_st)
    return st

    


# function to retrieve specified format to format mappings from
# the metarelate triplestore
#triple store must exist as defined by the FusekiServer instance
def retrieve_mappings(fu_p, source_format
        , target_format, nsources=None, ntargets=None,
        source_prefix=None, target_prefix=None):
    source_concepts = moq.get_concepts_by_format(fu_p, source_format,
                                                 source_prefix, nsources)
    sc = ['<%s>' % sc['concept'] for sc in source_concepts]
    target_concepts = moq.get_concepts_by_format(fu_p, target_format,
                                                 target_prefix, ntargets)
    tc = ['<%s>' % tc['concept'] for tc in target_concepts]
    st_mappings = moq.mappings_by_ordered_concept(fu_p, sc, tc)
    mappings = [st['map'] for st in st_mappings]
    st_maps = moq.mapping_by_id(fu_p, mappings)
    return st_maps


with fuseki.FusekiServer(3333) as fu_p:
#retrieve valid stash (one and only one) to cf (one and only one) mappings from
#the metarelate triplestore
    st_cf_maps = fu_p.retrieve_mappings('http://metarelate.net/metocean/format/um',
                'http://metarelate.net/metocean/format/cf',
                nsources=1, ntargets=1,
                source_prefix='http://reference.metoffice.gov.uk/def/um/stash/concept/')
                
    stash_list = []
    for mapping in st_cf_maps:
        stashcode = mapping['source_comps']
        if len(stashcode.split('&')) == 1:
            stashcode = stashcode.split('/')[-1]
        else:
            raise ValueError('multiple stash codes in mapping %s' % stashcode)
        
        cfitems = mapping['target_cfitems']
        if len(cfitems.split('&')) != 1:
            raise ValueError('multiple cf items codes in mapping %s' % cfitems)
        cfitems = cfitems.split('|')
        cfitems = dict([(cf.split(';')[0], cf.split(';')[1]) for cf in cfitems])
        st_name = cfitems['http://www.metarelate.net/predicates/CF.html#standard_name'].split('/')[-1]
        units = cfitems['http://www.metarelate.net/predicates/CF.html#units']
        stash_list.append('\t"%s" : CFname(cfname="%s", unit="%s"),' % (stashcode, st_name, units))
    stash_string = '\n'.join(stash_list)
    stash_string = line_sort(stash_string)
    stash_dict = 'STASH_TO_CF = {\n' + stash_string + enddict

#retrieve valid fieldcode (one and only one) to cf (one and only one) mappings from
#the metarelate triplestore
    fc_cf_maps = fu_p.retrieve_mappings('http://metarelate.net/metocean/format/um',
                'http://metarelate.net/metocean/format/cf',
                nsources=1, ntargets=1,
                source_prefix='http://reference.metoffice.gov.uk/def/um/fieldcode/')
    fc_list = []
    for mapping in fc_cf_maps:
        fieldcode = mapping['source_comps']
        if len(fieldcode.split('&')) == 1:
            fieldcode = fieldcode.split('/')[-1]
        else:
            raise ValueError('multiple stash codes in mapping %s' % stashcode)
        
        cfitems = mapping['target_cfitems']
        if len(cfitems.split('&')) != 1:
            raise ValueError('multiple cf items codes in mapping %s' % cfitems)
        cfitems = cfitems.split('|')
        cfitems = dict([(cf.split(';')[0], cf.split(';')[1]) for cf in cfitems])
        st_name = cfitems['http://www.metarelate.net/predicates/CF.html#standard_name'].split('/')[-1]
        units = cfitems['http://www.metarelate.net/predicates/CF.html#units']
        fc_list.append('\t%s : CFname(cfname="%s", unit="%s"),' % (fieldcode, st_name, units))
    fc_string = '\n'.join(fc_list)
    fc_string = num_line_sort(fc_string)
    fc_dict = 'LBFC_TO_CF = {\n' + fc_string + enddict
                

#retrieve valid fieldcode (one and only one) to cf (one and only one) mappings from
#the metarelate triplestore
    cf_fc_maps = fu_p.retrieve_mappings('http://metarelate.net/metocean/format/cf',
                'http://metarelate.net/metocean/format/um', nsources=1, ntargets=1,
                target_prefix='http://reference.metoffice.gov.uk/def/um/fieldcode/')
    cf_list = []
    for mapping in cf_fc_maps:
        cfitems = mapping['source_cfitems']
        if len(cfitems.split('&')) != 1:
            raise ValueError('multiple cf items codes in mapping %s' % cfitems)
        cfitems = cfitems.split('|')
        cfitems = dict([(cf.split(';')[0], cf.split(';')[1]) for cf in cfitems])
        fieldcode = mapping['target_comps']
        if len(fieldcode.split('&')) == 1:
            fieldcode = fieldcode.split('/')[-1]
        else:
            raise ValueError('multiple stash codes in mapping %s' % stashcode)
        st_name = cfitems['http://www.metarelate.net/predicates/CF.html#standard_name'].split('/')[-1]
        units = cfitems['http://www.metarelate.net/predicates/CF.html#units']
        cf_list.append('\tCFname(cfname="%s", unit="%s"): %s,' % (st_name, units, fieldcode))
    cf_string = '\n'.join(cf_list)
    cf_string = line_sort(cf_string)
    cf_dict = 'CF_TO_LBFC = {\n' + cf_string + enddict
                
#retrieve valid grib quartets (one and only one) to cf (one and only one) mappings from
#the metarelate triplestore
    g2p_cf_maps = fu_p.retrieve_mappings('http://metarelate.net/metocean/format/grib/2',
                'http://metarelate.net/metocean/format/cf', nsources=1, ntargets=1,
        source_prefix='http://codes.wmo.int/grib/2/codeflag/4.2')
    g2p_list = []
    for mapping in g2p_cf_maps:
        g2param = mapping['source_comps']
        if len(g2param.split('&')) == 1:
            g2param = {'edition': '2', 'discipline':g2param.split('/')[-3],'category':g2param.split('/')[-2], 'number':g2param.split('/')[-1]}
        else:
            raise ValueError('multiple grib2 parameter codes in mapping %s' % grparam)
        cfitems = mapping['target_cfitems']
        if len(cfitems.split('&')) != 1:
            raise ValueError('multiple cf items codes in mapping %s' % cfitems)
        cfitems = cfitems.split('|')
        cfitems = dict([(cf.split(';')[0], cf.split(';')[1]) for cf in cfitems])
        st_name = cfitems['http://www.metarelate.net/predicates/CF.html#standard_name'].split('/')[-1]
        units = cfitems['http://www.metarelate.net/predicates/CF.html#units']
        g2param.update({'sn':st_name, 'u':units})
        g2p_list.append('\tG2param(edition=%(edition)s, discipline=%(discipline)s, category=%(category)s, number=%(number)s) : CFname(cfname="%(sn)s", unit="%(u)s"),' % g2param)
    g2pcf_string = '\n'.join(g2p_list)
    g2pcf_string = line_sort(g2pcf_string)
    g2pcf_dict = 'GRIB2P_TO_CF = {\n' + g2pcf_string + enddict




    
with open('../lib/iris/fileformats/metarelate.py', 'w') as umcf:
    umcf.write(header)
    umcf.write(stash_dict)
    umcf.write('\n')
    umcf.write(fc_dict)
    umcf.write('\n')
    umcf.write(cf_dict)
    umcf.write('\n')
    umcf.write(g2pcf_dict)
    umcf.write('\n')
#     umcf.write(cfgrib_dict)
#     umcf.write('\n')


    
