# api calls

objdimensions_ss  Measurements of the cataloged object
objcollector_ss     The name(s) of the person(s) who collected the cataloged object

objkeelingser_s     Used for audio recordings only: The Keeling series numbero

objassoccult_s  The cultural group(s) associated with the object in its original context
objculturetree_ss   The higher-order cultural group names for the associated cultural group(s)

objfcpgeoloc_s  The latitude and longitude of the field collection place
objfcpelevation_s   The elevation of the field collection place

objinscrtext_ss     Textual inscriptions placed found on the cataloged object

objname_s   A name for the cataloged object
objtitle_s   A title for the cataloged object
objdescr_s  A description of the cataloged object
objfcpverbatim_s    A verbatim statement of provenience
objcontextuse_s     The context in which the object was originally used
objmaterials_ss     Materials from which the cataloged object was made
objcomment_s    Additional, relevant information about an object
objcollector_ss     The name(s) of the person(s) who collected the cataloged object


# api query stuff

    params = {
        #'q': 'objculturetee_txt:Arctic',
        #'q': 'objmaterials_txt:gold',
        'q': 'objname_txt:' + user_query,
        'wt': 'json',
        'indent': True,
        #'facet': 'true',
        #'facet.field':'objculturetree_ss'
        }
    r = requests.get(url, params=params, headers=headers)

    return json.dumps(json.loads(r.text), indent=4)



