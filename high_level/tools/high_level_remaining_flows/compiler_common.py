"""Restricted remaining-workflow AST admission and ordinary GNU emission from explicit text."""
import ast
import re
from dataclasses import asdict
from .target import BINDINGS,NEW_BINDINGS,REUSED_BINDINGS,BY_NAME,validate_binding,NEW_BYTES,REUSED_BYTES,TOTAL_BYTES,INSTRUCTIONS

class CompileError(ValueError): pass

def require_declared_names(functions,imported):
    builtins={'tuple','range','type','int','bool','ValueError','sum','min','str','enumerate','max','len','isinstance','abs','all','any','getattr','zip','divmod'}
    available=set(functions)|imported|builtins
    for fn in functions.values():
        if fn.type_params: raise CompileError('generic declarations outside fixed ABI')
        local={a.arg for a in ast.walk(fn) if isinstance(a,ast.arg)}
        local.update(n.name for n in ast.walk(fn) if isinstance(n,ast.FunctionDef) and n is not fn)
        local.update(n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store))
        local.update(n.name for n in ast.walk(fn) if isinstance(n,ast.ExceptHandler) and n.name is not None)
        local_imports={a.name for n in ast.walk(fn) if isinstance(n,ast.ImportFrom) for a in n.names}
        assigned=set(local)
        local.update(local_imports)
        used={n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
        if used-local-available: raise CompileError(fn.name+': undeclared names '+repr(sorted(used-local-available)))
        if assigned&(imported|builtins|local_imports) or fn.name in imported: raise CompileError(fn.name+': typed import shadowing '+repr(sorted(assigned&(imported|builtins|local_imports))))

def semantic_functions(source,declarations,approved):
    if type(source) is not str or len(source)>4000000: raise CompileError('bounded explicit Python text required')
    try: tree=ast.parse(source)
    except (SyntaxError,ValueError) as exc: raise CompileError('invalid business Python') from exc
    functions,imported={},set()
    for node in tree.body:
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and type(node.value.value) is str: continue
        if isinstance(node,ast.ImportFrom):
            if node.module=='__future__' and node.level==0 and [n.name for n in node.names]==['annotations']: continue
            import_key = (node.level, node.module) if node.level == 2 else node.module
            allowed=approved.get(import_key,set())
            if (node.level not in (1,2) and not (node.level==0 and node.module=='dataclasses' and [n.name for n in node.names]==['replace'])) or any(n.asname or n.name not in allowed for n in node.names): raise CompileError('approved explicit semantic imports required')
            imported.update(n.name for n in node.names);continue
        if not isinstance(node,ast.FunctionDef) or node.name not in declarations or node.name in functions: raise CompileError('complete function declarations required')
        if node.type_params or node.decorator_list: raise CompileError('generic/decorated ABI not supported')
        for child in ast.walk(node):
            if isinstance(child,ast.ImportFrom):
                local_key = (child.level, child.module) if child.level == 2 else child.module
                local_allowed = approved.get(local_key, set())
                if (child.level not in (1,2) and not (child.level==0 and child.module=='dataclasses' and [n.name for n in child.names]==['replace'])) or any(n.asname or n.name not in local_allowed for n in child.names):
                    raise CompileError('approved explicit local semantic imports required')
        functions[node.name]=node
    if set(functions)!=set(declarations): raise CompileError('all complete business bodies required')
    require_declared_names(functions,imported)
    records={}
    for name,fn in functions.items():
        d=declarations[name]
        expected=ast.parse('def '+name+'('+d['signature']+')'+('->'+d['returns'] if d['returns'] else '')+':\n'+'\n'.join('    '+s for s in d['flow'].splitlines())).body[0]
        body=list(fn.body)
        if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and type(body[0].value.value) is str: body=body[1:]
        actual=ast.FunctionDef(name=fn.name,args=fn.args,body=body,decorator_list=fn.decorator_list,returns=fn.returns,type_comment=fn.type_comment,type_params=fn.type_params)
        rules={};slots=d.get('slots',{})
        def match(want,have):
            if type(want) is not type(have): raise CompileError(name+': unsupported typed AST/control edit')
            if isinstance(want,ast.Constant) and type(want.value) is int and want.value in slots:
                role,lo,hi=slots[want.value]
                if type(have.value) is not int or not lo<=have.value<=hi: raise CompileError(name+': strict bounded literal required')
                if role in rules and rules[role]!=have.value: raise CompileError(name+': semantic slot must remain consistent')
                rules[role]=have.value;return
            if isinstance(want,ast.AST):
                if want._fields!=have._fields: raise CompileError(name+': unsupported AST schema')
                for f in want._fields: match(getattr(want,f,None),getattr(have,f,None))
            elif type(want) is list:
                if len(want)!=len(have): raise CompileError(name+': complete control/return required')
                for a,b in zip(want,have): match(a,b)
            elif want!=have: raise CompileError(name+': unsupported semantic expression/ABI edit')
        match(expected,actual)
        records[name]=dict(name=name,rules=rules,effects=ast.dump(actual,include_attributes=False))
    return records

ASSEMBLY_PREFIX='.cpu 68000\n.text\n.set remaining_pc_000206,0x206\n.set remaining_pc_000ea6,0xea6\n.set remaining_pc_000f10,0xf10\n.set remaining_pc_0011ee,0x11ee\n.set remaining_pc_001228,0x1228\n.set remaining_pc_001264,0x1264\n.set remaining_pc_00133a,0x133a\n.set remaining_pc_0013dc,0x13dc\n.set remaining_pc_0015be,0x15be\n.set remaining_pc_0016b4,0x16b4\n.set remaining_pc_001d18,0x1d18\n.set remaining_pc_0023f6,0x23f6\n.set remaining_pc_003a00,0x3a00\n.set remaining_pc_004890,0x4890\n.set remaining_pc_004998,0x4998\n.set remaining_pc_004a16,0x4a16\n.set remaining_pc_00506c,0x506c\n.set remaining_pc_0055b0,0x55b0\n.set remaining_pc_005694,0x5694\n.set remaining_pc_005868,0x5868\n.set remaining_pc_005a2a,0x5a2a\n.set remaining_pc_005abc,0x5abc\n.set remaining_pc_005c98,0x5c98\n.set remaining_pc_005f48,0x5f48\n.set remaining_pc_005f7c,0x5f7c\n.set remaining_pc_0063e6,0x63e6\n.set remaining_pc_006518,0x6518\n.set remaining_pc_00651c,0x651c\n.set remaining_pc_0067ca,0x67ca\n.set remaining_pc_00808a,0x808a\n.set remaining_pc_0083d4,0x83d4\n.set remaining_pc_008a60,0x8a60\n.set remaining_pc_0090d8,0x90d8\n.set remaining_pc_009390,0x9390\n.set remaining_pc_009e5e,0x9e5e\n.set remaining_pc_009f7c,0x9f7c\n.set remaining_pc_00a0cc,0xa0cc\n.set remaining_pc_00a10c,0xa10c\n.set remaining_pc_00a14e,0xa14e\n.set remaining_pc_00a158,0xa158\n.set remaining_pc_00a3da,0xa3da\n.set remaining_pc_00ac08,0xac08\n.set remaining_pc_00ad06,0xad06\n.set remaining_pc_00ae8a,0xae8a\n.set remaining_pc_00c0b6,0xc0b6\n.set remaining_pc_00c11e,0xc11e\n.set remaining_pc_00c3ce,0xc3ce\n.set remaining_pc_00c56e,0xc56e\n.set remaining_pc_00c58e,0xc58e\n.set remaining_pc_00c590,0xc590\n.set remaining_pc_00c764,0xc764\n.set remaining_pc_00c790,0xc790\n.set remaining_pc_00d8ae,0xd8ae\n.set remaining_pc_00dcf0,0xdcf0\n.set remaining_pc_00dea6,0xdea6\n.set remaining_pc_00e1f6,0xe1f6\n.set remaining_pc_00e592,0xe592\n.set remaining_pc_00e7b0,0xe7b0\n.set remaining_pc_00e82e,0xe82e\n.set remaining_pc_00ea38,0xea38\n.set remaining_pc_00ec0e,0xec0e\n.set remaining_pc_00ec16,0xec16\n.set remaining_pc_00ee16,0xee16\n.set remaining_pc_00f018,0xf018\n.set remaining_pc_00f088,0xf088\n.set remaining_pc_00f778,0xf778\n.set remaining_pc_00f7da,0xf7da\n.set remaining_pc_00f82c,0xf82c\n.set remaining_pc_00f990,0xf990\n.set remaining_pc_00f9d0,0xf9d0\n.set remaining_pc_00fae0,0xfae0\n.set remaining_pc_00fbaa,0xfbaa\n.set remaining_pc_00fdd0,0xfdd0\n.set remaining_pc_0101f8,0x101f8\n.set remaining_pc_01072c,0x1072c\n.set remaining_pc_011186,0x11186\n.set remaining_pc_0111ac,0x111ac\n.set remaining_pc_011624,0x11624\n.set remaining_pc_011cf2,0x11cf2\n.set remaining_pc_011e3c,0x11e3c\n.set remaining_pc_011f82,0x11f82\n.set remaining_pc_012008,0x12008\n.set remaining_pc_01221c,0x1221c\n.set remaining_pc_012292,0x12292\n.set remaining_pc_012314,0x12314\n.set remaining_pc_012418,0x12418\n.set remaining_pc_0125ac,0x125ac\n.set remaining_pc_012602,0x12602\n.set remaining_pc_012620,0x12620\n.set remaining_pc_01268c,0x1268c\n.set remaining_pc_0126d2,0x126d2\n.set remaining_pc_01270a,0x1270a\n.set remaining_pc_012734,0x12734\n.set remaining_pc_01273c,0x1273c\n.set remaining_pc_012744,0x12744\n.set remaining_pc_01274c,0x1274c\n.set remaining_pc_01278c,0x1278c\n.set remaining_pc_012878,0x12878\n.set remaining_pc_0128e2,0x128e2\n.set remaining_pc_01293c,0x1293c\n.set remaining_pc_012980,0x12980\n.set remaining_pc_012a98,0x12a98\n.set remaining_pc_012b6a,0x12b6a\n.set remaining_pc_012bc0,0x12bc0\n.set remaining_pc_012c0c,0x12c0c\n.set remaining_pc_012c84,0x12c84\n.set remaining_pc_012cbe,0x12cbe\n.set remaining_pc_012f58,0x12f58\n.set remaining_pc_013034,0x13034\n.set remaining_pc_01306a,0x1306a\n.set remaining_pc_013188,0x13188\n.set remaining_pc_01321c,0x1321c\n.set remaining_pc_013270,0x13270\n.set remaining_pc_013510,0x13510\n.set remaining_pc_01353e,0x1353e\n.set remaining_pc_0136f4,0x136f4\n.set remaining_pc_01374a,0x1374a\n.set remaining_pc_013934,0x13934\n.set remaining_pc_013958,0x13958\n.set remaining_pc_013b86,0x13b86\n.set remaining_pc_013bda,0x13bda\n.set remaining_pc_013c7e,0x13c7e\n.set remaining_pc_013df6,0x13df6\n.set remaining_pc_013e92,0x13e92\n.set remaining_pc_013f6c,0x13f6c\n.set remaining_pc_013faa,0x13faa\n.set remaining_pc_013fe4,0x13fe4\n.set remaining_pc_014106,0x14106\n.set remaining_pc_014120,0x14120\n.set remaining_pc_01416a,0x1416a\n.set remaining_pc_014294,0x14294\n.set remaining_pc_0142a2,0x142a2\n.set remaining_pc_014494,0x14494\n.set remaining_pc_014574,0x14574\n.set remaining_pc_0148a4,0x148a4\n.set remaining_pc_014914,0x14914\n.set remaining_pc_0149a0,0x149a0\n.set remaining_pc_014c7c,0x14c7c\n.set remaining_pc_014ca4,0x14ca4\n.set remaining_pc_014e20,0x14e20\n.set remaining_pc_0150de,0x150de\n.set remaining_pc_01512e,0x1512e\n.set remaining_pc_0152be,0x152be\n.set remaining_pc_015384,0x15384\n.set remaining_pc_015572,0x15572\n.set remaining_pc_015de6,0x15de6\n.set remaining_pc_0161d4,0x161d4\n.set remaining_pc_01626c,0x1626c\n.set remaining_pc_0164d4,0x164d4\n.set remaining_pc_016874,0x16874\n.set remaining_pc_016946,0x16946\n.set remaining_pc_0169aa,0x169aa\n.set remaining_pc_016c72,0x16c72\n.set remaining_pc_017c8a,0x17c8a\n.set remaining_pc_017f30,0x17f30\n.set remaining_pc_018f18,0x18f18\n.set remaining_pc_018ffc,0x18ffc\n.set remaining_pc_019018,0x19018\n.set remaining_pc_01a16e,0x1a16e\n.set remaining_pc_01a438,0x1a438\n.set remaining_pc_01a44e,0x1a44e\n.set remaining_pc_01a706,0x1a706\n.set remaining_pc_01a7a2,0x1a7a2\n.set remaining_pc_01b246,0x1b246\n.set remaining_pc_01b24c,0x1b24c\n.set remaining_pc_01b262,0x1b262\n.set remaining_pc_01b27a,0x1b27a\n.set remaining_pc_01b2bc,0x1b2bc\n.set remaining_pc_01b472,0x1b472\n.set remaining_pc_01b6c2,0x1b6c2\n.set remaining_pc_01b90c,0x1b90c\n.set remaining_pc_01b968,0x1b968\n.set remaining_pc_01cea0,0x1cea0\n.set remaining_pc_01d3bc,0x1d3bc\n.set remaining_pc_01e422,0x1e422\n.set remaining_pc_01e464,0x1e464\n.set remaining_pc_01e85a,0x1e85a\n.set remaining_pc_01ed78,0x1ed78\n.set remaining_pc_01f13c,0x1f13c\n.set remaining_pc_01f8d4,0x1f8d4\n.set remaining_pc_01faa8,0x1faa8\n.set remaining_pc_01fb12,0x1fb12\n.set remaining_pc_01fbd4,0x1fbd4\n.set remaining_pc_01fc50,0x1fc50\n.set remaining_pc_01fc7e,0x1fc7e\n.set remaining_pc_0208ce,0x208ce\n.set remaining_pc_021514,0x21514\n.set remaining_pc_0217c8,0x217c8\n.set remaining_pc_022b26,0x22b26\n.set remaining_pc_022c18,0x22c18\n.set remaining_pc_022c78,0x22c78\n.set remaining_pc_022cfe,0x22cfe\n.set remaining_pc_022d30,0x22d30\n.set remaining_pc_022ee0,0x22ee0\n.set remaining_pc_023046,0x23046\n.set remaining_pc_023198,0x23198\n.set remaining_pc_02330a,0x2330a\n.set remaining_pc_0233e2,0x233e2\n.set remaining_pc_0234d2,0x234d2\n.set remaining_pc_023736,0x23736\n.set remaining_pc_0239d6,0x239d6\n.set remaining_pc_0239f4,0x239f4\n.set remaining_pc_023a1a,0x23a1a\n.set remaining_pc_023a3c,0x23a3c\n.set remaining_pc_023b08,0x23b08\n.set remaining_pc_023ba6,0x23ba6\n.set remaining_pc_023bf4,0x23bf4\n.set remaining_pc_023c9a,0x23c9a\n.set remaining_pc_023d54,0x23d54\n.set remaining_pc_023e68,0x23e68\n.set remaining_pc_023ef2,0x23ef2\n.set remaining_pc_023f80,0x23f80\n.set remaining_pc_024048,0x24048\n.set remaining_pc_024188,0x24188\n.set remaining_pc_02419a,0x2419a\n.set remaining_pc_0241ae,0x241ae\n.set remaining_pc_024278,0x24278\n.set remaining_pc_0243a0,0x243a0\n.set remaining_pc_02443e,0x2443e\n.set remaining_pc_02456e,0x2456e\n.set remaining_pc_024580,0x24580\n.set remaining_pc_024594,0x24594\n.set remaining_pc_0245ba,0x245ba\n.set remaining_pc_02467e,0x2467e\n.set remaining_pc_024926,0x24926\n.set remaining_pc_024990,0x24990\n.set remaining_pc_024a14,0x24a14\n.set remaining_pc_024a36,0x24a36\n.set remaining_pc_024ab6,0x24ab6\n.set remaining_pc_026086,0x26086\n.set remaining_pc_0260b0,0x260b0\n.set remaining_pc_0260e4,0x260e4\n.set remaining_pc_0261a4,0x261a4\n.set remaining_pc_026214,0x26214\n.set remaining_pc_0262c6,0x262c6\n.set remaining_pc_026378,0x26378\n.set remaining_pc_0263d0,0x263d0\n.set remaining_pc_02648a,0x2648a\n.set remaining_pc_0264d0,0x264d0\n.set remaining_pc_026528,0x26528\n.set remaining_pc_026638,0x26638\n.set remaining_pc_02665e,0x2665e\n.set remaining_pc_026692,0x26692\n.set remaining_pc_026752,0x26752\n.set remaining_pc_0267aa,0x267aa\n.set remaining_pc_026854,0x26854\n.set remaining_pc_0268c4,0x268c4\n.set remaining_pc_026972,0x26972\n.set remaining_pc_026a20,0x26a20\n.set remaining_pc_026a78,0x26a78\n.set remaining_pc_026b2e,0x26b2e\n.set remaining_pc_026b74,0x26b74\n.set remaining_pc_026bc6,0x26bc6\n.set remaining_pc_026bfa,0x26bfa\n.set remaining_pc_027d1c,0x27d1c\n.set remaining_pc_03080e,0x3080e\n.set remaining_pc_030a74,0x30a74\n.set remaining_pc_0318ac,0x318ac\n.set remaining_pc_0320a0,0x320a0\n.set remaining_pc_032260,0x32260\n.set remaining_pc_03229c,0x3229c\n.set remaining_pc_032340,0x32340\n.set remaining_pc_03236e,0x3236e\n.set remaining_pc_032404,0x32404\n.set remaining_pc_03244a,0x3244a\n.set remaining_pc_0324fa,0x324fa\n.set remaining_pc_032a3a,0x32a3a\n.set remaining_pc_032a68,0x32a68\n.set remaining_pc_032b10,0x32b10\n.set remaining_pc_032b42,0x32b42\n.set remaining_pc_032c40,0x32c40\n.set remaining_pc_032d72,0x32d72\n.set remaining_pc_032e72,0x32e72\n.set remaining_pc_0330cc,0x330cc\n.set remaining_pc_0330de,0x330de\n.set remaining_pc_0333f4,0x333f4\n.set remaining_pc_033422,0x33422\n.set remaining_pc_033cf2,0x33cf2\n.set remaining_pc_03473a,0x3473a\n.set remaining_pc_03477a,0x3477a\n.set remaining_pc_035760,0x35760\n.set remaining_pc_03a978,0x3a978\n.set remaining_pc_03aa38,0x3aa38\n.set remaining_pc_03aab6,0x3aab6\n.set remaining_pc_03aad6,0x3aad6\n.set remaining_pc_03b2b0,0x3b2b0\n.set remaining_pc_03b2d8,0x3b2d8\n.set remaining_pc_0402c2,0x402c2\n.set remaining_pc_0662e4,0x662e4\n.set remaining_pc_0671b6,0x671b6\n.set remaining_pc_0674ca,0x674ca\n.set remaining_pc_0676c4,0x676c4\n.set remaining_pc_0676f2,0x676f2\n.set remaining_pc_0679fc,0x679fc\n'
EXTERNAL_TARGET_SYMBOLS=[518, 3750, 3856, 4590, 4648, 4708, 4922, 5084, 5566, 5812, 7448, 9206, 14848, 18576, 18840, 18966, 20588, 21936, 22164, 22632, 23082, 23228, 23704, 24392, 24444, 25574, 25880, 25884, 26570, 32906, 33748, 35424, 37080, 37776, 40542, 40828, 41164, 41228, 41294, 41304, 41946, 44040, 44294, 44682, 49334, 49438, 50126, 50542, 50574, 50576, 51044, 51088, 55470, 56560, 56998, 57846, 58770, 59312, 59438, 59960, 60430, 60438, 60950, 61464, 61576, 63352, 63450, 63532, 63888, 63952, 64224, 64426, 64976, 66040, 67372, 70022, 70060, 71204, 72946, 73276, 73602, 73736, 74268, 74386, 74516, 74776, 75180, 75266, 75296, 75404, 75474, 75530, 75572, 75580, 75588, 75596, 75660, 75896, 76002, 76092, 76160, 76440, 76650, 76736, 76812, 76932, 76990, 77656, 77876, 77930, 78216, 78364, 78448, 79120, 79166, 79604, 79690, 80180, 80216, 80774, 80858, 81022, 81398, 81554, 81772, 81834, 81892, 82182, 82208, 82282, 82580, 82594, 83092, 83316, 84132, 84244, 84384, 85116, 85156, 85536, 86238, 86318, 86718, 86916, 87410, 89574, 90580, 90732, 91348, 92276, 92486, 92586, 93298, 97418, 98096, 102168, 102396, 102424, 106862, 107576, 107598, 108294, 108450, 111174, 111180, 111202, 111226, 111292, 111730, 112322, 112908, 113000, 118432, 119740, 123938, 124004, 125018, 126328, 127292, 129236, 129704, 129810, 130004, 130128, 130174, 133326, 136468, 137160, 142118, 142360, 142456, 142590, 142640, 143072, 143430, 143768, 144138, 144354, 144594, 145206, 145878, 145908, 145946, 145980, 146184, 146342, 146420, 146586, 146772, 147048, 147186, 147328, 147528, 147848, 147866, 147886, 148088, 148384, 148542, 148846, 148864, 148884, 148922, 149118, 149798, 149904, 150036, 150070, 150198, 155782, 155824, 155876, 156068, 156180, 156358, 156536, 156624, 156810, 156880, 156968, 157240, 157278, 157330, 157522, 157610, 157780, 157892, 158066, 158240, 158328, 158510, 158580, 158662, 158714, 163100, 198670, 199284, 202924, 204960, 205408, 205468, 205632, 205678, 205828, 205898, 206074, 207418, 207464, 207632, 207682, 207936, 208242, 208498, 209100, 209118, 209908, 209954, 212210, 214842, 214906, 218976, 239992, 240184, 240310, 240342, 242352, 242392, 262850, 418532, 422326, 423114, 423620, 423666, 424444]

class Emitter:
    """Physical segments and ordinary instructions, not a virtual machine."""
    def __init__(self,binding):
        validate_binding(binding)
        self.binding=binding
        self.instructions=[]
        self.current=None
        self.segment_index=-1

    def segment(self,start,end):
        if self.current is not None and self.current!=self.binding.segments[self.segment_index][1]:
            raise CompileError('complete preceding segment required')
        self.segment_index+=1
        if self.segment_index>=len(self.binding.segments) or (start,end)!=self.binding.segments[self.segment_index]:
            raise CompileError('declared ordered physical segment required')
        self.current=start

    def ins(self,operation,operands='',width=2):
        if type(operation) is not str or re.fullmatch(r'[a-z]+(?:\.[bwl])?',operation) is None:
            raise CompileError('ordinary mnemonic required')
        if type(operands) is not str or any(c in operands for c in ('\n',';')):
            raise CompileError('one ordinary operand expression required')
        if type(width) is not int or width not in (2,4,6,8,10):
            raise CompileError('original instruction width required')
        if self.current is None or self.current+width>self.binding.segments[self.segment_index][1]:
            raise CompileError('instruction outside current physical segment')
        symbol='hl_'+self.binding.name+'_'+str(len(self.instructions))
        self.instructions.append(dict(symbol=symbol,operation=operation,operands=operands,
            encoding_bytes=width,target_PC=self.current,segment_index=self.segment_index))
        self.current+=width

    def unit(self,effects):
        if self.segment_index+1!=len(self.binding.segments) or self.current!=self.binding.segments[-1][1]:
            raise CompileError('all complete physical segments required')
        return dict(binding=asdict(self.binding),instructions=self.instructions,effects=effects)

def lower_declared(records,bindings,lowerers):
    if set(lowerers)!={b.name for b in bindings} or not set(lowerers)<=set(records):
        raise CompileError('complete physical lowerer coverage required')
    units=[]
    for binding in bindings:
        emitter=Emitter(binding)
        lowerers[binding.name](emitter,records[binding.name]['rules'])
        units.append(emitter.unit(records[binding.name]['effects']))
    return dict(units=units,original_generation_input=False,whole_closed_workflow=False)

def render_physical(units):
    """Interleaved components are emitted in actual PC order, never by entry."""
    instructions=sorted((row for unit in units for row in unit['instructions']),key=lambda r:r['target_PC'])
    if len({row['target_PC'] for row in instructions})!=len(instructions):
        raise CompileError('one instruction authority per physical PC required')
    beginnings,ends,entries={},{},{}
    for binding in BINDINGS:
        for index,(start,end) in enumerate(binding.segments):
            beginnings.setdefault(start,[]).append(binding.name+'_segment_'+str(index))
            ends.setdefault(end,[]).append(binding.name+'_segment_'+str(index)+'_end')
        for pc,name in binding.entries:
            entries.setdefault(pc,[]).append(name)
    lines=[ASSEMBLY_PREFIX]
    previous=None
    def labels(names):
        for name in names:lines.extend(('.global '+name,name+':'))
    for row in instructions:
        pc=row['target_PC']
        if previous is not None:
            labels(ends.get(previous,()))
        if previous!=pc:lines.append('.org 0x'+format(pc,'x'))
        labels(beginnings.get(pc,()))
        labels(entries.get(pc,()))
        labels(('remaining_pc_'+format(pc,'06x'),row['symbol']))
        lines.append('    '+row['operation']+(' '+row['operands'] if row['operands'] else ''))
        previous=pc+row['encoding_bytes']
    if previous is not None:labels(ends.get(previous,()))
    return '\n'.join(lines)+'\n'

def compile_modules(sources):
    from importlib import import_module
    from .target import MODULE_ROLES
    if type(sources) is not dict or set(sources)!=set(MODULE_ROLES) or any(type(v) is not str for v in sources.values()):
        raise CompileError('all declared business modules as explicit texts required')
    units=[]
    for name in MODULE_ROLES:
        compiler=import_module('.compiler_'+name.removeprefix('business_'),__package__)
        units.extend(compiler.compile_source(sources[name])['units'])
    units.sort(key=lambda unit:unit['binding']['entry'])
    if [unit['binding'] for unit in units]!=[asdict(binding) for binding in BINDINGS]:
        raise CompileError('complete disjoint source authority required')
    count=sum(len(unit['instructions']) for unit in units)
    total=sum(row['encoding_bytes'] for unit in units for row in unit['instructions'])
    if count!=INSTRUCTIONS or total!=TOTAL_BYTES:
        raise CompileError('complete physical instruction scope required')
    return dict(units=units,assembly=render_physical(units),allocated_bytes=total,
        instructions=count,new_bytes=NEW_BYTES,reused_bytes=REUSED_BYTES,
        original_generation_input=False,opaque_opcode_payload=False,
        complete_CPU=False,whole_closed_workflow=False,external_target_symbols=EXTERNAL_TARGET_SYMBOLS)
