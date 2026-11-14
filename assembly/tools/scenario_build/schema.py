"""Derived JSON Schema. Python validation additionally requires strict integers."""
from . import scenario_build as sb


def schema():
    def obj(properties):
        return {'type':'object', 'additionalProperties':False,
                'required':list(properties), 'properties':properties}
    def uint(width): return {'type':'integer', 'minimum':0, 'maximum':(1 << (width*8))-1}
    def fixed(items):
        return {'type':'array', 'prefixItems':items, 'items':False,
                'minItems':len(items), 'maxItems':len(items)}
    def field(spec):
        if spec.table_id in sb.SPLIT_WORDS:
            result = obj({'unknown_high_word':uint(2), 'value_low_word':uint(2)})
        elif spec.table_id == 'ram_ea88':
            result = obj({f'source_byte{i}':uint(1) for i in range(3)})
        else: result = uint(spec.source_record_width)
        result['description'] = sb.field_semantics()[spec.table_id]['meaning']
        return result
    definitions = {s.table_id:field(s) for s in sb.SPECS}
    scenarios = []
    for ident in sb.IDS:
        properties = {'id':{'const':ident}, 'descriptor_targets':obj({s.table_id:{
            'type':'string', 'enum':[f'{i}.{s.table_id}' for i in sb.IDS]} for s in sb.SPECS})}
        for group,count,first in sb.GROUPS:
            properties[group] = fixed([obj({'id':{'type':'integer', 'const':i+first}, **{
                s.table_id:{'$ref':'#/$defs/'+s.table_id} for s in sb.GROUP_SPECS[group]}}) for i in range(count)])
        scenarios.append(obj(properties))
    result = obj({'schema_version':{'type':'integer','const':1}, 'format':{'const':sb.FORMAT},
        'canonical_rom_sha256':{'const':sb.legacy.CANONICAL_SHA256},
        'directory_targets':{'type':'array','minItems':3,'maxItems':3,'items':{'enum':list(sb.IDS)}},
        'scenarios':fixed(scenarios)})
    result.update({'$schema':'https://json-schema.org/draft/2020-12/schema', '$defs':definitions,
        'title':'Fixed scenario source fields', 'description':
        'Only assets.json is editable. Pointer aliases are editor policy, not original CPU bounds. '
        'Python rejects booleans/floats including integral floats; source words are never clamped to gameplay caps.'})
    return result
