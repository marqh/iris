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

import pdb

import itertools

import metocean.queries as moq
import metocean.fuseki as fuseki

OPEQ = '<http://www.openmath.org/cd/relation1.xhtml#eq>'

header = '''# (C) British Crown Copyright 2010 - 2013, Met Office
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

# DO NOT EDIT: AUTO-GENERATED TRANSLATIONS


'''

icol = 'import collections\n'

cf_tuple_def = '''
CFname = collections.namedtuple('CFname', ['standard_name', 'long_name',
                                           'unit'])
'''

grib_tuple_def = '''
G2param = collections.namedtuple('G2param', ['edition', 'discipline',
                                             'category', 'number'])
'''

end_dictionary = '''
}
'''

BUILT_FILES = {'../lib/iris/fileformats/um_cf_map.py': [icol, cf_tuple_def],
               '../lib/iris/fileformats/grib_cf_map.py': [icol, grib_tuple_def,
                                                          cf_tuple_def],
               '../lib/iris/etc/grib_rules.txt':[],
               '../lib/iris/etc/grib_save_rules.txt':[],}


cf_iris_types = {}

def str_line_sort(st):
    sort_st = st.split('\n')
    sort_st.sort()
    st = '\n'.join(sort_st)
    return st

def dict_line_sort(st):
    sort_st = st.split('\n')
    try:
        sort_st.sort(key=lambda str: int(str.split(':')[0].strip().replace('"','')))
        st = '\n'.join(sort_st)
    except ValueError:
        st = str_line_sort(st)
    return st


class Mapping(object):
    """
    abstract Mapping class
    """
    in_file = None
    container = None
    closure = None
    to_sort = None
    def __init__(self, amap, source, target, fu_p):
        return NotImplemented
    def encode(self):
        return NotImplemented
    def type_match(definition):
        return NotImplemented

        

class StashCFMapping(Mapping):
    """
    a mapping object, obtained from the metarelate repository
    defining a source concept, a target concept and any mapped values
    
    """
    in_file = '../lib/iris/fileformats/um_cf_map.py'
    container = '\nSTASH_TO_CF = {'
    closure = '\n\t}\n'
    to_sort = True
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        self.valuemaps = amap.get('mr:hasValueMaps')
        self.fu_p = fu_p
    def encode(self):
#        pdb.set_trace()
        stash = self.source.notation()
        cfsname, lname, units =  self.target.notation()
        #lname
        str_elem = '\t{stash} : CFname({cfsname}, {lname}, {units}),\n'
        str_elem = str_elem.format(stash=stash, cfsname=cfsname,
                                   lname=lname, units=units)
        return str_elem
    @staticmethod
    def type_match(source, target):
        if isinstance(source, StashConcept) and \
            isinstance(target,CFPhenomDefConcept):
            typematch = True
        else:
            typematch = False
        return typematch

class FieldcodeCFMapping(Mapping):
    """
    a mapping object, obtained from the metarelate repository
    defining a source concept, a target concept and any mapped values
    
    """
    in_file = '../lib/iris/fileformats/um_cf_map.py'
    container = '\nLBFC_TO_CF = {'
    closure = '\n\t}\n'
    to_sort = True
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        #self.valuemaps = amap.get('mr:hasValueMaps')
        self.fu_p = fu_p
    def encode(self):
        fc = self.source.notation()
        cfsname, lname, units =  self.target.notation()
        #lname
        str_elem = '\t{fc} : CFname({cfsname}, {lname}, {units}),\n'
        str_elem = str_elem.format(fc=fc, cfsname=cfsname,
                                   lname=lname, units=units)
        return str_elem
    @staticmethod
    def type_match(source, target):
        if isinstance(source, FieldcodeConcept) and \
            isinstance(target,CFPhenomDefConcept):
            typematch = True
        else:
            typematch = False
        return typematch

class CFFieldcodeMapping(Mapping):
    """
    a mapping object, obtained from the metarelate repository
    defining a source concept, a target concept and any mapped values
    
    """
    in_file = '../lib/iris/fileformats/um_cf_map.py'
    container = '\nCF_TO_LBFC = {'
    closure = '\n\t}\n'
    to_sort = True
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        #self.valuemaps = amap.get('mr:hasValueMaps')
        self.fu_p = fu_p
    def encode(self):
        fc = self.target.notation()
        cfsname, lname, units =  self.source.notation()
        str_elem = '\tCFname({cfsname}, {lname}, {units}) : {fc},\n'
        try:
            str_elem = str_elem.format(fc=fc, cfsname=cfsname, units=units)
        except KeyError:
            str_elem = str_elem.format(fc=fc, cfsname=cfsname,
                                   lname=lname, units=units)
        return str_elem
    @staticmethod
    def type_match(source, target):
        if isinstance(source, CFPhenomDefConcept) and \
            isinstance(target, FieldcodeConcept):
            typematch = True
        else:
            typematch = False
        return typematch

class Grib2CFParamMapping(Mapping):
    """
    a mapping object, obtained from the metarelate repository
    defining a source concept, a target concept and any mapped values
    
    """
    in_file = '../lib/iris/fileformats/grib_cf_map.py'
    container = '\nGRIB2_TO_CF = {'
    closure = '\n\t}\n'
    to_sort = True
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        self.fu_p = fu_p
    def encode(self):
        ed, disc, param, cat = self.source.notation()
        cfsname, lname, units =  self.target.notation()
        str_elem = '\tG2param({ed}, {disc}, {cat}, {num}): '
        str_elem += 'CFname({cfsname}, {lname}, {units}),\n'
        str_elem = str_elem.format(ed=ed, disc=disc, cat=cat, num=param,
                                   cfsname=cfsname, lname=lname, units=units)
        return str_elem
    @staticmethod
    def type_match(source, target):
        if isinstance(source, Grib2ParamConcept) and \
            isinstance(target, CFPhenomDefConcept):
            typematch = True
        else:
            typematch = False
        return typematch

    
class CFGrib2ParamMapping(Mapping):
    """
    a mapping object, obtained from the metarelate repository
    defining a source concept, a target concept and any mapped values
    
    """
    in_file = '../lib/iris/fileformats/grib_cf_map.py'
    container = '\nCF_TO_GRIB2 = {'
    closure = '\n\t}\n'
    to_sort = True
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        self.valuemaps = amap.get('mr:hasValueMaps', [])
        self.fu_p = fu_p
    def encode(self):
        ed, disc, param, cat = self.target.notation()
        cfsname, lname, units =  self.source.notation()
        str_elem = '\tCFname({cfsname}, {lname}, {units}):'
        str_elem += 'G2param({ed}, {disc}, {cat}, {num}),\n '
        str_elem = str_elem.format(ed=ed, disc=disc, cat=cat, num=param,
                                   cfsname=cfsname, lname=lname, units=units)
        return str_elem
    @staticmethod
    def type_match(source, target):
        if isinstance(source, CFPhenomDefConcept) and \
            isinstance(target, Grib2ParamConcept):
            typematch = True
        else:
            typematch = False
        return typematch

class CFGribMapping(Mapping):
    """
    """
    in_file = '../lib/iris/etc/grib_save_rules.txt'
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        self.valuemaps = amap.get('mr:hasValueMaps', [])
        self.fu_p = fu_p
    def encode(self):
        cftest = self.source.notation('test')
        gribassign = self.target.notation('assign')
        encoding = 'IF\n'
        encoding += cftest
        encoding += 'THEN\n'
        encoding += gribassign#.format
        encoding += '\n\n'
        return encoding
    @staticmethod
    def type_match(source, target):
        if isinstance(source, CFConcept) and \
            isinstance(target, GribConcept):
            typematch = True
        else:
            typematch = False
        return typematch




class GribCFMapping(Mapping):
    """
    """
    in_file = '../lib/iris/etc/grib_rules.txt'
    def __init__(self, amap, source, target, fu_p):
        self.source = source
        self.target = target
        self.valuemaps = amap.get('mr:hasValueMaps', [])
        self.fu_p = fu_p
    def encode(self):
        gribtest = self.source.notation('test')
        cfassign = self.target.notation('assign')
        #if set(assign_keys) == 
        encoding = 'IF\n'
        encoding += gribtest
        encoding += 'THEN\n'
        encoding += cfassign#.format
        encoding += '\n\n'
        return encoding
    @staticmethod
    def type_match(source, target):
        if isinstance(source, GribConcept) and \
            isinstance(target, CFConcept):
            typematch = True
        else:
            typematch = False
        return typematch




def make_mapping(mapping, fu_p):
    """
    Mapping object factory
    selects the appropriate subclass for the inputs
    """
    built_mappings = []
    for mapping_type in Mapping.__subclasses__():
        source = make_concept(mapping.get('mr:source'), fu_p)
        target = make_concept(mapping.get('mr:target'), fu_p)
        if mapping_type.type_match(source, target):
            built_mappings.append(mapping_type(mapping, source, target, fu_p))
    if len(built_mappings) != 1:
        if len(built_mappings) == 0:
            #print source
            #print target
            #print ''
            #raise ValueError('no matching Mapping type found')
            built_mappings = [None]
        else:
            raise ValueError('multiple matching Mapping types found')
            built_mappings = [None]
    return built_mappings[0]
    

class Concept(object):
    """
    a source or target concept
    """
    def __init__(self, definition, fu_p):
        return NotImplemented
    def notation(self, direction):
        ## direction should be 'test' or 'assign' only
        return NotImplemented
    def type_match(definition, fu_p):
        return NotImplemented
    

class StashConcept(Concept):
    """
    a concept which is a UM stash code only
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition['mr:hasProperty']
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction=None):
        val = self.properties[0].get('rdf:value')
        stash = moq.get_label(self.fu_p, val)
        return stash
    @staticmethod
    def type_match(definition, fu_p):
        STASHC = '<http://reference.metoffice.gov.uk/def/um/stash/concept/'
        F3STASH = '<http://reference.metoffice.gov.uk/def/um/umdp/F3/stash>'
        fformat = '<http://www.metarelate.net/metOcean/format/um>'
        ff = definition['mr:hasFormat'] == fformat
        properties = definition.get('mr:hasProperty', [])
        components = definition.get('mr:hasComponent', [])
        if ff and len(properties) == 1 and len(components) == 0:
            val = properties[0].get('rdf:value')
            if val:
                stashval = val.startswith(STASHC)
            else:
                stashval = False
            name = properties[0].get('mr:name')
            if name:
                stashname = name == F3STASH
            else:
                stashname = False
            operator = properties[0].get('mr:operator')
            if operator:
                op_eq = operator = OPEQ
            else:
                op_eq = False
            if stashval and stashname and op_eq:
                stash = True
            else:
                stash = False
        else:
            stash = False
        return stash


class FieldcodeConcept(Concept):
    """
    a concept which is a UM field code only
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition['mr:hasProperty']
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction=None):
        val = self.properties[0].get('rdf:value')
        fcode = moq.get_label(self.fu_p, val)
        return fcode
    @staticmethod
    def type_match(definition, fu_p):
        FIELDC = '<http://reference.metoffice.gov.uk/def/um/fieldcode/'
        F3FIELD = '<http://reference.metoffice.gov.uk/def/um/umdp/F3/lbfc>'
        fformat = '<http://www.metarelate.net/metOcean/format/um>'
        ff = definition['mr:hasFormat'] == fformat
        properties = definition.get('mr:hasProperty', [])
        components = definition.get('mr:hasComponent', [])
        if ff and len(properties) == 1 and len(components) == 0:
            val = properties[0].get('rdf:value')
            if val:
                fieldval = val.startswith(FIELDC)
            else:
                fieldval = False
            name = properties[0].get('mr:name')
            if name:
                fieldname = name == F3FIELD
            else:
                fieldname = False
            operator = properties[0].get('mr:operator')
            if operator:
                op_eq = operator = OPEQ
            else:
                op_eq = False
            if fieldval and fieldname and op_eq:
                fieldcode = True
            else:
                fieldcode = False
        else:
            fieldcode = False
        return fieldcode



class CFPhenomDefConcept(Concept):
    """
    a concept which is only defining a CF Field's base phenomenon
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition['mr:hasProperty']
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction=None):
        cfsn = None
        lname = None
        units = None
        for p in self.properties:
            if moq.get_label(self.fu_p, p.get('mr:name')) == '"standard_name"':
                cfsn = moq.get_label(self.fu_p, p.get('rdf:value'))
                if cfsn.startswith('<'):
                    cfsn = None
            elif moq.get_label(self.fu_p, p.get('mr:name')) == '"long_name"':
                lname = p.get('rdf:value')
            elif moq.get_label(self.fu_p, p.get('mr:name')) == '"units"':
                units = moq.get_label(self.fu_p, p.get('rdf:value'))
        return cfsn, lname, units
    @staticmethod
    def type_match(definition, fu_p):
        fformat = '<http://www.metarelate.net/metOcean/format/cf>'
        ff = definition['mr:hasFormat'] == fformat
        properties = definition.get('mr:hasProperty', [])
        components = definition.get('mr:hasComponent', [])
        if ff and len(components) == 0:
            define = {}
            for prop in properties:
                op = prop.get('mr:operator')
                name = prop.get('mr:name', '')
                value = prop.get('rdf:value')
                if op and value and op == OPEQ:
                    name_label = moq.get_label(fu_p, name)
                    value_label = moq.get_label(fu_p, value)
                    if not define.get(name_label):
                        define[name_label] = value_label
            required = set(('"units"', '"type"'))
            eitheror = set(('"standard_name"', '"long_name"'))
            if set(define.keys()).issuperset(required) and \
                set(define.keys()).issubset(required.union(eitheror)):
                phenom = True
            else:
                phenom = False
        else:
            phenom = False
        return phenom

def _cfprop(props, fu_p, eq):
    """
    """
    t_str = ''
    elem_str = ''
    for prop in props:
        if prop.get('mr:name').endswith('/type>'):
            t_str = moq.get_label(fu_p, prop.get('rdf:value', ''))
            t_str = t_str.strip('"')
            t_str += '('
        #elif prop.get('mr:name').endswith('/coordinate>'):
        #    print prop
        elif prop.get('mr:hasComponent'):
            comp = prop.get('mr:hasComponent')
            comp_notation = _cfprop(comp.get('mr:hasProperty'), fu_p, eq)
            name = moq.get_label(fu_p, prop.get('mr:name', ''))
            name = name.strip('"')
            elem_str += '{} {} {},'.format(name, eq, comp_notation)
        else:
            name = moq.get_label(fu_p, prop.get('mr:name', ''))
            name = name.strip('"')
            val = moq.get_label(fu_p, prop.get('rdf:value', ''))
            if val:
                elem_str += '{} {} {},'.format(name, eq, val)
            else:
                elem_str += '%s %s {%s},' % (name, eq, name)
    p_str = t_str + elem_str + ')\n'
    return p_str

class CFConcept(Concept):
    """
    a cf concept which doesn't match the specialised cf concepts
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition.get('mr:hasProperty', [])
        self.components = definition.get('mr:hasComponent', [])
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction):
        # prop_notation = ''
        # assign_keys = []
        eq = None
        if direction == 'test':
            eq = '=='
        elif direction == 'assign':
            eq = '='
        if len(self.components) == 0:
            prop_notation = _cfprop(self.properties, self.fu_p, eq)
            # t_str = ''
            # elem_str = ''
            # for prop in self.properties:
            #     if prop.get('mr:name').endswith('/type>'):
            #         t_str = moq.get_label(self.fu_p, prop.get('rdf:value', ''))
            #         t_str += '('
            #     else:
            #         name = moq.get_label(self.fu_p, prop.get('mr:name', ''))
            #         name = name.strip('"')
            #         val = moq.get_label(self.fu_p, prop.get('rdf:value', ''))
            #         if val:
            #             elem_str += '{} {} {},'.format(name, eq, val)
            #         else:
            #             elem_str += '%s %s {name},' % (name, eq )
            #             assign_keys.append(name)
            # p_str = t_str + elem_str + ')\n'
            # prop_notation += p_str
        elif len(self.properties) == 0:
            for comp in self.components:
                prop_notation = ''
                props = comp.get('mr:hasProperty')
                if props:
                    prop_notation += _cfprop(props, self.fu_p, eq) 
                prop_notation += '\n'
        else:
            raise ValueError('components and properties cannot coexist on',
                             ' a cf concept')
        if direction == 'test':
            r_val = prop_notation
        elif direction == 'assign':
            r_val = prop_notation
        return r_val
    @staticmethod
    def type_match(definition, fu_p):
        fformat = '<http://www.metarelate.net/metOcean/format/cf>'
        ff = definition['mr:hasFormat'] == fformat
        pd =  CFPhenomDefConcept.type_match(definition, fu_p)
        if ff and not pd:
            cfc = True
        else:
            cfc = False
        return cfc
    
        
class GribConcept(Concept):
    """
    a grib concept which doesn't match the specialised grib concepts
    and has only properties, not components
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition['mr:hasProperty']
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction):
        prop_notation = ''
#        assign_keys = []
        for prop in self.properties:
            name = moq.get_label(self.fu_p, prop.get('mr:name'))
            name = name.strip('"')
            op = prop.get('mr:operator') == OPEQ
            val = prop.get('rdf:value')
            n = ''
            if name and op and val:
                if direction == 'test':
                    n = 'grib.{} == {}\n'.format(name, val)
                elif direction == 'assign':
                    n = 'grib.{} = {}\n'.format(name, val)
                
            elif name:
                if direction == 'test':
                    n = 'grib.{}\n'.format(name)
                elif direction == 'assign':
                    n = 'grib.{}'.format(name)
                    n += ' = {%s}\n' % prop.get('mr:name')
#                    assign_keys.append(prop.get('mr:name'))
            prop_notation += n
        if direction == 'test':
            r_val = prop_notation
        elif direction == 'assign':
            r_val = prop_notation#, assign_keys

        return r_val
    @staticmethod
    def type_match(definition, fu_p):
        fformat = '<http://www.metarelate.net/metOcean/format/grib>'
        ff = definition['mr:hasFormat'] == fformat
        components = definition.get('mr:hasComponent', [])
        g2param = Grib2ParamConcept.type_match(definition, fu_p)
        if ff and len(components) == 0 and not g2param:
            grib_c = True
        else:
            grib_c = False
        return grib_c

    

class Grib2ParamConcept(Concept):
    """
    a concept which is only defining a GRIB2 parameter code
    """
    def __init__(self, definition, fu_p):
        self.fformat = definition['mr:hasFormat']
        self.properties = definition['mr:hasProperty']
        self.id = definition['component']
        self.fu_p = fu_p
    def notation(self, direction=None):
        for prop in self.properties:
            name = prop.get('mr:name', '')
            if name == '<http://def.ecmwf.int/api/grib/keys/editionNumber>':
                ed = prop.get('rdf:value')
            elif name == '<http://def.ecmwf.int/api/grib/keys/discipline>':
                disc = prop.get('rdf:value')
            elif name == '<http://def.ecmwf.int/api/grib/keys/parameterNumber>':
                param = prop.get('rdf:value')
            elif name == '<http://def.ecmwf.int/api/grib/keys/parameterCategory>':
                cat = prop.get('rdf:value')
        return ed, disc, param, cat
    @staticmethod
    def type_match(definition, fu_p):
        fformat = '<http://www.metarelate.net/metOcean/format/grib>'
        ed = '<http://def.ecmwf.int/api/grib/keys/editionNumber>'
        disc = '<http://def.ecmwf.int/api/grib/keys/discipline>'
        param = '<http://def.ecmwf.int/api/grib/keys/parameterNumber>'
        cat = '<http://def.ecmwf.int/api/grib/keys/parameterCategory>'
#        pdb.set_trace()
        ff = definition['mr:hasFormat'] == fformat
        properties = definition.get('mr:hasProperty', [])
        components = definition.get('mr:hasComponent', [])
        def_keys = set([p.get('mr:name', '') for p in properties])
        param_keys = set((ed, disc, param, cat))
        if ff and len(components) == 0 and def_keys == param_keys:
            grib2param = True
        else:
            grib2param = False
        return grib2param

def make_concept(definition, fu_p):
    """
    Concept object factory
    selects the appropriate subclass for the inputs
    """

    built_concepts = []
    for concept_type in Concept.__subclasses__():
        if concept_type.type_match(definition, fu_p):
            built_concepts.append(concept_type(definition, fu_p))
    if len(built_concepts) != 1:
        if len(built_concepts) == 0:
            ec = 'no matching Concept type found \n{}'.format(definition)
            #raise ValueError(ec)
            built_concepts = [None]
        else:
            raise ValueError('multiple matching Concept types found')
            built_concepts = [None]
    return built_concepts[0]

iris_format = '<http://www.metarelate.net/metOcean/format/cf>'

formats = ['<http://www.metarelate.net/metOcean/format/grib>',
           '<http://www.metarelate.net/metOcean/format/um>']



def main():
    """
    picks out a fformat to iris pair as export and import
    retrieves all valid mappings from the repository
    creates relevant mapping subclasses and
    creates the necessary encodings in the Iris code base
    """
    format_maps = {}
    with fuseki.FusekiServer(3333) as fu_p:
        for fformat in formats:
            format_maps[fformat] = {'import':{}, 'export':{}}
            import_maps = fu_p.retrieve_mappings(fformat, iris_format)
            import_maps = [make_mapping(amap, fu_p) for amap in import_maps]
            import_maps.sort(key=type)
            for g_type, group in itertools.groupby(import_maps, key=type):
                format_maps[fformat]['import'][g_type.__name__] = list(group)
            export_maps = fu_p.retrieve_mappings(iris_format, fformat)
            export_maps = [make_mapping(amap, fu_p) for amap in export_maps]
            export_maps.sort(key=type)
            for g_type, group in itertools.groupby(export_maps, key=type):
                format_maps[fformat]['export'][g_type.__name__] = list(group)
        #pdb.set_trace()

        for afile in BUILT_FILES:
            f = open(afile, 'w')
            f.write(header)
            for extras in BUILT_FILES[afile]:
                f.write(extras)
            f.close()

        for fformat in formats:
            for direction in ['import', 'export']:
                ports = format_maps[fformat][direction]
                for map_set in ports:
                    print direction
                    print map_set
                    if map_set == 'NoneType':
                        ec = 'Some {} {} mappings not categorised'
                        ec = ec.format(fformat, direction)
                        print ec
                    else:
                        if ports[map_set][0].in_file not in BUILT_FILES:
                            ec = '{} writing to unmanaged file {}'
                            ec.format(map_set, ports[map_set][0].in_file)
                            raise ValueError(ec)
                        map_str = ''
                        for mappings in ports[map_set]:
                            map_str += mappings.encode()
                        if ports[map_set][0].to_sort:
                            map_str = dict_line_sort(map_str)
                        if ports[map_set][0].container:
                            map_str = ports[map_set][0].container + map_str
                        if ports[map_set][0].closure:
                            map_str += ports[map_set][0].closure
                        with open(ports[map_set][0].in_file, 'a') as in_file:
                            in_file.write(map_str)

if __name__ == '__main__':
    main()

