"""Export and build candidate direct-control descendants of seven prior sources.

Only explicit export disassembles. Normal builds consume the sealed ledger and
editable mnemonic source, validate actual GNU labels, and splice only extents.
Unknown indirect targets and primary ownership are deliberately not promoted.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse, csv, io, json, re, sys
from collections import defaultdict, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from tools.m68k_build import m68k_build as m
from tools.m68k_build.elf_verify import verify_object
from tools.vdp_word_streams import build as v
from tools.vdp_word_streams import format as f

LEDGER=ROOT/'analysis/direct_code/generated/instructions.json'
SOURCE=ROOT/'src/m68k/direct_descendants.s'
LEDGER_SHA=reference_value(__name__, 'LEDGER_SHA')
SEEDS=('recovered_code','candidate_filter','candidate_action','candidate_handler_818',
       'candidate_handler_49e','candidate_handler_9b0','candidate_handler_c26')
PATTERN=r'\s*\.incbin "segments/bank([0-9a-f]{2})\.bin", 0x([0-9A-F]+), 0x([0-9A-F]+)'
MNEMONICS=m.MNEMONICS|{'rol','sf','st'}

def validate_source(source,records):
    return m.validate_source(source,records,allowed_mnemonics=MNEMONICS)

def base_layout(rom):
    from tools.dictionary_streams import codec as d
    return v.render_layout(rom,v.read_fields(v.DEFAULT_FIELDS),d.load_json(d.read(ROOT/'analysis/dictionary_streams/generated/fields.json',d.MAX_JSON)))

def raw_positions(base):
    selected=set()
    for bank in range(16):
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(PATTERN,line)
            if match:
                if int(match[1],16)!=bank:raise ValueError('wrong raw bank')
                start=bank*65536+int(match[2],16);size=int(match[3],16)
                selected.update(range(start,start+size))
    return selected

def raw_edge(rom,row,edge):
    """Independently check direct target from original opcode words, not map operand text."""
    a=int(row['address']);size=int(row['size']);op=int.from_bytes(rom[a:a+2],'big')
    def signed(n):return n-65536 if n&32768 else n
    kind=edge['type'];target=int(edge['target'])
    if kind in ('fallthrough','call_fallthrough','branch_fallthrough','exception_return_fallthrough'):
        expected=a+size
    elif op>>12==6:
        b=op&255;delta=(b-256 if b&128 else b) if b else signed(int.from_bytes(rom[a+2:a+4],'big'))
        expected=a+2+delta
    elif op&0xF0F8==0x50C8:
        expected=a+2+signed(int.from_bytes(rom[a+2:a+4],'big'))
    elif op&0xFFC0 in (0x4E80,0x4EC0):
        mode,reg=(op>>3)&7,op&7
        if (mode,reg)==(7,1):expected=int.from_bytes(rom[a+2:a+6],'big')
        elif (mode,reg)==(7,0):expected=signed(int.from_bytes(rom[a+2:a+4],'big'))&0xFFFFFFFF
        elif (mode,reg)==(7,2):expected=a+2+signed(int.from_bytes(rom[a+2:a+4],'big'))
        else:raise ValueError('indirect transfer cannot be an admitted direct edge')
    elif kind=='trap_handler' and op&0xFFF0==0x4E40:
        p=(32+(op&15))*4;expected=int.from_bytes(rom[p:p+4],'big')
    else:raise ValueError(f'unknown direct edge at {a:06X}: {kind}')
    if expected!=target:raise ValueError('raw opcode disagrees with direct graph target')

def export_bundle(rom):
    from tools.code_analysis.m68k_code_map import load_capstone
    from tools.m68k_build.source import format_instruction
    m.af.verify_rom(rom);base=base_layout(rom);raw=raw_positions(base)
    seeds=set();pins={}
    for name in SEEDS:
        data=m.read(ROOT/f'src/m68k/{name}.s');pins[name]=m.sha(data)
        seeds.update(int(a,16) for a in re.findall(r'^m68k_([0-9a-f]{6}):$',data.decode(),re.M))
    if len(seeds)!=12921:raise ValueError('prior seven-source topology changed')
    data=m.read(m.INSTRUCTIONS)
    if m.sha(data)!=m.INSTRUCTIONS_HASH:raise ValueError('enhanced instruction map changed')
    rows={int(r['address']):r for r in csv.DictReader(io.StringIO(data.decode('utf-8-sig')))}
    edge_data=m.read(ROOT/'analysis/code/phase3_indirect/generated/enhanced_map/edges.csv')
    edges=defaultdict(list)
    for e in csv.DictReader(io.StringIO(edge_data.decode('utf-8-sig'))):
        if e['direct']=='True' and e['target'] and e['evidence_type']=='direct_control_flow':edges[int(e['source'])].append(e)
    queue=deque(sorted(seeds));seen=set(seeds);parent={};blocked=[]
    while queue:
        a=queue.popleft()
        for edge in edges[a]:
            raw_edge(rom,rows[a],edge);target=int(edge['target'])
            if target in seen:continue
            r=rows.get(target)
            if r and all(p in raw for p in range(target,target+int(r['size']))):
                seen.add(target);parent[target]=edge;queue.append(target)
            else:blocked.append(edge)
    cap=load_capstone()
    if cap.__version__!='5.0.6':raise ValueError('export requires Capstone 5.0.6')
    decoder=cap.Cs(cap.CS_ARCH_M68K,cap.CS_MODE_BIG_ENDIAN|cap.CS_MODE_M68K_000);decoder.detail=True
    records=[];lines=['| Candidate direct descendants; explicit call/branch/linear provenance.',
        '| No opaque-byte instructions, guessed indirect targets or new primary ownership.',
        '.cpu 68000','.section .text','_start:']
    for a in sorted(seen-seeds):
        r=rows[a];size=int(r['size']);data=bytes.fromhex(r['bytes'])
        ins=next(decoder.disasm(rom[a:a+size],a,count=1),None)
        if ins is None or ins.size!=size or bytes(ins.bytes)!=data or data!=rom[a:a+size]:raise ValueError('decoder extent/identity mismatch')
        p=parent[a]
        records.append(dict(address=a,size=size,bytes=data.hex(),original_mnemonic=r['mnemonic'],
            original_operand=r['operand'],discovery_confidence=r['confidence'],confidence='candidate',
            direct_parent=int(p['source']),edge_type=p['type']))
        lines.extend([f'.org 0x{a:X}',f'| {data.hex()} from {p["source_hex"]} {p["type"]}',
                      f'm68k_{a:06x}:','        '+format_instruction(ins),f'm68k_{a:06x}_end:'])
    source=('\n'.join(lines)+'\n').encode();validate_source(source,records)
    if len(records)!=7956 or sum(r['size'] for r in records)!=30416:raise ValueError('fixed batch scope changed')
    ledger=m.dump(records)
    info=dict(format='g5510-direct-code-v1',confidence='candidate',instructions=7956,bytes=30416,
        prior_instructions=12921,prior_code_bytes=47088,ranges=m.coalesce(records),
        instructions_sha256=m.sha(ledger),canonical_source_sha256=m.sha(source),prior_source_sha256=pins,
        original_rom_sha256=f.ROM_SHA,instruction_map_sha256=m.sha(m.read(m.INSTRUCTIONS)),
        edges_sha256=m.sha(edge_data),raw_bytes_before=len(raw),blocked=blocked,
        ownership_bytes_added=0,natural_entries_added=0,complete_indirect_domains_added=0,
        statement='Direct descendants are conditional executable code, not recovered gameplay semantics or natural-path proof.')
    return {'instructions.json':ledger,'manifest.json':m.dump(info),'direct_descendants.s':source}

def inventory(rom):
    m.af.verify_rom(rom);data=m.read(LEDGER)
    if m.sha(data)!=LEDGER_SHA:raise ValueError('direct ledger changed')
    rows=json.loads(data);end=0;known=set()
    for r in rows:
        a,size=r['address'],r['size']
        if type(a)is not int or type(size)is not int or a&1 or not 2<=size<=10 or size&1 or a<end or a+size>f.ROM_SIZE:raise ValueError('bad instruction extent')
        if bytes.fromhex(r['bytes'])!=rom[a:a+size]:raise ValueError('original instruction mismatch')
        if r['confidence']!='candidate':raise ValueError('unsupported confidence promotion')
        known.add(a);end=a+size
    if len(rows)!=7956 or sum(r['size'] for r in rows)!=30416:raise ValueError('fixed scope mismatch')
    return rows

def verify_image(rom,source,object_data,image,canonical=False):
    rows=inventory(rom);validate_source(source,rows)
    if verify_object(object_data,rows)!=image or len(image)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('ELF/image differ')
    positions=set()
    for row in rows:
        a,z=row['address'],row['address']+row['size'];positions.update(range(a,z))
        if canonical and image[a:z]!=rom[a:z]:raise ValueError('canonical mnemonic bytes mismatch')
    if any(value for a,value in enumerate(image) if a not in positions):raise ValueError('sparse zero padding changed')
    return dict(instructions=len(rows),compiled_bytes=len(positions),canonical=canonical,elf_labels=len(rows)*2,
                ownership_bytes_added=0,complete_indirect_domains_added=0)

def add_to_layout(rom,source,base):
    rows=inventory(rom);validate_source(source,rows);raw=raw_positions(base)
    positions={p for r in rows for p in range(r['address'],r['address']+r['size'])}
    if not positions<=raw:raise ValueError('direct source overlaps an existing authority')
    ranges=m.coalesce(rows);consumed=[];result=dict(base)
    for bank in range(16):
        lines=[]
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(PATTERN,line)
            if not match:lines.append(line);continue
            first=bank*65536+int(match[2],16);last=first+int(match[3],16);cursor=first
            for a,z in ranges:
                if z<=first or a>=last:continue
                if a<first or z>last:raise ValueError('code crosses bank/authority boundary')
                if cursor<a:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{a-cursor:X}')
                lines.append(f'        .incbin "m68k_direct_code.bin", 0x{a:X}, 0x{z-a:X}')
                consumed.extend(range(a,z));cursor=z
            if cursor<last:lines.append(f'        .incbin "segments/bank{bank:02x}.bin", 0x{cursor-bank*65536:X}, 0x{last-cursor:X}')
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=len(positions) or set(consumed)!=positions:raise ValueError('code omitted/duplicated')
    info=json.loads(base['manifest.json']);info.update(direct_code_bytes=30416,direct_code_instructions=7956,
        direct_code_source_sha256=m.sha(source),direct_code_ledger_sha256=LEDGER_SHA,direct_code_confidence='candidate',
        compiled_instruction_union=20877,compiled_code_union_bytes=77504,
        compiled_or_typed_bytes=info['compiled_or_typed_bytes']+30416,
        remaining_raw_slice_bytes=info['remaining_raw_slice_bytes']-30416,direct_code_owner_bytes_added=0)
    result['manifest.json']=m.dump(info);return result

def add_resource_fields(rom,fields,base,codec,label,expected_bytes):
    rows=codec.blocks(rom,fields);positions={p for r in rows for p in range(r['start'],r['end'])}
    if len(positions)!=expected_bytes or sum(r['end']-r['start'] for r in rows)!=expected_bytes or not positions<=raw_positions(base):raise ValueError(label+' fields overlap authority or change scope')
    consumed=[];result=dict(base)
    for bank in range(16):
        lines=[]
        for line in base[f'm68k_bank{bank:02x}.s'].decode().splitlines():
            match=re.fullmatch(PATTERN,line)
            if match:lines.extend(m.typed_gap(bank,int(match[2],16),int(match[3],16),[],[],rows,consumed))
            else:lines.append(line)
        result[f'm68k_bank{bank:02x}.s']=('\n'.join(lines)+'\n').encode()
    if len(consumed)!=expected_bytes or set(consumed)!=positions:raise ValueError(label+' resources omitted or duplicated')
    info=json.loads(base['manifest.json']);info.update({f'typed_{label}_bytes':expected_bytes,
        f'{label}_fields_sha256':codec.sha(codec.dump(fields)),f'{label}_confidence':'candidate',
        'compiled_or_typed_bytes':info['compiled_or_typed_bytes']+expected_bytes,
        'remaining_raw_slice_bytes':info['remaining_raw_slice_bytes']-expected_bytes})
    result['manifest.json']=m.dump(info);return result

def add_sprite_resources(rom,fields,base):
    from tools.sprite_word_resources import codec as sprite
    return add_resource_fields(rom,fields,base,sprite,'sprite_word_resource',17401)

def add_battle_variants(rom,fields,base):
    from tools.battle_variant_tiles import codec as variant
    return add_resource_fields(rom,fields,base,variant,'battle_variant_tiles',53806)

def add_world_chunks(rom,fields,base):
    from tools.world_tile_chunks import codec as world
    return add_resource_fields(rom,fields,base,world,'world_tile_chunks',35782)

def add_compact_sprites(rom,fields,base):
    from tools.compact_sprite_records import codec as compact
    return add_resource_fields(rom,fields,base,compact,'compact_sprite_records',12685)

def add_scene_sprites(rom,fields,base):
    from tools.scene_sprite_resources import codec as scene
    return add_resource_fields(rom,fields,base,scene,'scene_sprite_resources',2832)

def add_scene_tiles(rom,fields,base):
    from tools.scene_tile_resources import codec as scene
    return add_resource_fields(rom,fields,base,scene,'scene_tile_resources',19482)

def add_battle_overlays(rom,fields,base):
    from tools.battle_overlay_maps import codec as overlay
    return add_resource_fields(rom,fields,base,overlay,'battle_overlay_maps',10655)

def add_audio_roots(rom,fields,base):
    from tools.audio_root_resources import codec as audio
    return add_resource_fields(rom,fields,base,audio,'audio_root_resources',77)

def add_display_tiles(rom,fields,base):
    from tools.display_tile_resources import codec as display
    return add_resource_fields(rom,fields,base,display,'display_tile_resources',3680)

def add_battle_rules(rom,fields,base):
    from tools.battle_rule_tables import codec as rules
    return add_resource_fields(rom,fields,base,rules,'battle_rule_tables',2024)

def add_battle_palettes(rom,fields,base):
    from tools.battle_palette_transfers import codec as palette
    return add_resource_fields(rom,fields,base,palette,'battle_palette_transfers',1288)

def add_audio_dispatch(rom,fields,base):
    from tools.audio_dispatch_fields import codec as audio
    return add_resource_fields(rom,fields,base,audio,'audio_dispatch_fields',88)

def add_legacy_text(rom,fields,base):
    from tools.legacy_text_fields import codec as text
    return add_resource_fields(rom,fields,base,text,'legacy_text_fields',2856)

def add_title_overlays(rom,fields,base):
    from tools.title_overlay_maps import codec as title
    return add_resource_fields(rom,fields,base,title,'title_overlay_maps',458)

def add_transport_cargo(rom,fields,base):
    from tools.transport_cargo_build import codec as cargo
    return add_resource_fields(rom,fields,base,cargo,'transport_cargo',24)

def add_battle_scene_sprites(rom,fields,base):
    from tools.battle_scene_sprites import codec as scene
    return add_resource_fields(rom,fields,base,scene,'battle_scene_sprites',2688)

def add_menu_tree(rom,fields,base):
    from tools.menu_tree_fields import codec as menu
    return add_resource_fields(rom,fields,base,menu,'menu_tree',914)

def add_bank08_display(rom,fields,base):
    from tools.bank08_display_resources import codec as display
    return add_resource_fields(rom,fields,base,display,'bank08_display',1018)

def add_battle_effect_sprites(rom,fields,base):
    from tools.battle_effect_sprites import codec as effect
    return add_resource_fields(rom,fields,base,effect,'battle_effect_sprites',1864)

def add_bank06_display_tail(rom,fields,base):
    from tools.bank06_display_tail import codec as display
    return add_resource_fields(rom,fields,base,display,'bank06_display_tail',676)

def add_palette_copy_fields(rom,fields,base):
    from tools.palette_copy_fields import codec as palette
    return add_resource_fields(rom,fields,base,palette,'palette_copy_fields',668)

def add_menu_tile_streams(rom,fields,base):
    from tools.menu_tile_streams import codec as tiles
    return add_resource_fields(rom,fields,base,tiles,'menu_tile_streams',462)

def add_ui_fixed_records(rom,fields,base):
    from tools.ui_fixed_records import codec as records
    return add_resource_fields(rom,fields,base,records,'ui_fixed_records',342)

def add_battle_command_sprites(rom,fields,base):
    from tools.battle_command_sprites import codec as sprites
    return add_resource_fields(rom,fields,base,sprites,'battle_command_sprites',476)

def add_battle_deployment_parameters(rom,fields,base):
    from tools.battle_deployment_parameters import codec as params
    return add_resource_fields(rom,fields,base,params,'battle_deployment_parameters',36)

def add_battle_formation_coordinates(rom,fields,base):
    from tools.battle_formation_coordinates import codec as coords
    return add_resource_fields(rom,fields,base,coords,'battle_formation_coordinates',340)

def add_officer_lookup_parameters(rom,fields,base):
    from tools.officer_lookup_parameters import codec as params
    return add_resource_fields(rom,fields,base,params,'officer_lookup_parameters',12)

def add_education_factor_fields(rom,fields,base):
    from tools.education_factor_fields import codec as factors
    return add_resource_fields(rom,fields,base,factors,'education_factor_fields',25)

def add_battle_marker_sprites(rom,fields,base):
    from tools.battle_marker_sprites import codec as sprites
    return add_resource_fields(rom,fields,base,sprites,'battle_marker_sprites',123)

def add_ai_selection_fields(rom,fields,base):
    from tools.ai_selection_fields import codec as selection
    return add_resource_fields(rom,fields,base,selection,'ai_selection_fields',196)

def add_save_bitwidth_masks(rom,fields,base):
    from tools.save_bitwidth_masks import codec as masks
    return add_resource_fields(rom,fields,base,masks,'save_bitwidth_masks',132)

def add_battle_outcome_masks(rom,fields,base):
    from tools.battle_outcome_masks import codec as masks
    return add_resource_fields(rom,fields,base,masks,'battle_outcome_masks',19)

def add_indexed_action_parameters(rom,fields,base):
    from tools.indexed_action_parameters import codec as params
    return add_resource_fields(rom,fields,base,params,'indexed_action_parameters',336)

def add_city_cycle_parameters(rom,fields,base):
    from tools.city_cycle_parameters import codec as params
    return add_resource_fields(rom,fields,base,params,'city_cycle_parameters',26)

def add_header_vector_fields(rom,fields,base):
    from tools.header_vector_fields import codec as header
    return add_resource_fields(rom,fields,base,header,'header_vector_fields',512)

def add_officer_status_font_fields(rom,fields,base):
    from tools.officer_status_font_fields import codec as font
    return add_resource_fields(rom,fields,base,font,'officer_status_font_fields',80)

def add_duel_ui_row_stream_fields(rom,fields,base):
    from tools.duel_ui_row_stream_fields import codec as rows
    return add_resource_fields(rom,fields,base,rows,'duel_ui_row_stream_fields',296)

def add_ui_cursor_sprite_templates(rom,fields,base):
    from tools.ui_cursor_sprite_templates import codec as sprites
    return add_resource_fields(rom,fields,base,sprites,'ui_cursor_sprite_templates',1962)

def add_portrait_alias_tiles(rom,fields,base):
    from tools.portrait_alias_tiles import codec as tiles
    return add_resource_fields(rom,fields,base,tiles,'portrait_alias_tiles',1728)

def add_ai_threshold_pair_fields(rom,fields,base):
    from tools.ai_threshold_pair_fields import codec as thresholds
    return add_resource_fields(rom,fields,base,thresholds,'ai_threshold_pair_fields',192)

def add_setup_ui_sprite_fields(rom,fields,base):
    from tools.setup_ui_sprite_fields import codec as setup
    return add_resource_fields(rom,fields,base,setup,'setup_ui_sprite_fields',270)

def add_battle_cell_offsets(rom,fields,base):
    from tools.battle_cell_offsets import codec as cells
    return add_resource_fields(rom,fields,base,cells,'battle_cell_offsets',216)

def add_portrait_blank_alias_tiles(rom,fields,base):
    from tools.portrait_blank_alias_tiles import codec as tiles
    return add_resource_fields(rom,fields,base,tiles,'portrait_blank_alias_tiles',288)

def add_vdp_directory_fields(rom,fields,base):
    from tools.vdp_directory_fields import codec as directory
    return directory.add_to_layout(rom,fields,base)

def add_portrait_alias_metadata(rom,fields,base):
    from tools.portrait_alias_metadata import codec as metadata
    return add_resource_fields(rom,fields,base,metadata,'portrait_alias_metadata',1010)

def add_fm_instrument_alias_fields(rom,fields,base):
    from tools.fm_instrument_alias_fields import codec as instruments
    return add_resource_fields(rom,fields,base,instruments,'fm_instrument_alias_fields',3150)

def add_audio_frequency_fields(rom,fields,base):
    from tools.audio_frequency_fields import codec as frequencies
    return add_resource_fields(rom,fields,base,frequencies,'audio_frequency_fields',162)

def add_indexed_ui_lookup_fields(rom,fields,base):
    from tools.indexed_ui_lookup_fields import codec as lookups
    return add_resource_fields(rom,fields,base,lookups,'indexed_ui_lookup_fields',36)

def add_portrait_external_alias_pixels(rom,fields,base):
    from tools.portrait_external_alias_pixels import codec as pixels
    return add_resource_fields(rom,fields,base,pixels,'portrait_external_alias_pixels',142)

def add_ui_panel_row_stream_fields(rom,fields,base):
    from tools.ui_panel_row_stream_fields import codec as panels
    return add_resource_fields(rom,fields,base,panels,'ui_panel_row_stream_fields',180)

def add_boot_hardware_fields(rom,fields,base):
    from tools.boot_hardware_fields import codec as boot
    return add_resource_fields(rom,fields,base,boot,'boot_hardware_fields',70)

def add_fm_external_alias_fields(rom,fields,base):
    from tools.fm_external_alias_fields import codec as instruments
    return add_resource_fields(rom,fields,base,instruments,'fm_external_alias_fields',4245)

def add_battle_probability_word_fields(rom,fields,base):
    from tools.battle_probability_word_fields import codec as predicates
    return add_resource_fields(rom,fields,base,predicates,'battle_probability_word_fields',300)

def add_scene_ui_panel_fields(rom,fields,base):
    from tools.scene_ui_panel_fields import codec as panels
    return add_resource_fields(rom,fields,base,panels,'scene_ui_panel_fields',160)

def add_scene_audio_command_word_fields(rom,fields,base):
    from tools.scene_audio_command_word_fields import codec as commands
    return add_resource_fields(rom,fields,base,commands,'scene_audio_command_word_fields',80)

def add_troop_movement_source_fields(rom,fields,base):
    from tools.troop_movement_source_fields import codec as movement
    return add_resource_fields(rom,fields,base,movement,'troop_movement_source_fields',24)

def add_font_source_alias_fields(rom,fields,base):
    from tools.font_source_alias_fields import codec as font_aliases
    return add_resource_fields(rom,fields,base,font_aliases,'font_source_alias_fields',574)

def add_scene_coordinate_word_fields(rom,fields,base):
    from tools.scene_coordinate_word_fields import codec as coordinates
    return add_resource_fields(rom,fields,base,coordinates,'scene_coordinate_word_fields',32)

def add_selected_tile_row_word_fields(rom,fields,base):
    from tools.selected_tile_row_word_fields import codec as rows
    return add_resource_fields(rom,fields,base,rows,'selected_tile_row_word_fields',128)

def add_stage_cursor_sprite_fields(rom,fields,base):
    from tools.stage_cursor_sprite_fields import codec as sprites
    return add_resource_fields(rom,fields,base,sprites,'stage_cursor_sprite_fields',180)

def add_ui_resource_word_sources(rom,fields,base):
    from tools.ui_resource_word_sources import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_resource_word_sources',250)

def add_runtime_indexed_source_fields(rom,fields,base):
    from tools.runtime_indexed_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'runtime_indexed_source_fields',172)

def add_diplomacy_parameter_word_fields(rom,fields,base):
    from tools.diplomacy_parameter_word_fields import codec as words
    return add_resource_fields(rom,fields,base,words,'diplomacy_parameter_word_fields',102)

def add_ui_state_dispatch_source_fields(rom,fields,base):
    from tools.ui_state_dispatch_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_state_dispatch_source_fields',274)

def add_ui_runtime_source_fields(rom,fields,base):
    from tools.ui_runtime_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_runtime_source_fields',246)

def add_render_selector_source_fields(rom,fields,base):
    from tools.render_selector_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'render_selector_source_fields',272)

def add_battle_action_byte_fields(rom,fields,base):
    from tools.battle_action_byte_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'battle_action_byte_fields',144)

def add_battle_action_rng_word_fields(rom,fields,base):
    from tools.battle_action_rng_word_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'battle_action_rng_word_fields',60)

def add_state_dispatch_word_fields(rom,fields,base):
    from tools.state_dispatch_word_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'state_dispatch_word_fields',190)

def add_display_motion_source_fields(rom,fields,base):
    from tools.display_motion_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'display_motion_source_fields',168)

def add_menu_scalar_source_fields(rom,fields,base):
    from tools.menu_scalar_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'menu_scalar_source_fields',224)

def add_ui_selector_pair_fields(rom,fields,base):
    from tools.ui_selector_pair_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_selector_pair_fields',232)

def add_counted_ui_row_sources(rom,fields,base):
    from tools.counted_ui_row_sources import codec as sources
    return add_resource_fields(rom,fields,base,sources,'counted_ui_row_sources',304)

def add_growth_threshold_word_fields(rom,fields,base):
    from tools.growth_threshold_word_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'growth_threshold_word_fields',52)

def add_compact_ui_sprite_fields(rom,fields,base):
    from tools.compact_ui_sprite_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'compact_ui_sprite_fields',170)

def add_ui_literal_parameter_sources(rom,fields,base):
    from tools.ui_literal_parameter_sources import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_literal_parameter_sources',184)

def add_z80_startup_seed_fields(rom,fields,base):
    from tools.z80_startup_seed_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'z80_startup_seed_fields',13)

def add_parameter_ui_word_sources(rom,fields,base):
    from tools.parameter_ui_word_sources import codec as sources
    return add_resource_fields(rom,fields,base,sources,'parameter_ui_word_sources',165)

def add_counted_ui_shared_sources(rom,fields,base):
    from tools.counted_ui_shared_sources import codec as sources
    return add_resource_fields(rom,fields,base,sources,'counted_ui_shared_sources',96)

def add_boot_queue_dispatch_source_fields(rom,fields,base):
    from tools.boot_queue_dispatch_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'boot_queue_dispatch_source_fields',142)

def add_counted_glyph_source_fields(rom,fields,base):
    from tools.counted_glyph_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'counted_glyph_source_fields',253)

def add_indexed_command_source_fields(rom,fields,base):
    from tools.indexed_command_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_command_source_fields',274)

def add_ui_tile_byte_alias_fields(rom,fields,base):
    from tools.ui_tile_byte_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'ui_tile_byte_alias_fields',36)

def add_fm_sparse_alias_fields(rom,fields,base):
    from tools.fm_sparse_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'fm_sparse_alias_fields',20)

def add_roster_pointer_source_alias_fields(rom,fields,base):
    from tools.roster_pointer_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'roster_pointer_source_alias_fields',1320)

def add_indexed_scalar_source_fields(rom,fields,base):
    from tools.indexed_scalar_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_scalar_source_fields',214)

def add_portrait_frontier_word_fields(rom,fields,base):
    from tools.portrait_frontier_word_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'portrait_frontier_word_fields',8)

def add_indexed_lowbank_source_alias_fields(rom,fields,base):
    from tools.indexed_lowbank_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_lowbank_source_alias_fields',1170)

def add_increment_selector_source_alias_fields(rom,fields,base):
    from tools.increment_selector_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'increment_selector_source_alias_fields',1644)

def add_indexed_command_source_alias_fields(rom,fields,base):
    from tools.indexed_command_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_command_source_alias_fields',1260)

def add_indexed_pair_source_alias_fields(rom,fields,base):
    from tools.indexed_pair_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_pair_source_alias_fields',321)

def add_vdp_empty_marker_fields(rom,fields,base):
    from tools.vdp_empty_marker_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'vdp_empty_marker_fields',1)

def add_terrain_neighbor_source_alias_fields(rom,fields,base):
    from tools.terrain_neighbor_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'terrain_neighbor_source_alias_fields',13504)

def add_rle_gap_source_alias_fields(rom,fields,base):
    from tools.rle_gap_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'rle_gap_source_alias_fields',542)

def add_battle_map_source_alias_fields(rom,fields,base):
    from tools.battle_map_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'battle_map_source_alias_fields',1460)

def add_duel_record_source_alias_fields(rom,fields,base):
    from tools.duel_record_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'duel_record_source_alias_fields',16)

def add_city_neighbor_source_alias_fields(rom,fields,base):
    from tools.city_neighbor_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'city_neighbor_source_alias_fields',8247)

def add_cart_mirrored_tile_source_alias_fields(rom,fields,base):
    from tools.cart_mirrored_tile_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'cart_mirrored_tile_source_alias_fields',90)

def add_indexed_transfer_source_alias_fields(rom,fields,base):
    from tools.indexed_transfer_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'indexed_transfer_source_alias_fields',78)

def add_camera_chunk_source_alias_fields(rom,fields,base):
    from tools.camera_chunk_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'camera_chunk_source_alias_fields',403)

def add_initial_map_source_alias_fields(rom,fields,base):
    from tools.initial_map_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'initial_map_source_alias_fields',19)

def add_scene_descriptor_source_alias_fields(rom,fields,base):
    from tools.scene_descriptor_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'scene_descriptor_source_alias_fields',559)

def add_conditional_scene_rle_source_fields(rom,fields,base):
    from tools.conditional_scene_rle_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'conditional_scene_rle_source_fields',958)

def add_scene_object_source_alias_fields(rom,fields,base):
    from tools.scene_object_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'scene_object_source_alias_fields',697)

def add_object_motion_source_alias_fields(rom,fields,base):
    from tools.object_motion_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'object_motion_source_alias_fields',1343)

def add_object_residue_source_alias_fields(rom,fields,base):
    from tools.object_residue_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'object_residue_source_alias_fields',195)

def add_object_id_source_alias_fields(rom,fields,base):
    from tools.object_id_source_alias_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'object_id_source_alias_fields',200)

def add_fullword_scene_rle_source_fields(rom,fields,base):
    from tools.fullword_scene_rle_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'fullword_scene_rle_source_fields',9245)

def add_scene_gap_rle_source_fields(rom,fields,base):
    from tools.scene_gap_rle_source_fields import codec as sources
    return add_resource_fields(rom,fields,base,sources,'scene_gap_rle_source_fields',542)

def overlay(rom,base_image,code):
    if type(base_image)is not bytes or len(base_image)!=f.ROM_SIZE:raise ValueError('full baseline image required')
    rows=inventory(rom)
    if len(code)!=rows[-1]['address']+rows[-1]['size']:raise ValueError('code image extent changed')
    result=bytearray(base_image)
    for r in rows:
        a,z=r['address'],r['address']+r['size'];result[a:z]=code[a:z]
    return bytes(result)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','prepare','verify-object','verify-image'))
    p.add_argument('--rom',default=str(f.DEFAULT_ROM));p.add_argument('--source',default=str(SOURCE));p.add_argument('--output-root')
    p.add_argument('--object');p.add_argument('--image');p.add_argument('--canonical',action='store_true');p.add_argument('--rom-image');p.add_argument('--base-image')
    p.add_argument('--sprite-word-fields')
    p.add_argument('--battle-variant-fields')
    p.add_argument('--dispatch-source')
    p.add_argument('--world-chunk-fields')
    p.add_argument('--nested-dispatch-source')
    p.add_argument('--compact-sprite-fields')
    p.add_argument('--final-dispatch-source')
    p.add_argument('--scene-sprite-fields')
    p.add_argument('--scene-tile-fields')
    p.add_argument('--battle-overlay-fields')
    p.add_argument('--audio-root-fields')
    p.add_argument('--display-tile-fields')
    p.add_argument('--battle-rule-fields')
    p.add_argument('--battle-palette-fields')
    p.add_argument('--z80-source')
    p.add_argument('--boot-z80-source')
    p.add_argument('--audio-dispatch-fields')
    p.add_argument('--legacy-text-fields')
    p.add_argument('--title-overlay-fields')
    p.add_argument('--transport-cargo-fields')
    p.add_argument('--battle-scene-sprite-fields')
    p.add_argument('--menu-tree-fields')
    p.add_argument('--bank08-display-fields')
    p.add_argument('--secondary-dispatch-source')
    p.add_argument('--battle-effect-sprite-fields')
    p.add_argument('--bank06-display-tail-fields')
    p.add_argument('--palette-copy-fields')
    p.add_argument('--menu-tile-stream-fields')
    p.add_argument('--ui-fixed-record-fields')
    p.add_argument('--battle-command-sprite-fields')
    p.add_argument('--battle-deployment-parameter-fields')
    p.add_argument('--battle-formation-coordinate-fields')
    p.add_argument('--officer-lookup-parameter-fields')
    p.add_argument('--education-factor-fields')
    p.add_argument('--battle-marker-sprite-fields')
    p.add_argument('--ai-selection-fields')
    p.add_argument('--save-bitwidth-mask-fields')
    p.add_argument('--battle-outcome-mask-fields')
    p.add_argument('--indexed-action-parameter-fields')
    p.add_argument('--city-cycle-parameter-fields')
    p.add_argument('--header-vector-fields')
    p.add_argument('--officer-status-font-fields')
    p.add_argument('--duel-ui-row-stream-fields')
    p.add_argument('--ui-cursor-sprite-template-fields')
    p.add_argument('--portrait-alias-tile-fields')
    p.add_argument('--ai-threshold-pair-fields')
    p.add_argument('--setup-ui-sprite-fields')
    p.add_argument('--battle-cell-offset-fields')
    p.add_argument('--portrait-blank-alias-tile-fields')
    p.add_argument('--vdp-directory-fields')
    p.add_argument('--portrait-alias-metadata-fields')
    p.add_argument('--fm-instrument-alias-fields')
    p.add_argument('--audio-frequency-fields')
    p.add_argument('--indexed-ui-lookup-fields')
    p.add_argument('--portrait-external-alias-pixel-fields')
    p.add_argument('--ui-panel-row-stream-fields')
    p.add_argument('--boot-hardware-fields')
    p.add_argument('--fm-external-alias-fields')
    p.add_argument('--battle-probability-word-fields')
    p.add_argument('--scene-ui-panel-fields')
    p.add_argument('--scene-audio-command-word-fields')
    p.add_argument('--troop-movement-source-fields')
    p.add_argument('--font-source-alias-fields')
    p.add_argument('--scene-coordinate-word-fields')
    p.add_argument('--selected-tile-row-word-fields')
    p.add_argument('--stage-cursor-sprite-fields')
    p.add_argument('--ui-resource-word-sources')
    p.add_argument('--runtime-indexed-source-fields')
    p.add_argument('--diplomacy-parameter-word-fields')
    p.add_argument('--ui-state-dispatch-source-fields')
    p.add_argument('--ui-runtime-source-fields')
    p.add_argument('--render-selector-source-fields')
    p.add_argument('--battle-action-byte-fields')
    p.add_argument('--battle-action-rng-word-fields')
    p.add_argument('--state-dispatch-word-fields')
    p.add_argument('--display-motion-source-fields')
    p.add_argument('--menu-scalar-source-fields')
    p.add_argument('--ui-selector-pair-fields')
    p.add_argument('--counted-ui-row-sources')
    p.add_argument('--growth-threshold-word-fields')
    p.add_argument('--compact-ui-sprite-fields')
    p.add_argument('--ui-literal-parameter-sources')
    p.add_argument('--z80-startup-seed-fields')
    p.add_argument('--parameter-ui-word-sources')
    p.add_argument('--counted-ui-shared-sources')
    p.add_argument('--boot-queue-dispatch-source-fields')
    p.add_argument('--counted-glyph-source-fields')
    p.add_argument('--indexed-command-source-fields')
    p.add_argument('--ui-tile-byte-alias-fields')
    p.add_argument('--fm-sparse-alias-fields')
    p.add_argument('--roster-pointer-source-alias-fields')
    p.add_argument('--indexed-scalar-source-fields')
    p.add_argument('--portrait-frontier-word-fields')
    p.add_argument('--indexed-lowbank-source-alias-fields')
    p.add_argument('--increment-selector-source-alias-fields')
    p.add_argument('--indexed-command-source-alias-fields')
    p.add_argument('--indexed-pair-source-alias-fields')
    p.add_argument('--vdp-empty-marker-fields')
    p.add_argument('--terrain-neighbor-source-alias-fields')
    p.add_argument('--rle-gap-source-alias-fields')
    p.add_argument('--battle-map-source-alias-fields')
    p.add_argument('--duel-record-source-alias-fields')
    p.add_argument('--city-neighbor-source-alias-fields')
    p.add_argument('--cart-mirrored-tile-source-alias-fields')
    p.add_argument('--indexed-transfer-source-alias-fields')
    p.add_argument('--camera-chunk-source-alias-fields')
    p.add_argument('--initial-map-source-alias-fields')
    p.add_argument('--scene-descriptor-source-alias-fields')
    p.add_argument('--conditional-scene-rle-source-fields')
    p.add_argument('--scene-object-source-alias-fields')
    p.add_argument('--object-motion-source-alias-fields')
    p.add_argument('--object-residue-source-alias-fields')
    p.add_argument('--object-id-source-alias-fields')
    p.add_argument('--fullword-scene-rle-source-fields')
    p.add_argument('--scene-gap-rle-source-fields')
    args=p.parse_args(argv);rom=m.read(args.rom,f.ROM_SIZE)
    if args.command=='export':
        if not args.output_root:raise ValueError('fresh output-root required')
        target=m.af.safe_path(args.output_root);m.af._separate(target,[m.af.safe_path(args.rom,regular_input=True)])
        if target.exists():raise ValueError('fresh output directory required')
        bundle=export_bundle(rom);target.mkdir(parents=True)
        for name,data in bundle.items():
            with (target/name).open('xb') as stream:stream.write(data)
        print(m.sha(bundle['instructions.json']))
    elif args.command=='prepare':
        if not args.output_root:raise ValueError('output-root required')
        target=m.af.safe_path(args.output_root);owned=ROOT/'build/direct_code'
        if target==owned or owned not in target.parents:raise ValueError('normal layout output must stay in build/direct_code')
        target.parent.mkdir(parents=True,exist_ok=True)
        result=add_to_layout(rom,m.read(args.source),base_layout(rom))
        if args.sprite_word_fields:
            from tools.sprite_word_resources import codec as sprite
            result=add_sprite_resources(rom,sprite.load_fields(m.read(args.sprite_word_fields)),result)
        if args.battle_variant_fields:
            from tools.battle_variant_tiles import codec as variant
            result=add_battle_variants(rom,variant.load_fields(m.read(args.battle_variant_fields)),result)
        if args.dispatch_source:
            from tools.dispatch_code import dispatch_code as dispatch
            result=dispatch.add_to_layout(rom,m.read(args.dispatch_source),result)
        if args.world_chunk_fields:
            from tools.world_tile_chunks import codec as world
            result=add_world_chunks(rom,world.load_fields(m.read(args.world_chunk_fields)),result)
        if args.nested_dispatch_source:
            from tools.nested_dispatch_code import nested_dispatch_code as nested
            result=nested.add_to_layout(rom,m.read(args.nested_dispatch_source),result)
        if args.compact_sprite_fields:
            from tools.compact_sprite_records import codec as compact
            result=add_compact_sprites(rom,compact.load_fields(m.read(args.compact_sprite_fields)),result)
        if args.final_dispatch_source:
            from tools.final_dispatch_code import final_dispatch_code as final
            result=final.add_to_layout(rom,m.read(args.final_dispatch_source),result)
        if args.scene_sprite_fields:
            from tools.scene_sprite_resources import codec as scene
            result=add_scene_sprites(rom,scene.load_fields(m.read(args.scene_sprite_fields)),result)
        if args.scene_tile_fields:
            from tools.scene_tile_resources import codec as scene
            result=add_scene_tiles(rom,scene.load_fields(m.read(args.scene_tile_fields)),result)
        if args.battle_overlay_fields:
            from tools.battle_overlay_maps import codec as overlay
            result=add_battle_overlays(rom,overlay.load_fields(m.read(args.battle_overlay_fields)),result)
        if args.audio_root_fields:
            from tools.audio_root_resources import codec as audio
            result=add_audio_roots(rom,audio.load_fields(m.read(args.audio_root_fields)),result)
        if args.display_tile_fields:
            from tools.display_tile_resources import codec as display
            result=add_display_tiles(rom,display.load_fields(m.read(args.display_tile_fields)),result)
        if args.battle_rule_fields:
            from tools.battle_rule_tables import codec as rules
            result=add_battle_rules(rom,rules.load_fields(m.read(args.battle_rule_fields)),result)
        if args.battle_palette_fields:
            from tools.battle_palette_transfers import codec as palette
            result=add_battle_palettes(rom,palette.load_fields(m.read(args.battle_palette_fields)),result)
        if args.z80_source:
            from tools.z80_code import z80_code as z80
            result=z80.add_to_layout(rom,m.read(args.z80_source),result)
        if args.audio_dispatch_fields:
            from tools.audio_dispatch_fields import codec as audio
            result=add_audio_dispatch(rom,audio.load_fields(m.read(args.audio_dispatch_fields)),result)
        if args.legacy_text_fields:
            from tools.legacy_text_fields import codec as text
            result=add_legacy_text(rom,text.load_fields(m.read(args.legacy_text_fields)),result)
        if args.title_overlay_fields:
            from tools.title_overlay_maps import codec as title
            result=add_title_overlays(rom,title.load_fields(m.read(args.title_overlay_fields)),result)
        if args.transport_cargo_fields:
            from tools.transport_cargo_build import codec as cargo
            result=add_transport_cargo(rom,cargo.load_fields(m.read(args.transport_cargo_fields)),result)
        if args.battle_scene_sprite_fields:
            from tools.battle_scene_sprites import codec as scene
            result=add_battle_scene_sprites(rom,scene.load_fields(m.read(args.battle_scene_sprite_fields)),result)
        if args.menu_tree_fields:
            from tools.menu_tree_fields import codec as menu
            result=add_menu_tree(rom,menu.load_fields(m.read(args.menu_tree_fields)),result)
        if args.bank08_display_fields:
            from tools.bank08_display_resources import codec as display
            result=add_bank08_display(rom,display.load_fields(m.read(args.bank08_display_fields)),result)
        if args.battle_effect_sprite_fields:
            from tools.battle_effect_sprites import codec as effect
            result=add_battle_effect_sprites(rom,effect.load_fields(m.read(args.battle_effect_sprite_fields)),result)
        if args.bank06_display_tail_fields:
            from tools.bank06_display_tail import codec as display
            result=add_bank06_display_tail(rom,display.load_fields(m.read(args.bank06_display_tail_fields)),result)
        if args.palette_copy_fields:
            from tools.palette_copy_fields import codec as palette
            result=add_palette_copy_fields(rom,palette.load_fields(m.read(args.palette_copy_fields)),result)
        if args.menu_tile_stream_fields:
            from tools.menu_tile_streams import codec as tiles
            result=add_menu_tile_streams(rom,tiles.load_fields(m.read(args.menu_tile_stream_fields)),result)
        if args.ui_fixed_record_fields:
            from tools.ui_fixed_records import codec as records
            result=add_ui_fixed_records(rom,records.load_fields(m.read(args.ui_fixed_record_fields)),result)
        if args.battle_command_sprite_fields:
            from tools.battle_command_sprites import codec as sprites
            result=add_battle_command_sprites(rom,sprites.load_fields(m.read(args.battle_command_sprite_fields)),result)
        if args.battle_deployment_parameter_fields:
            from tools.battle_deployment_parameters import codec as params
            result=add_battle_deployment_parameters(rom,params.load_fields(m.read(args.battle_deployment_parameter_fields)),result)
        if args.battle_formation_coordinate_fields:
            from tools.battle_formation_coordinates import codec as coords
            result=add_battle_formation_coordinates(rom,coords.load_fields(m.read(args.battle_formation_coordinate_fields)),result)
        if args.officer_lookup_parameter_fields:
            from tools.officer_lookup_parameters import codec as params
            result=add_officer_lookup_parameters(rom,params.load_fields(m.read(args.officer_lookup_parameter_fields)),result)
        if args.education_factor_fields:
            from tools.education_factor_fields import codec as factors
            result=add_education_factor_fields(rom,factors.load_fields(m.read(args.education_factor_fields)),result)
        if args.battle_marker_sprite_fields:
            from tools.battle_marker_sprites import codec as sprites
            result=add_battle_marker_sprites(rom,sprites.load_fields(m.read(args.battle_marker_sprite_fields)),result)
        if args.ai_selection_fields:
            from tools.ai_selection_fields import codec as selection
            result=add_ai_selection_fields(rom,selection.load_fields(m.read(args.ai_selection_fields)),result)
        if args.save_bitwidth_mask_fields:
            from tools.save_bitwidth_masks import codec as masks
            result=add_save_bitwidth_masks(rom,masks.load_fields(m.read(args.save_bitwidth_mask_fields)),result)
        if args.battle_outcome_mask_fields:
            from tools.battle_outcome_masks import codec as masks
            result=add_battle_outcome_masks(rom,masks.load_fields(m.read(args.battle_outcome_mask_fields)),result)
        if args.indexed_action_parameter_fields:
            from tools.indexed_action_parameters import codec as params
            result=add_indexed_action_parameters(rom,params.load_fields(m.read(args.indexed_action_parameter_fields)),result)
        if args.city_cycle_parameter_fields:
            from tools.city_cycle_parameters import codec as params
            result=add_city_cycle_parameters(rom,params.load_fields(m.read(args.city_cycle_parameter_fields)),result)
        if args.header_vector_fields:
            from tools.header_vector_fields import codec as header
            result=add_header_vector_fields(rom,header.load_fields(m.read(args.header_vector_fields)),result)
        if args.officer_status_font_fields:
            from tools.officer_status_font_fields import codec as font
            result=add_officer_status_font_fields(rom,font.load_fields(m.read(args.officer_status_font_fields)),result)
        if args.duel_ui_row_stream_fields:
            from tools.duel_ui_row_stream_fields import codec as rows
            result=add_duel_ui_row_stream_fields(rom,rows.load_fields(m.read(args.duel_ui_row_stream_fields)),result)
        if args.ui_cursor_sprite_template_fields:
            from tools.ui_cursor_sprite_templates import codec as sprites
            result=add_ui_cursor_sprite_templates(rom,sprites.load_fields(m.read(args.ui_cursor_sprite_template_fields)),result)
        if args.portrait_alias_tile_fields:
            from tools.portrait_alias_tiles import codec as tiles
            result=add_portrait_alias_tiles(rom,tiles.load_fields(m.read(args.portrait_alias_tile_fields)),result)
        if args.ai_threshold_pair_fields:
            from tools.ai_threshold_pair_fields import codec as thresholds
            result=add_ai_threshold_pair_fields(rom,thresholds.load_fields(m.read(args.ai_threshold_pair_fields)),result)
        if args.setup_ui_sprite_fields:
            from tools.setup_ui_sprite_fields import codec as setup
            result=add_setup_ui_sprite_fields(rom,setup.load_fields(m.read(args.setup_ui_sprite_fields)),result)
        if args.battle_cell_offset_fields:
            from tools.battle_cell_offsets import codec as cells
            result=add_battle_cell_offsets(rom,cells.load_fields(m.read(args.battle_cell_offset_fields)),result)
        if args.portrait_blank_alias_tile_fields:
            from tools.portrait_blank_alias_tiles import codec as tiles
            result=add_portrait_blank_alias_tiles(rom,tiles.load_fields(m.read(args.portrait_blank_alias_tile_fields)),result)
        if args.vdp_directory_fields:
            from tools.vdp_directory_fields import codec as directory
            result=add_vdp_directory_fields(rom,directory.load_fields(m.read(args.vdp_directory_fields)),result)
        if args.portrait_alias_metadata_fields:
            from tools.portrait_alias_metadata import codec as metadata
            result=add_portrait_alias_metadata(rom,metadata.load_fields(m.read(args.portrait_alias_metadata_fields)),result)
        if args.fm_instrument_alias_fields:
            from tools.fm_instrument_alias_fields import codec as instruments
            result=add_fm_instrument_alias_fields(rom,instruments.load_fields(m.read(args.fm_instrument_alias_fields)),result)
        if args.audio_frequency_fields:
            from tools.audio_frequency_fields import codec as frequencies
            result=add_audio_frequency_fields(rom,frequencies.load_fields(m.read(args.audio_frequency_fields)),result)
        if args.indexed_ui_lookup_fields:
            from tools.indexed_ui_lookup_fields import codec as lookups
            result=add_indexed_ui_lookup_fields(rom,lookups.load_fields(m.read(args.indexed_ui_lookup_fields)),result)
        if args.portrait_external_alias_pixel_fields:
            from tools.portrait_external_alias_pixels import codec as pixels
            result=add_portrait_external_alias_pixels(rom,pixels.load_fields(m.read(args.portrait_external_alias_pixel_fields)),result)
        if args.ui_panel_row_stream_fields:
            from tools.ui_panel_row_stream_fields import codec as panels
            result=add_ui_panel_row_stream_fields(rom,panels.load_fields(m.read(args.ui_panel_row_stream_fields)),result)
        if args.boot_hardware_fields:
            from tools.boot_hardware_fields import codec as boot
            result=add_boot_hardware_fields(rom,boot.load_fields(m.read(args.boot_hardware_fields)),result)
        if args.fm_external_alias_fields:
            from tools.fm_external_alias_fields import codec as instruments
            result=add_fm_external_alias_fields(rom,instruments.load_fields(m.read(args.fm_external_alias_fields)),result)
        if args.battle_probability_word_fields:
            from tools.battle_probability_word_fields import codec as predicates
            result=add_battle_probability_word_fields(rom,predicates.load_fields(m.read(args.battle_probability_word_fields)),result)
        if args.scene_ui_panel_fields:
            from tools.scene_ui_panel_fields import codec as panels
            result=add_scene_ui_panel_fields(rom,panels.load_fields(m.read(args.scene_ui_panel_fields)),result)
        if args.scene_audio_command_word_fields:
            from tools.scene_audio_command_word_fields import codec as commands
            result=add_scene_audio_command_word_fields(rom,commands.load_fields(m.read(args.scene_audio_command_word_fields)),result)
        if args.troop_movement_source_fields:
            from tools.troop_movement_source_fields import codec as movement
            result=add_troop_movement_source_fields(rom,movement.load_fields(m.read(args.troop_movement_source_fields)),result)
        if args.font_source_alias_fields:
            from tools.font_source_alias_fields import codec as font_aliases
            result=add_font_source_alias_fields(rom,font_aliases.load_fields(m.read(args.font_source_alias_fields)),result)
        if args.scene_coordinate_word_fields:
            from tools.scene_coordinate_word_fields import codec as coordinates
            result=add_scene_coordinate_word_fields(rom,coordinates.load_fields(m.read(args.scene_coordinate_word_fields)),result)
        if args.selected_tile_row_word_fields:
            from tools.selected_tile_row_word_fields import codec as rows
            result=add_selected_tile_row_word_fields(rom,rows.load_fields(m.read(args.selected_tile_row_word_fields)),result)
        if args.stage_cursor_sprite_fields:
            from tools.stage_cursor_sprite_fields import codec as sprites
            result=add_stage_cursor_sprite_fields(rom,sprites.load_fields(m.read(args.stage_cursor_sprite_fields)),result)
        if args.ui_resource_word_sources:
            from tools.ui_resource_word_sources import codec as sources
            result=add_ui_resource_word_sources(rom,sources.load_fields(m.read(args.ui_resource_word_sources)),result)
        if args.runtime_indexed_source_fields:
            from tools.runtime_indexed_source_fields import codec as sources
            result=add_runtime_indexed_source_fields(rom,sources.load_fields(m.read(args.runtime_indexed_source_fields)),result)
        if args.diplomacy_parameter_word_fields:
            from tools.diplomacy_parameter_word_fields import codec as words
            result=add_diplomacy_parameter_word_fields(rom,words.load_fields(m.read(args.diplomacy_parameter_word_fields)),result)
        if args.ui_state_dispatch_source_fields:
            from tools.ui_state_dispatch_source_fields import codec as sources
            result=add_ui_state_dispatch_source_fields(rom,sources.load_fields(m.read(args.ui_state_dispatch_source_fields)),result)
        if args.ui_runtime_source_fields:
            from tools.ui_runtime_source_fields import codec as sources
            result=add_ui_runtime_source_fields(rom,sources.load_fields(m.read(args.ui_runtime_source_fields)),result)
        if args.render_selector_source_fields:
            from tools.render_selector_source_fields import codec as sources
            result=add_render_selector_source_fields(rom,sources.load_fields(m.read(args.render_selector_source_fields)),result)
        if args.battle_action_byte_fields:
            from tools.battle_action_byte_fields import codec as sources
            result=add_battle_action_byte_fields(rom,sources.load_fields(m.read(args.battle_action_byte_fields)),result)
        if args.battle_action_rng_word_fields:
            from tools.battle_action_rng_word_fields import codec as sources
            result=add_battle_action_rng_word_fields(rom,sources.load_fields(m.read(args.battle_action_rng_word_fields)),result)
        if args.state_dispatch_word_fields:
            from tools.state_dispatch_word_fields import codec as sources
            result=add_state_dispatch_word_fields(rom,sources.load_fields(m.read(args.state_dispatch_word_fields)),result)
        if args.display_motion_source_fields:
            from tools.display_motion_source_fields import codec as sources
            result=add_display_motion_source_fields(rom,sources.load_fields(m.read(args.display_motion_source_fields)),result)
        if args.menu_scalar_source_fields:
            from tools.menu_scalar_source_fields import codec as sources
            result=add_menu_scalar_source_fields(rom,sources.load_fields(m.read(args.menu_scalar_source_fields)),result)
        if args.ui_selector_pair_fields:
            from tools.ui_selector_pair_fields import codec as sources
            result=add_ui_selector_pair_fields(rom,sources.load_fields(m.read(args.ui_selector_pair_fields)),result)
        if args.counted_ui_row_sources:
            from tools.counted_ui_row_sources import codec as sources
            result=add_counted_ui_row_sources(rom,sources.load_fields(m.read(args.counted_ui_row_sources)),result)
        if args.growth_threshold_word_fields:
            from tools.growth_threshold_word_fields import codec as sources
            result=add_growth_threshold_word_fields(rom,sources.load_fields(m.read(args.growth_threshold_word_fields)),result)
        if args.compact_ui_sprite_fields:
            from tools.compact_ui_sprite_fields import codec as sources
            result=add_compact_ui_sprite_fields(rom,sources.load_fields(m.read(args.compact_ui_sprite_fields)),result)
        if args.ui_literal_parameter_sources:
            from tools.ui_literal_parameter_sources import codec as sources
            result=add_ui_literal_parameter_sources(rom,sources.load_fields(m.read(args.ui_literal_parameter_sources)),result)
        if args.z80_startup_seed_fields:
            from tools.z80_startup_seed_fields import codec as sources
            result=add_z80_startup_seed_fields(rom,sources.load_fields(m.read(args.z80_startup_seed_fields)),result)
        if args.parameter_ui_word_sources:
            from tools.parameter_ui_word_sources import codec as sources
            result=add_parameter_ui_word_sources(rom,sources.load_fields(m.read(args.parameter_ui_word_sources)),result)
        if args.counted_ui_shared_sources:
            from tools.counted_ui_shared_sources import codec as sources
            result=add_counted_ui_shared_sources(rom,sources.load_fields(m.read(args.counted_ui_shared_sources)),result)
        if args.boot_queue_dispatch_source_fields:
            from tools.boot_queue_dispatch_source_fields import codec as sources
            result=add_boot_queue_dispatch_source_fields(rom,sources.load_fields(m.read(args.boot_queue_dispatch_source_fields)),result)
        if args.counted_glyph_source_fields:
            from tools.counted_glyph_source_fields import codec as sources
            result=add_counted_glyph_source_fields(rom,sources.load_fields(m.read(args.counted_glyph_source_fields)),result)
        if args.indexed_command_source_fields:
            from tools.indexed_command_source_fields import codec as sources
            result=add_indexed_command_source_fields(rom,sources.load_fields(m.read(args.indexed_command_source_fields)),result)
        if args.ui_tile_byte_alias_fields:
            from tools.ui_tile_byte_alias_fields import codec as sources
            result=add_ui_tile_byte_alias_fields(rom,sources.load_fields(m.read(args.ui_tile_byte_alias_fields)),result)
        if args.fm_sparse_alias_fields:
            from tools.fm_sparse_alias_fields import codec as sources
            result=add_fm_sparse_alias_fields(rom,sources.load_fields(m.read(args.fm_sparse_alias_fields)),result)
        if args.roster_pointer_source_alias_fields:
            from tools.roster_pointer_source_alias_fields import codec as sources
            result=add_roster_pointer_source_alias_fields(rom,sources.load_fields(m.read(args.roster_pointer_source_alias_fields)),result)
        if args.indexed_scalar_source_fields:
            from tools.indexed_scalar_source_fields import codec as sources
            result=add_indexed_scalar_source_fields(rom,sources.load_fields(m.read(args.indexed_scalar_source_fields)),result)
        if args.portrait_frontier_word_fields:
            from tools.portrait_frontier_word_fields import codec as sources
            result=add_portrait_frontier_word_fields(rom,sources.load_fields(m.read(args.portrait_frontier_word_fields)),result)
        if args.indexed_lowbank_source_alias_fields:
            from tools.indexed_lowbank_source_alias_fields import codec as sources
            result=add_indexed_lowbank_source_alias_fields(rom,sources.load_fields(m.read(args.indexed_lowbank_source_alias_fields)),result)
        if args.increment_selector_source_alias_fields:
            from tools.increment_selector_source_alias_fields import codec as sources
            result=add_increment_selector_source_alias_fields(rom,sources.load_fields(m.read(args.increment_selector_source_alias_fields)),result)
        if args.indexed_command_source_alias_fields:
            from tools.indexed_command_source_alias_fields import codec as sources
            result=add_indexed_command_source_alias_fields(rom,sources.load_fields(m.read(args.indexed_command_source_alias_fields)),result)
        if args.indexed_pair_source_alias_fields:
            from tools.indexed_pair_source_alias_fields import codec as sources
            result=add_indexed_pair_source_alias_fields(rom,sources.load_fields(m.read(args.indexed_pair_source_alias_fields)),result)
        if args.vdp_empty_marker_fields:
            from tools.vdp_empty_marker_fields import codec as sources
            result=add_vdp_empty_marker_fields(rom,sources.load_fields(m.read(args.vdp_empty_marker_fields)),result)
        if args.terrain_neighbor_source_alias_fields:
            from tools.terrain_neighbor_source_alias_fields import codec as sources
            result=add_terrain_neighbor_source_alias_fields(rom,sources.load_fields(m.read(args.terrain_neighbor_source_alias_fields)),result)
        if args.rle_gap_source_alias_fields:
            from tools.rle_gap_source_alias_fields import codec as sources
            result=add_rle_gap_source_alias_fields(rom,sources.load_fields(m.read(args.rle_gap_source_alias_fields)),result)
        if args.battle_map_source_alias_fields:
            from tools.battle_map_source_alias_fields import codec as sources
            result=add_battle_map_source_alias_fields(rom,sources.load_fields(m.read(args.battle_map_source_alias_fields)),result)
        if args.duel_record_source_alias_fields:
            from tools.duel_record_source_alias_fields import codec as sources
            result=add_duel_record_source_alias_fields(rom,sources.load_fields(m.read(args.duel_record_source_alias_fields)),result)
        if args.city_neighbor_source_alias_fields:
            from tools.city_neighbor_source_alias_fields import codec as sources
            result=add_city_neighbor_source_alias_fields(rom,sources.load_fields(m.read(args.city_neighbor_source_alias_fields)),result)
        if args.cart_mirrored_tile_source_alias_fields:
            from tools.cart_mirrored_tile_source_alias_fields import codec as sources
            result=add_cart_mirrored_tile_source_alias_fields(rom,sources.load_fields(m.read(args.cart_mirrored_tile_source_alias_fields)),result)
        if args.indexed_transfer_source_alias_fields:
            from tools.indexed_transfer_source_alias_fields import codec as sources
            result=add_indexed_transfer_source_alias_fields(rom,sources.load_fields(m.read(args.indexed_transfer_source_alias_fields)),result)
        if args.camera_chunk_source_alias_fields:
            from tools.camera_chunk_source_alias_fields import codec as sources
            result=add_camera_chunk_source_alias_fields(rom,sources.load_fields(m.read(args.camera_chunk_source_alias_fields)),result)
        if args.initial_map_source_alias_fields:
            from tools.initial_map_source_alias_fields import codec as sources
            result=add_initial_map_source_alias_fields(rom,sources.load_fields(m.read(args.initial_map_source_alias_fields)),result)
        if args.scene_descriptor_source_alias_fields:
            from tools.scene_descriptor_source_alias_fields import codec as sources
            result=add_scene_descriptor_source_alias_fields(rom,sources.load_fields(m.read(args.scene_descriptor_source_alias_fields)),result)
        if args.conditional_scene_rle_source_fields:
            from tools.conditional_scene_rle_source_fields import codec as sources
            result=add_conditional_scene_rle_source_fields(rom,sources.load_fields(m.read(args.conditional_scene_rle_source_fields)),result)
        if args.scene_object_source_alias_fields:
            from tools.scene_object_source_alias_fields import codec as sources
            result=add_scene_object_source_alias_fields(rom,sources.load_fields(m.read(args.scene_object_source_alias_fields)),result)
        if args.object_motion_source_alias_fields:
            from tools.object_motion_source_alias_fields import codec as sources
            result=add_object_motion_source_alias_fields(rom,sources.load_fields(m.read(args.object_motion_source_alias_fields)),result)
        if args.object_residue_source_alias_fields:
            from tools.object_residue_source_alias_fields import codec as sources
            result=add_object_residue_source_alias_fields(rom,sources.load_fields(m.read(args.object_residue_source_alias_fields)),result)
        if args.object_id_source_alias_fields:
            from tools.object_id_source_alias_fields import codec as sources
            result=add_object_id_source_alias_fields(rom,sources.load_fields(m.read(args.object_id_source_alias_fields)),result)
        if args.fullword_scene_rle_source_fields:
            from tools.fullword_scene_rle_source_fields import codec as sources
            result=add_fullword_scene_rle_source_fields(rom,sources.load_fields(m.read(args.fullword_scene_rle_source_fields)),result)
        if args.scene_gap_rle_source_fields:
            from tools.scene_gap_rle_source_fields import codec as sources
            result=add_scene_gap_rle_source_fields(rom,sources.load_fields(m.read(args.scene_gap_rle_source_fields)),result)
        if args.secondary_dispatch_source:
            from tools.secondary_dispatch_code import secondary_dispatch_code as secondary
            result=secondary.add_to_layout(rom,m.read(args.secondary_dispatch_source),result)
        if args.boot_z80_source:
            from tools.boot_z80_code import boot_z80_code as boot_code
            result=boot_code.add_to_layout(rom,m.read(args.boot_z80_source),result)
        print(m.publish_content_addressed(result,target,[args.rom,args.source,LEDGER]))
    else:
        if not args.object or not args.image:raise ValueError('actual object and image required')
        image=m.read(args.image);info=verify_image(rom,m.read(args.source),m.read(args.object),image,args.canonical)
        if args.command=='verify-image':
            if not args.base_image or not args.rom_image:raise ValueError('base-image/rom-image required')
            if overlay(rom,m.read(args.base_image,f.ROM_SIZE),image)!=m.read(args.rom_image,f.ROM_SIZE):raise ValueError('whole ROM differs from sources')
            info['whole_ROM_exact']=True
        print(json.dumps(info))
    return 0
if __name__=='__main__':raise SystemExit(main())
