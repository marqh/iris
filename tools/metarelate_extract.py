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

G2param = collections.namedtuple('G2param',
                                ['edition', 'discipline', 'category', 'number'])


'''

ENDDICT = '''
}
'''

def line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort()
    st = '\n'.join(sort_st)
    return st

def num_line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort(key=lambda str: int(str.split(':')[0].strip().replace('"','')))
    st = '\n'.join(sort_st)
    return st

OPEQ = '<http://www.openmath.org/cd/relation1.xhtml#eq>'

def get_stash(members, fu_p):
    """
    returns a STASH code if this is the only information present
    otherwise None
    """
    F3STASH = '<http://reference.metoffice.gov.uk/def/um/umdp/F3/stash>'
    STASHC = '<http://reference.metoffice.gov.uk/def/um/stash/concept/'
    if len(members) == 1:
        val = members[0].get('rdf:value')
        if val:
            stashval = val.startswith(STASHC)
        else:
            stashval = False
        name = members[0].get('mr:name')
        if name:
            stashname = name == F3STASH
        else:
            stashname = False
        operator = members[0].get('mr:operator')
        if operator:
            op_eq = operator = OPEQ
        else:
            op_eq = False
        if stashval and stashname and op_eq:
            label = moq.get_label(fu_p, val)
            if label == val:
                stashcode = None
            else:
                stashcode = label
        else:
            stashcode = None
    else:
        stashcode = None
    return stashcode

def get_fieldcode(members, fu_p):
    """
    returns a FIELD code if this is the only information present
    otherwise None
    """
    F3FIELD = '<http://reference.metoffice.gov.uk/def/um/umdp/F3/lbfc>'
    FIELDC = '<http://reference.metoffice.gov.uk/def/um/fieldcode/'
    if len(members) == 1:
        val = members[0].get('rdf:value')
        if val:
            fieldval = val.startswith(FIELDC)
        else:
            fieldval = False
        name = members[0].get('mr:name')
        if name:
            fieldname = name == F3FIELD
        else:
            fieldname = False
        operator = members[0].get('mr:operator')
        if operator:
            op_eq = operator = OPEQ
        else:
            op_eq = False
        if fieldval and fieldname and op_eq:
            label = moq.get_label(fu_p, val)
            if label == val:
                fieldcode = None
            else:
                fieldcode = label
        else:
            fieldcode = None
    else:
        fieldcode = None
    return fieldcode

def get_cf_sname(members, fu_p):
    """
    returns a reference for one cf_standard name and one unit for a Field,
    if this is the only information present
    otherwise None
    """
    sub_members = []
    for member in members:
        subm = member.get('skos:member')
        if subm:
            submembers.append(subm)
    if sub_members == []:
        define = {}

        for member in members:
            op = member.get('mr:operator')
            name = member.get('mr:name', '')
            value = member.get('rdf:value')
            if op and value and op == OPEQ:
                name_label = moq.get_label(fu_p, name)
                value_label = moq.get_label(fu_p, value)
                if not define.get(name_label):
                    define[name_label] = value_label
                
        required = set(('units', 'standard_name', 'type'))
        if set(define.keys()) == required:
            if not define['standard_name'].startswith('<'):
                cf_name = define
            else:
                cf_name = None
        else:
            ec = '''required keys missing from cfsn record {}'''
            # ec = ec.format(members)
            # print ec
            cf_name = None
    else:
        cf_name = None
    return cf_name

def main():
    with fuseki.FusekiServer(3333) as fu_p:

        um_cf_maps = fu_p.retrieve_mappings(
            '<http://metarelate.net/metocean/format/um>',
            '<http://metarelate.net/metocean/format/cf>')
        stash_to_cfsn = []
        fieldc_to_cfsn = []
        not_used_maps = []
        for mapping in um_cf_maps:
            source_mems = mapping['mr:source']['skos:member']
            target_mems = mapping['mr:target']['skos:member']
            stash = get_stash(source_mems, fu_p)
            cfsn = get_cf_sname(target_mems, fu_p)
            fieldc = get_fieldcode(source_mems, fu_p)
            if stash and cfsn:
                stash_to_cfsn.append({'stash':stash, 'cfsn':cfsn})
            elif fieldc and cfsn:
                fieldc_to_cfsn.append({'fieldc':fieldc, 'cfsn':cfsn})
            else:
                not_used_maps.append(mapping)
                print mapping
                print stash
                print cfsn
                print fieldc
                print 40*'-'
        um_cf_maps = not_used_maps
        ## and inverted
        cf_um_maps = fu_p.retrieve_mappings(
            '<http://metarelate.net/metocean/format/cf>',
            '<http://metarelate.net/metocean/format/um>')
        cfsn_to_fieldc = []
        not_used_maps = []
        for mapping in cf_um_maps:
            source_mems = mapping['mr:source']['skos:member']
            target_mems = mapping['mr:target']['skos:member']
            stash = get_stash(target_mems, fu_p)
            cfsn = get_cf_sname(source_mems, fu_p)
            fieldc = get_fieldcode(target_mems, fu_p)
            #if stash and cfsn:
            #    stash_to_cfsn.append({'stash':stash, 'cfsn':cfsn})
            if fieldc and cfsn:
                cfsn_to_fieldc.append({'fieldc':fieldc, 'cfsn':cfsn})
            else:
                not_used_maps.append(mapping)
                print mapping
                print cfsn
                print fieldc
                print 40*'-'

    # for um_cf_map in um_cf_maps:
    #     print 25*'-'
    #     print um_cf_map


    ## make a python dictionary of entries for STASH to CFSN
    stcf_list = []
    for stcf in stash_to_cfsn:
        str_elem = '\t"{stash}" : CFname(cfname="{cfsn}", unit="{units}"),'
        str_elem = str_elem.format(stash=stcf['stash'],
                                   cfsn=stcf['cfsn']['standard_name'],
                                   units=stcf['cfsn']['units'])
        stcf_list.append(str_elem)
    stcf_str = '\n'.join(stcf_list)
    stcf_str = line_sort(stcf_str)
    stcf_str = 'STASH_TO_CF = {\n' + stcf_str
    stcf_str += ENDDICT
    
    #make a python dictionary of fc to cf
    fccf_list = []
    for fccf in fieldc_to_cfsn:
        fcr_elem = '\t"{fieldc}" : CFname(cfname="{cfsn}", unit="{units}"),'
        fcr_elem = fcr_elem.format(fieldc=fccf['fieldc'],
                                   cfsn=fccf['cfsn']['standard_name'],
                                   units=fccf['cfsn']['units'])
        fccf_list.append(fcr_elem)
    fccf_str = '\n'.join(fccf_list)
    fccf_str = num_line_sort(fccf_str)
    fccf_str = 'LBFC_TO_CF = {\n' + fccf_str
    fccf_str += ENDDICT

    cffc_list = []
    for cffc in cfsn_to_fieldc:
        cfr_elem = '\tCFname(cfname="{cfsn}", unit="{units}") : {fieldc},'
        cfr_elem = cfr_elem.format(fieldc=cffc['fieldc'],
                                   cfsn=cffc['cfsn']['standard_name'],
                                   units=cffc['cfsn']['units'])
        cffc_list.append(cfr_elem)
    cffc_str = '\n'.join(cffc_list)
    cffc_str = line_sort(cffc_str)
    cffc_str = 'CF_TO_LBFC = {\n' + cffc_str
    cffc_str += ENDDICT

    # g2pcf_str

    with open('../lib/iris/fileformats/um_cf_map.py', 'w') as umcf:
        umcf.write(header)
        umcf.write(stcf_str)
        umcf.write('\n')
        umcf.write(fccf_str)
        umcf.write('\n')
        umcf.write(cffc_str)
        umcf.write('\n')

    # with open('../lib/iris/fileformats/grib_cf_map.py', 'w') as gribcf:
    #     umcf.write(g2pcf_str)
    #     umcf.write('\n')
    # umcf.write(cfgrib_dict)
    # umcf.write('\n')

if __name__ == '__main__':
    main()




                    
        
         
     

     




