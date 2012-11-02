import metocean.queries as moq
import metocean.fuseki as fuseki


with fuseki.FusekiServer() as fu:

    mappings = moq.fast_mapping_by_link(False,False,True)


    cflinks = moq.get_cflinks(None,True)

    cflinks = {cflink['s']:cflink for cflink in cflinks}

    for amap in mappings:
        for key in amap.keys():
            if key in ['cflinks','griblinks','umlinks']:
                amap[key] = amap[key].split('&')
            if key == 'cflinks':
                for cflink in amap['cflinks']:
                    amap['cflinks'] = cflinks[cflink]
                    





