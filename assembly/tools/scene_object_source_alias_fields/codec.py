"""Conditionally read original scene-object compact-sprite source BYTE fields.

A real 3D810 JSR enters4033C:4040A builds a pointer list from live RAM objects,
then40354/40446 selects source units before the original3B13C SAT reader.
Only697 unique physical BYTEs are editable; old overlapping sources stay live.
"""
from __future__ import annotations

from tools.resource_reference import reference_value
import argparse
from functools import lru_cache
import json
from pathlib import Path
import re
from tools.scene_descriptor_source_alias_fields import codec as scene
from tools.initial_map_source_alias_fields import codec as initial
from tools.camera_chunk_source_alias_fields import codec as camera

ROOT=Path(__file__).resolve().parents[2]
ROM_SIZE,ROM_SHA256,DEFAULT_ROM=scene.ROM_SIZE,scene.ROM_SHA256,scene.DEFAULT_ROM
OUTPUT_ROOT=ROOT/'build/scene_object_source_alias_fields'
FORMAL_ROOT=ROOT/'analysis/scene_object_source_alias_fields/generated'
DEFAULT_FIELDS=FORMAL_ROOT/'fields.json'
FORMAT='g5510-conditional-object-indexed-compact-sprite-source-BYTEs-v1'
MAX_JSON=16*1024*1024
MEMBERS=scene.MEMBERS
LAYOUT_ID=reference_value(__name__, 'LAYOUT_ID')
LAYOUT_SHA256=reference_value(__name__, 'LAYOUT_SHA256')
EDITABLE_BYTES,PHYSICAL_BLOCKS=697,53
WITNESS_STATES=(1186,2448,2807,3169,3321,3686,)
SOURCE_SPANS=(
    (0xC045A,0xC047A),
    (0xC04BA,0xC04DA),
    (0xC34FA,0xC353A),
    (0xC357A,0xC357C),
    (0xF463E,0xF463F),
    (0xF4640,0xF4642),
    (0xF4643,0xF4648),
    (0xF464A,0xF464B),
    (0xF464E,0xF464F),
    (0xF4659,0xF465A),
    (0xF465C,0xF465D),
    (0xF465E,0xF465F),
    (0xF4661,0xF4665),
    (0xF4666,0xF4668),
    (0xF466A,0xF4670),
    (0xF4672,0xF4677),
    (0xF467B,0xF4680),
    (0xF4687,0xF4688),
    (0xF468A,0xF468D),
    (0xF4694,0xF4695),
    (0xF4698,0xF4699),
    (0xF469B,0xF469C),
    (0xF46A4,0xF46A6),
    (0xF46AA,0xF46AB),
    (0xF46AD,0xF46AE),
    (0xF46B4,0xF46C0),
    (0xF46C6,0xF46C7),
    (0xF46C8,0xF46CA),
    (0xF46CB,0xF46D4),
    (0xF46D5,0xF46D7),
    (0xF46DE,0xF46E0),
    (0xF46E4,0xF46E5),
    (0xF46EB,0xF46EC),
    (0xF46F3,0xF46F5),
    (0xF46F7,0xF46F8),
    (0xF46FE,0xF4707),
    (0xF470A,0xF470B),
    (0xF470D,0xF470E),
    (0xF470F,0xF4710),
    (0xF4712,0xF4713),
    (0xF4715,0xF471A),
    (0xF4722,0xF4726),
    (0xF472A,0xF472D),
    (0xF4734,0xF4736),
    (0xF4739,0xF473A),
    (0xF4745,0xF4746),
    (0xF4747,0xF474C),
    (0xF4750,0xF4751),
    (0xF4756,0xF475A),
    (0xF477A,0xF477B),
    (0xF6684,0xF6700),
    (0xF6704,0xF6708),
    (0xF67A8,0xF68E8),
)
BODIES=(
    (0x3D810,0x3D814,reference_value(__name__, 'BODIES')),
    (0x4033C,0x404CC,reference_value(__name__, 'BODIES_2')),
    (0x3B13C,0x3B23C,reference_value(__name__, 'BODIES_3')),
    (0x1A0,0x1BC,reference_value(__name__, 'BODIES_4')),
)
_INSTRUCTIONS=(
    (0x3B13C,"48e70640","movem.l","d5-d6/a1, -(a7)"),
    (0x3B140,"0c380050f300","cmpi.b","#$50, $f300.w"),
    (0x3B146,"640000ee","bcc.w","$3b236"),
    (0x3B14A,"02840000ffff","andi.l","#$ffff, d4"),
    (0x3B150,"3e02","move.w","d2, d7"),
    (0x3B152,"0242fff8","andi.w","#$fff8, d2"),
    (0x3B156,"02470007","andi.w","#$7, d7"),
    (0x3B15A,"e547","asl.w","#$2, d7"),
    (0x3B15C,"90788020","sub.w","$8020.w, d0"),
    (0x3B160,"06400080","addi.w","#$80, d0"),
    (0x3B164,"6b0000d0","bmi.w","$3b236"),
    (0x3B168,"08020005","btst.b","#$5, d2"),
    (0x3B16C,"6704","beq.b","$3b172"),
    (0x3B16E,"04400008","subi.w","#$8, d0"),
    (0x3B172,"92788022","sub.w","$8022.w, d1"),
    (0x3B176,"06410080","addi.w","#$80, d1"),
    (0x3B17A,"08020004","btst.b","#$4, d2"),
    (0x3B17E,"6704","beq.b","$3b184"),
    (0x3B180,"04410008","subi.w","#$8, d1"),
    (0x3B184,"4245","clr.w","d5"),
    (0x3B186,"1a38f300","move.b","$f300.w, d5"),
    (0x3B18A,"e74d","lsl.w","#$3, d5"),
    (0x3B18C,"43f8f800","lea.l","$f800.w, a1"),
    (0x3B190,"45f88044","lea.l","$8044.w, a2"),
    (0x3B194,"43f15000","lea.l","(a1, d5.w), a1"),
    (0x3B198,"3c00","move.w","d0, d6"),
    (0x3B19A,"7a00","moveq","#$0, d5"),
    (0x3B19C,"1a10","move.b","(a0), d5"),
    (0x3B19E,"0c050080","cmpi.b","#$80, d5"),
    (0x3B1A2,"67000092","beq.w","$3b236"),
    (0x3B1A6,"08020005","btst.b","#$5, d2"),
    (0x3B1AA,"67000004","beq.w","$3b1b0"),
    (0x3B1AE,"4405","neg.b","d5"),
    (0x3B1B0,"08050007","btst.b","#$7, d5"),
    (0x3B1B4,"6706","beq.b","$3b1bc"),
    (0x3B1B6,"4405","neg.b","d5"),
    (0x3B1B8,"9c45","sub.w","d5, d6"),
    (0x3B1BA,"6002","bra.b","$3b1be"),
    (0x3B1BC,"dc45","add.w","d5, d6"),
    (0x3B1BE,"3286","move.w","d6, (a1)"),
    (0x3B1C0,"3c01","move.w","d1, d6"),
    (0x3B1C2,"1a280003","move.b","$3(a0), d5"),
    (0x3B1C6,"08020004","btst.b","#$4, d2"),
    (0x3B1CA,"6702","beq.b","$3b1ce"),
    (0x3B1CC,"4405","neg.b","d5"),
    (0x3B1CE,"08050007","btst.b","#$7, d5"),
    (0x3B1D2,"08050007","btst.b","#$7, d5"),
    (0x3B1D6,"6706","beq.b","$3b1de"),
    (0x3B1D8,"4405","neg.b","d5"),
    (0x3B1DA,"9c45","sub.w","d5, d6"),
    (0x3B1DC,"6002","bra.b","$3b1e0"),
    (0x3B1DE,"dc45","add.w","d5, d6"),
    (0x3B1E0,"33460006","move.w","d6, $6(a1)"),
    (0x3B1E4,"136800010002","move.b","$1(a0), $2(a1)"),
    (0x3B1EA,"4ab27000","tst.l","(a2, d7.w)"),
    (0x3B1EE,"6600000e","bne.w","$3b1fe"),
    (0x3B1F2,"25897000","move.l","a1, (a2, d7.w)"),
    (0x3B1F6,"15b8f3007020","move.b","$f300.w, $20(a2, d7.w)"),
    (0x3B1FC,"600a","bra.b","$3b208"),
    (0x3B1FE,"26727040","movea.l","$40(a2, d7.w), a3"),
    (0x3B202,"1778f3000003","move.b","$f300.w, $3(a3)"),
    (0x3B208,"25897040","move.l","a1, $40(a2, d7.w)"),
    (0x3B20C,"5238f300","addq.b","#$1, $f300.w"),
    (0x3B210,"1a280001","move.b","$1(a0), d5"),
    (0x3B214,"024500f0","andi.w","#$f0, d5"),
    (0x3B218,"da03","add.b","d3, d5"),
    (0x3B21A,"b545","eor.w","d2, d5"),
    (0x3B21C,"ef45","asl.w","#$7, d5"),
    (0x3B21E,"8a280002","or.b","$2(a0), d5"),
    (0x3B222,"da44","add.w","d4, d5"),
    (0x3B224,"33450004","move.w","d5, $4(a1)"),
    (0x3B228,"5089","addq.l","#$8, a1"),
    (0x3B22A,"5888","addq.l","#$4, a0"),
    (0x3B22C,"0c380050f300","cmpi.b","#$50, $f300.w"),
    (0x3B232,"6500ff64","bcs.w","$3b198"),
    (0x3B236,"4cdf0260","movem.l","(a7)+, d5-d6/a1"),
    (0x3B23A,"4e75","rts",""),
    (0x3D810,"4eba2b2a","jsr","$4033c(pc)"),
    (0x4033C,"610000cc","bsr.w","$4040a"),
    (0x40340,"4bf8836a","lea.l","$836a.w, a5"),
    (0x40344,"4a95","tst.l","(a5)"),
    (0x40346,"6718","beq.b","$40360"),
    (0x40348,"2c5d","movea.l","(a5)+, a6"),
    (0x4034A,"08160007","btst.b","#$7, (a6)"),
    (0x4034E,"67f4","beq.b","$40344"),
    (0x40350,"48e70004","movem.l","a5, -(a7)"),
    (0x40354,"4eba00f0","jsr","$40446(pc)"),
    (0x40358,"4e71","nop",""),
    (0x4035A,"4cdf2000","movem.l","(a7)+, a5"),
    (0x4035E,"60e4","bra.b","$40344"),
    (0x40360,"4a78814c","tst.w","$814c.w"),
    (0x40364,"670000a2","beq.w","$40408"),
    (0x40368,"0c7800028152","cmpi.w","#$2, $8152.w"),
    (0x4036E,"67000014","beq.w","$40384"),
    (0x40372,"4a78813e","tst.w","$813e.w"),
    (0x40376,"66000090","bne.w","$40408"),
    (0x4037A,"0c7800018152","cmpi.w","#$1, $8152.w"),
    (0x40380,"67000086","beq.w","$40408"),
    (0x40384,"42788152","clr.w","$8152.w"),
    (0x40388,"53788154","subq.w","#$1, $8154.w"),
    (0x4038C,"6a00007a","bpl.w","$40408"),
    (0x40390,"52788150","addq.w","#$1, $8150.w"),
    (0x40394,"0c7800108150","cmpi.w","#$10, $8150.w"),
    (0x4039A,"6436","bcc.b","$403d2"),
    (0x4039C,"41f8816a","lea.l","$816a.w, a0"),
    (0x403A0,"0c780001814c","cmpi.w","#$1, $814c.w"),
    (0x403A6,"67000006","beq.w","$403ae"),
    (0x403AA,"41f8826a","lea.l","$826a.w, a0"),
    (0x403AE,"30388150","move.w","$8150.w, d0"),
    (0x403B2,"e940","asl.w","#$4, d0"),
    (0x403B4,"083000070000","btst.b","#$7, (a0, d0.w)"),
    (0x403BA,"6700ffd4","beq.w","$40390"),
    (0x403BE,"30300000","move.w","(a0, d0.w), d0"),
    (0x403C2,"0240007f","andi.w","#$7f, d0"),
    (0x403C6,"b078814e","cmp.w","$814e.w, d0"),
    (0x403CA,"6600ffc4","bne.w","$40390"),
    (0x403CE,"60000026","bra.w","$403f6"),
    (0x403D2,"42788150","clr.w","$8150.w"),
    (0x403D6,"5278814e","addq.w","#$1, $814e.w"),
    (0x403DA,"0c780004814e","cmpi.w","#$4, $814e.w"),
    (0x403E0,"6514","bcs.b","$403f6"),
    (0x403E2,"4278814e","clr.w","$814e.w"),
    (0x403E6,"5278814c","addq.w","#$1, $814c.w"),
    (0x403EA,"0c780003814c","cmpi.w","#$3, $814c.w"),
    (0x403F0,"6504","bcs.b","$403f6"),
    (0x403F2,"4278814c","clr.w","$814c.w"),
    (0x403F6,"42788154","clr.w","$8154.w"),
    (0x403FA,"0c780002814e","cmpi.w","#$2, $814e.w"),
    (0x40400,"6506","bcs.b","$40408"),
    (0x40402,"31fc00018154","move.w","#$1, $8154.w"),
    (0x40408,"4e75","rts",""),
    (0x4040A,"3038f320","move.w","$f320.w, d0"),
    (0x4040E,"0240000f","andi.w","#$f, d0"),
    (0x40412,"66000030","bne.w","$40444"),
    (0x40416,"4bf8836a","lea.l","$836a.w, a5"),
    (0x4041A,"701e","moveq","#$1e, d0"),
    (0x4041C,"4df8816a","lea.l","$816a.w, a6"),
    (0x40420,"08160007","btst.b","#$7, (a6)"),
    (0x40424,"670c","beq.b","$40432"),
    (0x40426,"322e0002","move.w","$2(a6), d1"),
    (0x4042A,"e849","lsr.w","#$4, d1"),
    (0x4042C,"b240","cmp.w","d0, d1"),
    (0x4042E,"6602","bne.b","$40432"),
    (0x40430,"2ace","move.l","a6, (a5)+"),
    (0x40432,"dcfc0010","adda.w","#$10, a6"),
    (0x40436,"bdfcffff836a","cmpa.l","#$ffff836a, a6"),
    (0x4043C,"65e2","bcs.b","$40420"),
    (0x4043E,"51c8ffdc","dbra","d0, $4041c"),
    (0x40442,"4295","clr.l","(a5)"),
    (0x40444,"4e75","rts",""),
    (0x40446,"4a78813e","tst.w","$813e.w"),
    (0x4044A,"6606","bne.b","$40452"),
    (0x4044C,"4eba0846","jsr","$40c94(pc)"),
    (0x40450,"4e71","nop",""),
    (0x40452,"3016","move.w","(a6), d0"),
    (0x40454,"024000ff","andi.w","#$ff, d0"),
    (0x40458,"7200","moveq","#$0, d1"),
    (0x4045A,"41fa0070","lea.l","$404cc(pc), a0"),
    (0x4045E,"4e71","nop",""),
    (0x40460,"12300000","move.b","(a0, d0.w), d1"),
    (0x40464,"0c38000380db","cmpi.b","#$3, $80db.w"),
    (0x4046A,"6604","bne.b","$40470"),
    (0x4046C,"12300004","move.b","$4(a0, d0.w), d1"),
    (0x40470,"4a788124","tst.w","$8124.w"),
    (0x40474,"6610","bne.b","$40486"),
    (0x40476,"bdfcffff826a","cmpa.l","#$ffff826a, a6"),
    (0x4047C,"6514","bcs.b","$40492"),
    (0x4047E,"06410060","addi.w","#$60, d1"),
    (0x40482,"6000000e","bra.w","$40492"),
    (0x40486,"bdfcffff826a","cmpa.l","#$ffff826a, a6"),
    (0x4048C,"6404","bcc.b","$40492"),
    (0x4048E,"06410060","addi.w","#$60, d1"),
    (0x40492,"302e0008","move.w","$8(a6), d0"),
    (0x40496,"e540","asl.w","#$2, d0"),
    (0x40498,"d240","add.w","d0, d1"),
    (0x4049A,"3038f320","move.w","$f320.w, d0"),
    (0x4049E,"e648","lsr.w","#$3, d0"),
    (0x404A0,"02400003","andi.w","#$3, d0"),
    (0x404A4,"d041","add.w","d1, d0"),
    (0x404A6,"3800","move.w","d0, d4"),
    (0x404A8,"e540","asl.w","#$2, d0"),
    (0x404AA,"207b0028","movea.l","$404d4(pc, d0.w), a0"),
    (0x404AE,"302e0002","move.w","$2(a6), d0"),
    (0x404B2,"322e0004","move.w","$4(a6), d1"),
    (0x404B6,"343c0005","move.w","#$5, d2"),
    (0x404BA,"7600","moveq","#$0, d3"),
    (0x404BC,"e344","asl.w","#$1, d4"),
    (0x404BE,"43fa0314","lea.l","$407d4(pc), a1"),
    (0x404C2,"4e71","nop",""),
    (0x404C4,"38314000","move.w","(a1, d4.w), d4"),
    (0x404C8,"4efaac72","jmp","$3b13c(pc)"),
)
_ROWS={p:dict(bytes=b,mnemonic=m,operand=o) for p,b,m,o in _INSTRUCTIONS}
MASK,sign,operands=camera.MASK,camera.sign,camera.operands
sha,dump,keys,same,uint,exact_list=camera.sha,camera.dump,camera.keys,camera.same,camera.uint,camera.exact_list
safe_path,read_bounded,put,load_fields=camera.safe_path,camera.read_bounded,camera.put,camera.load_fields
verify_rom=camera.verify_rom
ROLES={0x3B19C:'first80h_terminator_or_record_X_BYTE',0x3B1C2:'record_Y_BYTE',
       0x3B1E4:'record_size_and_attribute_BYTE',0x3B210:'repeated_record_attribute_BYTE',
       0x3B21E:'record_tile_low_BYTE'}

def _controls(image):
    for a,z,h in BODIES:
        if sha(image[a:z])!=h:raise ValueError('original object/SAT control or cart geometry differs:'+hex(a))

class _ObjectReader(scene._SceneReader):
    def __init__(self,image,state,budget,ram_before):
        if ram_before is None:
            initial_ram=bytearray(65536)
            initial_ram[0x816A:0x816C]=(0x8000).to_bytes(2,'big')
            initial_ram[0x813E:0x8140]=(1).to_bytes(2,'big')
            ram_before=bytes(initial_ram)
        initial._InitialReader.__init__(self,image,{0x8172:state},budget,ram_before,0)
        self.pc=0x3D810;self.rows=_ROWS;self.steps=[]

    def run(self):
        result='instrumentation_budget_exhausted_not_CPU_stop'
        try:
            while self.pc!=0x3D814:
                if len(self.steps)>=self.budget:raise camera._ReadBoundary(result)
                if self.pc not in self.rows:raise camera._ReadBoundary('not_pinned_original_PC:'+hex(self.pc))
                row=self.rows[self.pc];raw=bytes.fromhex(row['bytes'])
                assert self.image[self.pc:self.pc+len(raw)]==raw
                name,*size=row['mnemonic'].split('.');width={'b':1,'w':2,'l':4}.get(size[0] if size else '',0)
                ops=operands(row['operand']) if row['operand'] else []
                nextpc=self.pc+len(raw);step=dict(PC=self.pc,bytes=raw.hex(),mnemonic=row['mnemonic'],operand=row['operand'])
                self.steps.append(step)
                if name=='nop':pass
                elif name=='jmp':nextpc=self.target(ops[0])
                elif name in ('jsr','bsr'):
                    target=self.target(ops[0]);self.A[7]=(self.A[7]-4)&0xFFFFFFFF
                    self.write(self.A[7],4,nextpc,'real_JSR_BSR_return_stack')
                    self.calls.append(dict(kind='call',PC=self.pc,target=target,return_PC=nextpc,SP=self.A[7]));nextpc=target
                elif name=='rts':
                    target=self.read(self.A[7],4,'real_RTS_return_stack');self.A[7]=(self.A[7]+4)&0xFFFFFFFF
                    self.calls.append(dict(kind='return',PC=self.pc,target=target,SP=self.A[7]));nextpc=target
                elif name=='dbra':
                    reg=int(ops[0][1:]);self.D[reg]=(self.D[reg]&0xFFFF0000)|((self.D[reg]-1)&65535)
                    if self.D[reg]&65535!=65535:nextpc=self.target(ops[1])
                elif name.startswith('b') and name not in ('btst','bclr'):
                    if self.condition(name):nextpc=self.target(ops[0])
                elif name=='move':
                    value=self.get(ops[0],width);self.put(ops[1],width,value)
                    if ops[1]!='sr':self.logic(value,width)
                elif name=='movea':
                    value=self.get(ops[0],width)
                    if width==2:value=sign(value,2)
                    self.A[int(ops[1][1:])]=value&0xFFFFFFFF
                elif name=='moveq':
                    value=sign(self.get(ops[0],1),1)&0xFFFFFFFF
                    self.D[int(ops[1][1:])]=value;self.logic(value,4)
                elif name=='lea':self.A[int(ops[1][1:])]=self.ea(ops[0],4,False)
                elif name=='movem':
                    if ops[1]=='-(a7)':
                        for kind,n in reversed(self.movem_regs(ops[0])):
                            self.A[7]=(self.A[7]-width)&0xFFFFFFFF
                            self.write(self.A[7],width,(self.D if kind=='d' else self.A)[n],'real_MOVEM_save')
                    elif ops[0]=='(a7)+':
                        for kind,n in self.movem_regs(ops[1]):
                            value=self.read(self.A[7],width,'real_MOVEM_restore');self.A[7]=(self.A[7]+width)&0xFFFFFFFF
                            (self.D if kind=='d' else self.A)[n]=value if width==4 else sign(value,2)&0xFFFFFFFF
                    else:raise camera._ReadBoundary('unsupported_original_MOVEM:'+row['operand'])
                elif name in ('clr','tst','ext','swap','neg'):
                    if name=='clr':value=0;self.put(ops[0],width,value);self.logic(value,width)
                    elif name=='tst':self.logic(self.get(ops[0],width),width)
                    elif name=='ext':
                        value=sign(self.get(ops[0],1 if width==2 else 2),1 if width==2 else 2)&MASK[width]
                        self.put(ops[0],width,value);self.logic(value,width)
                    elif name=='swap':
                        value=self.get(ops[0],4);value=((value<<16)|(value>>16))&0xFFFFFFFF
                        self.put(ops[0],4,value);self.logic(value,4)
                    else:
                        value=self.calc(0,self.get(ops[0],width),width,True);self.put(ops[0],width,value)
                elif name in ('lsr','lsl','asl'):
                    count=self.get(ops[0],4);value=self.get(ops[1],width)
                    last=False;overflow=False
                    for _ in range(count):
                        if name=='lsr':last=bool(value&1);value>>=1
                        else:
                            last=bool(value&(1<<(width*8-1)));value=(value<<1)&MASK[width]
                            overflow|=last!=bool(value&(1<<(width*8-1)))
                    self.put(ops[1],width,value);self.logic(value,width);self.C=last;self.V=overflow if name=='asl' else False
                    if count:self.X=last
                elif name=='cmpa':
                    right=sign(self.get(ops[0],width),width)
                    left=self.get(ops[1],4);oldX=self.X;self.calc(left,right,4,True);self.X=oldX
                elif name in ('addi','subi','add','sub','addq','subq','cmp','cmpi','adda'):
                    right=self.get(ops[0],width);left=self.get(ops[1],width)
                    if name=='adda' or name in ('addq','subq') and ops[1].startswith('a') and len(ops[1])==2:
                        reg=int(ops[1][1:]);v=sign(right,2) if width==2 else sign(right,4)
                        self.A[reg]=(self.A[reg]+(-v if name=='subq' else v))&0xFFFFFFFF
                    else:
                        oldX=self.X;v=self.calc(left,right,width,name.startswith('sub') or name.startswith('cmp'))
                        if name.startswith('cmp'):self.X=oldX
                        else:self.put(ops[1],width,v)
                elif name in ('andi','ori','or','and','eor'):
                    right=self.get(ops[0],width);left=self.get(ops[1],width)
                    value=(left&right if name.startswith('and') else left^right if name=='eor' else left|right)
                    self.put(ops[1],width,value);self.logic(value,width)
                elif name in ('mulu','divu'):
                    src=self.get(ops[0],2);n=int(ops[1][1:])
                    if name=='mulu':self.D[n]=(self.D[n]&65535)*src;self.logic(self.D[n],4)
                    else:
                        if not src:raise camera._ReadBoundary('original_DIVU_zero')
                        q,r=divmod(self.D[n],src)
                        if q>65535:self.V=True;self.C=False
                        else:self.D[n]=(r<<16)|q;self.logic(q,2)
                elif name in ('btst','bclr'):
                    bit=self.get(ops[0],4);w=4 if re.fullmatch(r'd[0-7]',ops[1]) else 1
                    bit%=32 if w==4 else 8;value=self.get(ops[1],w);self.Z=not bool(value&(1<<bit))
                    if name=='bclr':self.put(ops[1],w,value&~(1<<bit))
                else:raise camera._ReadBoundary('unsupported_original_opcode:'+row['mnemonic']+' '+row['operand'])
                self.pc=nextpc
            result='actual_JSR_4033C_RTS_to_3D814'
        except camera._ReadBoundary as e:result=str(e)
        return dict(result=result,conditional_ram_WORDs={f'{a:04X}':v for a,v in self.frame.items()},
                    entry_call_PC=0x3D810,requested_normal_return_PC=0x3D814,
                    actual_final_PC=self.pc,initial_SP=self.initial_sp,final_SP=self.A[7],
                    instruction_count=len(self.steps),actual_call_return_events=self.calls,
                    ordered_data_events=self.events,final_RAM_sha256=sha(self.ram),
                    source_events=[e for e in self.events if e['kind']=='read' and 'ROM' in e['memory']],
                    CPU=False,natural_frame=False,earlier_parent_UI_helpers_closed=False,
                    budget_is_instrumentation_only=True)
    

def source_view(image,state_WORD,instruction_budget=50000,RAM_before=None,include_prefix_events=False):
    """Live original3D810 caller; optional complete immutable RAM plus FF8172.W.

    Default RAM is zero except FF816A.W=8000 and FF813E.W=1; state_WORD is
    the complete FF8172 input. With supplied RAM all other bytes remain live.
    No A6, list pointer, source pointer, helper register or artificial return
    is supplied. The API diagnoses conditional reads, not natural gameplay.
    """
    camera._image(image);_controls(image)
    state=uint(state_WORD,65535,'complete object+8 WORD')
    budget=uint(instruction_budget,200000,'instrumentation instruction budget')
    if budget<1:raise ValueError('positive instruction budget required')
    if type(include_prefix_events) is not bool:raise ValueError('boolean event inclusion required')
    if RAM_before is not None and (type(RAM_before) is not bytes or len(RAM_before)!=65536):
        raise ValueError('complete immutable64KiB RAM bytes required')
    reader=_ObjectReader(image,state,budget,RAM_before)
    initial_ram=bytes(reader.ram);view=reader.run()
    events=view.pop('ordered_data_events');source=view.pop('source_events')
    physical=sorted({p for e in source for p in e['physical_addresses'] if p is not None})
    view.update(state_WORD=state,source_events=source,
        physical_source=physical,
        ordered_data_event_count=len(events),ordered_data_events_sha256=sha(dump(events)),
        RAM_before_sha256=sha(initial_ram),prefix_memoized=False,
        RAM_frame_default='zero64KiB + FF816A.W8000/FF813E.W1 + FF8172.W input'
            if RAM_before is None else 'complete supplied64KiB + FF8172.W input',
        final_registers=dict(D=list(reader.D),A=list(reader.A),
            SR=(reader.SR&0xFFE0)|(int(reader.X)<<4)|(int(reader.N)<<3)|(int(reader.Z)<<2)|(int(reader.V)<<1)|int(reader.C)),
        last_explicit_SR_write=reader.SR,final_CCR=dict(X=reader.X,N=reader.N,Z=reader.Z,V=reader.V,C=reader.C),
        complete_function_recovery=False,allocation_owner='unknown',natural_domain='unknown',
        earlier_3D810_battle_state_closed=False,original_hardware_equivalence='unknown',
        source_read_budget_is_CPU_stop=False,padding_or_free_space=False,
        cart_profile='measured MAME24bit: ROMmirror0..200000/204000..400000; SRAMexcluded; beyond4MiBunknown',
        operand_diagnostics_not_complete_exception_frame=True,
        managed_source_reached=sorted(set(physical) & {p for a,z in SOURCE_SPANS for p in range(a,z)}))
    if include_prefix_events:view['ordered_data_events']=events
    return view

def _coalesce(positions):return camera._coalesce(sorted(positions))

@lru_cache(maxsize=2)
def _catalog(rom):
    verify_rom(rom)
    wanted={p for a,z in SOURCE_SPANS for p in range(a,z)};found={}
    for state in WITNESS_STATES:
        v=source_view(rom,state)
        if v['result']!='actual_JSR_4033C_RTS_to_3D814' or v['final_SP']!=0xFFFFFD00:
            raise ValueError('canonical object conditional caller no longer returns')
        for order,e in enumerate(v['source_events']):
            for lane,p in enumerate(e['physical_addresses']):
                if p in wanted and p not in found:
                    if e['PC'] not in ROLES or e['width']!=1:raise ValueError('unknown admitted compact source role')
                    found[p]=dict(address=p,state_WORD=state,read_PC=e['PC'],
                        source_role=ROLES[e['PC']],read_width=1,source_address=e['address'],
                        bus_address=e['bus_address'],unit_BYTE_lane=lane,source_event_index=order,
                        canonical_read_value=e['value'],true_caller_PC=0x3D810,
                        generated_list_helper=0x4040A,actual_render_JSR=0x40354,
                        original_return_PC=0x3D814,actual_final_SP=v['final_SP'])
    if set(found)!=wanted or len(found)!=EDITABLE_BYTES or len(_coalesce(found))!=PHYSICAL_BLOCKS:
        raise ValueError('canonical true object source scope differs')
    return tuple(found[p] for p in sorted(found))

def physical_positions(rom):
    verify_rom(rom)
    return tuple(r['address'] for r in _catalog(rom))

def witness(rom,address):
    verify_rom(rom);address=uint(address,ROM_SIZE-1,'source BYTE address')
    for row in _catalog(rom):
        if row['address']==address:return load_fields(dump(row))
    raise ValueError('outside physical object source authority')

def metadata(rom):
    positions=physical_positions(rom)
    return dict(format=FORMAT,confidence='confirmed_conditional_original_object_SAT_source_reads',
        canonical_source=dict(size=ROM_SIZE,sha256=ROM_SHA256),
        source_union_BYTES=EDITABLE_BYTES,source_union_sha256=sha(bytes(rom[p] for p in positions)),
        physical_blocks=PHYSICAL_BLOCKS,physical_scope=[dict(start=a,end=z,bytes=z-a) for a,z in SOURCE_SPANS],
        raw_baseline=dict(layout_id=LAYOUT_ID,manifest_sha256=LAYOUT_SHA256,raw_BYTES=13180,resources=102),
        roles=dict(resource='live_compact_sprite_source_components',
            BYTE_values='full0..255; X/first80h marker, Y, size/attributes, tilelow keepallbits',
            field_roles=sorted(ROLES.values()),zero_values='actual conditional source bytes, not padding/free',
            shared_fields='old typed and prospective RLE318 overlapping BYTEs live-read only; no re-emission'),
        evidence=dict(real_entry_call_PC=0x3D810,call_target=0x4033C,list_BSR_PC=0x4033C,
            list_producer=0x4040A,object_start_RAM=0xFF816A,object_end_RAM=0xFF836A,stride_BYTES=16,
            list='31descending X>>4 bins; BTST.B7 active objects; realLONG pointer writes intoFF836A; trailingCLRL',
            rendered_object_JSR=0x40354,render_target=0x40446,object_status_read_PC=0x40492,
            indexed_source='live404CC BYTE + WORDwrap(object+8<<2) + (F320.W>>3)&3; LSL.W2→404D4+s16LONG',
            live_attribute='407D4+s16(LSL.W1 prepointerindex) fullWORD',
            SAT_tail_PC=0x404C8,SAT_entry=0x3B13C,
            source_gates='F300 BYTE unsigned<50h; signed X clipping; first80h BYTE; 50h (80 decimal) capacity after each record',
            read_order='XBYTE then YBYTE(+3), sizeBYTE(+1), repeatedattributeBYTE(+1), tilelowBYTE(+2)',
            source_stop='first80h marker or F300 reaches50h; zero is a normal record component, not terminator',
            actual_canonical_return=0x3D814,witness_states=list(WITNESS_STATES),
            whole_code_controls=[dict(start=a,end=z,sha256=h) for a,z,h in BODIES],complete_RTS_guards=True),
        conditional_frame='fullzero64KiB + FF816A.W8000, FF813E.W1, object+8fullWORD; SPFFFFFD00, SR2500, D/A0; noIRQ/deviceeventneeded',
        overlap=dict(prospective_RLE_source_scope=[0xC383C,0xC641F],excluded_BYTES=318,
            prospective_unique_authority='tools.conditional_scene_rle_source_fields; not claimed alreadyaccepted'),
        natural_object_status='unknown; verified411CC→41482/414E6 direction writers set0..3, not a fullWORD natural producer',
        allocation_or_resource_owner='unknown',owner_bytes_added=0,functions_added=0,natural_domains_added=0,
        complete_domains_added=0,complete_function_recovery=False,independent_CPU_comparison=False,
        earlier_3D810_UI_state_closed=False,edited_gameplay_safety='unknown',
        padding_or_free_space_claimed=False,instrumentation_budget_is_original_CPU_stop=False,
        final_semantic_high_level_recovery=False,
        diagnostic_scope='ordered successful operand reads/writes and calls only; stopped postincrement register diagnostics may differ from successfirst reference; notcompletebuscycle/exceptionframe')

def _fixed(row):return dict(address=row['address'],source_role=row['source_role'],read_width=row['read_width'],unit_BYTE_lane=row['unit_BYTE_lane'])

def extract(rom):
    return dict(**metadata(rom),source_BYTEs=[dict(**_fixed(r),BYTE=rom[r['address']]) for r in _catalog(rom)])

def blocks(rom,fields):
    fixed=metadata(rom);keys(fields,set(fixed)|{'source_BYTEs'},'object source package')
    for k,v in fixed.items():same(fields[k],v,'package.'+k)
    values={}
    for expected,row in zip(_catalog(rom),exact_list(fields['source_BYTEs'],EDITABLE_BYTES,'literal source BYTEs')):
        keys(row,set(_fixed(expected))|{'BYTE'},'compact source component')
        for k,v in _fixed(expected).items():same(row[k],v,'source.'+k)
        values[expected['address']]=uint(row['BYTE'],255,'complete source BYTE')
    return [dict(id=f'rom_{a:06X}_object_compact_source_BYTEs',start=a,end=z,
        data=bytes(values[p] for p in range(a,z)),role='conditional_object_compact_sprite_source_BYTEs')
        for a,z in SOURCE_SPANS]

def rebuild(rom,fields):
    verify_rom(rom);image=bytearray(rom)
    for r in blocks(rom,fields):image[r['start']:r['end']]=r['data']
    return bytes(image)

def schema(rom):
    def obj(p):return dict(type='object',properties=p,required=list(p),additionalProperties=False)
    def fixed(v):
        if type(v) is dict:return obj({k:fixed(x) for k,x in v.items()})
        if type(v) is list:return dict(type='array',prefixItems=[fixed(x) for x in v],items=False,minItems=len(v),maxItems=len(v))
        return dict(type={str:'string',int:'integer',bool:'boolean'}[type(v)],const=v)
    p={k:fixed(v) for k,v in metadata(rom).items()}
    p['source_BYTEs']=dict(type='array',minItems=EDITABLE_BYTES,maxItems=EDITABLE_BYTES,items=False,
        prefixItems=[obj(dict(**{k:fixed(v) for k,v in _fixed(r).items()},BYTE=dict(type='integer',minimum=0,maximum=255))) for r in _catalog(rom)])
    return dict(**obj(p),**{'$schema':'https://json-schema.org/draft/2020-12/schema'},
        description='697 single-authority conditional compact-sprite source components; no catalog clamp.')

def render_bundle(rom):
    f=extract(rom);image=rebuild(rom,load_fields(dump(f)))
    if image!=rom:raise ValueError('wholeROM serialized roundtrip differs')
    validation=dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True,
        whole_ROM_sha256=sha(image),canonical_BYTE_witnesses=list(_catalog(rom)),
        limitations=['Constructed fullRAM caller frame; natural fullWORD status and ownerunknown.',
            'Every original source/old pointer/attribute/neighbor remains live; editedfirst80h maystop earlier.',
            'No fakehelperreturn, IRQ, RAMrepair, fullCPU, exceptionframe or completefunction claim.'])
    members={'fields.json':dump(f),'fields.schema.json':dump(schema(rom)),'validation.json':dump(validation)}
    members['manifest.json']=dump(dict(**metadata(rom),editable_bytes=EDITABLE_BYTES,
        members={k:dict(bytes=len(v),sha256=sha(v)) for k,v in members.items()}))
    return members

def fresh_output(value,bundle=False):
    path=safe_path(value)
    for ancestor in (path,*path.parents):
        if ancestor.is_symlink() or getattr(ancestor,'is_junction',lambda:False)():raise ValueError('reparse output refused')
    if not (path!=OUTPUT_ROOT and OUTPUT_ROOT in path.parents) and not (bundle and path==FORMAL_ROOT):
        raise ValueError('dedicated fresh build output or exact fresh formal bundle required')
    if path.exists() or not path.parent.is_dir():raise ValueError('fresh output and existing parent required')
    return path

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=('export','import','verify'))
    p.add_argument('--rom',default=str(DEFAULT_ROM));p.add_argument('--fields');p.add_argument('--bundle');p.add_argument('--output')
    a=p.parse_args();target=None
    if a.command=='export':
        if a.output is None or a.fields is not None or a.bundle is not None:raise ValueError('export needsoutputonly')
        target=fresh_output(a.output,True)
    elif a.command=='import':
        if a.output is None or a.bundle is not None:raise ValueError('import needsfreshBIN')
        target=fresh_output(a.output)
        if target.suffix.lower()!='.bin':raise ValueError('freshBIN required')
    elif a.output is not None or a.fields is not None and a.bundle is not None:
        raise ValueError('verify acceptsfieldsorbundle and writesnothing')
    rom=read_bounded(a.rom,ROM_SIZE)
    if a.command=='export':
        members=render_bundle(rom);target.mkdir()
        for n,data in members.items():put(target/n,data)
        result=dict(path=str(target),editable_bytes=EDITABLE_BYTES,members={k:sha(v) for k,v in members.items()})
    elif a.command=='verify' and a.bundle is not None:
        path=safe_path(a.bundle)
        if not path.is_dir() or {p.name for p in path.iterdir()}!=MEMBERS:raise ValueError('exactfourmembers required')
        for name,data in render_bundle(rom).items():
            if read_bounded(path/name,MAX_JSON)!=data:raise ValueError('bundle drift:'+name)
        result=dict(verified=True,editable_bytes=EDITABLE_BYTES,whole_ROM_exact=True)
    else:
        image=rebuild(rom,load_fields(read_bounded(a.fields or DEFAULT_FIELDS,MAX_JSON)))
        if target is not None:put(target,image)
        result=dict(exact_canonical=image==rom,sha256=sha(image),editable_bytes=EDITABLE_BYTES)
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
