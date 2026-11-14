"""Explicit MC68000 ABI, data bindings and allocation; no encoded instructions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Binding:
    name: str
    entry: int
    size: int
    variables: dict
    scratch: str | None = None

BINDINGS=(
 Binding('build_roster',0x5F48,52,dict(city='d0',assignments='a0',roster='a1',officer='d1',count='d3',head='d4',assigned='d2')),
 Binding('step_random',0x83D4,38,dict(seed='d1',previous='d0',sample='d0')),
 Binding('credit_primary',0x16C2C,26,dict(city='d0',modifiers='a0',offset='d1',factor='d7',ledger='a3')),
 Binding('credit_secondary',0x16C46,22,dict(city='d0',modifiers='a0',offset='d1',factor='d7',ledger='a3')),
 Binding('commit_income',0x16C5C,22,dict(city='d0',offset='d1',factor='d7',ledger='a3',gain='d3')),
 Binding('scaled_income',0x16C72,38,dict(offset='d1',factor='d7',rates='a1',thresholds='a2',bases='a5',gain='d3')),
 Binding('deplete_income',0x16C98,100,dict(city='d0',thresholds='a2',offset='d1',threshold='d2',tier='d3',saved_city='d2',parameters='a1',reduction_factor='d2',reserve='a2',loss='d3')),
 Binding('debit_primary',0x16D10,26,dict(city='d0',modifiers='a3',factor='d7',offset='d3',ledger='a5')),
 Binding('debit_secondary',0x16D2A,22,dict(city='d0',modifiers='a3',factor='d7',offset='d1',ledger='a5')),
 Binding('settle_expense',0x16D40,160,dict(city='d0',factor='d7',ledger='a5',categories='a4',count='d3',amounts='a0',roster='a1',total='d1',member='d2',fees_table='a1',fees='d2',category='d4',offset='d3',remaining='d4',borrowed='carry'),scratch='d3'),
 Binding('settle_shortage',0x16DEA,240,dict(outstanding='d4',factor='d7',roster='a0',scores='a1',first='a2',second='a3',member='d1',first_score='d2',score='d3',passes='d1',compared='d2',member_offset='d3',score_offset='d5',left='d6',amounts='a1',modifiers='a2',offset='d3',amount='d2',quantity='d6',modifier='d5',penalties='a2',deduction='d2',borrowed='carry'),scratch='d5'),
)
BY_NAME={b.name:b for b in BINDINGS}
SIGNATURES={
 'credit_primary':(('state','CityState'),('city','Word')),
 'credit_secondary':(('state','CityState'),('city','Word')),
 'commit_income':(('state','CityState'),('city','Word'),('offset','Word'),('factor','Word'),('ledger','Table')),
 'scaled_income':(('state','CityState'),('offset','Word'),('factor','Word')),
 'deplete_income':(('state','CityState'),('city','Word'),('thresholds','Table')),
 'debit_primary':(('state','CityState'),('city','Word')),
 'debit_secondary':(('state','CityState'),('city','Word')),
 'settle_expense':(('state','CityState'),('city','Word'),('factor','Word'),('ledger','Table')),
 'build_roster':(('state','CityState'),('city','Word')),
 'settle_shortage':(('state','CityState'),('outstanding','Long'),('factor','Word')),
 'step_random':(('state','CityState'),)}
RETURNS={'scaled_income':('d3',32),'build_roster':('d3',16),'step_random':('d0',16)}
TABLE_EXITS={'scaled_income':{'a1':'secondary_rates','a2':'depletion_modifiers','a5':'income_bases'}}
CALL_WRITES={
 'scaled_income':frozenset(('d7','d3','a1','a2','a5')),
 'step_random':frozenset(('d0','d1')),
 'build_roster':frozenset(('d1','d2','d3','d4','a0','a1')),
 'deplete_income':frozenset(('d0','d1','d2','d3','a1','a2')),
 'commit_income':frozenset(('d0','d1','d2','d3','d7','a1','a2','a5')),
 'settle_shortage':frozenset(('d1','d2','d3','d4','d5','d6','a0','a1','a2','a3')),
 'settle_expense':frozenset(('d0','d1','d2','d3','d4','d5','d6','a0','a1','a2','a3','a4'))}
TABLES=dict(city_modifiers=0xE280,primary_ledger=0xE000,secondary_ledger=0xE0A0,
 secondary_rates=0xE1E0,depletion_modifiers=0xE3C0,income_bases=0xE140,
 depletion_parameters=0x16CFC,depletion_reserve=0xE320,officer_categories=0xC700,
 officer_amounts=0xC800,roster=0xF500,expense_parameters=0x16DE0,
 officer_assignments=0xCC00,scores=0xEA60,first_score_components=0xBE00,
 second_score_components=0xC000,officer_modifiers=0xC200,officer_penalties=0xC300)
SCALARS=dict(head=(0xF630,16),roster_count=(0xF636,16),seed=(0xF61C,32),seed_high=(0xF61C,16))
CALLS={'commit_income':'bsr.w','scaled_income':'bsr.w','deplete_income':'bsr.w',
       'settle_expense':'bsr.w','settle_shortage':'bsr.w','build_roster':'jsr','step_random':'jsr'}
CONTRACT={
 'deplete_income':'incoming thresholds pointer remains live, supplied by scaled-income in credit chain; direct helper has no default clamp',
 'settle_expense':'roster rebind switches semantic cursor from a1 to a0 for second pass; ordinary original 2-byte compatibility NOP retained',
 'settle_shortage':'scores/roster/modifiers rebind between phases; WORD-clear preserves high outstanding bits; indexed displacement added after signed WORD',
 'all':'caller supplies real return frame; partial writes retain untouched register bits; input domains and ownership unknown; no IRQ/exception/timing claim'}

def tables_for_host():
    return {name:(address if address>65535 else (address|0xFFFF0000)) for name,address in TABLES.items()}
def scalars_for_host():
    return {name:(address|0xFFFF0000,width//8) for name,(address,width) in SCALARS.items()}
