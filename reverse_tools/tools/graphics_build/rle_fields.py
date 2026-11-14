"""Lossless command fields for the two original graphics RLE grammars.

Commands are the sole editable representation. Decoded projections are never
silently preferred over them. Fixed-cost encoding is optional, not relocation.
"""
from tools.audio_formats import audio_formats as af


def integer(value, maximum, label): return af._integer(value, maximum, label)


def parse_word(data, order, words):
    if type(data) is not bytes or not data or order not in ('big','little'):
        raise ValueError('invalid word stream')
    marker=data[0]; cursor=1; commands=[]; emitted=0
    while cursor<len(data):
        if data[cursor]==marker:
            if cursor+2>len(data): raise ValueError('short escape')
            count=data[cursor+1]; cursor+=2
            if count==0:
                if cursor!=len(data) or emitted!=words: raise ValueError('wrong terminator/decoded extent')
                return {'marker':marker,'commands':commands}
            if cursor+2>len(data): raise ValueError('short repeat word')
            value=int.from_bytes(data[cursor:cursor+2],order); cursor+=2
            commands.append({'op':'repeat','count':count+1,'word':value}); emitted+=count+1
        else:
            if cursor+2>len(data): raise ValueError('short literal word')
            value=int.from_bytes(data[cursor:cursor+2],order); cursor+=2
            commands.append({'op':'literal','word':value}); emitted+=1
        if emitted>words: raise ValueError('decoded word overrun')
    raise ValueError('missing word terminator')


def pack_word(fields,order,words):
    af._keys(fields,{'marker','commands'},'word stream')
    marker=integer(fields['marker'],255,'marker')
    if order not in ('big','little'): raise ValueError('word byte order')
    if type(fields['commands']) is not list or len(fields['commands'])>words:
        raise ValueError('word command count')
    output=bytearray([marker]); decoded=bytearray()
    for command in fields['commands']:
        if type(command) is not dict: raise ValueError('word command object')
        op=command.get('op')
        af._keys(command,{'op','word'}|({'count'} if op=='repeat' else set()),'word command')
        value=integer(command['word'],65535,'word'); raw=value.to_bytes(2,order)
        if op=='literal':
            if raw[0]==marker: raise ValueError('literal first byte equals escape marker')
            count=1; output.extend(raw)
        elif op=='repeat':
            count=integer(command['count'],256,'repeat count')
            if count<2: raise ValueError('word repeat requires 2..256 words')
            output.extend(bytes([marker,count-1])+raw)
        else: raise ValueError('unknown word command')
        decoded.extend(value.to_bytes(2,'big')*count)
        if len(decoded)>2*words: raise ValueError('decoded word overrun')
    if len(decoded)!=2*words: raise ValueError('decoded word extent')
    output.extend([marker,0])
    return bytes(output),bytes(decoded)


def parse_lanes(data,lane_size=1280):
    if type(data) is not bytes: raise ValueError('lane bytes required')
    cursor=0; lanes=[]
    for _ in range(2):
        commands=[]; count=0
        while count<lane_size:
            if cursor>=len(data): raise ValueError('short lane')
            control=data[cursor]; cursor+=1
            if control<0x80: op='literal'; n=control+1; size=n; produced=n
            elif control<0xc0: op='repeat'; n=(control&63)+1; size=1; produced=n
            elif control<0xe0: op='pair'; n=(control&31)+1; size=2; produced=2*n
            else: op='increment'; n=(control&31)+1; size=1; produced=n
            if cursor+size>len(data) or count+produced>lane_size: raise ValueError('lane overrun/truncated payload')
            payload=list(data[cursor:cursor+size]); cursor+=size; count+=produced
            command={'op':op,'values':payload} if op=='literal' else {'op':op,'count':n,'values':payload}
            commands.append(command)
        lanes.append(commands)
    if cursor!=len(data): raise ValueError('trailing lane bytes')
    return {'lanes':lanes}


def pack_lanes(fields,lane_size=1280):
    af._keys(fields,{'lanes'},'lane stream')
    if type(fields['lanes']) is not list or len(fields['lanes'])!=2: raise ValueError('two lanes required')
    output=bytearray(); decoded=[]
    for commands in fields['lanes']:
        if type(commands) is not list or len(commands)>lane_size: raise ValueError('lane command count')
        lane=bytearray()
        for command in commands:
            if type(command) is not dict: raise ValueError('lane command object')
            op=command.get('op')
            af._keys(command,{'op','values'}|({'count'} if op!='literal' else set()),'lane command')
            values=command['values']
            if type(values) is not list: raise ValueError('lane values array')
            raw=bytes(integer(v,255,'lane byte') for v in values)
            if op=='literal':
                if not 1<=len(raw)<=128: raise ValueError('literal count')
                control=len(raw)-1; expanded=raw
            elif op in ('repeat','pair','increment'):
                n=integer(command['count'],64 if op=='repeat' else 32,'lane count')
                if n==0 or len(raw)!=(2 if op=='pair' else 1): raise ValueError('lane payload/count')
                control={'repeat':0x80,'pair':0xc0,'increment':0xe0}[op]+n-1
                expanded=bytes((raw[0]+p)&255 for p in range(n)) if op=='increment' else raw*n
            else: raise ValueError('unknown lane command')
            output.extend(bytes([control])+raw); lane.extend(expanded)
            if len(lane)>lane_size: raise ValueError('lane decoded overrun')
        if len(lane)!=lane_size: raise ValueError('lane decoded extent')
        decoded.append(lane)
    interleaved=bytearray(2*lane_size); interleaved[::2]=decoded[0]; interleaved[1::2]=decoded[1]
    return bytes(output),bytes(interleaved)


def encode_word_exact(decoded,order,marker,encoded_size):
    """Find an exact-cost command path for ONE specified marker, or reject.

    A failed search proves nothing about other markers or relocated storage.
    Bits in reachable[p] denote body byte costs after p decoded words.
    """
    integer(marker,255,'marker'); integer(encoded_size,65536,'encoded size')
    if type(decoded) is not bytes or len(decoded)%2 or len(decoded)>8192 or order not in ('big','little'):
        raise ValueError('bounded even decoded words required')
    target=encoded_size-3
    if target<0 or target&1: raise ValueError('word stream cost parity')
    words=[int.from_bytes(decoded[p:p+2],'big') for p in range(0,len(decoded),2)]
    reachable=[0]*(len(words)+1); reachable[0]=1; mask=(1<<(target+1))-1
    def options(p):
        if words[p].to_bytes(2,order)[0]!=marker: yield 1,2
        n=2
        while n<=256 and p+n<=len(words) and words[p+n-1]==words[p]:
            yield n,4; n+=1
    for p in range(len(words)):
        if reachable[p]:
            for n,cost in options(p): reachable[p+n]|=(reachable[p]<<cost)&mask
    if not (reachable[-1]>>target)&1: raise ValueError('no exact fit for this marker and fixed slot')
    # Reverse traversal gives a deterministic command sequence in the same grammar.
    p=len(words); cost=target; commands=[]
    while p:
        found=False
        for n in range(1,min(256,p)+1):
            previous=p-n; expense=2 if n==1 else 4
            if cost<expense or not (reachable[previous]>>(cost-expense))&1: continue
            if n==1:
                if words[previous].to_bytes(2,order)[0]==marker: continue
            elif any(v!=words[previous] for v in words[previous:p]): continue
            command={'op':'literal','word':words[previous]} if n==1 else {'op':'repeat','count':n,'word':words[previous]}
            commands.append(command); p=previous; cost-=expense; found=True; break
        if not found: raise AssertionError('word path backtracking failed')
    result={'marker':marker,'commands':list(reversed(commands))}
    encoded,check=pack_word(result,order,len(words))
    if len(encoded)!=encoded_size or check!=decoded: raise AssertionError('word exact encoder mismatch')
    return result
