"""Machine-readable authoring shape; the codec additionally enforces byte layout."""


def asset_schema():
    def obj(properties):
        return {'type':'object','additionalProperties':False,'required':list(properties),'properties':properties}
    def array(item,n=None):
        return {'type':'array','items':item,**({'minItems':n,'maxItems':n} if n is not None else {})}
    def uint(n): return {'type':'integer','minimum':0,'maximum':n}
    def ref(name): return {'$ref':'#/$defs/'+name}
    name=obj({'id':{'type':'string'},'index':uint(255),'start':uint(0xfffff),'words':array(uint(0x1fff))})
    result=obj({'schema_version':{'const':1},'format':{'const':'g5510_main_dialogue_fixed_layout'},
        'directory':obj({'address':{'const':0x92c4a},'page_base':{'const':0x92c56},
                         'page_targets':{'const':[0x92c56,0x92df8]}}),
        'pages':array(ref('page'),2),'records':array(ref('record'),275),
        'officer_names':array(ref('officer'),256),'city_names':array(ref('city'),40)})
    officer={**name,'properties':{**name['properties'],'words':array(uint(0x1fff),3)}}
    city={**name,'properties':{**name['properties'],'words':array(uint(0x1fff),2)}}
    result.update({'$schema':'https://json-schema.org/draft/2020-12/schema',
        'title':'G-5510 main dialogue fixed-layout authoring schema',
        'description':'The runtime validator additionally fixes record identity/addresses, checks signed glyph windows, terminators, trim safety, and signed target offsets. No Unicode or playability guarantee.',
        '$defs':{'officer':officer,'city':city,
            'token':obj({'type':{'enum':['glyph','control','special_fixed_bitmap']},'word':uint(65535)}),
            'page':obj({'index':uint(1),'start':uint(0xfffff),'end':uint(0x100000),'text_base':uint(0xfffff),
                        'entries':array({'type':'string','pattern':'^message_[0-9a-f]{6}$'})}),
            'record':obj({'id':{'type':'string','pattern':'^message_[0-9a-f]{6}$'},'start':uint(0xfffff),
                          'end':uint(0x100000),'tokens':array(ref('token'))})}})
    return result
