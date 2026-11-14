"""Documentation schema; runtime validation additionally enforces row identity/order."""
from tools.audio_formats import audio_formats as af


def asset_schema():
    def integer(low,high): return {'type':'integer','minimum':low,'maximum':high}
    def array(items,low,high=None): return {'type':'array','items':items,'minItems':low,'maxItems':low if high is None else high}
    def obj(fields): return {'type':'object','additionalProperties':False,'required':list(fields),'properties':fields}
    u8=integer(0,255); masks=array(u8,3)
    city=obj({'id':integer(1,40),'x_fixed16':integer(16,1151),'y_fixed16':integer(0,1151),
              'availability':masks,'candidates':array(integer(1,40),0,7),
              'terminator':integer(128,255),'padding':array(u8,0,7)})
    point=obj({'index':integer(0,5),'x':integer(0,127),'y':u8,'availability':masks})
    schema=obj({'schema_version':{'type':'integer','const':1},
                'format':{'const':'g5510_world_fixed_layout'},'canonical_rom_sha256':{'const':af.ROM_SHA256},
                'terrain_costs':array(u8,6),'terrain_rows':array(array(integer(0,5),72),72),
                'cities':array(city,40),'points':array(point,6),'point_terminator':integer(128,255)})
    schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema',
        'title':'G5510 world fixed-layout editable authority',
        '$comment':'Runtime also fixes city/point ordering and enforces candidates+terminator+padding=8. City footprint, candidate IDs and terrain codes are editor constraints, not CPU clamps. Zero masks are representable, not safe gameplay.'})
    return schema
