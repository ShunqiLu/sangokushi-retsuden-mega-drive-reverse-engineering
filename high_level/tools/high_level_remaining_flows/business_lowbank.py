"""Structured remaining gameplay/state logic, mechanically drafted then reviewed.

No instruction decoder, PC state, code array, file reader or media payload is
used at runtime. Ordinary values, typed live views and structured conditionals
retain width/order quirks. This draft is not full CPU or natural-call proof.
"""
from .domain import SceneState, Boundary, u8, u16, u32, s8, s16, low8, low16, replace_byte, replace_word, swap_words, checked_state
from .services import call_target, FirstDeploymentFrame
from .contexts_lowbank import (
    LowbankSelectLiveState1Input,
    LowbankSelectLiveState1Result,
    LowbankCoordinateLiveState1Input,
    LowbankCoordinateLiveState1Result,
    LowbankCoordinateLiveState1Service1,
    LowbankCoordinateLiveState1Service2,
    LowbankCoordinateLiveState1Service3,
    LowbankCoordinateLiveState1Service4,
    LowbankCoordinateLiveState1Service5,
    LowbankCoordinateLiveState2Input,
    LowbankCoordinateLiveState2Result,
    LowbankCoordinateLiveState2Service1,
    LowbankCoordinateLiveState2Service2,
    LowbankCoordinateLiveState2Service3,
    LowbankCoordinateLiveState2Service4,
    LowbankCoordinateLiveState2Service5,
    LowbankSelectLiveState2Input,
    LowbankSelectLiveState2Result,
    LowbankUpdateRecordFlags1Input,
    LowbankUpdateRecordFlags1Result,
    LowbankUpdateRecordFlags1Service1,
    LowbankUpdateRecordFlags1Service2,
    LowbankCoordinateLiveState3Input,
    LowbankCoordinateLiveState3Result,
    LowbankCoordinateLiveState4Input,
    LowbankCoordinateLiveState4Result,
    LowbankCoordinateLiveState5Input,
    LowbankCoordinateLiveState5Result,
    LowbankCoordinateLiveState6Input,
    LowbankCoordinateLiveState6Result,
    LowbankUpdateRecordFlags2Input,
    LowbankUpdateRecordFlags2Result,
    LowbankUpdateRecordFlags2Service1,
    LowbankUpdateRecordFlags2Service2,
    LowbankUpdateRecordFlags2Service3,
    LowbankUpdateRecordFlags2Service4,
    LowbankUpdateRecordFlags2Service5,
    LowbankSelectLiveState3Input,
    LowbankSelectLiveState3Result,
    LowbankSelectLiveState4Input,
    LowbankSelectLiveState4Result,
    LowbankCoordinateLiveState9Input,
    LowbankCoordinateLiveState9Result,
    LowbankCoordinateLiveState9Service1,
    LowbankCoordinateLiveState10Input,
    LowbankCoordinateLiveState10Result,
    LowbankCoordinateLiveState10Service1,
    LowbankCoordinateLiveState10Service2,
    LowbankSelectLiveState5Input,
    LowbankSelectLiveState5Result,
    LowbankUpdateRecordFlags3Input,
    LowbankUpdateRecordFlags3Result,
    LowbankSelectLiveState6Input,
    LowbankSelectLiveState6Result,
    LowbankUpdateRecordFlags2Alternate1Input,
    LowbankUpdateRecordFlags2Alternate1Result,
    LowbankUpdateRecordFlags2Alternate1Service1,
    LowbankUpdateRecordFlags2Alternate1Service2,
    LowbankUpdateRecordFlags2Alternate1Service3,
    LowbankUpdateRecordFlags2Alternate1Service4,
    LowbankUpdateRecordFlags2Alternate1Service5,
    LowbankUpdateRecordFlags2Alternate2Input,
    LowbankUpdateRecordFlags2Alternate2Result,
    LowbankUpdateRecordFlags2Alternate2Service1,
    LowbankUpdateRecordFlags2Alternate2Service2,
    LowbankUpdateRecordFlags2Alternate2Service3,
    LowbankUpdateRecordFlags2Alternate2Service4,
    LowbankUpdateRecordFlags2Alternate2Service5,
    LowbankCoordinateLiveState11Input,
    LowbankCoordinateLiveState11Result,
    LowbankCoordinateLiveState11Service1,
    LowbankCoordinateLiveState8Input,
    LowbankCoordinateLiveState8Result,
    LowbankCoordinateLiveState8Service1,
    LowbankCoordinateLiveState8Service2,
    LowbankCoordinateLiveState8Service3,
    LowbankCoordinateLiveState12Input,
    LowbankCoordinateLiveState12Result,
    LowbankCoordinateLiveState12Service1,
    LowbankUpdateRecordFlags2Alternate3Input,
    LowbankUpdateRecordFlags2Alternate3Result,
    LowbankUpdateRecordFlags2Alternate3Service1,
    LowbankUpdateRecordFlags2Alternate3Service2,
    LowbankUpdateRecordFlags2Alternate3Service3,
    LowbankUpdateRecordFlags2Alternate3Service4,
    LowbankUpdateRecordFlags2Alternate3Service5,
    LowbankUpdateRecordFlags2Alternate3Service6,
    LowbankUpdateRecordFlags2Alternate3Service7,
    LowbankUpdateRecordFlags2Alternate3Service8,
    LowbankUpdateRecordFlags2Alternate3Service9,
    LowbankUpdateRecordFlags2Alternate3Service10,
    LowbankUpdateRecordFlags2Alternate3Service11,
    LowbankUpdateRecordFlags2Alternate3Service12,
    LowbankUpdateRecordFlags2Alternate3Service13,
    LowbankUpdateRecordFlags2Alternate3Service14,
    LowbankCoordinateLiveState7Input,
    LowbankCoordinateLiveState7Result,
    LowbankCoordinateLiveState7Service1,
    LowbankCoordinateLiveState7Service2,
    LowbankUpdateRecordFlags2Alternate4Input,
    LowbankUpdateRecordFlags2Alternate4Result,
    LowbankUpdateRecordFlags2Alternate4Service1,
    LowbankUpdateRecordFlags2Alternate4Service2,
    LowbankUpdateRecordFlags2Alternate4Service3,
    LowbankUpdateRecordFlags2Alternate4Service4,
    LowbankUpdateRecordFlags2Alternate4Service5,
    LowbankUpdateRecordFlags3Alternate1Input,
    LowbankUpdateRecordFlags3Alternate1Result,
    LowbankUpdateRecordFlags3Alternate1Service1,
    LowbankCoordinateLiveState13Input,
    LowbankCoordinateLiveState13Result,
    LowbankCoordinateLiveState8Alternate1Input,
    LowbankCoordinateLiveState8Alternate1Result,
    LowbankCoordinateLiveState8Alternate1Service1,
    LowbankCoordinateLiveState8Alternate1Service2,
    LowbankCoordinateLiveState8Alternate1Service3,
    LowbankSelectLiveState7Input,
    LowbankSelectLiveState7Result,
    LowbankCoordinateLiveState14Input,
    LowbankCoordinateLiveState14Result,
    LowbankSelectLiveState8Input,
    LowbankSelectLiveState8Result,
    LowbankSelectLiveState9Input,
    LowbankSelectLiveState9Result,
    LowbankSelectLiveState10Input,
    LowbankSelectLiveState10Result,
    LowbankUpdateRecordFlags2Alternate5Input,
    LowbankUpdateRecordFlags2Alternate5Result,
    LowbankUpdateRecordFlags2Alternate5Service1,
    LowbankUpdateRecordFlags2Alternate5Service2,
    LowbankUpdateRecordFlags2Alternate5Service3,
    LowbankUpdateRecordFlags2Alternate5Service4,
    LowbankUpdateRecordFlags2Alternate5Service5,
    LowbankCoordinateLiveState15Input,
    LowbankCoordinateLiveState15Result,
    LowbankUpdateLiveFields1Input,
    LowbankUpdateLiveFields1Result,
    LowbankCoordinateLiveState16Input,
    LowbankCoordinateLiveState16Result,
    LowbankCoordinateLiveState16Service1,
    LowbankUpdateRecordFlags4Input,
    LowbankUpdateRecordFlags4Result,
    LowbankCoordinateLiveState17Input,
    LowbankCoordinateLiveState17Result,
    LowbankCoordinateLiveState17Service1,
    LowbankUpdateLiveFields2Input,
    LowbankUpdateLiveFields2Result,
    LowbankUpdateLiveFields3Input,
    LowbankUpdateLiveFields3Result,
    LowbankCoordinateLiveState18Input,
    LowbankCoordinateLiveState18Result,
    LowbankCoordinateLiveState18Service1,
    LowbankCoordinateLiveState18Service2,
    LowbankCoordinateLiveState18Service3,
    LowbankCoordinateLiveState19Input,
    LowbankCoordinateLiveState19Result,
    LowbankCoordinateLiveState19Service1,
    LowbankCoordinateLiveState19Service2,
    LowbankCoordinateLiveState20Input,
    LowbankCoordinateLiveState20Result,
    LowbankCoordinateLiveState20Service1,
    LowbankCoordinateLiveState20Service2,
    LowbankCoordinateLiveState21Input,
    LowbankCoordinateLiveState21Result,
    LowbankCoordinateLiveState21Service1,
    LowbankCoordinateLiveState21Service2,
    LowbankCoordinateLiveState22Input,
    LowbankCoordinateLiveState22Result,
    LowbankCoordinateLiveState22Service1,
    LowbankCoordinateLiveState22Service2,
    LowbankUpdateRecordFlags3Alternate2Input,
    LowbankUpdateRecordFlags3Alternate2Result,
    LowbankUpdateRecordFlags3Alternate2Service1,
    LowbankCoordinateLiveState23Input,
    LowbankCoordinateLiveState23Result,
    LowbankCoordinateLiveState23Service1,
    LowbankCoordinateLiveState23Service2,
    LowbankCoordinateLiveState24Input,
    LowbankCoordinateLiveState24Result,
    LowbankCoordinateLiveState25Input,
    LowbankCoordinateLiveState25Result,
    LowbankCoordinateLiveState26Input,
    LowbankCoordinateLiveState26Result,
    LowbankCoordinateLiveState27Input,
    LowbankCoordinateLiveState27Result,
    LowbankCoordinateLiveState28Input,
    LowbankCoordinateLiveState28Result,
    LowbankCoordinateLiveState29Input,
    LowbankCoordinateLiveState29Result,
    LowbankUpdateRecordFlags5Input,
    LowbankUpdateRecordFlags5Result,
    LowbankUpdateRecordFlags5Service1,
    LowbankCoordinateLiveState30Input,
    LowbankCoordinateLiveState30Result,
    LowbankCoordinateLiveState30Service1,
    LowbankCoordinateLiveState30Service2,
    LowbankUpdateRecordFlags6Input,
    LowbankUpdateRecordFlags6Result,
    LowbankUpdateRecordFlags6Service1,
    LowbankUpdateRecordFlags6Service2,
    LowbankCoordinateLiveState31Input,
    LowbankCoordinateLiveState31Result,
    LowbankCoordinateLiveState31Service1,
    LowbankCoordinateLiveState31Service2,
    LowbankCoordinateLiveState32Input,
    LowbankCoordinateLiveState32Result,
    LowbankUpdateRecordFlags7Input,
    LowbankUpdateRecordFlags7Result,
    LowbankUpdateRecordFlags7Service1,
    LowbankUpdateRecordFlags7Service2,
    LowbankUpdateRecordFlags7Service3,
    LowbankUpdateRecordFlags7Service4,
    LowbankCoordinateLiveState33Input,
    LowbankCoordinateLiveState33Result,
    LowbankCoordinateLiveState33Service1,
    LowbankCoordinateLiveState33Service2,
    LowbankCoordinateLiveState34Input,
    LowbankCoordinateLiveState34Result,
    LowbankCoordinateLiveState34Service1,
    LowbankUpdateRecordFlags8Input,
    LowbankUpdateRecordFlags8Result,
    LowbankUpdateRecordFlags8Service1,
    LowbankUpdateRecordFlags8Service2,
    LowbankSelectLiveState11Input,
    LowbankSelectLiveState11Result,
    LowbankCoordinateLiveState35Input,
    LowbankCoordinateLiveState35Result,
    LowbankCoordinateLiveState35Service1,
    LowbankCoordinateLiveState35Service2,
    LowbankCoordinateLiveState36Input,
    LowbankCoordinateLiveState36Result,
    LowbankCoordinateLiveState37Input,
    LowbankCoordinateLiveState37Result,
    LowbankCoordinateLiveState37Service1,
    LowbankCoordinateLiveState38Input,
    LowbankCoordinateLiveState38Result,
    LowbankCoordinateLiveState38Service1,
    LowbankCoordinateLiveState39Input,
    LowbankCoordinateLiveState39Result,
    LowbankCoordinateLiveState39Service1,
    LowbankCoordinateLiveState39Service2,
    LowbankCoordinateLiveState39Service3,
    LowbankCoordinateLiveState39Service4,
    LowbankCoordinateLiveState39Service5,
    LowbankCoordinateLiveState40Input,
    LowbankCoordinateLiveState40Result,
    LowbankCoordinateLiveState40Service1,
    LowbankCoordinateLiveState40Service2,
    LowbankCoordinateLiveState40Service3,
    LowbankCoordinateLiveState40Service4,
    LowbankCoordinateLiveState41Input,
    LowbankCoordinateLiveState41Result,
    LowbankCoordinateLiveState41Service1,
    LowbankCoordinateLiveState41Service2,
    LowbankCoordinateLiveState41Service3,
    LowbankCoordinateLiveState42Input,
    LowbankCoordinateLiveState42Result,
    LowbankCoordinateLiveState42Service1,
    LowbankCoordinateLiveState42Service2,
    LowbankCoordinateLiveState42Service3,
    LowbankProcessCountedRecords1Input,
    LowbankProcessCountedRecords1Result,
    LowbankCoordinateLiveState43Input,
    LowbankCoordinateLiveState43Result,
    LowbankCoordinateLiveState43Service1,
    LowbankCoordinateLiveState44Input,
    LowbankCoordinateLiveState44Result,
    LowbankCoordinateLiveState45Input,
    LowbankCoordinateLiveState45Result,
    LowbankCoordinateLiveState45Service1,
    LowbankCoordinateLiveState45Service2,
    LowbankCoordinateLiveState46Input,
    LowbankCoordinateLiveState46Result,
    LowbankCoordinateLiveState46Service1,
    LowbankCoordinateLiveState47Input,
    LowbankCoordinateLiveState47Result,
    LowbankSelectLiveState12Input,
    LowbankSelectLiveState12Result,
    LowbankCoordinateLiveState48Input,
    LowbankCoordinateLiveState48Result,
    LowbankCoordinateLiveState48Service1,
    LowbankCoordinateLiveState48Service2,
    LowbankCoordinateLiveState48Service3,
    LowbankCoordinateLiveState48Service4,
    LowbankCoordinateLiveState48Service5,
    LowbankCoordinateLiveState48Service6,
    LowbankCoordinateLiveState49Input,
    LowbankCoordinateLiveState49Result,
    LowbankCoordinateLiveState49Service1,
    LowbankCoordinateLiveState50Input,
    LowbankCoordinateLiveState50Result,
    LowbankCoordinateLiveState50Service1,
    LowbankCoordinateLiveState50Service2,
    LowbankCoordinateLiveState51Input,
    LowbankCoordinateLiveState51Result,
    LowbankCoordinateLiveState51Service1,
    LowbankCoordinateLiveState52Input,
    LowbankCoordinateLiveState52Result,
    LowbankCoordinateLiveState52Service1,
    LowbankCoordinateLiveState52Service2,
    LowbankCoordinateLiveState53Input,
    LowbankCoordinateLiveState53Result,
    LowbankCoordinateLiveState53Service1,
    LowbankCoordinateLiveState54Input,
    LowbankCoordinateLiveState54Result,
    LowbankCoordinateLiveState54Service1,
    LowbankCoordinateLiveState54Service2,
    LowbankCoordinateLiveState55Input,
    LowbankCoordinateLiveState55Result,
    LowbankCoordinateLiveState55Service1,
    LowbankCoordinateLiveState55Service2,
    LowbankCoordinateLiveState55Service3,
    LowbankCoordinateLiveState56Input,
    LowbankCoordinateLiveState56Result,
    LowbankCoordinateLiveState56Service1,
    LowbankCoordinateLiveState56Service2,
    LowbankSelectLiveState13Input,
    LowbankSelectLiveState13Result,
    LowbankSelectLiveState14Input,
    LowbankSelectLiveState14Result,
    LowbankSelectLiveState15Input,
    LowbankSelectLiveState15Result,
    LowbankCoordinateLiveState57Input,
    LowbankCoordinateLiveState57Result,
    LowbankCoordinateLiveState57Service1,
    LowbankCoordinateLiveState57Service2,
    LowbankCoordinateLiveState58Input,
    LowbankCoordinateLiveState58Result,
    LowbankUpdateLiveFields4Input,
    LowbankUpdateLiveFields4Result,
    LowbankSelectLiveState16Input,
    LowbankSelectLiveState16Result,
    LowbankProcessDeviceControl1Input,
    LowbankProcessDeviceControl1Result,
    LowbankProcessDeviceControl1Service1,
    LowbankProcessDeviceControl1Service2,
    LowbankSelectLiveState17Input,
    LowbankSelectLiveState17Result,
    LowbankProcessCountedRecords2Input,
    LowbankProcessCountedRecords2Result,
    LowbankProcessDeviceControl2Input,
    LowbankProcessDeviceControl2Result,
    LowbankProcessDeviceControl3Input,
    LowbankProcessDeviceControl3Result,
    LowbankProcessDeviceControl3Service1,
    LowbankProcessDeviceControl3Service2,
    LowbankProcessDeviceControl3Service3,
    LowbankProcessDeviceControl3Service4,
    LowbankProcessDeviceControl3Service5,
    LowbankProcessDeviceControl3Service6,
    LowbankProcessDeviceControl3Service7,
    LowbankProcessDeviceControl3Service8,
    LowbankProcessDeviceControl3Service9,
    LowbankProcessDeviceControl3Service10,
    LowbankProcessDeviceControl3Service11,
    LowbankProcessDeviceControl3Service12,
    LowbankProcessDeviceControl3Service13,
    LowbankProcessDeviceControl3Service14,
    LowbankProcessDeviceControl3Service15,
    LowbankProcessDeviceControl3Service16,
    LowbankProcessDeviceControl3Service17,
    LowbankProcessDeviceControl3Service18,
    LowbankProcessDeviceControl3Service19,
    LowbankProcessCountedRecords3Input,
    LowbankProcessCountedRecords3Result,
    LowbankProcessCountedRecords4Input,
    LowbankProcessCountedRecords4Result,
    LowbankSelectLiveState18Input,
    LowbankSelectLiveState18Result,
    LowbankProcessCountedRecords5Input,
    LowbankProcessCountedRecords5Result,
    LowbankProcessCountedRecords6Input,
    LowbankProcessCountedRecords6Result,
    LowbankProcessCountedRecords6Service1,
    LowbankCoordinateLiveState59Input,
    LowbankCoordinateLiveState59Result,
    LowbankCoordinateLiveState59Service1,
    LowbankCoordinateLiveState59Service2,
    LowbankProcessDeviceControl5Input,
    LowbankProcessDeviceControl5Result,
    LowbankCoordinateLiveState60Input,
    LowbankCoordinateLiveState60Result,
    LowbankCoordinateLiveState60Service1,
    LowbankCoordinateLiveState61Input,
    LowbankCoordinateLiveState61Result,
    LowbankCoordinateLiveState61Service1,
    LowbankCoordinateLiveState61Service2,
    LowbankCoordinateLiveState61Service3,
    LowbankCoordinateLiveState61Service4,
    LowbankProcessDeviceControl6Input,
    LowbankProcessDeviceControl6Result,
    LowbankProcessDeviceControl6Service1,
    LowbankCoordinateLiveState62Input,
    LowbankCoordinateLiveState62Result,
    LowbankSelectLiveState19Input,
    LowbankSelectLiveState19Result,
    LowbankSelectLiveState19Service1,
    LowbankProcessDeviceControl4Input,
    LowbankProcessDeviceControl4Result,
    LowbankProcessDeviceControl4Service1,
    LowbankProcessDeviceControl4Service2,
    LowbankCoordinateLiveState63Input,
    LowbankCoordinateLiveState63Result,
    LowbankProcessDeviceControl7Input,
    LowbankProcessDeviceControl7Result,
    LowbankCoordinateLiveState64Input,
    LowbankCoordinateLiveState64Result,
    LowbankCoordinateLiveState64Service1,
    LowbankCoordinateLiveState65Input,
    LowbankCoordinateLiveState65Result,
    LowbankCoordinateLiveState66Input,
    LowbankCoordinateLiveState66Result,
    LowbankProcessDeviceControl8Input,
    LowbankProcessDeviceControl8Result,
    LowbankProcessDeviceControl8Service1,
    LowbankProcessDeviceControl9Input,
    LowbankProcessDeviceControl9Result,
    LowbankProcessDeviceControl9Service1,
    LowbankSelectLiveState20Input,
    LowbankSelectLiveState20Result,
    LowbankCoordinateLiveState67Input,
    LowbankCoordinateLiveState67Result,
    LowbankCoordinateLiveState67Service1,
    LowbankSelectLiveState21Input,
    LowbankSelectLiveState21Result,
    LowbankCoordinateLiveState68Input,
    LowbankCoordinateLiveState68Result,
    LowbankCoordinateLiveState69Input,
    LowbankCoordinateLiveState69Result,
    LowbankProcessDeviceControl10Input,
    LowbankProcessDeviceControl10Result,
    LowbankCoordinateLiveState70Input,
    LowbankCoordinateLiveState70Result,
    LowbankCoordinateLiveState71Input,
    LowbankCoordinateLiveState71Result,
    LowbankUpdateLiveFields5Input,
    LowbankUpdateLiveFields5Result,
    LowbankUpdateLiveFields5Service1,
    LowbankSelectLiveState22Input,
    LowbankSelectLiveState22Result,
    LowbankSelectLiveState22Service1,
    LowbankCoordinateLiveState72Input,
    LowbankCoordinateLiveState72Result,
    LowbankCoordinateLiveState73Input,
    LowbankCoordinateLiveState73Result,
    LowbankProcessCountedRecords7Input,
    LowbankProcessCountedRecords7Result,
    LowbankProcessCountedRecords7Service1,
    LowbankProcessCountedRecords7Alternate1Input,
    LowbankProcessCountedRecords7Alternate1Result,
    LowbankProcessCountedRecords7Alternate1Service1,
    LowbankSelectLiveState23Input,
    LowbankSelectLiveState23Result,
    LowbankSelectLiveState24Input,
    LowbankSelectLiveState24Result,
    LowbankSelectLiveState24Service1,
    LowbankSelectLiveState25Input,
    LowbankSelectLiveState25Result,
    LowbankSelectLiveState25Service1,
    LowbankProcessCountedRecords8Input,
    LowbankProcessCountedRecords8Result,
    LowbankProcessCountedRecords8Alternate1Input,
    LowbankProcessCountedRecords8Alternate1Result,
    LowbankProcessCountedRecords8Alternate2Input,
    LowbankProcessCountedRecords8Alternate2Result,
    LowbankProcessCountedRecords8Alternate3Input,
    LowbankProcessCountedRecords8Alternate3Result,
    LowbankProcessCountedRecords8Alternate4Input,
    LowbankProcessCountedRecords8Alternate4Result,
    LowbankProcessCountedRecords8Alternate5Input,
    LowbankProcessCountedRecords8Alternate5Result,
    LowbankProcessCountedRecords9Input,
    LowbankProcessCountedRecords9Result,
    LowbankProcessCountedRecords9Service1,
    LowbankProcessCountedRecords9Alternate1Input,
    LowbankProcessCountedRecords9Alternate1Result,
    LowbankProcessCountedRecords9Alternate1Service1,
    LowbankProcessCountedRecords9Alternate2Input,
    LowbankProcessCountedRecords9Alternate2Result,
    LowbankProcessCountedRecords9Alternate2Service1,
    LowbankProcessCountedRecords9Alternate3Input,
    LowbankProcessCountedRecords9Alternate3Result,
    LowbankProcessCountedRecords9Alternate3Service1,
    LowbankCoordinateLiveState74Input,
    LowbankCoordinateLiveState74Result,
    LowbankCoordinateLiveState75Input,
    LowbankCoordinateLiveState75Result,
    LowbankCoordinateLiveState76Input,
    LowbankCoordinateLiveState76Result,
    LowbankCoordinateLiveState76Service1,
    LowbankCoordinateLiveState76Service2,
    LowbankCoordinateLiveState76Service3,
    LowbankCoordinateLiveState76Alternate1Input,
    LowbankCoordinateLiveState76Alternate1Result,
    LowbankCoordinateLiveState76Alternate1Service1,
    LowbankCoordinateLiveState76Alternate1Service2,
    LowbankCoordinateLiveState76Alternate1Service3,
    LowbankProcessCountedRecords10Input,
    LowbankProcessCountedRecords10Result,
    LowbankCoordinateLiveState77Input,
    LowbankCoordinateLiveState77Result,
    LowbankCoordinateLiveState77Service1,
    LowbankCoordinateLiveState77Service2,
    LowbankCoordinateLiveState77Service3,
    LowbankUpdateLiveFields6Input,
    LowbankUpdateLiveFields6Result,
    LowbankProcessCountedRecords11Input,
    LowbankProcessCountedRecords11Result,
    LowbankCoordinateLiveState78Input,
    LowbankCoordinateLiveState78Result,
    LowbankCoordinateLiveState78Service1,
    LowbankProcessCountedRecords12Input,
    LowbankProcessCountedRecords12Result,
    LowbankProcessDeviceControl11Input,
    LowbankProcessDeviceControl11Result,
    LowbankProcessDeviceControl11Service1,
    LowbankProcessDeviceControl11Service2,
    LowbankSelectLiveState26Input,
    LowbankSelectLiveState26Result,
    LowbankCoordinateLiveState79Input,
    LowbankCoordinateLiveState79Result,
    LowbankCoordinateLiveState79Service1,
    LowbankProcessCountedRecords13Input,
    LowbankProcessCountedRecords13Result,
    LowbankProcessCountedRecords13Service1,
    LowbankProcessCountedRecords14Input,
    LowbankProcessCountedRecords14Result,
    LowbankProcessCountedRecords14Service1,
    LowbankProcessCountedRecords13Alternate1Input,
    LowbankProcessCountedRecords13Alternate1Result,
    LowbankProcessCountedRecords13Alternate1Service1,
    LowbankProcessCountedRecords13Alternate2Input,
    LowbankProcessCountedRecords13Alternate2Result,
    LowbankProcessCountedRecords13Alternate2Service1,
    LowbankCoordinateLiveState80Input,
    LowbankCoordinateLiveState80Result,
    LowbankCoordinateLiveState80Service1,
    LowbankCoordinateLiveState81Input,
    LowbankCoordinateLiveState81Result,
    LowbankCoordinateLiveState81Service1,
    LowbankCoordinateLiveState82Input,
    LowbankCoordinateLiveState82Result,
    LowbankCoordinateLiveState82Service1,
    LowbankProcessCountedRecords15Input,
    LowbankProcessCountedRecords15Result,
    LowbankCoordinateLiveState83Input,
    LowbankCoordinateLiveState83Result,
    LowbankUpdateLiveFields7Input,
    LowbankUpdateLiveFields7Result,
    LowbankProcessCountedRecords16Input,
    LowbankProcessCountedRecords16Result,
    LowbankProcessCountedRecords16Service1,
    LowbankProcessCountedRecords17Input,
    LowbankProcessCountedRecords17Result,
    LowbankSelectLiveState27Input,
    LowbankSelectLiveState27Result,
    LowbankCoordinateLiveState84Input,
    LowbankCoordinateLiveState84Result,
    LowbankCoordinateLiveState84Service1,
    LowbankProcessCountedRecords18Input,
    LowbankProcessCountedRecords18Result,
    LowbankUpdateRecordFlags9Input,
    LowbankUpdateRecordFlags9Result,
    LowbankUpdateRecordFlags9Service1,
    LowbankCoordinateLiveState85Input,
    LowbankCoordinateLiveState85Result,
    LowbankCoordinateLiveState85Service1,
    LowbankCoordinateLiveState85Service2,
    LowbankCoordinateLiveState85Service3,
    LowbankResolveReadonlyState1Input,
    LowbankResolveReadonlyState1Result,
    LowbankProcessCountedRecords19Input,
    LowbankProcessCountedRecords19Result,
    LowbankCoordinateLiveState86Input,
    LowbankCoordinateLiveState86Result,
    LowbankCoordinateLiveState86Service1,
    LowbankCoordinateLiveState86Service2,
    LowbankProcessCountedRecords20Input,
    LowbankProcessCountedRecords20Result,
    LowbankProcessCountedRecords21Input,
    LowbankProcessCountedRecords21Result,
    LowbankCoordinateLiveState87Input,
    LowbankCoordinateLiveState87Result,
    LowbankCoordinateLiveState87Service1,
    LowbankCoordinateLiveState87Service2,
    LowbankCoordinateLiveState87Service3,
    LowbankSelectLiveState28Input,
    LowbankSelectLiveState28Result,
    LowbankSelectLiveState29Input,
    LowbankSelectLiveState29Result,
    LowbankSelectLiveState29Service1,
    LowbankSelectLiveState29Service2,
    LowbankSelectLiveState29Service3,
    LowbankSelectLiveState29Service4,
    LowbankUpdateRecordFlags10Input,
    LowbankUpdateRecordFlags10Result,
    LowbankUpdateRecordFlags10Service1,
    LowbankProcessCountedRecords22Input,
    LowbankProcessCountedRecords22Result,
    LowbankProcessCountedRecords23Input,
    LowbankProcessCountedRecords23Result,
    LowbankCoordinateLiveState88Input,
    LowbankCoordinateLiveState88Result,
    LowbankProcessCountedRecords24Input,
    LowbankProcessCountedRecords24Result,
    LowbankUpdateLiveFields8Input,
    LowbankUpdateLiveFields8Result,
    LowbankProcessCountedRecords25Input,
    LowbankProcessCountedRecords25Result,
    LowbankProcessCountedRecords26Input,
    LowbankProcessCountedRecords26Result,
    LowbankProcessCountedRecords27Input,
    LowbankProcessCountedRecords27Result,
    LowbankCoordinateLiveState90Input,
    LowbankCoordinateLiveState90Result,
    LowbankCoordinateLiveState90Service1,
    LowbankCoordinateLiveState90Service2,
    LowbankCoordinateLiveState91Input,
    LowbankCoordinateLiveState91Result,
    LowbankCoordinateLiveState91Alternate1Input,
    LowbankCoordinateLiveState91Alternate1Result,
    LowbankSelectLiveState30Input,
    LowbankSelectLiveState30Result,
    LowbankProcessCountedRecords28Input,
    LowbankProcessCountedRecords28Result,
    LowbankProcessCountedRecords28Service1,
    LowbankProcessCountedRecords29Input,
    LowbankProcessCountedRecords29Result,
    LowbankCoordinateLiveState92Input,
    LowbankCoordinateLiveState92Result,
    LowbankCoordinateLiveState92Service1,
    LowbankSelectLiveState31Input,
    LowbankSelectLiveState31Result,
    LowbankCoordinateLiveState93Input,
    LowbankCoordinateLiveState93Result,
    LowbankProcessCountedRecords30Input,
    LowbankProcessCountedRecords30Result,
    LowbankProcessCountedRecords31Input,
    LowbankProcessCountedRecords31Result,
    LowbankProcessCountedRecords33Input,
    LowbankProcessCountedRecords33Result,
    LowbankProcessCountedRecords34Input,
    LowbankProcessCountedRecords34Result,
    LowbankCoordinateLiveState94Input,
    LowbankCoordinateLiveState94Result,
    LowbankCoordinateLiveState95Input,
    LowbankCoordinateLiveState95Result,
    LowbankCoordinateLiveState95Service1,
    LowbankCoordinateLiveState96Input,
    LowbankCoordinateLiveState96Result,
    LowbankUpdateRecordFlags11Input,
    LowbankUpdateRecordFlags11Result,
    LowbankCoordinateLiveState97Input,
    LowbankCoordinateLiveState97Result,
    LowbankCoordinateLiveState98Input,
    LowbankCoordinateLiveState98Result,
    LowbankCoordinateLiveState98Service1,
    LowbankCoordinateLiveState98Service2,
    LowbankCoordinateLiveState98Service3,
    LowbankCoordinateLiveState99Input,
    LowbankCoordinateLiveState99Result,
    LowbankProcessCountedRecords35Input,
    LowbankProcessCountedRecords35Result,
    LowbankProcessCountedRecords36Input,
    LowbankProcessCountedRecords36Result,
    LowbankCoordinateLiveState100Input,
    LowbankCoordinateLiveState100Result,
    LowbankCoordinateLiveState101Input,
    LowbankCoordinateLiveState101Result,
    LowbankCoordinateLiveState101Service1,
    LowbankCoordinateLiveState102Input,
    LowbankCoordinateLiveState102Result,
    LowbankSelectLiveState32Input,
    LowbankSelectLiveState32Result,
    LowbankCoordinateLiveState103Input,
    LowbankCoordinateLiveState103Result,
    LowbankCoordinateLiveState103Service1,
    LowbankCoordinateLiveState103Service2,
    LowbankCoordinateLiveState103Service3,
    LowbankUpdateLiveFields9Input,
    LowbankUpdateLiveFields9Result,
    LowbankCoordinateLiveState104Input,
    LowbankCoordinateLiveState104Result,
    LowbankUpdateRecordFlags12Input,
    LowbankUpdateRecordFlags12Result,
    LowbankSelectLiveState33Input,
    LowbankSelectLiveState33Result,
    LowbankUpdateRecordFlags12Alternate1Input,
    LowbankUpdateRecordFlags12Alternate1Result,
    LowbankCoordinateLiveState105Input,
    LowbankCoordinateLiveState105Result,
    LowbankCoordinateLiveState105Service1,
    LowbankCalculateLiveQuotient1Input,
    LowbankCalculateLiveQuotient1Result,
    LowbankCalculateLiveQuotient1Service1,
    LowbankCalculateLiveQuotient1Service2,
    LowbankCalculateLiveQuotient1Service3,
    LowbankScaleLiveRecordValue1Input,
    LowbankScaleLiveRecordValue1Result,
    LowbankScaleLiveRecordValue1Service1,
    LowbankScaleLiveRecordValue1Service2,
    LowbankScaleLiveRecordValue1Service3,
    LowbankScaleLiveRecordValue1Service4,
    LowbankUpdateLiveFields10Input,
    LowbankUpdateLiveFields10Result,
    LowbankCoordinateLiveState107Input,
    LowbankCoordinateLiveState107Result,
    LowbankCoordinateLiveState107Service1,
    LowbankCoordinateLiveState107Service2,
    LowbankCoordinateLiveState107Service3,
    LowbankUpdateRecordFlags13Input,
    LowbankUpdateRecordFlags13Result,
    LowbankUpdateRecordFlags13Service1,
    LowbankUpdateRecordFlags13Service2,
    LowbankCoordinateLiveState106Input,
    LowbankCoordinateLiveState106Result,
    LowbankCoordinateLiveState106Service1,
    LowbankUpdateLiveFields11Input,
    LowbankUpdateLiveFields11Result,
    LowbankCoordinateLiveState108Input,
    LowbankCoordinateLiveState108Result,
    LowbankCoordinateLiveState108Service1,
    LowbankCalculateLiveQuotient2Input,
    LowbankCalculateLiveQuotient2Result,
    LowbankCalculateLiveQuotient2Service1,
    LowbankCalculateLiveQuotient2Service2,
    LowbankCoordinateLiveState106Alternate1Input,
    LowbankCoordinateLiveState106Alternate1Result,
    LowbankCoordinateLiveState106Alternate1Service1,
    LowbankCalculateLiveQuotient3Input,
    LowbankCalculateLiveQuotient3Result,
    LowbankCalculateLiveQuotient3Service1,
    LowbankCalculateLiveQuotient3Service2,
    LowbankCalculateLiveQuotient3Service3,
    LowbankCoordinateLiveState109Input,
    LowbankCoordinateLiveState109Result,
    LowbankCoordinateLiveState109Service1,
    LowbankCoordinateLiveState109Service2,
    LowbankUpdateRecordFlags14Input,
    LowbankUpdateRecordFlags14Result,
    LowbankSelectLiveState34Input,
    LowbankSelectLiveState34Result,
    LowbankProcessCountedRecords37Input,
    LowbankProcessCountedRecords37Result,
    LowbankProcessCountedRecords37Service1,
    LowbankCalculateLiveQuotient4Input,
    LowbankCalculateLiveQuotient4Result,
    LowbankCoordinateLiveState110Input,
    LowbankCoordinateLiveState110Result,
    LowbankCoordinateLiveState110Service1,
    LowbankUpdateLiveFields12Input,
    LowbankUpdateLiveFields12Result,
    LowbankUpdateLiveFields13Input,
    LowbankUpdateLiveFields13Result,
    LowbankUpdateLiveFields14Input,
    LowbankUpdateLiveFields14Result,
    LowbankUpdateLiveFields15Input,
    LowbankUpdateLiveFields15Result,
    LowbankUpdateLiveFields16Input,
    LowbankUpdateLiveFields16Result,
    LowbankUpdateLiveFields17Input,
    LowbankUpdateLiveFields17Result,
    LowbankUpdateLiveFields18Input,
    LowbankUpdateLiveFields18Result,
    LowbankUpdateLiveFields19Input,
    LowbankUpdateLiveFields19Result,
    LowbankScaleLiveRecordValue2Input,
    LowbankScaleLiveRecordValue2Result,
    LowbankScaleLiveRecordValue2Service1,
    LowbankScaleLiveRecordValue2Service2,
    LowbankCoordinateLiveState111Input,
    LowbankCoordinateLiveState111Result,
    LowbankCoordinateLiveState112Input,
    LowbankCoordinateLiveState112Result,
    LowbankCoordinateLiveState112Service1,
    LowbankUpdateRecordFlags15Input,
    LowbankUpdateRecordFlags15Result,
    LowbankProcessCountedRecords38Input,
    LowbankProcessCountedRecords38Result,
    LowbankProcessCountedRecords38Service1,
    LowbankProcessCountedRecords38Service2,
    LowbankProcessCountedRecords38Service3,
    LowbankCalculateLiveQuotient5Input,
    LowbankCalculateLiveQuotient5Result,
    LowbankCoordinateLiveState113Input,
    LowbankCoordinateLiveState113Result,
    LowbankCoordinateLiveState113Service1,
    LowbankCoordinateLiveState114Input,
    LowbankCoordinateLiveState114Result,
    LowbankCoordinateLiveState114Service1,
    LowbankCoordinateLiveState114Service2,
    LowbankCoordinateLiveState115Input,
    LowbankCoordinateLiveState115Result,
    LowbankCoordinateLiveState116Input,
    LowbankCoordinateLiveState116Result,
    LowbankCoordinateLiveState117Input,
    LowbankCoordinateLiveState117Result,
    LowbankCoordinateLiveState118Input,
    LowbankCoordinateLiveState118Result,
    LowbankCoordinateLiveState118Service1,
    LowbankScaleLiveRecordValue3Input,
    LowbankScaleLiveRecordValue3Result,
    LowbankResolveReadonlyState2Input,
    LowbankResolveReadonlyState2Result,
    LowbankScaleLiveRecordValue4Input,
    LowbankScaleLiveRecordValue4Result,
    LowbankScaleLiveRecordValue4Service1,
    LowbankScaleLiveRecordValue4Service2,
    LowbankScaleLiveRecordValue4Service3,
    LowbankCoordinateLiveState119Input,
    LowbankCoordinateLiveState119Result,
    LowbankCoordinateLiveState119Service1,
    LowbankCoordinateLiveState119Alternate1Input,
    LowbankCoordinateLiveState119Alternate1Result,
    LowbankCoordinateLiveState119Alternate1Service1,
    LowbankCoordinateLiveState119Alternate1Service2,
    LowbankCoordinateLiveState119Alternate1Service3,
    LowbankCoordinateLiveState119Alternate2Input,
    LowbankCoordinateLiveState119Alternate2Result,
    LowbankCoordinateLiveState119Alternate2Service1,
    LowbankCoordinateLiveState119Alternate2Service2,
    LowbankCoordinateLiveState119Alternate2Service3,
    LowbankCoordinateLiveState120Input,
    LowbankCoordinateLiveState120Result,
    LowbankCoordinateLiveState121Input,
    LowbankCoordinateLiveState121Result,
    LowbankCoordinateLiveState122Input,
    LowbankCoordinateLiveState122Result,
    LowbankCoordinateLiveState123Input,
    LowbankCoordinateLiveState123Result,
    LowbankScaleLiveRecordValue4Alternate1Input,
    LowbankScaleLiveRecordValue4Alternate1Result,
    LowbankScaleLiveRecordValue4Alternate1Service1,
    LowbankScaleLiveRecordValue4Alternate1Service2,
    LowbankScaleLiveRecordValue4Alternate1Service3,
    LowbankScaleLiveRecordValue4Alternate1Service4,
    LowbankScaleLiveRecordValue4Alternate1Service5,
    LowbankScaleLiveRecordValue4Alternate1Service6,
    LowbankCoordinateLiveState124Input,
    LowbankCoordinateLiveState124Result,
    LowbankCoordinateLiveState124Service1,
    LowbankSelectLiveState35Input,
    LowbankSelectLiveState35Result,
    LowbankSelectLiveState36Input,
    LowbankSelectLiveState36Result,
    LowbankUpdateRecordFlags16Input,
    LowbankUpdateRecordFlags16Result,
    LowbankUpdateRecordFlags16Service1,
    LowbankUpdateRecordFlags16Service2,
    LowbankCoordinateLiveState125Input,
    LowbankCoordinateLiveState125Result,
    LowbankCoordinateLiveState125Service1,
    LowbankCoordinateLiveState126Input,
    LowbankCoordinateLiveState126Result,
    LowbankCoordinateLiveState126Service1,
    LowbankCoordinateLiveState126Service2,
    LowbankCoordinateLiveState126Service3,
    LowbankCoordinateLiveState126Service4,
    LowbankCoordinateLiveState126Service5,
    LowbankCoordinateLiveState126Service6,
    LowbankCoordinateLiveState126Service7,
    LowbankCoordinateLiveState126Service8,
    LowbankCoordinateLiveState126Service9,
    LowbankUpdateRecordFlags17Input,
    LowbankUpdateRecordFlags17Result,
    LowbankUpdateRecordFlags17Service1,
    LowbankUpdateRecordFlags17Service2,
    LowbankUpdateRecordFlags17Service3,
    LowbankUpdateRecordFlags17Service4,
    LowbankUpdateRecordFlags17Service5,
    LowbankCoordinateLiveState127Input,
    LowbankCoordinateLiveState127Result,
    LowbankCoordinateLiveState127Service1,
    LowbankCoordinateLiveState127Service2,
    LowbankSelectLiveState37Input,
    LowbankSelectLiveState37Result,
    LowbankSelectLiveState37Service1,
    LowbankUpdateRecordFlags18Input,
    LowbankUpdateRecordFlags18Result,
    LowbankUpdateRecordFlags18Service1,
    LowbankUpdateRecordFlags18Service2,
    LowbankSelectLiveState38Input,
    LowbankSelectLiveState38Result,
    LowbankSelectLiveState38Service1,
    LowbankCalculateLiveQuotient6Input,
    LowbankCalculateLiveQuotient6Result,
    LowbankCalculateLiveQuotient6Service1,
    LowbankCalculateLiveQuotient6Service2,
    LowbankCalculateLiveQuotient6Service3,
    LowbankCalculateLiveQuotient6Service4,
    LowbankCalculateLiveQuotient6Service5,
    LowbankCoordinateLiveState128Input,
    LowbankCoordinateLiveState128Result,
    LowbankCoordinateLiveState128Service1,
    LowbankScaleLiveRecordValue5Input,
    LowbankScaleLiveRecordValue5Result,
    LowbankScaleLiveRecordValue5Service1,
    LowbankScaleLiveRecordValue5Service2,
    LowbankScaleLiveRecordValue5Service3,
    LowbankScaleLiveRecordValue5Service4,
    LowbankScaleLiveRecordValue5Service5,
    LowbankScaleLiveRecordValue5Service6,
    LowbankScaleLiveRecordValue5Service7,
    LowbankScaleLiveRecordValue5Service8,
    LowbankScaleLiveRecordValue5Service9,
    LowbankScaleLiveRecordValue5Service10,
    LowbankCoordinateLiveState129Input,
    LowbankCoordinateLiveState129Result,
    LowbankCoordinateLiveState129Service1,
    LowbankCoordinateLiveState129Service2,
    LowbankCoordinateLiveState129Service3,
    LowbankCoordinateLiveState129Service4,
    LowbankCoordinateLiveState129Service5,
    LowbankCoordinateLiveState129Service6,
    LowbankCoordinateLiveState129Service7,
    LowbankProcessCountedRecords39Input,
    LowbankProcessCountedRecords39Result,
    LowbankProcessCountedRecords39Service1,
    LowbankProcessCountedRecords39Service2,
    LowbankProcessCountedRecords39Service3,
    LowbankCoordinateLiveState130Input,
    LowbankCoordinateLiveState130Result,
    LowbankCoordinateLiveState130Service1,
    LowbankCoordinateLiveState130Service2,
    LowbankCoordinateLiveState130Service3,
    LowbankCoordinateLiveState130Service4,
    LowbankCoordinateLiveState130Service5,
    LowbankCoordinateLiveState130Service6,
)

def lowbank_select_live_state_1(state: SceneState, inputs: LowbankSelectLiveState1Input | FirstDeploymentFrame) -> LowbankSelectLiveState1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_1_fields(state,inputs)
    return LowbankSelectLiveState1Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_1(state: SceneState, inputs: LowbankCoordinateLiveState1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_1_fields(state,inputs)
    return LowbankCoordinateLiveState1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_2(state: SceneState, inputs: LowbankCoordinateLiveState2Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_2_fields(state,inputs)
    return LowbankCoordinateLiveState2Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_2(state: SceneState, inputs: LowbankSelectLiveState2Input | FirstDeploymentFrame) -> LowbankSelectLiveState2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_2_fields(state,inputs)
    return LowbankSelectLiveState2Result(value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_1(state: SceneState, inputs: LowbankUpdateRecordFlags1Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_1_fields(state,inputs)
    return LowbankUpdateRecordFlags1Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_3(state: SceneState, inputs: LowbankCoordinateLiveState3Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_3_fields(state,inputs)
    return LowbankCoordinateLiveState3Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_4(state: SceneState, inputs: LowbankCoordinateLiveState4Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_4_fields(state,inputs)
    return LowbankCoordinateLiveState4Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_5(state: SceneState, inputs: LowbankCoordinateLiveState5Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_5_fields(state,inputs)
    return LowbankCoordinateLiveState5Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_6(state: SceneState, inputs: LowbankCoordinateLiveState6Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_6_fields(state,inputs)
    return LowbankCoordinateLiveState6Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2(state: SceneState, inputs: LowbankUpdateRecordFlags2Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_fields(state,inputs)
    return LowbankUpdateRecordFlags2Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_3(state: SceneState, inputs: LowbankSelectLiveState3Input | FirstDeploymentFrame) -> LowbankSelectLiveState3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_3_fields(state,inputs)
    return LowbankSelectLiveState3Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_4(state: SceneState, inputs: LowbankSelectLiveState4Input | FirstDeploymentFrame) -> LowbankSelectLiveState4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_4_fields(state,inputs)
    return LowbankSelectLiveState4Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_9(state: SceneState, inputs: LowbankCoordinateLiveState9Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_9_fields(state,inputs)
    return LowbankCoordinateLiveState9Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_10(state: SceneState, inputs: LowbankCoordinateLiveState10Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_10_fields(state,inputs)
    return LowbankCoordinateLiveState10Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_5(state: SceneState, inputs: LowbankSelectLiveState5Input | FirstDeploymentFrame) -> LowbankSelectLiveState5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_5_fields(state,inputs)
    return LowbankSelectLiveState5Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_3(state: SceneState, inputs: LowbankUpdateRecordFlags3Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_3_fields(state,inputs)
    return LowbankUpdateRecordFlags3Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_6(state: SceneState, inputs: LowbankSelectLiveState6Input | FirstDeploymentFrame) -> LowbankSelectLiveState6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_6_fields(state,inputs)
    return LowbankSelectLiveState6Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2_alternate_1(state: SceneState, inputs: LowbankUpdateRecordFlags2Alternate1Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_alternate_1_fields(state,inputs)
    return LowbankUpdateRecordFlags2Alternate1Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2_alternate_2(state: SceneState, inputs: LowbankUpdateRecordFlags2Alternate2Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_alternate_2_fields(state,inputs)
    return LowbankUpdateRecordFlags2Alternate2Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_11(state: SceneState, inputs: LowbankCoordinateLiveState11Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_11_fields(state,inputs)
    return LowbankCoordinateLiveState11Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_8(state: SceneState, inputs: LowbankCoordinateLiveState8Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_8_fields(state,inputs)
    return LowbankCoordinateLiveState8Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_12(state: SceneState, inputs: LowbankCoordinateLiveState12Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState12Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState12Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_12_fields(state,inputs)
    return LowbankCoordinateLiveState12Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2_alternate_3(state: SceneState, inputs: LowbankUpdateRecordFlags2Alternate3Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Alternate3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Alternate3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_alternate_3_fields(state,inputs)
    return LowbankUpdateRecordFlags2Alternate3Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_7(state: SceneState, inputs: LowbankCoordinateLiveState7Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_7_fields(state,inputs)
    return LowbankCoordinateLiveState7Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2_alternate_4(state: SceneState, inputs: LowbankUpdateRecordFlags2Alternate4Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Alternate4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Alternate4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_alternate_4_fields(state,inputs)
    return LowbankUpdateRecordFlags2Alternate4Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_3_alternate_1(state: SceneState, inputs: LowbankUpdateRecordFlags3Alternate1Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags3Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags3Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_3_alternate_1_fields(state,inputs)
    return LowbankUpdateRecordFlags3Alternate1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_13(state: SceneState, inputs: LowbankCoordinateLiveState13Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState13Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState13Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_13_fields(state,inputs)
    return LowbankCoordinateLiveState13Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_8_alternate_1(state: SceneState, inputs: LowbankCoordinateLiveState8Alternate1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState8Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState8Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_8_alternate_1_fields(state,inputs)
    return LowbankCoordinateLiveState8Alternate1Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_7(state: SceneState, inputs: LowbankSelectLiveState7Input | FirstDeploymentFrame) -> LowbankSelectLiveState7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_7_fields(state,inputs)
    return LowbankSelectLiveState7Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_14(state: SceneState, inputs: LowbankCoordinateLiveState14Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState14Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState14Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_14_fields(state,inputs)
    return LowbankCoordinateLiveState14Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_8(state: SceneState, inputs: LowbankSelectLiveState8Input | FirstDeploymentFrame) -> LowbankSelectLiveState8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_8_fields(state,inputs)
    return LowbankSelectLiveState8Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_9(state: SceneState, inputs: LowbankSelectLiveState9Input | FirstDeploymentFrame) -> LowbankSelectLiveState9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_9_fields(state,inputs)
    return LowbankSelectLiveState9Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_10(state: SceneState, inputs: LowbankSelectLiveState10Input | FirstDeploymentFrame) -> LowbankSelectLiveState10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_10_fields(state,inputs)
    return LowbankSelectLiveState10Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_2_alternate_5(state: SceneState, inputs: LowbankUpdateRecordFlags2Alternate5Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags2Alternate5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags2Alternate5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_2_alternate_5_fields(state,inputs)
    return LowbankUpdateRecordFlags2Alternate5Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_15(state: SceneState, inputs: LowbankCoordinateLiveState15Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState15Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState15Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_15_fields(state,inputs)
    return LowbankCoordinateLiveState15Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_1(state: SceneState, inputs: LowbankUpdateLiveFields1Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_1_fields(state,inputs)
    return LowbankUpdateLiveFields1Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_16(state: SceneState, inputs: LowbankCoordinateLiveState16Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState16Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState16Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_16_fields(state,inputs)
    return LowbankCoordinateLiveState16Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_4(state: SceneState, inputs: LowbankUpdateRecordFlags4Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_4_fields(state,inputs)
    return LowbankUpdateRecordFlags4Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_17(state: SceneState, inputs: LowbankCoordinateLiveState17Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState17Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState17Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_17_fields(state,inputs)
    return LowbankCoordinateLiveState17Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_2(state: SceneState, inputs: LowbankUpdateLiveFields2Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_2_fields(state,inputs)
    return LowbankUpdateLiveFields2Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_3(state: SceneState, inputs: LowbankUpdateLiveFields3Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_3_fields(state,inputs)
    return LowbankUpdateLiveFields3Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_18(state: SceneState, inputs: LowbankCoordinateLiveState18Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState18Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState18Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_18_fields(state,inputs)
    return LowbankCoordinateLiveState18Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_19(state: SceneState, inputs: LowbankCoordinateLiveState19Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState19Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState19Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_19_fields(state,inputs)
    return LowbankCoordinateLiveState19Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_20(state: SceneState, inputs: LowbankCoordinateLiveState20Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState20Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState20Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_20_fields(state,inputs)
    return LowbankCoordinateLiveState20Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_21(state: SceneState, inputs: LowbankCoordinateLiveState21Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState21Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState21Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_21_fields(state,inputs)
    return LowbankCoordinateLiveState21Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_22(state: SceneState, inputs: LowbankCoordinateLiveState22Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState22Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState22Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_22_fields(state,inputs)
    return LowbankCoordinateLiveState22Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_3_alternate_2(state: SceneState, inputs: LowbankUpdateRecordFlags3Alternate2Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags3Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags3Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_3_alternate_2_fields(state,inputs)
    return LowbankUpdateRecordFlags3Alternate2Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_23(state: SceneState, inputs: LowbankCoordinateLiveState23Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState23Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState23Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_23_fields(state,inputs)
    return LowbankCoordinateLiveState23Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_24(state: SceneState, inputs: LowbankCoordinateLiveState24Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState24Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState24Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_24_fields(state,inputs)
    return LowbankCoordinateLiveState24Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_25(state: SceneState, inputs: LowbankCoordinateLiveState25Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState25Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState25Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_25_fields(state,inputs)
    return LowbankCoordinateLiveState25Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_26(state: SceneState, inputs: LowbankCoordinateLiveState26Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState26Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState26Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_26_fields(state,inputs)
    return LowbankCoordinateLiveState26Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_27(state: SceneState, inputs: LowbankCoordinateLiveState27Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState27Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState27Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_27_fields(state,inputs)
    return LowbankCoordinateLiveState27Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_28(state: SceneState, inputs: LowbankCoordinateLiveState28Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState28Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState28Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_28_fields(state,inputs)
    return LowbankCoordinateLiveState28Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_29(state: SceneState, inputs: LowbankCoordinateLiveState29Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState29Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState29Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_29_fields(state,inputs)
    return LowbankCoordinateLiveState29Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_5(state: SceneState, inputs: LowbankUpdateRecordFlags5Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_5_fields(state,inputs)
    return LowbankUpdateRecordFlags5Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_30(state: SceneState, inputs: LowbankCoordinateLiveState30Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState30Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState30Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_30_fields(state,inputs)
    return LowbankCoordinateLiveState30Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_6(state: SceneState, inputs: LowbankUpdateRecordFlags6Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_6_fields(state,inputs)
    return LowbankUpdateRecordFlags6Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_31(state: SceneState, inputs: LowbankCoordinateLiveState31Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState31Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState31Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_31_fields(state,inputs)
    return LowbankCoordinateLiveState31Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_32(state: SceneState, inputs: LowbankCoordinateLiveState32Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState32Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState32Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_32_fields(state,inputs)
    return LowbankCoordinateLiveState32Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_7(state: SceneState, inputs: LowbankUpdateRecordFlags7Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_7_fields(state,inputs)
    return LowbankUpdateRecordFlags7Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_33(state: SceneState, inputs: LowbankCoordinateLiveState33Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState33Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState33Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_33_fields(state,inputs)
    return LowbankCoordinateLiveState33Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_34(state: SceneState, inputs: LowbankCoordinateLiveState34Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState34Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState34Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_34_fields(state,inputs)
    return LowbankCoordinateLiveState34Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_8(state: SceneState, inputs: LowbankUpdateRecordFlags8Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_8_fields(state,inputs)
    return LowbankUpdateRecordFlags8Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_11(state: SceneState, inputs: LowbankSelectLiveState11Input | FirstDeploymentFrame) -> LowbankSelectLiveState11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_11_fields(state,inputs)
    return LowbankSelectLiveState11Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_35(state: SceneState, inputs: LowbankCoordinateLiveState35Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState35Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState35Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_35_fields(state,inputs)
    return LowbankCoordinateLiveState35Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_36(state: SceneState, inputs: LowbankCoordinateLiveState36Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState36Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState36Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_36_fields(state,inputs)
    return LowbankCoordinateLiveState36Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_37(state: SceneState, inputs: LowbankCoordinateLiveState37Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState37Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState37Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_37_fields(state,inputs)
    return LowbankCoordinateLiveState37Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_38(state: SceneState, inputs: LowbankCoordinateLiveState38Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState38Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState38Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_38_fields(state,inputs)
    return LowbankCoordinateLiveState38Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_39(state: SceneState, inputs: LowbankCoordinateLiveState39Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState39Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState39Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_39_fields(state,inputs)
    return LowbankCoordinateLiveState39Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_40(state: SceneState, inputs: LowbankCoordinateLiveState40Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState40Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState40Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_40_fields(state,inputs)
    return LowbankCoordinateLiveState40Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_41(state: SceneState, inputs: LowbankCoordinateLiveState41Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState41Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState41Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_41_fields(state,inputs)
    return LowbankCoordinateLiveState41Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_42(state: SceneState, inputs: LowbankCoordinateLiveState42Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState42Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState42Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_42_fields(state,inputs)
    return LowbankCoordinateLiveState42Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_1(state: SceneState, inputs: LowbankProcessCountedRecords1Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_1_fields(state,inputs)
    return LowbankProcessCountedRecords1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_43(state: SceneState, inputs: LowbankCoordinateLiveState43Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState43Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState43Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_43_fields(state,inputs)
    return LowbankCoordinateLiveState43Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_44(state: SceneState, inputs: LowbankCoordinateLiveState44Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState44Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState44Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_44_fields(state,inputs)
    return LowbankCoordinateLiveState44Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_45(state: SceneState, inputs: LowbankCoordinateLiveState45Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState45Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState45Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_45_fields(state,inputs)
    return LowbankCoordinateLiveState45Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_46(state: SceneState, inputs: LowbankCoordinateLiveState46Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState46Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState46Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_46_fields(state,inputs)
    return LowbankCoordinateLiveState46Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_47(state: SceneState, inputs: LowbankCoordinateLiveState47Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState47Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState47Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_47_fields(state,inputs)
    return LowbankCoordinateLiveState47Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_12(state: SceneState, inputs: LowbankSelectLiveState12Input | FirstDeploymentFrame) -> LowbankSelectLiveState12Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState12Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_12_fields(state,inputs)
    return LowbankSelectLiveState12Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_48(state: SceneState, inputs: LowbankCoordinateLiveState48Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState48Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState48Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_48_fields(state,inputs)
    return LowbankCoordinateLiveState48Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_49(state: SceneState, inputs: LowbankCoordinateLiveState49Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState49Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState49Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_49_fields(state,inputs)
    return LowbankCoordinateLiveState49Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_50(state: SceneState, inputs: LowbankCoordinateLiveState50Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState50Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState50Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_50_fields(state,inputs)
    return LowbankCoordinateLiveState50Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_51(state: SceneState, inputs: LowbankCoordinateLiveState51Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState51Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState51Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_51_fields(state,inputs)
    return LowbankCoordinateLiveState51Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_52(state: SceneState, inputs: LowbankCoordinateLiveState52Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState52Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState52Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_52_fields(state,inputs)
    return LowbankCoordinateLiveState52Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_53(state: SceneState, inputs: LowbankCoordinateLiveState53Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState53Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState53Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_53_fields(state,inputs)
    return LowbankCoordinateLiveState53Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_54(state: SceneState, inputs: LowbankCoordinateLiveState54Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState54Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState54Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_54_fields(state,inputs)
    return LowbankCoordinateLiveState54Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_55(state: SceneState, inputs: LowbankCoordinateLiveState55Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState55Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState55Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_55_fields(state,inputs)
    return LowbankCoordinateLiveState55Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_56(state: SceneState, inputs: LowbankCoordinateLiveState56Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState56Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState56Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_56_fields(state,inputs)
    return LowbankCoordinateLiveState56Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_13(state: SceneState, inputs: LowbankSelectLiveState13Input | FirstDeploymentFrame) -> LowbankSelectLiveState13Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState13Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_13_fields(state,inputs)
    return LowbankSelectLiveState13Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_14(state: SceneState, inputs: LowbankSelectLiveState14Input | FirstDeploymentFrame) -> LowbankSelectLiveState14Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState14Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_14_fields(state,inputs)
    return LowbankSelectLiveState14Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_15(state: SceneState, inputs: LowbankSelectLiveState15Input | FirstDeploymentFrame) -> LowbankSelectLiveState15Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState15Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_15_fields(state,inputs)
    return LowbankSelectLiveState15Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_57(state: SceneState, inputs: LowbankCoordinateLiveState57Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState57Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState57Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_57_fields(state,inputs)
    return LowbankCoordinateLiveState57Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_58(state: SceneState, inputs: LowbankCoordinateLiveState58Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState58Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState58Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_58_fields(state,inputs)
    return LowbankCoordinateLiveState58Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_4(state: SceneState, inputs: LowbankUpdateLiveFields4Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_4_fields(state,inputs)
    return LowbankUpdateLiveFields4Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_16(state: SceneState, inputs: LowbankSelectLiveState16Input | FirstDeploymentFrame) -> LowbankSelectLiveState16Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState16Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_16_fields(state,inputs)
    return LowbankSelectLiveState16Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_1(state: SceneState, inputs: LowbankProcessDeviceControl1Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_1_fields(state,inputs)
    return LowbankProcessDeviceControl1Result(value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_17(state: SceneState, inputs: LowbankSelectLiveState17Input | FirstDeploymentFrame) -> LowbankSelectLiveState17Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState17Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_17_fields(state,inputs)
    return LowbankSelectLiveState17Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_2(state: SceneState, inputs: LowbankProcessCountedRecords2Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_2_fields(state,inputs)
    return LowbankProcessCountedRecords2Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, limit=returned.offset_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_2(state: SceneState, inputs: LowbankProcessDeviceControl2Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_2_fields(state,inputs)
    return LowbankProcessDeviceControl2Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_3(state: SceneState, inputs: LowbankProcessDeviceControl3Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_3_fields(state,inputs)
    return LowbankProcessDeviceControl3Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_3(state: SceneState, inputs: LowbankProcessCountedRecords3Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_3_fields(state,inputs)
    return LowbankProcessCountedRecords3Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_4(state: SceneState, inputs: LowbankProcessCountedRecords4Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_4_fields(state,inputs)
    return LowbankProcessCountedRecords4Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_18(state: SceneState, inputs: LowbankSelectLiveState18Input | FirstDeploymentFrame) -> LowbankSelectLiveState18Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState18Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_18_fields(state,inputs)
    return LowbankSelectLiveState18Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_5(state: SceneState, inputs: LowbankProcessCountedRecords5Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_5_fields(state,inputs)
    return LowbankProcessCountedRecords5Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_6(state: SceneState, inputs: LowbankProcessCountedRecords6Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_6_fields(state,inputs)
    return LowbankProcessCountedRecords6Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_59(state: SceneState, inputs: LowbankCoordinateLiveState59Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState59Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState59Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_59_fields(state,inputs)
    return LowbankCoordinateLiveState59Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_5(state: SceneState, inputs: LowbankProcessDeviceControl5Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_5_fields(state,inputs)
    return LowbankProcessDeviceControl5Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_60(state: SceneState, inputs: LowbankCoordinateLiveState60Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState60Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState60Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_60_fields(state,inputs)
    return LowbankCoordinateLiveState60Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_61(state: SceneState, inputs: LowbankCoordinateLiveState61Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState61Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState61Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_61_fields(state,inputs)
    return LowbankCoordinateLiveState61Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, limit=returned.offset_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_6(state: SceneState, inputs: LowbankProcessDeviceControl6Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_6_fields(state,inputs)
    return LowbankProcessDeviceControl6Result(destination=returned.roster, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_62(state: SceneState, inputs: LowbankCoordinateLiveState62Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState62Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState62Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_62_fields(state,inputs)
    return LowbankCoordinateLiveState62Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_19(state: SceneState, inputs: LowbankSelectLiveState19Input | FirstDeploymentFrame) -> LowbankSelectLiveState19Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState19Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_19_fields(state,inputs)
    return LowbankSelectLiveState19Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_4(state: SceneState, inputs: LowbankProcessDeviceControl4Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_4_fields(state,inputs)
    return LowbankProcessDeviceControl4Result(port=returned.auxiliary, value=returned.target_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_63(state: SceneState, inputs: LowbankCoordinateLiveState63Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState63Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState63Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_63_fields(state,inputs)
    return LowbankCoordinateLiveState63Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, palette=returned.opponent, roster=returned.scratch, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_7(state: SceneState, inputs: LowbankProcessDeviceControl7Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_7_fields(state,inputs)
    return LowbankProcessDeviceControl7Result(port=returned.auxiliary, value=returned.target_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_64(state: SceneState, inputs: LowbankCoordinateLiveState64Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState64Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState64Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_64_fields(state,inputs)
    return LowbankCoordinateLiveState64Result(port=returned.auxiliary, value=returned.target_x, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_65(state: SceneState, inputs: LowbankCoordinateLiveState65Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState65Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState65Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_65_fields(state,inputs)
    return LowbankCoordinateLiveState65Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_66(state: SceneState, inputs: LowbankCoordinateLiveState66Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState66Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState66Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_66_fields(state,inputs)
    return LowbankCoordinateLiveState66Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_8(state: SceneState, inputs: LowbankProcessDeviceControl8Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_8_fields(state,inputs)
    return LowbankProcessDeviceControl8Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_9(state: SceneState, inputs: LowbankProcessDeviceControl9Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_9_fields(state,inputs)
    return LowbankProcessDeviceControl9Result(port=returned.auxiliary, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_20(state: SceneState, inputs: LowbankSelectLiveState20Input | FirstDeploymentFrame) -> LowbankSelectLiveState20Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState20Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_20_fields(state,inputs)
    return LowbankSelectLiveState20Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_67(state: SceneState, inputs: LowbankCoordinateLiveState67Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState67Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState67Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_67_fields(state,inputs)
    return LowbankCoordinateLiveState67Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_21(state: SceneState, inputs: LowbankSelectLiveState21Input | FirstDeploymentFrame) -> LowbankSelectLiveState21Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState21Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_21_fields(state,inputs)
    return LowbankSelectLiveState21Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_68(state: SceneState, inputs: LowbankCoordinateLiveState68Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState68Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState68Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_68_fields(state,inputs)
    return LowbankCoordinateLiveState68Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_69(state: SceneState, inputs: LowbankCoordinateLiveState69Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState69Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState69Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_69_fields(state,inputs)
    return LowbankCoordinateLiveState69Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_10(state: SceneState, inputs: LowbankProcessDeviceControl10Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_10_fields(state,inputs)
    return LowbankProcessDeviceControl10Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_70(state: SceneState, inputs: LowbankCoordinateLiveState70Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState70Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState70Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_70_fields(state,inputs)
    return LowbankCoordinateLiveState70Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_71(state: SceneState, inputs: LowbankCoordinateLiveState71Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState71Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState71Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_71_fields(state,inputs)
    return LowbankCoordinateLiveState71Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_5(state: SceneState, inputs: LowbankUpdateLiveFields5Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_5_fields(state,inputs)
    return LowbankUpdateLiveFields5Result(row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_22(state: SceneState, inputs: LowbankSelectLiveState22Input | FirstDeploymentFrame) -> LowbankSelectLiveState22Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState22Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_22_fields(state,inputs)
    return LowbankSelectLiveState22Result(row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_72(state: SceneState, inputs: LowbankCoordinateLiveState72Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState72Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState72Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_72_fields(state,inputs)
    return LowbankCoordinateLiveState72Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_73(state: SceneState, inputs: LowbankCoordinateLiveState73Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState73Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState73Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_73_fields(state,inputs)
    return LowbankCoordinateLiveState73Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_7(state: SceneState, inputs: LowbankProcessCountedRecords7Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_7_fields(state,inputs)
    return LowbankProcessCountedRecords7Result(port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_7_alternate_1(state: SceneState, inputs: LowbankProcessCountedRecords7Alternate1Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords7Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords7Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_7_alternate_1_fields(state,inputs)
    return LowbankProcessCountedRecords7Alternate1Result(port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_23(state: SceneState, inputs: LowbankSelectLiveState23Input | FirstDeploymentFrame) -> LowbankSelectLiveState23Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState23Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_23_fields(state,inputs)
    return LowbankSelectLiveState23Result(port=returned.auxiliary, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_24(state: SceneState, inputs: LowbankSelectLiveState24Input | FirstDeploymentFrame) -> LowbankSelectLiveState24Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState24Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_24_fields(state,inputs)
    return LowbankSelectLiveState24Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_25(state: SceneState, inputs: LowbankSelectLiveState25Input | FirstDeploymentFrame) -> LowbankSelectLiveState25Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState25Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_25_fields(state,inputs)
    return LowbankSelectLiveState25Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8(state: SceneState, inputs: LowbankProcessCountedRecords8Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_fields(state,inputs)
    return LowbankProcessCountedRecords8Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8_alternate_1(state: SceneState, inputs: LowbankProcessCountedRecords8Alternate1Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_alternate_1_fields(state,inputs)
    return LowbankProcessCountedRecords8Alternate1Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8_alternate_2(state: SceneState, inputs: LowbankProcessCountedRecords8Alternate2Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_alternate_2_fields(state,inputs)
    return LowbankProcessCountedRecords8Alternate2Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8_alternate_3(state: SceneState, inputs: LowbankProcessCountedRecords8Alternate3Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Alternate3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Alternate3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_alternate_3_fields(state,inputs)
    return LowbankProcessCountedRecords8Alternate3Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8_alternate_4(state: SceneState, inputs: LowbankProcessCountedRecords8Alternate4Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Alternate4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Alternate4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_alternate_4_fields(state,inputs)
    return LowbankProcessCountedRecords8Alternate4Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_8_alternate_5(state: SceneState, inputs: LowbankProcessCountedRecords8Alternate5Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords8Alternate5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords8Alternate5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_8_alternate_5_fields(state,inputs)
    return LowbankProcessCountedRecords8Alternate5Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_9(state: SceneState, inputs: LowbankProcessCountedRecords9Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_9_fields(state,inputs)
    return LowbankProcessCountedRecords9Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_9_alternate_1(state: SceneState, inputs: LowbankProcessCountedRecords9Alternate1Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords9Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords9Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_9_alternate_1_fields(state,inputs)
    return LowbankProcessCountedRecords9Alternate1Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_9_alternate_2(state: SceneState, inputs: LowbankProcessCountedRecords9Alternate2Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords9Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords9Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_9_alternate_2_fields(state,inputs)
    return LowbankProcessCountedRecords9Alternate2Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_9_alternate_3(state: SceneState, inputs: LowbankProcessCountedRecords9Alternate3Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords9Alternate3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords9Alternate3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_9_alternate_3_fields(state,inputs)
    return LowbankProcessCountedRecords9Alternate3Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_74(state: SceneState,
                                    inputs: LowbankCoordinateLiveState74Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState74Result:
    """Project the sole full core; old unobserved SP/X/A2..A6 remain unknown."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState74Input:
        inputs.validate(state)
        raise Boundary('5AEE legacy DTO has no actual full entry frame/SP/X; use complete fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete entry fields required')
    result = lowbank_coordinate_live_state_74_fields(state, inputs)
    return LowbankCoordinateLiveState74Result(destination=result.roster, value=result.target_x,
        tile=result.unit, carry=bool(result.status & 1), zero=bool(result.status & 4),
        negative=bool(result.status & 8), overflow=bool(result.status & 2))

def lowbank_coordinate_live_state_75(state: SceneState,
                                    inputs: LowbankCoordinateLiveState75Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState75Result:
    """Project the sole full core, never manufacture missing address carriers."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState75Input:
        inputs.validate(state)
        raise Boundary('5B48 legacy DTO has no actual full entry frame/SP/X; use complete fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete entry fields required')
    result = lowbank_coordinate_live_state_75_fields(state, inputs)
    return LowbankCoordinateLiveState75Result(destination=result.roster, value=result.target_x,
        tile=result.unit, carry=bool(result.status & 1), zero=bool(result.status & 4),
        negative=bool(result.status & 8), overflow=bool(result.status & 2))

def lowbank_coordinate_live_state_76(state: SceneState, inputs: LowbankCoordinateLiveState76Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState76Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState76Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_76_fields(state,inputs)
    return LowbankCoordinateLiveState76Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_76_alternate_1(state: SceneState, inputs: LowbankCoordinateLiveState76Alternate1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState76Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState76Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_76_alternate_1_fields(state,inputs)
    return LowbankCoordinateLiveState76Alternate1Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_10(state: SceneState, inputs: LowbankProcessCountedRecords10Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_10_fields(state,inputs)
    return LowbankProcessCountedRecords10Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_77(state: SceneState, inputs: LowbankCoordinateLiveState77Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState77Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState77Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_77_fields(state,inputs)
    return LowbankCoordinateLiveState77Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_6(state: SceneState, inputs: LowbankUpdateLiveFields6Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_6_fields(state,inputs)
    return LowbankUpdateLiveFields6Result(destination=returned.roster, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_11(state: SceneState, inputs: LowbankProcessCountedRecords11Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_11_fields(state,inputs)
    return LowbankProcessCountedRecords11Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_78(state: SceneState, inputs: LowbankCoordinateLiveState78Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState78Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState78Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_78_fields(state,inputs)
    return LowbankCoordinateLiveState78Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_12(state: SceneState, inputs: LowbankProcessCountedRecords12Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords12Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords12Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_12_fields(state,inputs)
    return LowbankProcessCountedRecords12Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_device_control_11(state: SceneState, inputs: LowbankProcessDeviceControl11Input | FirstDeploymentFrame) -> LowbankProcessDeviceControl11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessDeviceControl11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_device_control_11_fields(state,inputs)
    return LowbankProcessDeviceControl11Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_26(state: SceneState, inputs: LowbankSelectLiveState26Input | FirstDeploymentFrame) -> LowbankSelectLiveState26Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState26Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_26_fields(state,inputs)
    return LowbankSelectLiveState26Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_79(state: SceneState, inputs: LowbankCoordinateLiveState79Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState79Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState79Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_79_fields(state,inputs)
    return LowbankCoordinateLiveState79Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_13(state: SceneState, inputs: LowbankProcessCountedRecords13Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords13Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords13Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_13_fields(state,inputs)
    return LowbankProcessCountedRecords13Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_14(state: SceneState, inputs: LowbankProcessCountedRecords14Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords14Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords14Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_14_fields(state,inputs)
    return LowbankProcessCountedRecords14Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_13_alternate_1(state: SceneState, inputs: LowbankProcessCountedRecords13Alternate1Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords13Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords13Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_13_alternate_1_fields(state,inputs)
    return LowbankProcessCountedRecords13Alternate1Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_13_alternate_2(state: SceneState, inputs: LowbankProcessCountedRecords13Alternate2Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords13Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords13Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_13_alternate_2_fields(state,inputs)
    return LowbankProcessCountedRecords13Alternate2Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_80(state: SceneState, inputs: LowbankCoordinateLiveState80Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState80Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState80Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_80_fields(state,inputs)
    return LowbankCoordinateLiveState80Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_81(state: SceneState, inputs: LowbankCoordinateLiveState81Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState81Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState81Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_81_fields(state,inputs)
    return LowbankCoordinateLiveState81Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_82(state: SceneState, inputs: LowbankCoordinateLiveState82Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState82Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState82Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_82_fields(state,inputs)
    return LowbankCoordinateLiveState82Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_15(state: SceneState, inputs: LowbankProcessCountedRecords15Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords15Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords15Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_15_fields(state,inputs)
    return LowbankProcessCountedRecords15Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_83(state: SceneState, inputs: LowbankCoordinateLiveState83Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState83Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState83Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_83_fields(state,inputs)
    return LowbankCoordinateLiveState83Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_7(state: SceneState, inputs: LowbankUpdateLiveFields7Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields7Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields7Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_7_fields(state,inputs)
    return LowbankUpdateLiveFields7Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_16(state: SceneState, inputs: LowbankProcessCountedRecords16Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords16Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords16Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_16_fields(state,inputs)
    return LowbankProcessCountedRecords16Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_17(state: SceneState, inputs: LowbankProcessCountedRecords17Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords17Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords17Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_17_fields(state,inputs)
    return LowbankProcessCountedRecords17Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_27(state: SceneState, inputs: LowbankSelectLiveState27Input | FirstDeploymentFrame) -> LowbankSelectLiveState27Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState27Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_27_fields(state,inputs)
    return LowbankSelectLiveState27Result(value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_84(state: SceneState, inputs: LowbankCoordinateLiveState84Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState84Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState84Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_84_fields(state,inputs)
    return LowbankCoordinateLiveState84Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_18(state: SceneState, inputs: LowbankProcessCountedRecords18Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords18Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords18Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_18_fields(state,inputs)
    return LowbankProcessCountedRecords18Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_9(state: SceneState, inputs: LowbankUpdateRecordFlags9Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_9_fields(state,inputs)
    return LowbankUpdateRecordFlags9Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_85(state: SceneState, inputs: LowbankCoordinateLiveState85Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState85Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState85Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_85_fields(state,inputs)
    return LowbankCoordinateLiveState85Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_resolve_readonly_state_1(state: SceneState, inputs: LowbankResolveReadonlyState1Input | FirstDeploymentFrame) -> LowbankResolveReadonlyState1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankResolveReadonlyState1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_resolve_readonly_state_1_fields(state,inputs)
    return LowbankResolveReadonlyState1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_19(state: SceneState, inputs: LowbankProcessCountedRecords19Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords19Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords19Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_19_fields(state,inputs)
    return LowbankProcessCountedRecords19Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_86(state: SceneState, inputs: LowbankCoordinateLiveState86Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState86Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState86Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_86_fields(state,inputs)
    return LowbankCoordinateLiveState86Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_20(state: SceneState, inputs: LowbankProcessCountedRecords20Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords20Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords20Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_20_fields(state,inputs)
    return LowbankProcessCountedRecords20Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_21(state: SceneState, inputs: LowbankProcessCountedRecords21Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords21Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords21Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_21_fields(state,inputs)
    return LowbankProcessCountedRecords21Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_87(state: SceneState, inputs: LowbankCoordinateLiveState87Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState87Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState87Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_87_fields(state,inputs)
    return LowbankCoordinateLiveState87Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_28(state: SceneState, inputs: LowbankSelectLiveState28Input | FirstDeploymentFrame) -> LowbankSelectLiveState28Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState28Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_28_fields(state,inputs)
    return LowbankSelectLiveState28Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_29(state: SceneState, inputs: LowbankSelectLiveState29Input | FirstDeploymentFrame) -> LowbankSelectLiveState29Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState29Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_29_fields(state,inputs)
    return LowbankSelectLiveState29Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_10(state: SceneState, inputs: LowbankUpdateRecordFlags10Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_10_fields(state,inputs)
    return LowbankUpdateRecordFlags10Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_22(state: SceneState, inputs: LowbankProcessCountedRecords22Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords22Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords22Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_22_fields(state,inputs)
    return LowbankProcessCountedRecords22Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_23(state: SceneState, inputs: LowbankProcessCountedRecords23Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords23Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords23Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_23_fields(state,inputs)
    return LowbankProcessCountedRecords23Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_88(state: SceneState, inputs: LowbankCoordinateLiveState88Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState88Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState88Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_88_fields(state,inputs)
    return LowbankCoordinateLiveState88Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_24(state: SceneState, inputs: LowbankProcessCountedRecords24Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords24Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords24Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_24_fields(state,inputs)
    return LowbankProcessCountedRecords24Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_8(state: SceneState, inputs: LowbankUpdateLiveFields8Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields8Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields8Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_8_fields(state,inputs)
    return LowbankUpdateLiveFields8Result(destination=returned.roster, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_25(state: SceneState, inputs: LowbankProcessCountedRecords25Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords25Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords25Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_25_fields(state,inputs)
    return LowbankProcessCountedRecords25Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_26(state: SceneState, inputs: LowbankProcessCountedRecords26Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords26Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords26Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_26_fields(state,inputs)
    return LowbankProcessCountedRecords26Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_27(state: SceneState, inputs: LowbankProcessCountedRecords27Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords27Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords27Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_27_fields(state,inputs)
    return LowbankProcessCountedRecords27Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_90(state: SceneState, inputs: LowbankCoordinateLiveState90Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState90Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState90Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_90_fields(state,inputs)
    return LowbankCoordinateLiveState90Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_91(state: SceneState, inputs: LowbankCoordinateLiveState91Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState91Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState91Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_91_fields(state,inputs)
    return LowbankCoordinateLiveState91Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_91_alternate_1(state: SceneState, inputs: LowbankCoordinateLiveState91Alternate1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState91Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState91Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_91_alternate_1_fields(state,inputs)
    return LowbankCoordinateLiveState91Alternate1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_30(state: SceneState, inputs: LowbankSelectLiveState30Input | FirstDeploymentFrame) -> LowbankSelectLiveState30Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState30Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_30_fields(state,inputs)
    return LowbankSelectLiveState30Result(value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_28(state: SceneState, inputs: LowbankProcessCountedRecords28Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords28Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords28Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_28_fields(state,inputs)
    return LowbankProcessCountedRecords28Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_29(state: SceneState, inputs: LowbankProcessCountedRecords29Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords29Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords29Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_29_fields(state,inputs)
    return LowbankProcessCountedRecords29Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_92(state: SceneState, inputs: LowbankCoordinateLiveState92Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState92Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState92Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_92_fields(state,inputs)
    return LowbankCoordinateLiveState92Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_31(state: SceneState, inputs: LowbankSelectLiveState31Input | FirstDeploymentFrame) -> LowbankSelectLiveState31Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState31Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_31_fields(state,inputs)
    return LowbankSelectLiveState31Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_93(state: SceneState, inputs: LowbankCoordinateLiveState93Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState93Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState93Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_93_fields(state,inputs)
    return LowbankCoordinateLiveState93Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_30(state: SceneState, inputs: LowbankProcessCountedRecords30Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords30Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords30Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_30_fields(state,inputs)
    return LowbankProcessCountedRecords30Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_31(state: SceneState, inputs: LowbankProcessCountedRecords31Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords31Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords31Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_31_fields(state,inputs)
    return LowbankProcessCountedRecords31Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_33(state: SceneState, inputs: LowbankProcessCountedRecords33Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords33Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords33Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_33_fields(state,inputs)
    return LowbankProcessCountedRecords33Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_34(state: SceneState, inputs: LowbankProcessCountedRecords34Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords34Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords34Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_34_fields(state,inputs)
    return LowbankProcessCountedRecords34Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_94(state: SceneState, inputs: LowbankCoordinateLiveState94Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState94Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState94Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_94_fields(state,inputs)
    return LowbankCoordinateLiveState94Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_95(state: SceneState, inputs: LowbankCoordinateLiveState95Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState95Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState95Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_95_fields(state,inputs)
    return LowbankCoordinateLiveState95Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_96(state: SceneState, inputs: LowbankCoordinateLiveState96Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState96Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState96Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_96_fields(state,inputs)
    return LowbankCoordinateLiveState96Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_11(state: SceneState, inputs: LowbankUpdateRecordFlags11Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_11_fields(state,inputs)
    return LowbankUpdateRecordFlags11Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_97(state: SceneState, inputs: LowbankCoordinateLiveState97Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState97Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState97Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_97_fields(state,inputs)
    return LowbankCoordinateLiveState97Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_98(state: SceneState, inputs: LowbankCoordinateLiveState98Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState98Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState98Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_98_fields(state,inputs)
    return LowbankCoordinateLiveState98Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_99(state: SceneState, inputs: LowbankCoordinateLiveState99Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState99Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState99Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_99_fields(state,inputs)
    return LowbankCoordinateLiveState99Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_35(state: SceneState, inputs: LowbankProcessCountedRecords35Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords35Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords35Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_35_fields(state,inputs)
    return LowbankProcessCountedRecords35Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_36(state: SceneState, inputs: LowbankProcessCountedRecords36Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords36Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords36Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_36_fields(state,inputs)
    return LowbankProcessCountedRecords36Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_100(state: SceneState, inputs: LowbankCoordinateLiveState100Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState100Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState100Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_100_fields(state,inputs)
    return LowbankCoordinateLiveState100Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_101(state: SceneState, inputs: LowbankCoordinateLiveState101Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState101Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState101Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_101_fields(state,inputs)
    return LowbankCoordinateLiveState101Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_102(state: SceneState, inputs: LowbankCoordinateLiveState102Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState102Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState102Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_102_fields(state,inputs)
    return LowbankCoordinateLiveState102Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_32(state: SceneState, inputs: LowbankSelectLiveState32Input | FirstDeploymentFrame) -> LowbankSelectLiveState32Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState32Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_32_fields(state,inputs)
    return LowbankSelectLiveState32Result(value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_103(state: SceneState, inputs: LowbankCoordinateLiveState103Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState103Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState103Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_103_fields(state,inputs)
    return LowbankCoordinateLiveState103Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_9(state: SceneState, inputs: LowbankUpdateLiveFields9Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields9Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields9Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_9_fields(state,inputs)
    return LowbankUpdateLiveFields9Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_104(state: SceneState, inputs: LowbankCoordinateLiveState104Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState104Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState104Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_104_fields(state,inputs)
    return LowbankCoordinateLiveState104Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_12(state: SceneState, inputs: LowbankUpdateRecordFlags12Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags12Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags12Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_12_fields(state,inputs)
    return LowbankUpdateRecordFlags12Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_33(state: SceneState, inputs: LowbankSelectLiveState33Input | FirstDeploymentFrame) -> LowbankSelectLiveState33Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState33Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_33_fields(state,inputs)
    return LowbankSelectLiveState33Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_12_alternate_1(state: SceneState, inputs: LowbankUpdateRecordFlags12Alternate1Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags12Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags12Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_12_alternate_1_fields(state,inputs)
    return LowbankUpdateRecordFlags12Alternate1Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_105(state: SceneState, inputs: LowbankCoordinateLiveState105Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState105Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState105Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_105_fields(state,inputs)
    return LowbankCoordinateLiveState105Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_1(state: SceneState, inputs: LowbankCalculateLiveQuotient1Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_1_fields(state,inputs)
    return LowbankCalculateLiveQuotient1Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_1(state: SceneState, inputs: LowbankScaleLiveRecordValue1Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_1_fields(state,inputs)
    return LowbankScaleLiveRecordValue1Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_10(state: SceneState, inputs: LowbankUpdateLiveFields10Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields10Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields10Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_10_fields(state,inputs)
    return LowbankUpdateLiveFields10Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_107(state: SceneState, inputs: LowbankCoordinateLiveState107Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState107Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState107Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_107_fields(state,inputs)
    return LowbankCoordinateLiveState107Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_13(state: SceneState, inputs: LowbankUpdateRecordFlags13Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags13Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags13Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_13_fields(state,inputs)
    return LowbankUpdateRecordFlags13Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_106(state: SceneState, inputs: LowbankCoordinateLiveState106Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState106Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState106Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_106_fields(state,inputs)
    return LowbankCoordinateLiveState106Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_11(state: SceneState, inputs: LowbankUpdateLiveFields11Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields11Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields11Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_11_fields(state,inputs)
    return LowbankUpdateLiveFields11Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_108(state: SceneState, inputs: LowbankCoordinateLiveState108Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState108Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState108Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_108_fields(state,inputs)
    return LowbankCoordinateLiveState108Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_2(state: SceneState, inputs: LowbankCalculateLiveQuotient2Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_2_fields(state,inputs)
    return LowbankCalculateLiveQuotient2Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_106_alternate_1(state: SceneState, inputs: LowbankCoordinateLiveState106Alternate1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState106Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState106Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_106_alternate_1_fields(state,inputs)
    return LowbankCoordinateLiveState106Alternate1Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_3(state: SceneState, inputs: LowbankCalculateLiveQuotient3Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_3_fields(state,inputs)
    return LowbankCalculateLiveQuotient3Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_109(state: SceneState, inputs: LowbankCoordinateLiveState109Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState109Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState109Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_109_fields(state,inputs)
    return LowbankCoordinateLiveState109Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_14(state: SceneState, inputs: LowbankUpdateRecordFlags14Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags14Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags14Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_14_fields(state,inputs)
    return LowbankUpdateRecordFlags14Result(source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_34(state: SceneState, inputs: LowbankSelectLiveState34Input | FirstDeploymentFrame) -> LowbankSelectLiveState34Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState34Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_34_fields(state,inputs)
    return LowbankSelectLiveState34Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_37(state: SceneState, inputs: LowbankProcessCountedRecords37Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords37Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords37Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_37_fields(state,inputs)
    return LowbankProcessCountedRecords37Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_4(state: SceneState, inputs: LowbankCalculateLiveQuotient4Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_4_fields(state,inputs)
    return LowbankCalculateLiveQuotient4Result(descriptor=returned.controller, records=returned.scan, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_110(state: SceneState, inputs: LowbankCoordinateLiveState110Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState110Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState110Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_110_fields(state,inputs)
    return LowbankCoordinateLiveState110Result(field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_12(state: SceneState, inputs: LowbankUpdateLiveFields12Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields12Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields12Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_12_fields(state,inputs)
    return LowbankUpdateLiveFields12Result(field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_13(state: SceneState, inputs: LowbankUpdateLiveFields13Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields13Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields13Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_13_fields(state,inputs)
    return LowbankUpdateLiveFields13Result(tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_14(state: SceneState, inputs: LowbankUpdateLiveFields14Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields14Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields14Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_14_fields(state,inputs)
    return LowbankUpdateLiveFields14Result(field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_15(state: SceneState, inputs: LowbankUpdateLiveFields15Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields15Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields15Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_15_fields(state,inputs)
    return LowbankUpdateLiveFields15Result(tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_16(state: SceneState, inputs: LowbankUpdateLiveFields16Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields16Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields16Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_16_fields(state,inputs)
    return LowbankUpdateLiveFields16Result(field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_17(state: SceneState, inputs: LowbankUpdateLiveFields17Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields17Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields17Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_17_fields(state,inputs)
    return LowbankUpdateLiveFields17Result(field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_18(state: SceneState, inputs: LowbankUpdateLiveFields18Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields18Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields18Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_18_fields(state,inputs)
    return LowbankUpdateLiveFields18Result(field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_live_fields_19(state: SceneState, inputs: LowbankUpdateLiveFields19Input | FirstDeploymentFrame) -> LowbankUpdateLiveFields19Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateLiveFields19Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_live_fields_19_fields(state,inputs)
    return LowbankUpdateLiveFields19Result(field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_2(state: SceneState, inputs: LowbankScaleLiveRecordValue2Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_2_fields(state,inputs)
    return LowbankScaleLiveRecordValue2Result(source=returned.candidates, descriptor=returned.controller, records=returned.scan, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_111(state: SceneState, inputs: LowbankCoordinateLiveState111Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState111Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState111Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_111_fields(state,inputs)
    return LowbankCoordinateLiveState111Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_112(state: SceneState, inputs: LowbankCoordinateLiveState112Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState112Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState112Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_112_fields(state,inputs)
    return LowbankCoordinateLiveState112Result(carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_15(state: SceneState, inputs: LowbankUpdateRecordFlags15Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags15Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags15Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_15_fields(state,inputs)
    return LowbankUpdateRecordFlags15Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_38(state: SceneState, inputs: LowbankProcessCountedRecords38Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords38Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords38Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_38_fields(state,inputs)
    return LowbankProcessCountedRecords38Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, palette=returned.opponent, roster=returned.scratch, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_5(state: SceneState, inputs: LowbankCalculateLiveQuotient5Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_5_fields(state,inputs)
    return LowbankCalculateLiveQuotient5Result(palette=returned.opponent, roster=returned.scratch, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_113(state: SceneState, inputs: LowbankCoordinateLiveState113Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState113Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState113Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_113_fields(state,inputs)
    return LowbankCoordinateLiveState113Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_114(state: SceneState, inputs: LowbankCoordinateLiveState114Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState114Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState114Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_114_fields(state,inputs)
    return LowbankCoordinateLiveState114Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_115(state: SceneState, inputs: LowbankCoordinateLiveState115Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState115Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState115Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_115_fields(state,inputs)
    return LowbankCoordinateLiveState115Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_116(state: SceneState, inputs: LowbankCoordinateLiveState116Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState116Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState116Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_116_fields(state,inputs)
    return LowbankCoordinateLiveState116Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_117(state: SceneState, inputs: LowbankCoordinateLiveState117Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState117Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState117Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_117_fields(state,inputs)
    return LowbankCoordinateLiveState117Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_118(state: SceneState, inputs: LowbankCoordinateLiveState118Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState118Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState118Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_118_fields(state,inputs)
    return LowbankCoordinateLiveState118Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, member=returned.offset_y, remaining=returned.choice, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_3(state: SceneState, inputs: LowbankScaleLiveRecordValue3Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue3Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue3Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_3_fields(state,inputs)
    return LowbankScaleLiveRecordValue3Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_resolve_readonly_state_2(state: SceneState, inputs: LowbankResolveReadonlyState2Input | FirstDeploymentFrame) -> LowbankResolveReadonlyState2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankResolveReadonlyState2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_resolve_readonly_state_2_fields(state,inputs)
    return LowbankResolveReadonlyState2Result(destination=returned.roster, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_4(state: SceneState, inputs: LowbankScaleLiveRecordValue4Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue4Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue4Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_4_fields(state,inputs)
    return LowbankScaleLiveRecordValue4Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, member=returned.offset_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_119(state: SceneState, inputs: LowbankCoordinateLiveState119Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState119Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState119Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_119_fields(state,inputs)
    return LowbankCoordinateLiveState119Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_119_alternate_1(state: SceneState, inputs: LowbankCoordinateLiveState119Alternate1Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState119Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState119Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_119_alternate_1_fields(state,inputs)
    return LowbankCoordinateLiveState119Alternate1Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_119_alternate_2(state: SceneState, inputs: LowbankCoordinateLiveState119Alternate2Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState119Alternate2Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState119Alternate2Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_119_alternate_2_fields(state,inputs)
    return LowbankCoordinateLiveState119Alternate2Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_120(state: SceneState, inputs: LowbankCoordinateLiveState120Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState120Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState120Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_120_fields(state,inputs)
    return LowbankCoordinateLiveState120Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_121(state: SceneState, inputs: LowbankCoordinateLiveState121Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState121Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState121Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_121_fields(state,inputs)
    return LowbankCoordinateLiveState121Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_122(state: SceneState, inputs: LowbankCoordinateLiveState122Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState122Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState122Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_122_fields(state,inputs)
    return LowbankCoordinateLiveState122Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_123(state: SceneState, inputs: LowbankCoordinateLiveState123Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState123Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState123Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_123_fields(state,inputs)
    return LowbankCoordinateLiveState123Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_4_alternate_1(state: SceneState, inputs: LowbankScaleLiveRecordValue4Alternate1Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue4Alternate1Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue4Alternate1Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_4_alternate_1_fields(state,inputs)
    return LowbankScaleLiveRecordValue4Alternate1Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, member=returned.offset_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_124(state: SceneState, inputs: LowbankCoordinateLiveState124Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState124Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState124Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_124_fields(state,inputs)
    return LowbankCoordinateLiveState124Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, port=returned.auxiliary, value=returned.target_x, tile=returned.unit, row=returned.count, offset=returned.distance, limit=returned.offset_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_35(state: SceneState, inputs: LowbankSelectLiveState35Input | FirstDeploymentFrame) -> LowbankSelectLiveState35Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState35Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_35_fields(state,inputs)
    return LowbankSelectLiveState35Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, tile=returned.unit, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_36(state: SceneState, inputs: LowbankSelectLiveState36Input | FirstDeploymentFrame) -> LowbankSelectLiveState36Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState36Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_36_fields(state,inputs)
    return LowbankSelectLiveState36Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, records=returned.scan, tile=returned.unit, offset=returned.distance, limit=returned.offset_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_16(state: SceneState, inputs: LowbankUpdateRecordFlags16Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags16Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags16Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_16_fields(state,inputs)
    return LowbankUpdateRecordFlags16Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_125(state: SceneState, inputs: LowbankCoordinateLiveState125Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState125Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState125Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_125_fields(state,inputs)
    return LowbankCoordinateLiveState125Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_126(state: SceneState, inputs: LowbankCoordinateLiveState126Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState126Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState126Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_126_fields(state,inputs)
    return LowbankCoordinateLiveState126Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_17(state: SceneState, inputs: LowbankUpdateRecordFlags17Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags17Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags17Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_17_fields(state,inputs)
    return LowbankUpdateRecordFlags17Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_127(state: SceneState, inputs: LowbankCoordinateLiveState127Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState127Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState127Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_127_fields(state,inputs)
    return LowbankCoordinateLiveState127Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_37(state: SceneState, inputs: LowbankSelectLiveState37Input | FirstDeploymentFrame) -> LowbankSelectLiveState37Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState37Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_37_fields(state,inputs)
    return LowbankSelectLiveState37Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_update_record_flags_18(state: SceneState, inputs: LowbankUpdateRecordFlags18Input | FirstDeploymentFrame) -> LowbankUpdateRecordFlags18Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankUpdateRecordFlags18Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_update_record_flags_18_fields(state,inputs)
    return LowbankUpdateRecordFlags18Result(destination=returned.roster, source=returned.candidates, port=returned.auxiliary, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_select_live_state_38(state: SceneState, inputs: LowbankSelectLiveState38Input | FirstDeploymentFrame) -> LowbankSelectLiveState38Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankSelectLiveState38Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_select_live_state_38_fields(state,inputs)
    return LowbankSelectLiveState38Result(destination=returned.roster, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_calculate_live_quotient_6(state: SceneState, inputs: LowbankCalculateLiveQuotient6Input | FirstDeploymentFrame) -> LowbankCalculateLiveQuotient6Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCalculateLiveQuotient6Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_calculate_live_quotient_6_fields(state,inputs)
    return LowbankCalculateLiveQuotient6Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_128(state: SceneState, inputs: LowbankCoordinateLiveState128Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState128Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState128Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_128_fields(state,inputs)
    return LowbankCoordinateLiveState128Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, tile=returned.unit, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_scale_live_record_value_5(state: SceneState, inputs: LowbankScaleLiveRecordValue5Input | FirstDeploymentFrame) -> LowbankScaleLiveRecordValue5Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankScaleLiveRecordValue5Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_scale_live_record_value_5_fields(state,inputs)
    return LowbankScaleLiveRecordValue5Result(destination=returned.roster, source=returned.candidates, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, offset=returned.distance, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_129(state: SceneState, inputs: LowbankCoordinateLiveState129Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState129Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState129Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_129_fields(state,inputs)
    return LowbankCoordinateLiveState129Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_process_counted_records_39(state: SceneState, inputs: LowbankProcessCountedRecords39Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords39Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords39Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_39_fields(state,inputs)
    return LowbankProcessCountedRecords39Result(destination=returned.roster, value=returned.target_x, field=returned.target_y, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

def lowbank_coordinate_live_state_130(state: SceneState, inputs: LowbankCoordinateLiveState130Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState130Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState130Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_130_fields(state,inputs)
    return LowbankCoordinateLiveState130Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

from .contexts_lowbank import (
    LowbankCoordinateLiveState89Input,
    LowbankCoordinateLiveState89Result,
    LowbankProcessCountedRecords32Input,
    LowbankProcessCountedRecords32Result,
)

def lowbank_process_counted_records_32(state: SceneState, inputs: LowbankProcessCountedRecords32Input | FirstDeploymentFrame) -> LowbankProcessCountedRecords32Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankProcessCountedRecords32Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_process_counted_records_32_fields(state,inputs)
    return LowbankProcessCountedRecords32Result(destination=returned.roster, source=returned.candidates, descriptor=returned.controller, value=returned.target_x, field=returned.target_y, tile=returned.unit, row=returned.count, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))

from dataclasses import replace

from .domain import SceneState, Boundary, u16, checked_state

from .services import call_target

from .contexts_lowbank import (
    LowbankCoordinateLiveState89Input, LowbankCoordinateLiveState89Result,
    LowbankProcessCountedRecords25Input,
)

def _require_force_relation_step_result(state, result):
    """Accept real supplied carrier/outcome results, never fake completion."""
    if type(result) is not LowbankCoordinateLiveState89Result:
        raise Boundary('force-relation step return ABI remains unbound')
    return result.validate(state)

def _force_relation_step_context(frame):
    """Expose only this draft's explicit contract; full older ABI is pending."""
    return LowbankCoordinateLiveState89Input(
        destination=frame.destination, value=frame.value,
        carry=frame.carry, zero=frame.zero,
        negative=frame.negative, overflow=frame.overflow)

def _compare_force_relation_word(frame, left, right):
    difference = u16(left - right)
    return replace(frame, carry=left < right, zero=difference == 0,
        negative=bool(difference & 0x8000),
        overflow=bool(((left ^ right) & (left ^ difference)) & 0x8000))

def _finish_force_relation_counted_records(state, frame):
    from .business_lowbank import lowbank_process_counted_records_25
    result = lowbank_process_counted_records_25(state,
        LowbankProcessCountedRecords25Input(value=frame.value,
            carry=frame.carry, zero=frame.zero,
            negative=frame.negative, overflow=frame.overflow))
    return LowbankCoordinateLiveState89Result(
        destination=result.destination, value=result.value,
        carry=result.carry, zero=result.zero,
        negative=result.negative, overflow=result.overflow).validate(state)

def lowbank_coordinate_live_state_89(state: SceneState, inputs: LowbankCoordinateLiveState89Input | FirstDeploymentFrame) -> LowbankCoordinateLiveState89Result:
    """Historic observation projection; missing real complete entry fields stop honestly."""
    checked_state(state)
    if type(inputs) is LowbankCoordinateLiveState89Input:
        inputs.validate(state)
        raise Boundary('legacy lowbank DTO did not observe complete D/A/CCR-X/SP; use actual Scene fields')
    if type(inputs) is not FirstDeploymentFrame:
        raise ValueError('function-specific DTO or actual complete fields required')
    returned=lowbank_coordinate_live_state_89_fields(state,inputs)
    return LowbankCoordinateLiveState89Result(destination=returned.roster, value=returned.target_x, carry=bool(returned.status & 1), zero=bool(returned.status & 4), negative=bool(returned.status & 8), overflow=bool(returned.status & 2))


# Current complete lowbank command-text queue; caller owns outer5ADE.
from .services import (first_replace, _movement_frame, _movement_move, _movement_compare, _movement_test, SceneRefreshMemory, stage_sprite_word_packet_fields, FirstDeploymentReturnBoundary, MovementContinuationBoundary)

def _lowbank_text_compare_fields(state: SceneState, frame: FirstDeploymentFrame,
                                 address: int, expected: int) -> FirstDeploymentFrame:
    """One ordered original CMPI.W, using the established WORD flag core."""
    return _movement_compare(state, frame, state.read(address, 2), expected, 16)
def _lowbank_text_mark_queue_fields(state: SceneState, frame: FirstDeploymentFrame,
                                  mask: int) -> FirstDeploymentFrame:
    """Preserve the actual F3A4 read/store and ORI.W CCR, including input X."""
    value = state.read(0xFFFFF3A4, 2) | mask
    state.write(0xFFFFF3A4, 2, value)
    return _movement_test(state, frame, value, 16)
def _lowbank_text_call_fields(state: SceneState, frame: FirstDeploymentFrame,
                             target: int, continuation: int) -> FirstDeploymentFrame:
    """Own one real inner LONG/RTS; preserve the caller's outer live slot."""
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    state.sr = (state.sr & 65504) | entered.status
    if target == 0x26BFA:
        result = stage_sprite_word_packet_fields(SceneRefreshMemory(state), entered)
    elif target == 0x5DCC:
        result = lowbank_coordinate_live_state_76_fields(state, entered)
    elif target == 0x5DD2:
        result = lowbank_coordinate_live_state_76_alternate_1_fields(state, entered)
    else:
        raise MovementContinuationBoundary(target, entered,
            'lowbank text child has no complete actual returned fields; real inner slot retained')
    result = _movement_frame(state, result)
    actual = result.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, result, continuation)
    result = first_replace(result, stack_cursor=result.stack_cursor.advance(4))
    state.sr = (state.sr & 65504) | result.status
    return result
def lowbank_coordinate_live_state_74_fields(state: SceneState,
                                           frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5AEE..5B48: select first command packet and conditionally extend it.

    A0 is the actual readonly source cursor; D2 carries the tile WORD without
    changing its high WORD. Every repeated mode/command read remains ordered.
    The extension5DCC keeps its real5B46 slot if its full child is unavailable.
    """
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, roster=state.table_at(0x5BE4).cursor())
    frame = _movement_move(state, frame, 'unit', 0xC484, 16)
    frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF612, 0x201)
    if frame.status & 4:
        frame = _movement_move(state, frame, 'unit', 0xC084, 16)
    else:
        frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF612, 0x20B)
        if frame.status & 4:
            frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF362, 5)
            if frame.status & 4:
                frame = _movement_move(state, frame, 'unit', 0xC084, 16)
    frame = _lowbank_text_call_fields(state, frame, 0x26BFA, 0x5B1E)
    frame = _lowbank_text_mark_queue_fields(state, frame, 0x8800)
    frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF612, 0x201)
    if frame.status & 4:
        return frame
    frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF612, 0x20B)
    if frame.status & 4:
        frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF362, 5)
        if frame.status & 4:
            return frame
    return _lowbank_text_call_fields(state, frame, 0x5DCC, 0x5B46)
def lowbank_coordinate_live_state_75_ordinary_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Actual5B5C entry: no F380 prefix reads; caller owns outer5ADE.

    The original5B48 facade delegates its ordinary arm here. This is the same
    sole packet algorithm, with actual inner26BFA/5B78 slot, not a second core.
    """
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'unit', 0xC084, 16)
    frame = first_replace(frame, roster=state.table_at(0x5C0C).cursor())
    frame = _lowbank_text_compare_fields(state, frame, 0xFFFFF612, 0x20A)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(0x5C68).cursor())
    frame = _lowbank_text_call_fields(state, frame, 0x26BFA, 0x5B78)
    return _lowbank_text_mark_queue_fields(state, frame, 0x8080)

def lowbank_coordinate_live_state_75_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5B48..5BE4: choose ordinary or special text packet, then stage it.

    Original mode85/87 arm intentionally re-reads F380 before each comparison.
    Table views take raw encoded WORD offsets; no source packet bytes are inline.
    """
    frame = _movement_frame(state, frame)
    frame = _lowbank_text_compare_fields(state, frame, 4294964096, 133)
    if not frame.status & 4:
        frame = _lowbank_text_compare_fields(state, frame, 4294964096, 135)
    if not frame.status & 4:
        return lowbank_coordinate_live_state_75_ordinary_fields(state, frame)
    return lowbank_coordinate_live_state_75_special_fields(state, frame)

def lowbank_coordinate_live_state_75_special_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Exact5B80 special packet entry; no5B48 F380 prefix and no extra physical CALL slot."""
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'unit', 49284, 16)
    frame = first_replace(frame, roster=state.table_at(23608).cursor())
    frame = _lowbank_text_compare_fields(state, frame, 4294964108, 161)
    if frame.status & 4:
        frame = first_replace(frame, roster=state.table_at(23656).cursor())
    else:
        frame = _lowbank_text_compare_fields(state, frame, 4294964754, 521)
        if frame.status & 4:
            frame = _lowbank_text_compare_fields(state, frame, 4294964066, 5)
            if frame.status & 4:
                frame = first_replace(frame, roster=state.table_at(23656).cursor())
    for mode in (108, 147, 148, 144):
        frame = _lowbank_text_compare_fields(state, frame, 4294964096, mode)
        if frame.status & 4:
            frame = first_replace(frame, roster=state.table_at(23564).cursor())
            break
    frame = _lowbank_text_call_fields(state, frame, 158714, 23516)
    return _lowbank_text_mark_queue_fields(state, frame, 32896)


# Lowbank52 full Scene UI: queue composition separated from input/choice logic.
from .services import (first_replace, _movement_frame, _movement_move, _movement_move_long, _movement_compare, _movement_test, _first_compare_long, FirstDeploymentReturnBoundary, MovementContinuationBoundary)

"""Lowbank UI shared packet operations; reuse existing Scene arithmetic/store cores.

The queue is live RAM, not a renderer substitute. Whole owners below retain
their own counters, actual return slots, addresses and original store order.
"""


def _lowbank_ui_store_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_store_fields
    return _city_ui_store_fields(state,frame,address,value,size,clear)


def _lowbank_ui_append_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_append_fields
    return _city_ui_append_fields(state,frame,value,size,clear)


def _lowbank_ui_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, subtract: bool=False) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_arithmetic_fields
    return _city_ui_arithmetic_fields(state,frame,name,amount,subtract)


def _lowbank_ui_memory_arithmetic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, amount: int, subtract: bool=False) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_memory_arithmetic_fields
    return _city_ui_memory_arithmetic_fields(state,frame,address,amount,subtract)


def _lowbank_ui_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, bit: int) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_bit_fields
    return _city_ui_bit_fields(state,frame,value,bit)


def _lowbank_ui_change_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int, enabled: bool) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _campaign_ui_change_bit_fields
    return _campaign_ui_change_bit_fields(state,frame,address,bit,enabled)


def _lowbank_ui_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int) -> FirstDeploymentFrame:
    from ..high_level_main_flows.business_commands import _city_ui_shift_fields
    return _city_ui_shift_fields(state,frame,name,amount)


def _lowbank_ui_packet_start_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Original LEA D100 followed by signed ADDA.W of the live queue WORD."""
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    return first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))


def _lowbank_ui_cell_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, offsets: tuple=()) -> FirstDeploymentFrame:
    """Write parallel rows in supplied original order, then postincrement A0."""
    for offset in offsets:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),value)
    return _lowbank_ui_append_fields(state,frame,value)


def _lowbank_ui_counter_fields(frame: FirstDeploymentFrame, name: str) -> FirstDeploymentFrame:
    """DBRA changes only the low counter WORD; MOVE/CLR flags remain live."""
    return first_replace(frame,**{name:replace_word(frame.carrier(name),u16(low16(frame.carrier(name))-1))})


def _lowbank_ui_repeat_cells_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, value: int, offsets: tuple=()) -> FirstDeploymentFrame:
    while True:
        frame=_lowbank_ui_cell_fields(state,frame,value,offsets)
        frame=_lowbank_ui_counter_fields(frame,name)
        if low16(frame.carrier(name))==65535:
            return frame


def _lowbank_ui_clear_cells_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, offsets: tuple=()) -> FirstDeploymentFrame:
    """Original CLR prior reads, in row order, with one real postincrement."""
    while True:
        for offset in offsets:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),0,2,True)
        frame=_lowbank_ui_append_fields(state,frame,0,2,True)
        frame=_lowbank_ui_counter_fields(frame,name)
        if low16(frame.carrier(name))==65535:
            return frame


def _lowbank_ui_call_fields(state: SceneState, frame: FirstDeploymentFrame,
        target: int, continuation: int) -> FirstDeploymentFrame:
    """One actual child LONG/RTS; only closed complete typed callees are routed."""
    stack = frame.stack_cursor.advance(-4)
    stack.set_long(0, continuation)
    entered = first_replace(frame, stack_cursor=stack)
    if target in (74268, 74386):
        from ..high_level_player_commands.contexts_command_fields import execute_command_menu_scene_fields
        returned = execute_command_menu_scene_fields(state, target, entered)
    elif target == 63352:
        from ..high_level_command_actions.contexts_personnel import execute_personnel_scene_fields
        returned = execute_personnel_scene_fields(state, target, entered)
    else:
        returned = _lowbank_ui_known_child_fields(state, entered, target)
    returned = _movement_frame(state, returned)
    actual = returned.stack_cursor.long()
    if actual != continuation:
        raise FirstDeploymentReturnBoundary(actual, returned, continuation)
    return first_replace(returned, stack_cursor=returned.stack_cursor.advance(4))


def _lowbank_ui_draw_choice_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: int, selection: int, origin_x: int, y: int,
        continuation: int) -> FirstDeploymentFrame:
    """Shared actual 3*selection*8 cursor packet, including its repeated RAM read."""
    frame=first_replace(frame,roster=state.table_at(source).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(selection,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',state.read(selection,2))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',3)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',origin_x)
    frame=_movement_move(state,frame,'target_y',y,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _lowbank_ui_call_fields(state,frame,0xAC08,continuation)


def _lowbank_ui_cursor_gate_fields(state: SceneState, frame: FirstDeploymentFrame,
        final_bit_set: bool=False) -> tuple[FirstDeploymentFrame, bool]:
    """Five closed cursor routines use this same ordered input observation."""
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return frame,False
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)
    if frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        return frame,bool(frame.status&4)!=final_bit_set
    return frame,True


def _lowbank_ui_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    return _movement_move(state,frame,'target_x',low16(frame.target_x)&3,16)


"""RAM word-queue composition: relation borders, lists and option packets.

Tile identifiers are original instruction immediates, not embedded media. Live
digits, lists and graphic descriptors stay in typed source/RAM resource views.
"""


def lowbank_process_counted_records_19_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C1E4: erase the selected paired row and optionally the following row."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    frame=_lowbank_ui_cell_fields(state,frame,13,(30,))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),3,16)
    if frame.status&1:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
        if not frame.status&4:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,3)
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',3)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',8)
    frame=_movement_move(state,frame,'target_y',0xCC34,16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x),True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.target_y))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',128)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',12,16)
    frame=_lowbank_ui_clear_cells_fields(state,frame,'target_x',(30,))
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
    # C232 really advances the queue by 0x3C0, not the neighboring 0x3C.
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,0x3C0)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),3)
    if not frame.status&4:
        frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),8,16)
        if frame.status&5:
            frame=first_replace(frame,roster=frame.roster.advance(30))
            frame=_lowbank_ui_cell_fields(state,frame,13,(30,))
            frame=_movement_move(state,frame,'target_x',0xCC84,16)
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF36A,2),16)
            frame=_lowbank_ui_shift_fields(state,frame,'target_y',8)
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y),True)
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.target_x))
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',128,True)
            frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
            frame=_movement_move(state,frame,'target_x',12,16)
            frame=_lowbank_ui_clear_cells_fields(state,frame,'target_x',(30,))
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,60)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)


def lowbank_process_counted_records_20_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C2A6: two neighboring 13-cell heading/footer borders."""
    frame=_movement_frame(state,frame)
    for left,right in ((13,13),(0xC234,0xC0B4),(0xD380,0xC380)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),left)
        frame=_lowbank_ui_append_fields(state,frame,right)
    frame=_movement_move(state,frame,'target_x',10,16)
    while True:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0xD381)
        frame=_lowbank_ui_append_fields(state,frame,0xC381)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0xDB80)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    return first_replace(frame,roster=frame.roster.advance(30))


def lowbank_process_counted_records_21_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C2E6: relation label, live city LONG decimal value and six digit cells."""
    frame=_movement_frame(state,frame)
    for left,right in ((13,13),(0xC1B4,0xC134),(0xC382,0xC382)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),left)
        frame=_lowbank_ui_append_fields(state,frame,right)
    for offset,value in ((0,0xC04D),(30,0xC04E),(2,0xC04F),(32,0xC050)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),value)
    frame=first_replace(frame,roster=frame.roster.advance(4))
    frame=_movement_move(state,frame,'target_x',2,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC001,(30,))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_x)))
    frame=_movement_move(state,frame,'target_y',0xC386,16)
    frame=_movement_move(state,frame,'unit',0xC001,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFD300))
    frame=_lowbank_ui_call_fields(state,frame,0x1270A,0xC34E)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',5,16)
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),value)
        frame=_lowbank_ui_append_fields(state,frame,0xC001)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(30,))
    return _lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)


def lowbank_process_counted_records_22_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C5EC: single eight-cell top border."""
    frame=_movement_frame(state,frame)
    for value in (8,0xC422,0xC380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',5,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC381)
    return _lowbank_ui_append_fields(state,frame,0xCB80)


def lowbank_process_counted_records_23_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C60A: paired option value cells followed by the single blank row."""
    frame=_movement_frame(state,frame)
    for left,right in ((8,8),(0xC522,0xC4A2),(0xC382,0xC382)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+20),left)
        frame=_lowbank_ui_append_fields(state,frame,right)
    for value,token in ((0xC080,0xC630),(0xC088,0xC638)):
        frame=_movement_move(state,frame,'target_x',value,16)
        frame=_lowbank_ui_call_fields(state,frame,0xC6DC,token)
    for value in (0xC080,0xC080,0xCB82):
        frame=_lowbank_ui_cell_fields(state,frame,value,(20,))
    frame=first_replace(frame,roster=frame.roster.advance(20))
    for value in (8,0xC5A2,0xC382):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',5,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC080)
    return _lowbank_ui_append_fields(state,frame,0xCB82)


def lowbank_process_counted_records_24_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C6BE: eight-cell bottom border with original postincrement footer."""
    frame=_movement_frame(state,frame)
    for value in (8,0xC722,0xD380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',5,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xD381)
    return _lowbank_ui_append_fields(state,frame,0xDB80)


def lowbank_update_live_fields_8_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C6DC: four incrementing option cells; D1 really advances three times."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    for offset in (0,20,2,22):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.target_y))
        if offset!=22:
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)
    return first_replace(frame,roster=frame.roster.advance(4))


def _lowbank_ui_clear_panel_fields(state: SceneState, frame: FirstDeploymentFrame,
        width: int, stride: int, counter: int, reservation: int) -> FirstDeploymentFrame:
    """Two original seven-row erasure owners share geometry, not copied loops."""
    if (width,stride,counter,reservation) not in ((8,20,7,140),(6,16,5,112)):
        raise ValueError('closed original relation-panel role required')
    frame=_lowbank_ui_packet_start_fields(state,frame)
    offsets=(stride*6,stride*5,stride*4,stride*3,stride*2,stride)
    frame=_lowbank_ui_cell_fields(state,frame,width,offsets)
    for offset,value in zip(offsets,(0xC722,0xC6A2,0xC622,0xC5A2,0xC522,0xC4A2)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),value)
    frame=_lowbank_ui_append_fields(state,frame,0xC422)
    frame=_movement_move(state,frame,'target_x',counter,16)
    frame=_lowbank_ui_clear_cells_fields(state,frame,'target_x',offsets)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+stride*6),0,2,True)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,reservation)


def lowbank_process_counted_records_25_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C832: clear seven eight-cell rows; reservation remains original140."""
    return _lowbank_ui_clear_panel_fields(state,_movement_frame(state,frame),8,20,7,140)


def lowbank_process_counted_records_26_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C9A6: bounded six-group roster rows with live tile and attribute values."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    for left,right in ((13,13),(0xC134,0xC0B4),(0xC382,0xC380)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),left)
        frame=_lowbank_ui_append_fields(state,frame,right)
    frame=_movement_move(state,frame,'target_x',10,16)
    while True:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0xC001)
        frame=_lowbank_ui_append_fields(state,frame,0xC381)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
    frame=first_replace(frame,roster=frame.roster.advance(30))
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,60)
    while True:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),5,16)
        if not frame.status&5:
            break
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3D8,2),16)
        if not frame.status&5:
            break
        frame=_lowbank_ui_cell_fields(state,frame,13,(60,30))
        frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame=_lowbank_ui_shift_fields(state,frame,'target_y',1)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x))
        frame=_lowbank_ui_shift_fields(state,frame,'target_y',7)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0xC134)
        for offset in (60,30,0):
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.target_y))
            if offset:
                frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',128,True)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_lowbank_ui_cell_fields(state,frame,0xC382,(60,30))
        frame=_lowbank_ui_cell_fields(state,frame,0xC001,(60,30))
        frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFF3E2,2))
        frame=_lowbank_ui_shift_fields(state,frame,'target_y',1)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFF3E2,2))
        frame=_lowbank_ui_shift_fields(state,frame,'target_y',2)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0xBFF9)
        frame=_movement_move(state,frame,'unit',5,16)
        frame=_lowbank_ui_value_columns_fields(state,frame,'target_y','unit',(0,30),60,0xC001)
        frame=_lowbank_ui_cell_fields(state,frame,0xC001,(60,30))
        frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',state.read(0xFFFFF3E2,2))
        frame=_lowbank_ui_shift_fields(state,frame,'target_y',2)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0xC66C)
        frame=_movement_move(state,frame,'unit',1,16)
        frame=_lowbank_ui_value_columns_fields(state,frame,'target_y','unit',(0,30),60,0xC001)
        frame=_lowbank_ui_cell_fields(state,frame,0xC001,(60,30))
        frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(60,30))
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+60),0,2,True)
        frame=first_replace(frame,roster=frame.roster.advance(60))
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,90)
    frame=_lowbank_ui_append_fields(state,frame,13)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x))
    frame=_lowbank_ui_shift_fields(state,frame,'target_y',7)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0xC034)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_y))
    frame=_lowbank_ui_append_fields(state,frame,0xD380)
    frame=_movement_move(state,frame,'unit',10,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'unit',0xD381)
    frame=_lowbank_ui_append_fields(state,frame,0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,30)


def _lowbank_ui_value_columns_fields(state: SceneState, frame: FirstDeploymentFrame,
        value_name: str, counter_name: str, offsets: tuple,
        blank_offset: int=0, blank: int=0) -> FirstDeploymentFrame:
    """A pair of consecutive value glyphs, with original ADDQ flags and DBRA."""
    while True:
        for offset in offsets:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.carrier(value_name)))
            frame=_lowbank_ui_arithmetic_fields(state,frame,value_name,1)
        if blank_offset:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+blank_offset),blank)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_lowbank_ui_counter_fields(frame,counter_name)
        if low16(frame.carrier(counter_name))==65535:
            return frame


def lowbank_process_counted_records_27_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CB2C: erase eighteen single rows without changing the queue reservation."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    frame=_movement_move(state,frame,'target_x',0xC0B4,16)
    frame=_movement_move(state,frame,'target_y',17,16)
    while True:
        frame=_lowbank_ui_append_fields(state,frame,13)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',128)
        frame=_movement_move(state,frame,'unit',12,16)
        frame=_lowbank_ui_clear_cells_fields(state,frame,'unit')
        frame=_lowbank_ui_counter_fields(frame,'target_y')
        if low16(frame.target_y)==65535:
            break
    return _lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)


def lowbank_process_counted_records_28_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CD72: seven six-cell relation rows and real message-control notification."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    for value in (6,0xC422,0xC380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',3,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC381)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    for left,right,first_value,token in ((0xC522,0xC4A2,0xC0AD,0xCDBC),(0xC6A2,0xC622,0xC0B5,0xCE0A)):
        for a,b in ((6,6),(left,right),(0xC382,0xC382)):
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+16),a)
            frame=_lowbank_ui_append_fields(state,frame,b)
        frame=_movement_move(state,frame,'target_x',first_value,16)
        frame=_lowbank_ui_call_fields(state,frame,0xCE48,token)
        frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(16,))
        frame=first_replace(frame,roster=frame.roster.advance(16))
        if token==0xCDBC:
            for value in (6,0xC5A2,0xC382):
                frame=_lowbank_ui_append_fields(state,frame,value)
            frame=_movement_move(state,frame,'target_x',3,16)
            frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC001)
            frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    for value in (6,0xC722,0xD380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',3,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xD381)
    frame=_lowbank_ui_append_fields(state,frame,0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,112)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0xCE46)


def lowbank_process_counted_records_29_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CE48: four pairs of consecutive relation label glyphs."""
    frame=_movement_move(state,_movement_frame(state,frame),'target_y',3,16)
    return _lowbank_ui_value_columns_fields(state,frame,'target_x','target_y',(0,16))


def lowbank_process_counted_records_30_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CF32: original six-cell, sixteen-byte-stride seven-row erasure."""
    return _lowbank_ui_clear_panel_fields(state,_movement_frame(state,frame),6,16,5,112)


def lowbank_process_counted_records_33_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D054: seven ten-cell rows, two live sequential option-cell calls."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    for value in (10,0xC49E,0xC380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC381)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    for value in (10,):
        frame=_lowbank_ui_cell_fields(state,frame,value,(24,))
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xC59E)
    frame=_lowbank_ui_append_fields(state,frame,0xC51E)
    frame=_lowbank_ui_cell_fields(state,frame,0xC382,(24,))
    for counter,token in ((5,0xD0A2),(1,0xD0AE)):
        frame=_movement_move(state,frame,'target_x',0xC001,16)
        frame=_movement_move(state,frame,'target_y',counter,16)
        frame=_lowbank_ui_call_fields(state,frame,0xD13C,token)
    frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(24,))
    frame=first_replace(frame,roster=frame.roster.advance(24))
    for value in (10,0xC61E,0xC382):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC001)
    frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    frame=_lowbank_ui_cell_fields(state,frame,10,(24,))
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xC71E)
    frame=_lowbank_ui_append_fields(state,frame,0xC69E)
    frame=_lowbank_ui_cell_fields(state,frame,0xC382,(24,))
    frame=_movement_move(state,frame,'target_x',0xC00D,16)
    frame=_movement_move(state,frame,'target_y',7,16)
    frame=_lowbank_ui_call_fields(state,frame,0xD13C,0xD102)
    frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(24,))
    frame=first_replace(frame,roster=frame.roster.advance(24))
    for value in (10,0xC79E,0xD380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',7,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xD381)
    frame=_lowbank_ui_append_fields(state,frame,0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,168)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,0,True)


def lowbank_process_counted_records_34_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D13C: unguarded original DBRA count and twenty-four-byte paired cells."""
    return _lowbank_ui_value_columns_fields(state,_movement_frame(state,frame),'target_x','target_y',(0,24))


def lowbank_process_counted_records_35_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D526: thirteen fourteen-cell erasure rows, then clear the live queue bit."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    frame=_movement_move(state,frame,'target_y',0xC39A,16)
    frame=_movement_move(state,frame,'target_x',12,16)
    while True:
        frame=_lowbank_ui_append_fields(state,frame,14)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_y))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',128)
        frame=_movement_move(state,frame,'unit',13,16)
        frame=_lowbank_ui_clear_cells_fields(state,frame,'unit')
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,416)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,0,False)


def lowbank_process_counted_records_36_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D560: three paired option rows, intervening blanks and final footer."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    for value in (6,0xC422,0xC380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',3,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC381)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    frame=_movement_move(state,frame,'target_x',2,16)
    frame=_movement_move(state,frame,'target_y',0xC005,16)
    frame=_movement_move(state,frame,'unit',0xC522,16)
    while True:
        frame=_lowbank_ui_cell_fields(state,frame,6,(16,))
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+16),low16(frame.unit))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',128,True)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.unit))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',256)
        frame=_lowbank_ui_cell_fields(state,frame,0xC382,(16,))
        frame=_movement_move(state,frame,'count',3,16)
        frame=_lowbank_ui_value_columns_fields(state,frame,'target_y','count',(0,16))
        frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(16,))
        frame=first_replace(frame,roster=frame.roster.advance(16))
        frame=_movement_test(state,frame,low16(frame.target_x),16)
        if frame.status&4:
            break
        frame=_lowbank_ui_append_fields(state,frame,6)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.unit))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',256)
        frame=_lowbank_ui_append_fields(state,frame,0xC382)
        frame=_movement_move(state,frame,'count',3,16)
        frame=_lowbank_ui_repeat_cells_fields(state,frame,'count',0xC001)
        frame=_lowbank_ui_append_fields(state,frame,0xCB82)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    for value in (6,low16(frame.unit),0xD380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'count',3,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'count',0xD381)
    frame=_lowbank_ui_append_fields(state,frame,0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,160)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,0,True)


"""Live menu input, list selection and original confirmation state transitions.

The real frame is supplied by the caller. BYTE/WORD writes retain all observed
high bits; state machines never invent missing fields, display or IRQ progress.
"""


def lowbank_resolve_readonly_state_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C138: gated two-dimensional cursor and original tail JMP AC08."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
    draw=not bool(frame.status&4)
    if not draw:
        frame=_movement_test(state,frame,state.read(0xFFFFF382,2),16)
        if not frame.status&4:
            frame=_lowbank_ui_input_fields(state,frame)
            draw=not bool(frame.status&4)
        if not draw:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
            if not frame.status&4:
                return frame
    frame=first_replace(frame,roster=state.table_at(0xC19A).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF386,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',3)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',48)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF388,2),16)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_y',2)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.unit))
    frame=_lowbank_ui_shift_fields(state,frame,'target_y',3)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',96)
    frame=_movement_move(state,frame,'unit',0,16)
    # A JMP inherits the actual outer caller LONG; do not create a JSR slot.
    return _lowbank_ui_known_child_fields(state,frame,0xAC08)


def lowbank_coordinate_live_state_86_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C28A: build the closed paired city-value packet and reserve120 bytes."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    frame=_lowbank_ui_call_fields(state,frame,0xC2A6,0xC296)
    frame=_lowbank_ui_call_fields(state,frame,0xC2E6,0xC29C)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,120)


def lowbank_coordinate_live_state_87_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C494: three-way selection, reject-own-force message or roster confirmation."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xC4EC,0xC498)
    frame=_lowbank_ui_call_fields(state,frame,0xC550,0xC49C)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF362,13)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF630,2),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF634,2),16)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF634,2))
            frame=_movement_move(state,frame,'target_x',0xBF,16)
            return _lowbank_ui_call_fields(state,frame,0x676F2,0xC4D4)
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xC4DA)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3DE,0,2,True)


def lowbank_select_live_state_28_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C4EC: original left/right repeat delay and three-choice wrap."""
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,2)
        else:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1,True)
    else:
        frame=_movement_compare(state,frame,state.read(0xFFFFF386,2),2,16)
        if frame.status&1:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1)
        else:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF608,12)


def lowbank_select_live_state_29_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C550: gated fallthrough into the sole C56E label owner, without a call."""
    frame,draw=_lowbank_ui_cursor_gate_fields(state,_movement_frame(state,frame),True)
    if not draw:
        return frame
    from ..high_level_main_flows.business_commands import append_force_relation_label_frame_fields
    return append_force_relation_label_frame_fields(state,frame)


def lowbank_update_record_flags_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C5C2: compose the live seven-row option panel and request its real message."""
    frame=_lowbank_ui_packet_start_fields(state,_movement_frame(state,frame))
    for target,token in ((0xC5EC,0xC5CC),(0xC60A,0xC5CE),(0xC678,0xC5D2),(0xC6BE,0xC5D6)):
        frame=_lowbank_ui_call_fields(state,frame,target,token)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,140)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,0,True)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0xC5EA)


def lowbank_coordinate_live_state_88_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C678: three original four-glyph paired value calls."""
    frame=_movement_frame(state,frame)
    for left,right in ((8,8),(0xC6A2,0xC622),(0xC382,0xC382)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+20),left)
        frame=_lowbank_ui_append_fields(state,frame,right)
    for value,token in ((0xC080,0xC69E),(0xC08C,0xC6A6),(0xC080,0xC6AE)):
        frame=_movement_move(state,frame,'target_x',value,16)
        frame=_lowbank_ui_call_fields(state,frame,0xC6DC,token)
    frame=_lowbank_ui_cell_fields(state,frame,0xCB82,(20,))
    return first_replace(frame,roster=frame.roster.advance(20))


def lowbank_coordinate_live_state_89_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """C6F6: cancel/confirm, including the original carry-controlled backedge."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xC764,0xC6FA)
    frame=_lowbank_ui_call_fields(state,frame,0xC790,0xC6FE)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    cancel=not bool(frame.status&4)
    if not cancel:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if frame.status&4:
            return frame
    while True:
        if cancel:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,1)
            frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),0x6D,16)
            if not frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x208)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
                frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),0xAC,16)
                if not frame.status&4:
                    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
                frame=_lowbank_ui_call_fields(state,frame,0xC832,0xC734)
                return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,0,2,True)
        frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xC750)
        if frame.status&1:
            cancel=True
            continue
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
        return _lowbank_ui_call_fields(state,frame,0xC832,0xC762)


def lowbank_coordinate_live_state_90_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CB58: initialize once, then browse the live force roster and confirm."""
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF3DE,2),16)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x676C4,0xCB64)
        return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3DE,1)
    frame=_lowbank_ui_call_fields(state,frame,0xCC28,0xCB6E)
    frame=_lowbank_ui_call_fields(state,frame,0xCBE4,0xCB70)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3E0,2),16)
            frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
            frame=first_replace(frame,roster=state.table_at(0xFFFFE730).cursor())
            frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
            frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
            frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
            frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.target_x))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
            frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xCBBC)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    return _lowbank_ui_call_fields(state,frame,0xCB2C,0xCBE2)


def lowbank_coordinate_live_state_91_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0xCBE4) -> FirstDeploymentFrame:
    """CBE4/CC02: guarded or true middle-entry roster cursor packet."""
    frame=_movement_frame(state,frame)
    if entry not in (0xCBE4,0xCC02):
        raise ValueError('two actual original lowbank cursor entry addresses required')
    if entry==0xCBE4:
        frame,draw=_lowbank_ui_cursor_gate_fields(state,frame)
        if not draw:
            return frame
    frame=first_replace(frame,roster=state.table_at(0xCC9A).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3E0,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF3E2,2),True)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',3)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',16)
    frame=_movement_move(state,frame,'target_y',216,16)
    frame=_movement_move(state,frame,'unit',0,16)
    return _lowbank_ui_call_fields(state,frame,0xAC08,0xCC26)


def lowbank_coordinate_live_state_91_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CC02 is a genuine entry, not another copied selection algorithm."""
    return lowbank_coordinate_live_state_91_fields(state,frame,0xCC02)


def lowbank_select_live_state_30_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CC28: roster selection and original scroll-window lower/upper limits."""
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF3E0,2),16)
        if frame.status&4:
            return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3E0,1,True)
    else:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3E0,1)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3E0,2),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3D8,2),16)
        if frame.status&4:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3E0,1,True)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3E0,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',2,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3D8,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',5,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.target_y),16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'target_x',low16(frame.target_y),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3E2,2),16)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3E2,low16(frame.target_x))
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def lowbank_coordinate_live_state_92_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CE5E: relation selection; preserve the original code-address store.

    The exact encoded destination is confirmed; whether this is an intended
    code write or a defect in naturally reachable gameplay remains unknown.
    """
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xCECC,0xCE62)
    frame=_lowbank_ui_call_fields(state,frame,0xCEF2,0xCE66)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),0x36,16)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0xCC02,0xCE72)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            # CE88 original 33FC00080000CE5E writes 0000CE5E, not CFD2.
            # An unavailable writable code mapping is an honest memory boundary.
            frame=_lowbank_ui_store_fields(state,frame,0x0000CE5E,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            frame=_lowbank_ui_call_fields(state,frame,0xCF32,0xCEA0)
            frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xCEA4)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xCF32,0xCEBE)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)


def lowbank_select_live_state_31_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CECC: two-choice XOR selection with real timer read/modify/write order."""
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,state.read(0xFFFFF386,2)^1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF608,12)


def lowbank_coordinate_live_state_93_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CEF2: relation option cursor, not a second sprite rendering implementation."""
    frame,draw=_lowbank_ui_cursor_gate_fields(state,_movement_frame(state,frame))
    if not draw:
        return frame
    return _lowbank_ui_draw_choice_fields(state,frame,0xC19A,0xFFFFF386,64,136,0xCF30)


def lowbank_process_counted_records_31_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """CFB8: collect selected relation BYTEs and the original WORD result count."""
    from ..high_level_gameplay_flow.contexts_services import SceneRefreshMemory
    from ..high_level_scene_flows.business_scene import _scene_fade_rotate_word_fields
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE710).cursor())
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_y',1)
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_movement_move(state,frame,'count',0,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE730).cursor())
    frame=_movement_move(state,frame,'target_y',15,16)
    while True:
        frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.count),16)
        self_relation=bool(frame.status&4)
        frame=_scene_fade_rotate_word_fields(SceneRefreshMemory(state),frame,'unit',1)
        if not self_relation and frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.count),1)
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
            frame=_lowbank_ui_arithmetic_fields(state,frame,'distance',1)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'count',1)
        frame=_lowbank_ui_counter_fields(frame,'target_y')
        if low16(frame.target_y)==65535:
            break
    frame=_movement_move(state,frame,'target_x',low16(frame.distance),16)
    return _lowbank_ui_store_fields(state,frame,frame.candidates.base,255,1)


def lowbank_process_counted_records_32_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D028: intersect forty officer BYTEs with the live relation BYTE list."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF428).cursor(),candidates=state.table_at(0xFFFFE750).cursor())
    frame=_movement_move(state,frame,'target_y',39,16)
    while True:
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
        value=frame.roster.byte()
        frame=first_replace(frame,roster=frame.roster.advance(1))
        frame=_movement_move(state,frame,'unit',value,8)
        if not frame.status&8:
            frame=first_replace(frame,controller=state.table_at(0xFFFFE730))
            while True:
                value=frame.controller.byte()
                frame=first_replace(frame,controller=frame.controller.advance(1))
                frame=_movement_move(state,frame,'count',value,8)
                if frame.status&8:
                    break
                # Original CMP.W deliberately retains BYTE-carrier upper BYTEs.
                frame=_movement_compare(state,frame,low16(frame.count),low16(frame.unit),16)
                if frame.status&4:
                    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.target_x),1)
                    frame=first_replace(frame,candidates=frame.candidates.advance(1))
                    break
        frame=_lowbank_ui_counter_fields(frame,'target_y')
        if low16(frame.target_y)==65535:
            break
    return _lowbank_ui_store_fields(state,frame,frame.candidates.base,255,1)


def lowbank_coordinate_live_state_94_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D14E: actual input and cursor calls; neither callback success is simulated."""
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xD158,0xD152)
    return _lowbank_ui_call_fields(state,frame,0xD1CA,0xD156)


def lowbank_coordinate_live_state_95_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D158: XOR selection, repeat cooldown and real cancel/confirm labels."""
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    else:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,state.read(0xFFFFF386,2)^1)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xD1A8)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,12)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def lowbank_coordinate_live_state_96_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D1CA: only bit3 gates this cursor; it intentionally ignores confirm input."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
    if not frame.status&4:
        return frame
    return _lowbank_ui_draw_choice_fields(state,frame,0xD1F6,0xFFFFF386,72,120,0xD1F4)


def lowbank_update_record_flags_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D270: three real readonly cost LONGs, followed by the live text packet."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xD2CA).cursor())
    for selection,offset,address in ((0xFFFFEF64,0,0xFFFFEF6A),(0xFFFFEF66,12,0xFFFFEF6E),(0xFFFFEF68,24,0xFFFFEF72)):
        frame=_movement_move(state,frame,'target_x',state.read(selection,2),16)
        frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
        frame=_lowbank_ui_store_fields(state,frame,address,frame.roster.long(low16(frame.target_x),offset),4)
    frame=_movement_move_long(state,frame,'target_x',0xC000000E)
    frame=_movement_move(state,frame,'target_y',10,16)
    frame=_movement_move(state,frame,'unit',0xC41A,16)
    frame=first_replace(frame,roster=state.table_at(0xD2EE).cursor())
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF692,0xC386)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFEF76,0xC0A1)
    frame=_lowbank_ui_call_fields(state,frame,0x26BFA,0xD2BC)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,0,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF600,0xF0)


def lowbank_coordinate_live_state_97_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D368: policy selector and cursor retain both real BSR pairs."""
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xD372,0xD36C)
    return _lowbank_ui_call_fields(state,frame,0xD49A,0xD370)


def lowbank_coordinate_live_state_98_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D372: choose among three policy rows or each row's enabled option bits.

    The original option loop remains unguarded when its actual bit mask is0;
    no artificial successful exit repairs that historical behavior.
    """
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
            if frame.status&4:
                frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3F0,1,True)
                if frame.status&8:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F0,2)
            else:
                frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3F0,1)
                frame=_movement_compare(state,frame,state.read(0xFFFFF3F0,2),3,16)
                if not frame.status&1:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F0,0,2,True)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_movement_move(state,frame,'target_x',low16(frame.target_x)&12,16)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        else:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
            if frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
                frame=first_replace(frame,roster=state.table_at(0xFFFFEF64).cursor(),candidates=state.table_at(0xFFFFEFB2).cursor())
                frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F0,2),16)
                frame=_lowbank_ui_shift_fields(state,frame,'target_y',1)
                frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
                frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.target_y)),16)
                frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
                backwards=bool(frame.status&4)
                while True:
                    frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',1,backwards)
                    if backwards:
                        if frame.status&8:
                            frame=_movement_move(state,frame,'unit',2,16)
                    else:
                        frame=_movement_compare(state,frame,low16(frame.unit),3,16)
                        if not frame.status&1:
                            frame=_movement_move(state,frame,'unit',0,16)
                    frame=_lowbank_ui_bit_fields(state,frame,frame.count,low16(frame.unit)&31)
                    if not frame.status&4:
                        break
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.unit))
                return _lowbank_ui_call_fields(state,frame,0xD270,0xD41A)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F0,2),16)
            frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
            frame=first_replace(frame,roster=state.table_at(0xFFFFEF6A).cursor())
            frame=_movement_move_long(state,frame,'target_x',frame.roster.long(low16(frame.target_x)))
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
            frame=_lowbank_ui_shift_fields(state,frame,'target_y',2)
            frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
            frame=_first_compare_long(frame,frame.target_x,frame.roster.long(low16(frame.target_y)))
            state.sr=(state.sr&65504)|frame.status
            if not frame.status&5:
                return frame
            frame=_lowbank_ui_call_fields(state,frame,0xD526,0xD46E)
            frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xD472)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xD526,0xD48C)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)


def lowbank_coordinate_live_state_99_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D49A: policy-row cursor using the actual D4DC resource descriptor."""
    frame,draw=_lowbank_ui_cursor_gate_fields(state,_movement_frame(state,frame))
    if not draw:
        return frame
    return _lowbank_ui_draw_choice_fields(state,frame,0xD4DC,0xFFFFF3F0,64,104,0xD4DA)


def lowbank_coordinate_live_state_100_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D624: three-choice input and cursor, with original real BSR continuations."""
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xD62E,0xD628)
    return _lowbank_ui_call_fields(state,frame,0xD6BE,0xD62C)


def lowbank_coordinate_live_state_101_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D62E: three-choice wrapped input plus original cancel/confirm cooldown."""
    frame=_lowbank_ui_input_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    else:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
            if frame.status&4:
                frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1,True)
                if frame.status&8:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,2)
            else:
                frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1)
                frame=_movement_compare(state,frame,state.read(0xFFFFF386,2),3,16)
                if not frame.status&1:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xD69E)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def lowbank_coordinate_live_state_102_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """D6BE: three-choice cursor using the genuine D700 descriptor."""
    frame,draw=_lowbank_ui_cursor_gate_fields(state,_movement_frame(state,frame))
    if not draw:
        return frame
    return _lowbank_ui_draw_choice_fields(state,frame,0xD700,0xFFFFF386,64,136,0xD6FE)


def calculate_live_debt_interest_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FBAA: live signed date difference and original split principal products."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word
    frame = _movement_frame(state, frame)
    frame = _movement_move(state, frame, 'unit', state.read(0xFFFFF374, 1), 8)
    frame = _economy_delta_fields(state, frame, 'unit', state.read(u32(frame.candidates.base + s16(low16(frame.target_x)) + 2), 1), 8, True)
    year_gap = low8(frame.unit)
    frame = _movement_move(state, frame, 'unit', year_gap | 0xFF00 if year_gap & 0x80 else year_gap, 16)
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 1)
    frame = _economy_delta_fields(state, frame, 'unit', low16(frame.count))
    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
    frame = _movement_move(state, frame, 'count', state.read(0xFFFFF375, 1), 8)
    frame = _economy_delta_fields(state, frame, 'count', state.read(u32(frame.candidates.base + s16(low16(frame.target_x)) + 3), 1), 8, True)
    month_gap = low8(frame.count)
    frame = _movement_move(state, frame, 'count', month_gap | 0xFF00 if month_gap & 0x80 else month_gap, 16)
    frame = _economy_delta_fields(state, frame, 'unit', low16(frame.count))
    if frame.status & 4:
        return frame
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)
    frame = _economy_delta_fields(state, frame, 'unit', low16(frame.count))
    frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)
    frame = _movement_multiply_word(state, frame, 'count', low16(frame.target_y))
    frame = _economy_swap_fields(state, frame, 'target_y')
    frame = _movement_multiply_word(state, frame, 'unit', low16(frame.target_y))
    frame = _economy_swap_fields(state, frame, 'target_y')
    frame = _economy_swap_fields(state, frame, 'unit')
    frame = _economy_delta_fields(state, frame, 'unit', frame.count, 32)
    frame = _movement_move_long(state, frame, 'count', frame.target_y)
    frame = _movement_move_long(state, frame, 'target_y', frame.unit)
    frame = _movement_move_long(state, frame, 'unit', 100)
    frame = _lowbank_ui_call_fields(state, frame, 0x35760, 0xFBEC)
    return _economy_delta_fields(state, frame, 'target_y', frame.count, 32)

def add_officer_progress_c000_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FDD0: wrapped officer WORD index, live add, then original 999 cap."""
    from .services import _movement_fixed_shift_word
    frame = _movement_frame(state, frame)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)
    frame = first_replace(frame, roster=state.table_at(0xFFFFC000).cursor())
    address = u32(frame.roster.base + s16(low16(frame.target_x)))
    frame = _economy_memory_delta_fields(state, frame, address, low16(frame.unit))
    frame = _movement_compare(state, frame, state.read(address, 2), 999, 16)
    if not frame.status & 5:
        frame = _lowbank_ui_store_fields(state, frame, address, 999)
    return frame

def average_selected_officer_attribute_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """101F8: scan the sentinel roster, retaining WORD sum and DIVU result."""
    from .services import _movement_divu_word
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, controller=state.table_at(0xFFFFC400))
    frame = _movement_move(state, frame, 'unit', 0, 16)
    frame = first_replace(frame, scan=state.table_at(0x00FF398A).cursor())
    while True:
        member = frame.scan.word()
        frame = first_replace(frame, scan=frame.scan.advance(2))
        frame = _movement_move(state, frame, 'count', member, 16)
        if frame.status & 8:
            break
        frame = _movement_move(state, frame, 'count', low16(frame.count) & 255, 16)
        frame = _movement_move(state, frame, 'distance', 0, 16)
        frame = _movement_move(state, frame, 'distance', frame.controller.byte(low16(frame.count)), 8)
        frame = _economy_delta_fields(state, frame, 'unit', low16(frame.distance))
    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)
    frame = _movement_move_long(state, frame, 'unit', low16(frame.unit))
    return _movement_divu_word(state, frame, 'unit', low16(frame.target_x), 0x10220)


def _lowbank_ui_known_child_fields(state: SceneState, frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """Only named original full cores; unknown child keeps its actual entered slot."""
    if target == 57582:
        from ..high_level_city_officer.business_scene_orders import queue_development_order_fields
        return queue_development_order_fields(state, frame)
    if target == 58362:
        from ..high_level_city_officer.business_scene_orders import queue_welfare_order_fields
        return queue_welfare_order_fields(state, frame)
    if target == 58748:
        from ..high_level_city_officer.business_scene_orders import commit_tax_rate_fields
        return commit_tax_rate_fields(state, frame)
    if target == 58770:
        from ..high_level_command_actions.contexts_personnel import execute_personnel_scene_fields
        return execute_personnel_scene_fields(state, target, frame)
    if target == 59426:
        return _economy_cleanup_tail_fields(state, frame)
    if target == 64500:
        from ..high_level_city_officer.business_scene_orders import commit_recruitment_fields
        return commit_recruitment_fields(state, frame)
    if target == 64534:
        from ..high_level_city_officer.business_scene_orders import commit_equipment_purchase_fields
        return commit_equipment_purchase_fields(state, frame)
    if target == 70060:
        from ..high_level_diplomacy_forces.business_scene_bribery import settle_personnel_joining_fields
        return settle_personnel_joining_fields(state, frame)
    if target == 59960:
        from ..high_level_command_actions.contexts_personnel import execute_personnel_scene_fields
        return execute_personnel_scene_fields(state, target, frame)
    if target == 61464:
        from ..high_level_diplomacy_forces.business_scene_stratagem_direct import settle_method61_stratagem_fields
        return settle_method61_stratagem_fields(state, frame)
    if target == 9946:
        return _menu_window_action_reset_fields(state, frame)
    if target == 10852:
        frame = _movement_frame(state, frame)
        frame = _lowbank_ui_store_fields(state, frame, 4294964066, 27)
        return _lowbank_ui_store_fields(state, frame, 4294954926, state.read(4294964196, 4), 4)
    if target == 25574:
        from ..high_level_main_flows.business_map import adjust_selected_roster_member_frame_fields
        return adjust_selected_roster_member_frame_fields(state, frame, entry=25574)
    if target == 75572:
        from .business_city import append_city_five_place_decimal_tail_fields
        return append_city_five_place_decimal_tail_fields(state, frame)
    if target == 3856:
        from ..high_level_main_flows.business_main import update_campaign_control_fields
        return update_campaign_control_fields(state, frame)
    if target == 240342:
        from ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields
        from .services import SceneRefreshMemory
        return read_vdp_plane_rle_rows_from_control_fields(SceneRefreshMemory(state), frame)
    if target == 3750:
        from ..high_level_main_flows.business_main import upload_three_formation_names_direct_fields
        return upload_three_formation_names_direct_fields(state, frame)
    if target == 18576:
        from ..high_level_main_flows.business_lowbank import poll_world_map_input_fields
        return poll_world_map_input_fields(state, frame)
    if target == 18840:
        from ..high_level_main_flows.business_lowbank import upload_world_map_palette_fields
        return upload_world_map_palette_fields(state, frame)
    if target == 37776:
        from ..high_level_main_flows.business_map import clear_officer_growth_frame_fields
        return clear_officer_growth_frame_fields(state, frame)
    if target == 91104:
        from .business_city import build_group_available_actions_fields
        return build_group_available_actions_fields(state, frame)
    if target == 91564:
        from .business_city import copy_group_members_to_action_roster_fields
        return copy_group_members_to_action_roster_fields(state, frame)
    if target == 101556:
        from .business_city import dispatch_city_video_selection_phase_fields
        return dispatch_city_video_selection_phase_fields(state, frame)
    if target == 118016:
        from .business_city import prepare_city_group_result_queue_fields
        return prepare_city_group_result_queue_fields(state, frame)
    if target == 118152:
        from .business_city import prepare_city_surviving_group_selection_fields
        return prepare_city_surviving_group_selection_fields(state, frame)
    if target == 118278:
        from .business_city import prepare_city_surviving_group_selection_alternate_1_fields
        return prepare_city_surviving_group_selection_alternate_1_fields(state, frame)
    if target == 166198:
        from .business_highbank import highbank_process_device_control_2_fields
        return highbank_process_device_control_2_fields(state, frame)
    if target == 176894:
        from .business_highbank import highbank_process_device_control_4_fields
        return highbank_process_device_control_4_fields(state, frame)
    if target == 240184:
        from ..high_level_dynamic_flows.business_early_phase import begin_scene_palette_lighten_fields
        from .services import SceneRefreshMemory
        return begin_scene_palette_lighten_fields(SceneRefreshMemory(state), frame)
    if target == 419302:
        from .business_highbank import highbank_update_record_flags_11_fields
        return highbank_update_record_flags_11_fields(state, frame)
    if target == 18966:
        from ..high_level_gameplay_flow.business_services import _reset_scene_input_marker_fields, _scene_refresh_flags
        from ..high_level_gameplay_flow.contexts_services import MarkerResetMemory, SceneRefreshMemory
        _reset_scene_input_marker_fields(MarkerResetMemory(state))
        return _scene_refresh_flags(SceneRefreshMemory(state), frame, 0, 2)
    if target == 60430:
        return _lowbank_ui_store_fields(state, frame, 4294964744, 120)
    if target == 64426:
        return calculate_live_debt_interest_fields(state, frame)
    if target == 64976:
        return add_officer_progress_c000_fields(state, frame)
    if target == 66040:
        return average_selected_officer_attribute_fields(state, frame)
    if target == 24392:
        from ..high_level_gameplay_flow.business_battle import build_roster_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        return build_roster_fields(BattlePresentationMemory(state), frame)
    if target == 57846:
        from ..high_level_gameplay_flow.business_battle import choose_city_head_fields
        from ..high_level_gameplay_flow.contexts_battle import BattlePresentationMemory
        return choose_city_head_fields(BattlePresentationMemory(state), frame)
    if target == 90580:
        from ..high_level_main_flows.business_gameplay import append_current_city_value_fields
        return append_current_city_value_fields(state, frame)
    if target == 423620:
        from ..high_level_main_flows.business_highbank import dispatch_message_control_frame_fields
        return dispatch_message_control_frame_fields(state, frame)
    if target in (72946, 73258, 73276, 73602, 73722, 73736, 73764, 73828, 74268, 74386, 74516, 74776, 75052, 75180, 75266, 75296, 75404, 75474, 75504, 75530, 75616, 75660, 75896, 76002, 76076, 76092, 76160, 76254, 76280, 76334, 76366, 76440, 76470, 76500, 76620, 76650, 76736, 76812, 76932, 76990, 77044, 77186, 77308, 77428, 77656, 77876, 77930, 78198, 78216, 78364, 78448, 79120, 79166, 79300, 79586, 79604, 79690, 80180, 80216, 80516, 80534, 80774, 80858, 81022, 81398, 81554, 81772, 81834, 81892):
        from ..high_level_player_commands.contexts_command_fields import execute_command_menu_scene_fields
        return execute_command_menu_scene_fields(state, target, frame)
    if target == 512:
        return lowbank_select_live_state_1_fields(state, frame)
    if target == 8808:
        return lowbank_coordinate_live_state_1_fields(state, frame)
    if target == 8924:
        return lowbank_coordinate_live_state_2_fields(state, frame)
    if target == 9132:
        return lowbank_select_live_state_2_fields(state, frame)
    if target == 9360:
        return lowbank_update_record_flags_1_fields(state, frame)
    if target == 9436:
        return lowbank_coordinate_live_state_3_fields(state, frame)
    if target == 9448:
        return lowbank_coordinate_live_state_4_fields(state, frame)
    if target == 9456:
        return lowbank_coordinate_live_state_5_fields(state, frame)
    if target == 9464:
        return lowbank_coordinate_live_state_6_fields(state, frame)
    if target == 9910:
        return lowbank_update_record_flags_2_fields(state, frame)
    if target == 10524:
        return lowbank_update_record_flags_2_alternate_1_fields(state, frame)
    if target == 10528:
        return lowbank_update_record_flags_2_alternate_2_fields(state, frame)
    if target == 10544:
        return lowbank_update_record_flags_2_alternate_3_fields(state, frame)
    if target == 10698:
        return lowbank_update_record_flags_2_alternate_4_fields(state, frame)
    if target == 11068:
        return lowbank_update_record_flags_2_alternate_5_fields(state, frame)
    if target == 9950:
        return lowbank_select_live_state_3_fields(state, frame)
    if target == 10042:
        return lowbank_select_live_state_4_fields(state, frame)
    if target == 10044:
        return lowbank_coordinate_live_state_9_fields(state, frame)
    if target == 10062:
        return lowbank_coordinate_live_state_10_fields(state, frame)
    if target == 10388:
        return lowbank_select_live_state_5_fields(state, frame)
    if target == 10458:
        return lowbank_update_record_flags_3_fields(state, frame)
    if target == 10708:
        return lowbank_update_record_flags_3_alternate_1_fields(state, frame)
    if target == 11730:
        return lowbank_update_record_flags_3_alternate_2_fields(state, frame)
    if target == 10462:
        return lowbank_select_live_state_6_fields(state, frame)
    if target == 10532:
        return lowbank_coordinate_live_state_11_fields(state, frame)
    if target == 10536:
        return lowbank_coordinate_live_state_8_fields(state, frame)
    if target == 10836:
        return lowbank_coordinate_live_state_8_alternate_1_fields(state, frame)
    if target == 10540:
        return lowbank_coordinate_live_state_12_fields(state, frame)
    if target == 10694:
        return lowbank_coordinate_live_state_7_fields(state, frame)
    if target == 10786:
        return lowbank_coordinate_live_state_13_fields(state, frame)
    if target == 10866:
        return lowbank_select_live_state_7_fields(state, frame)
    if target == 10896:
        return lowbank_coordinate_live_state_14_fields(state, frame)
    if target == 10950:
        return lowbank_select_live_state_8_fields(state, frame)
    if target == 10974:
        return lowbank_select_live_state_9_fields(state, frame)
    if target == 11026:
        return lowbank_select_live_state_10_fields(state, frame)
    if target == 11072:
        return lowbank_coordinate_live_state_15_fields(state, frame)
    if target == 11126:
        return lowbank_update_live_fields_1_fields(state, frame)
    if target == 11144:
        return lowbank_coordinate_live_state_16_fields(state, frame)
    if target == 11208:
        return lowbank_update_record_flags_4_fields(state, frame)
    if target == 11276:
        return lowbank_coordinate_live_state_17_fields(state, frame)
    if target == 11334:
        return lowbank_update_live_fields_2_fields(state, frame)
    if target == 11354:
        return lowbank_update_live_fields_3_fields(state, frame)
    if target == 11394:
        return lowbank_coordinate_live_state_18_fields(state, frame)
    if target == 11462:
        return lowbank_coordinate_live_state_19_fields(state, frame)
    if target == 11496:
        return lowbank_coordinate_live_state_20_fields(state, frame)
    if target == 11568:
        return lowbank_coordinate_live_state_21_fields(state, frame)
    if target == 11678:
        return lowbank_coordinate_live_state_22_fields(state, frame)
    if target == 11862:
        return lowbank_coordinate_live_state_23_fields(state, frame)
    if target == 11892:
        return lowbank_coordinate_live_state_24_fields(state, frame)
    if target == 11900:
        return lowbank_coordinate_live_state_25_fields(state, frame)
    if target == 11908:
        return lowbank_coordinate_live_state_26_fields(state, frame)
    if target == 11916:
        return lowbank_coordinate_live_state_27_fields(state, frame)
    if target == 11924:
        return lowbank_coordinate_live_state_28_fields(state, frame)
    if target == 11932:
        return lowbank_coordinate_live_state_29_fields(state, frame)
    if target == 12006:
        return lowbank_update_record_flags_5_fields(state, frame)
    if target == 12048:
        return lowbank_coordinate_live_state_30_fields(state, frame)
    if target == 12094:
        return lowbank_update_record_flags_6_fields(state, frame)
    if target == 12144:
        return lowbank_coordinate_live_state_31_fields(state, frame)
    if target == 12238:
        return lowbank_coordinate_live_state_32_fields(state, frame)
    if target == 12252:
        return lowbank_update_record_flags_7_fields(state, frame)
    if target == 12346:
        return lowbank_coordinate_live_state_33_fields(state, frame)
    if target == 12364:
        return lowbank_coordinate_live_state_34_fields(state, frame)
    if target == 12372:
        return lowbank_update_record_flags_8_fields(state, frame)
    if target == 12442:
        return lowbank_select_live_state_11_fields(state, frame)
    if target == 12564:
        return lowbank_coordinate_live_state_35_fields(state, frame)
    if target == 12602:
        return lowbank_coordinate_live_state_36_fields(state, frame)
    if target == 12610:
        return lowbank_coordinate_live_state_37_fields(state, frame)
    if target == 12630:
        return lowbank_coordinate_live_state_38_fields(state, frame)
    if target == 12644:
        return lowbank_coordinate_live_state_39_fields(state, frame)
    if target == 12724:
        return lowbank_coordinate_live_state_40_fields(state, frame)
    if target == 12798:
        return lowbank_coordinate_live_state_41_fields(state, frame)
    if target == 12866:
        return lowbank_coordinate_live_state_42_fields(state, frame)
    if target == 12930:
        return lowbank_process_counted_records_1_fields(state, frame)
    if target == 13068:
        return lowbank_coordinate_live_state_43_fields(state, frame)
    if target == 13100:
        return lowbank_coordinate_live_state_44_fields(state, frame)
    if target == 13108:
        return lowbank_coordinate_live_state_45_fields(state, frame)
    if target == 13206:
        return lowbank_coordinate_live_state_46_fields(state, frame)
    if target == 13250:
        return lowbank_coordinate_live_state_47_fields(state, frame)
    if target == 13258:
        return lowbank_select_live_state_12_fields(state, frame)
    if target == 13288:
        return lowbank_coordinate_live_state_48_fields(state, frame)
    if target == 13346:
        return lowbank_coordinate_live_state_49_fields(state, frame)
    if target == 13360:
        return lowbank_coordinate_live_state_50_fields(state, frame)
    if target == 13408:
        return lowbank_coordinate_live_state_51_fields(state, frame)
    if target == 13442:
        return lowbank_coordinate_live_state_52_fields(state, frame)
    if target == 13482:
        return lowbank_coordinate_live_state_53_fields(state, frame)
    if target == 13538:
        return lowbank_coordinate_live_state_54_fields(state, frame)
    if target == 13592:
        return lowbank_coordinate_live_state_55_fields(state, frame)
    if target == 13664:
        return lowbank_coordinate_live_state_56_fields(state, frame)
    if target == 13684:
        return lowbank_select_live_state_13_fields(state, frame)
    if target == 13716:
        return lowbank_select_live_state_14_fields(state, frame)
    if target == 13748:
        return lowbank_select_live_state_15_fields(state, frame)
    if target == 13778:
        return lowbank_coordinate_live_state_57_fields(state, frame)
    if target == 13800:
        return lowbank_coordinate_live_state_58_fields(state, frame)
    if target == 13808:
        return lowbank_update_live_fields_4_fields(state, frame)
    if target == 13828:
        return lowbank_select_live_state_16_fields(state, frame)
    if target == 13864:
        return lowbank_process_device_control_1_fields(state, frame)
    if target == 14026:
        return lowbank_select_live_state_17_fields(state, frame)
    if target == 9656:
        return _menu_window_action_reset_fields(state, frame)
    if target == 9660:
        return _menu_window_action_setup_fields(state, frame)
    if target == 10326:
        return _menu_window_trait_choice_fields(state, frame)
    if target == 9994:
        return lowbank_select_live_state_4_fields(state, frame)
    if target == 9828:
        return lowbank_coordinate_live_state_8_fields(state, frame)
    if target == 9794:
        return lowbank_coordinate_live_state_7_fields(state, frame)
    if target == 10142:
        return lowbank_coordinate_live_state_11_fields(state, frame)
    if target == 10246:
        return lowbank_coordinate_live_state_12_fields(state, frame)
    if target == 20588:
        from ..high_level_main_flows.business_commands import render_current_city_command_labels_frame_fields
        return render_current_city_command_labels_frame_fields(state, frame)
    if target == 22164:
        from ..high_level_main_flows.business_commands import start_selection_prompt_fields
        return start_selection_prompt_fields(state, frame)
    if target == 23228:
        from ..high_level_main_flows.business_commands import present_current_command_prompt_frame_fields
        return present_current_command_prompt_frame_fields(state, frame)
    if target == 49438:
        from ..high_level_main_flows.business_commands import set_roster_selection_notice_frame_fields
        return set_roster_selection_notice_frame_fields(state, frame)
    if target == 50126:
        from ..high_level_main_flows.business_commands import append_force_relation_commands_fields
        return append_force_relation_commands_fields(state, frame)
    if target == 50576:
        from ..high_level_main_flows.business_commands import append_force_relation_digits_frame_fields
        return append_force_relation_digits_frame_fields(state, frame)
    if target == 55470:
        from ..high_level_main_flows.business_commands import append_city_command_heading_frame_fields
        return append_city_command_heading_frame_fields(state, frame)
    if target == 56560:
        from ..high_level_main_flows.business_commands import append_diplomacy_command_choices_fields
        return append_diplomacy_command_choices_fields(state, frame)
    if target == 90732:
        from ..high_level_main_flows.business_gameplay import append_four_row_status_panel_fields
        return append_four_row_status_panel_fields(state, frame)
    if target == 4922:
        from ..high_level_main_flows.business_main import clear_pointer_cost_caches_fields
        return clear_pointer_cost_caches_fields(state, frame)
    if target == 5812:
        from ..high_level_main_flows.business_main import scroll_campaign_camera_toward_pointer_fields
        return scroll_campaign_camera_toward_pointer_fields(state, frame)
    if target == 7448:
        from ..high_level_main_flows.business_main import append_campaign_frame_progress_fields
        return append_campaign_frame_progress_fields(state, frame)
    if target == 111004:
        from .business_city import city_coordinate_live_state_84_fields
        return city_coordinate_live_state_84_fields(state, frame)
    if target == 418532:
        from ..high_level_main_flows.business_highbank import advance_officer_growth_levels_fields
        return advance_officer_growth_levels_fields(state, frame)
    if target == 40542:
        from ..high_level_main_flows.business_map import update_world_cursor_from_inputs_frame_fields
        return update_world_cursor_from_inputs_frame_fields(state, frame)
    if target == 40828:
        from ..high_level_main_flows.business_map import queue_map_strip_transfer_fields
        return queue_map_strip_transfer_fields(state, frame)
    if target == 14694:
        return lowbank_process_counted_records_2_fields(state, frame)
    if target == 15156:
        return lowbank_process_device_control_2_fields(state, frame)
    if target == 16760:
        return lowbank_process_device_control_3_fields(state, frame)
    if target == 17340:
        return lowbank_process_counted_records_3_fields(state, frame)
    if target == 17408:
        return lowbank_process_counted_records_4_fields(state, frame)
    if target == 17440:
        return lowbank_select_live_state_18_fields(state, frame)
    if target == 17474:
        return lowbank_process_counted_records_5_fields(state, frame)
    if target == 17536:
        return lowbank_process_counted_records_6_fields(state, frame)
    if target == 17846:
        return lowbank_coordinate_live_state_59_fields(state, frame)
    if target == 18004:
        return lowbank_process_device_control_5_fields(state, frame)
    if target == 18026:
        return lowbank_coordinate_live_state_60_fields(state, frame)
    if target == 18242:
        return lowbank_coordinate_live_state_61_fields(state, frame)
    if target == 18462:
        return lowbank_process_device_control_6_fields(state, frame)
    if target == 18520:
        return lowbank_coordinate_live_state_62_fields(state, frame)
    if target == 18524:
        return lowbank_select_live_state_19_fields(state, frame)
    if target == 18528:
        return lowbank_process_device_control_4_fields(state, frame)
    if target == 18532:
        return lowbank_coordinate_live_state_63_fields(state, frame)
    if target == 18536:
        return lowbank_process_device_control_7_fields(state, frame)
    if target == 18540:
        return lowbank_coordinate_live_state_64_fields(state, frame)
    if target == 18544:
        return lowbank_coordinate_live_state_65_fields(state, frame)
    if target == 18548:
        return lowbank_coordinate_live_state_66_fields(state, frame)
    if target == 18552:
        return lowbank_process_device_control_8_fields(state, frame)
    if target == 18754:
        return lowbank_process_device_control_9_fields(state, frame)
    if target == 19020:
        return lowbank_select_live_state_20_fields(state, frame)
    if target == 19706:
        return lowbank_coordinate_live_state_67_fields(state, frame)
    if target == 19796:
        return lowbank_select_live_state_21_fields(state, frame)
    if target == 19864:
        return lowbank_coordinate_live_state_68_fields(state, frame)
    if target == 20678:
        return lowbank_coordinate_live_state_69_fields(state, frame)
    if target == 20700:
        return lowbank_process_device_control_10_fields(state, frame)
    if target == 20836:
        return lowbank_coordinate_live_state_70_fields(state, frame)
    if target == 20882:
        return lowbank_coordinate_live_state_71_fields(state, frame)
    if target == 22628:
        return lowbank_update_live_fields_5_fields(state, frame)
    if target == 22660:
        return lowbank_select_live_state_22_fields(state, frame)
    if target == 22666:
        return lowbank_coordinate_live_state_72_fields(state, frame)
    if target == 22690:
        return lowbank_coordinate_live_state_73_fields(state, frame)
    if target == 22714:
        return lowbank_process_counted_records_7_fields(state, frame)
    if target == 22756:
        return lowbank_process_counted_records_7_alternate_1_fields(state, frame)
    if target == 22782:
        return lowbank_select_live_state_23_fields(state, frame)
    if target == 22786:
        return lowbank_select_live_state_24_fields(state, frame)
    if target == 22790:
        return lowbank_select_live_state_25_fields(state, frame)
    if target == 22812:
        return lowbank_process_counted_records_8_fields(state, frame)
    if target == 22826:
        return lowbank_process_counted_records_8_alternate_1_fields(state, frame)
    if target == 22844:
        return lowbank_process_counted_records_8_alternate_2_fields(state, frame)
    if target == 22872:
        return lowbank_process_counted_records_8_alternate_3_fields(state, frame)
    if target == 22892:
        return lowbank_process_counted_records_8_alternate_4_fields(state, frame)
    if target == 22914:
        return lowbank_process_counted_records_8_alternate_5_fields(state, frame)
    if target == 22938:
        return lowbank_process_counted_records_9_fields(state, frame)
    if target == 23000:
        return lowbank_process_counted_records_9_alternate_1_fields(state, frame)
    if target == 23026:
        return lowbank_process_counted_records_9_alternate_2_fields(state, frame)
    if target == 23056:
        return lowbank_process_counted_records_9_alternate_3_fields(state, frame)
    if target == 24012:
        return lowbank_coordinate_live_state_76_fields(state, frame)
    if target == 24018:
        return lowbank_coordinate_live_state_76_alternate_1_fields(state, frame)
    if target == 24060:
        return lowbank_process_counted_records_10_fields(state, frame)
    if target == 24154:
        return lowbank_coordinate_live_state_77_fields(state, frame)
    if target == 24250:
        return lowbank_update_live_fields_6_fields(state, frame)
    if target == 24274:
        return lowbank_process_counted_records_11_fields(state, frame)
    if target == 24298:
        return lowbank_coordinate_live_state_78_fields(state, frame)
    if target == 38046:
        return lowbank_process_counted_records_12_fields(state, frame)
    if target == 38152:
        return lowbank_process_device_control_11_fields(state, frame)
    if target == 41778:
        return lowbank_select_live_state_26_fields(state, frame)
    if target == 41806:
        return lowbank_coordinate_live_state_79_fields(state, frame)
    if target == 43700:
        return lowbank_process_counted_records_13_fields(state, frame)
    if target == 43818:
        return lowbank_process_counted_records_13_alternate_1_fields(state, frame)
    if target == 43828:
        return lowbank_process_counted_records_13_alternate_2_fields(state, frame)
    if target == 43746:
        return lowbank_process_counted_records_14_fields(state, frame)
    if target == 48056:
        return lowbank_coordinate_live_state_80_fields(state, frame)
    if target == 48090:
        return lowbank_coordinate_live_state_81_fields(state, frame)
    if target == 48128:
        return lowbank_coordinate_live_state_82_fields(state, frame)
    if target == 48164:
        return lowbank_process_counted_records_15_fields(state, frame)
    if target == 48206:
        return lowbank_coordinate_live_state_83_fields(state, frame)
    if target == 48346:
        return lowbank_update_live_fields_7_fields(state, frame)
    if target == 48372:
        return lowbank_process_counted_records_16_fields(state, frame)
    if target == 48502:
        return lowbank_process_counted_records_17_fields(state, frame)
    if target == 48676:
        return lowbank_select_live_state_27_fields(state, frame)
    if target == 48708:
        return lowbank_coordinate_live_state_84_fields(state, frame)
    if target == 48870:
        return lowbank_process_counted_records_18_fields(state, frame)
    if target == 48986:
        return lowbank_update_record_flags_9_fields(state, frame)
    if target == 49058:
        return lowbank_coordinate_live_state_85_fields(state, frame)
    if target == 16560:
        return lowbank_process_device_control_4_fields(state, frame)
    if target == 44682:
        from ..high_level_scene_flows.business_scene import decode_glyph_rows_to_buffers_fields
        from .services import SceneRefreshMemory
        return decode_glyph_rows_to_buffers_fields(SceneRefreshMemory(state), frame)
    if target == 56998:
        from ..high_level_scene_flows.business_scene import darken_palette_fields
        from .services import SceneRefreshMemory
        return darken_palette_fields(SceneRefreshMemory(state), frame)
    if target == 239992:
        from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields
        from .services import SceneRefreshMemory
        return advance_scene_palette_fade_fields(SceneRefreshMemory(state), frame)
    if target == 44294:
        from ..high_level_scene_flows.business_scene import flush_scene_transfer_queue_fields
        from .services import SceneRefreshMemory
        return flush_scene_transfer_queue_fields(SceneRefreshMemory(state), frame)
    if target == 41946:
        from ..high_level_main_flows.business_lowbank import refresh_scene_palettes_frame_fields
        return refresh_scene_palettes_frame_fields(state, frame)
    if target == 22632:
        from ..high_level_main_flows.business_commands import set_command_selection_cursor_frame_fields
        return set_command_selection_cursor_frame_fields(state, frame)
    if target == 23082:
        from ..high_level_main_flows.business_commands import store_command_selection_value_frame_fields
        return store_command_selection_value_frame_fields(state, frame)
    if target == 5566:
        from ..high_level_main_flows.business_main import clamp_campaign_camera_targets_fields
        return clamp_campaign_camera_targets_fields(state, frame)
    if target == 9206:
        from ..high_level_main_flows.business_main import draw_campaign_fade_marker_fields
        return draw_campaign_fade_marker_fields(state, frame)
    if target == 15956:
        from ..high_level_main_flows.business_map import restore_scene_descriptor_fields
        return restore_scene_descriptor_fields(state, frame)
    if target == 14848:
        from ..high_level_main_flows.business_title import upload_title_emblem_set_fields
        return upload_title_emblem_set_fields(state, frame)
    if target == 240310:
        from ..high_level_main_flows.business_scene_support import decode_unmasked_literal_plane_fields
        return decode_unmasked_literal_plane_fields(state, frame)
    if target == 238902:
        from .business_highbank import highbank_process_device_control_7_fields
        return highbank_process_device_control_7_fields(state, frame)
    if target == 239772:
        from .business_highbank import highbank_process_device_control_8_fields
        return highbank_process_device_control_8_fields(state, frame)
    if target == 23704:
        from ..high_level_main_flows.business_commands import present_command_warning_frame_fields
        return present_command_warning_frame_fields(state, frame)
    if target == 56860:
        return lowbank_select_live_state_32_fields(state, frame)
    if target == 57652:
        return lowbank_coordinate_live_state_103_fields(state, frame)
    if target == 58360:
        return lowbank_update_live_fields_9_fields(state, frame)
    if target == 58432:
        return lowbank_coordinate_live_state_104_fields(state, frame)
    if target == 58466:
        return lowbank_update_record_flags_12_fields(state, frame)
    if target == 58640:
        return lowbank_update_record_flags_12_alternate_1_fields(state, frame)
    if target == 58532:
        return lowbank_select_live_state_33_fields(state, frame)
    if target == 59280:
        return lowbank_coordinate_live_state_105_fields(state, frame)
    if target == 59622:
        return lowbank_calculate_live_quotient_1_fields(state, frame)
    if target == 60514:
        return lowbank_scale_live_record_value_1_fields(state, frame)
    if target == 60884:
        return lowbank_update_live_fields_10_fields(state, frame)
    if target == 60886:
        return lowbank_coordinate_live_state_107_fields(state, frame)
    if target == 66538:
        return lowbank_process_counted_records_38_fields(state, frame)
    if target == 66956:
        return lowbank_calculate_live_quotient_5_fields(state, frame)
    if target == 67220:
        return lowbank_coordinate_live_state_113_fields(state, frame)
    if target == 67300:
        return lowbank_coordinate_live_state_114_fields(state, frame)
    if target == 68148:
        return lowbank_coordinate_live_state_115_fields(state, frame)
    if target == 68156:
        return lowbank_coordinate_live_state_116_fields(state, frame)
    if target == 68164:
        return lowbank_coordinate_live_state_117_fields(state, frame)
    if target == 73500:
        return lowbank_update_record_flags_16_fields(state, frame)
    if target == 73986:
        return lowbank_coordinate_live_state_125_fields(state, frame)
    if target == 73996:
        return lowbank_coordinate_live_state_126_fields(state, frame)
    if target == 75224:
        return lowbank_update_record_flags_17_fields(state, frame)
    if target == 77554:
        return lowbank_coordinate_live_state_127_fields(state, frame)
    if target == 77636:
        return lowbank_select_live_state_37_fields(state, frame)
    if target == 77710:
        return lowbank_update_record_flags_18_fields(state, frame)
    if target == 77856:
        return lowbank_select_live_state_38_fields(state, frame)
    if target == 78510:
        return lowbank_calculate_live_quotient_6_fields(state, frame)
    if target == 78972:
        return lowbank_coordinate_live_state_128_fields(state, frame)
    if target == 79770:
        return lowbank_scale_live_record_value_5_fields(state, frame)
    if target == 80566:
        return lowbank_coordinate_live_state_129_fields(state, frame)
    if target == 81274:
        return lowbank_process_counted_records_39_fields(state, frame)
    if target == 81474:
        return lowbank_coordinate_live_state_130_fields(state, frame)
    if target == 75530:
        from .business_city import append_city_order_decimal_fields
        return append_city_order_decimal_fields(state, frame)
    if target in (112030, 112132, 114656, 32906):
        from .business_city import execute_deployment_menu_fields
        return execute_deployment_menu_fields(state, target, frame)
    if target == 41304:
        from ..high_level_main_flows.business_map import refresh_world_cursor_attributes_alternate_1_frame_fields
        return refresh_world_cursor_attributes_alternate_1_frame_fields(state, frame)
    if target == 117950:
        from .business_city import begin_city_group_result_notice_fields
        return begin_city_group_result_notice_fields(state, frame)
    if target == 64252:
        return lowbank_update_record_flags_13_fields(state, frame)
    if target == 64496:
        return lowbank_coordinate_live_state_106_fields(state, frame)
    if target == 64752:
        return lowbank_coordinate_live_state_106_alternate_1_fields(state, frame)
    if target == 64640:
        return lowbank_update_live_fields_11_fields(state, frame)
    if target == 64642:
        return lowbank_coordinate_live_state_108_fields(state, frame)
    if target == 64664:
        return lowbank_calculate_live_quotient_2_fields(state, frame)
    if target == 64756:
        return lowbank_calculate_live_quotient_3_fields(state, frame)
    if target == 65030:
        return lowbank_coordinate_live_state_109_fields(state, frame)
    if target == 65306:
        return lowbank_update_record_flags_14_fields(state, frame)
    if target == 65368:
        return lowbank_select_live_state_34_fields(state, frame)
    if target == 65432:
        return lowbank_process_counted_records_37_fields(state, frame)
    if target == 65604:
        return lowbank_calculate_live_quotient_4_fields(state, frame)
    if target == 65644:
        return lowbank_coordinate_live_state_110_fields(state, frame)
    if target == 65692:
        return lowbank_update_live_fields_12_fields(state, frame)
    if target == 65696:
        return lowbank_update_live_fields_13_fields(state, frame)
    if target == 65702:
        return lowbank_update_live_fields_14_fields(state, frame)
    if target == 65708:
        return lowbank_update_live_fields_15_fields(state, frame)
    if target == 65714:
        return lowbank_update_live_fields_16_fields(state, frame)
    if target == 65724:
        return lowbank_update_live_fields_17_fields(state, frame)
    if target == 65734:
        return lowbank_update_live_fields_18_fields(state, frame)
    if target == 65744:
        return lowbank_update_live_fields_19_fields(state, frame)
    if target == 65754:
        return lowbank_scale_live_record_value_2_fields(state, frame)
    if target == 66084:
        return lowbank_coordinate_live_state_111_fields(state, frame)
    if target == 66092:
        return lowbank_coordinate_live_state_112_fields(state, frame)
    if target == 66100:
        return lowbank_update_record_flags_15_fields(state, frame)
    if target == 68184:
        return lowbank_coordinate_live_state_118_fields(state, frame)
    if target == 68264:
        return lowbank_scale_live_record_value_3_fields(state, frame)
    if target == 68318:
        return lowbank_resolve_readonly_state_2_fields(state, frame)
    if target == 68724:
        return lowbank_scale_live_record_value_4_fields(state, frame)
    if target == 69522:
        return lowbank_scale_live_record_value_4_alternate_1_fields(state, frame)
    if target == 68884:
        return lowbank_coordinate_live_state_119_fields(state, frame)
    if target == 68964:
        return lowbank_coordinate_live_state_119_alternate_1_fields(state, frame)
    if target == 69044:
        return lowbank_coordinate_live_state_119_alternate_2_fields(state, frame)
    if target == 69138:
        return lowbank_coordinate_live_state_120_fields(state, frame)
    if target == 69258:
        return lowbank_coordinate_live_state_121_fields(state, frame)
    if target == 69296:
        return lowbank_coordinate_live_state_122_fields(state, frame)
    if target == 69434:
        return lowbank_coordinate_live_state_123_fields(state, frame)
    if target == 69772:
        return lowbank_coordinate_live_state_124_fields(state, frame)
    if target == 69838:
        return lowbank_select_live_state_35_fields(state, frame)
    if target == 69922:
        return lowbank_select_live_state_36_fields(state, frame)
    if target == 33748:
        from .services import BattlePolicyMemory, first_deployment_random_fields
        return first_deployment_random_fields(BattlePolicyMemory(state), frame)
    if target == 67372:
        from .services import SceneRefreshMemory, load_gameplay_scene_fields
        return load_gameplay_scene_fields(SceneRefreshMemory(state), frame)
    if target == 218976:
        from .services import signed_divmod_fields
        return signed_divmod_fields(state, frame)
    if target == 111174:
        from .business_city import deploy_selected_group_fields
        return deploy_selected_group_fields(state, frame)
    if target == 199284:
        from .services import SceneRefreshMemory
        from ..high_level_gameplay_flow.business_services import present_gameplay_message_fields
        return present_gameplay_message_fields(SceneRefreshMemory(state), frame)
    if target == 49464:
        return lowbank_resolve_readonly_state_1_fields(state, frame)
    elif target == 49636:
        return lowbank_process_counted_records_19_fields(state, frame)
    elif target == 49802:
        return lowbank_coordinate_live_state_86_fields(state, frame)
    elif target == 49830:
        return lowbank_process_counted_records_20_fields(state, frame)
    elif target == 49894:
        return lowbank_process_counted_records_21_fields(state, frame)
    elif target == 50324:
        return lowbank_coordinate_live_state_87_fields(state, frame)
    elif target == 50412:
        return lowbank_select_live_state_28_fields(state, frame)
    elif target == 50512:
        return lowbank_select_live_state_29_fields(state, frame)
    elif target == 50626:
        return lowbank_update_record_flags_10_fields(state, frame)
    elif target == 50668:
        return lowbank_process_counted_records_22_fields(state, frame)
    elif target == 50698:
        return lowbank_process_counted_records_23_fields(state, frame)
    elif target == 50808:
        return lowbank_coordinate_live_state_88_fields(state, frame)
    elif target == 50878:
        return lowbank_process_counted_records_24_fields(state, frame)
    elif target == 50908:
        return lowbank_update_live_fields_8_fields(state, frame)
    elif target == 50934:
        return lowbank_coordinate_live_state_89_fields(state, frame)
    elif target == 51250:
        return lowbank_process_counted_records_25_fields(state, frame)
    elif target == 51622:
        return lowbank_process_counted_records_26_fields(state, frame)
    elif target == 52012:
        return lowbank_process_counted_records_27_fields(state, frame)
    elif target == 52056:
        return lowbank_coordinate_live_state_90_fields(state, frame)
    elif target == 52196:
        return lowbank_coordinate_live_state_91_fields(state, frame)
    elif target == 52226:
        return lowbank_coordinate_live_state_91_alternate_1_fields(state, frame)
    elif target == 52264:
        return lowbank_select_live_state_30_fields(state, frame)
    elif target == 52594:
        return lowbank_process_counted_records_28_fields(state, frame)
    elif target == 52808:
        return lowbank_process_counted_records_29_fields(state, frame)
    elif target == 52830:
        return lowbank_coordinate_live_state_92_fields(state, frame)
    elif target == 52940:
        return lowbank_select_live_state_31_fields(state, frame)
    elif target == 52978:
        return lowbank_coordinate_live_state_93_fields(state, frame)
    elif target == 53042:
        return lowbank_process_counted_records_30_fields(state, frame)
    elif target == 53176:
        return lowbank_process_counted_records_31_fields(state, frame)
    elif target == 53288:
        return lowbank_process_counted_records_32_fields(state, frame)
    elif target == 53332:
        return lowbank_process_counted_records_33_fields(state, frame)
    elif target == 53564:
        return lowbank_process_counted_records_34_fields(state, frame)
    elif target == 53582:
        return lowbank_coordinate_live_state_94_fields(state, frame)
    elif target == 53592:
        return lowbank_coordinate_live_state_95_fields(state, frame)
    elif target == 53706:
        return lowbank_coordinate_live_state_96_fields(state, frame)
    elif target == 53872:
        return lowbank_update_record_flags_11_fields(state, frame)
    elif target == 54120:
        return lowbank_coordinate_live_state_97_fields(state, frame)
    elif target == 54130:
        return lowbank_coordinate_live_state_98_fields(state, frame)
    elif target == 54426:
        return lowbank_coordinate_live_state_99_fields(state, frame)
    elif target == 54566:
        return lowbank_process_counted_records_35_fields(state, frame)
    elif target == 54624:
        return lowbank_process_counted_records_36_fields(state, frame)
    elif target == 54820:
        return lowbank_coordinate_live_state_100_fields(state, frame)
    elif target == 54830:
        return lowbank_coordinate_live_state_101_fields(state, frame)
    elif target == 54974:
        return lowbank_coordinate_live_state_102_fields(state, frame)
    if target in (44040, 423666, 75530, 75580, 75588, 75596):
        from .business_city import execute_deployment_menu_fields
        return execute_deployment_menu_fields(state, target, frame)
    if target == 158714:
        from .services import SceneRefreshMemory, stage_sprite_word_packet_fields
        return stage_sprite_word_packet_fields(SceneRefreshMemory(state), frame)
    if target == 49334:
        from ..high_level_main_flows.business_commands import open_roster_selection_message_frame_fields
        return open_roster_selection_message_frame_fields(state, frame)
    if target == 51044:
        from ..high_level_main_flows.business_commands import adjust_force_relation_selection_frame_fields
        return adjust_force_relation_selection_frame_fields(state, frame)
    if target == 51088:
        from ..high_level_main_flows.business_commands import confirm_force_relation_selection_frame_fields
        return confirm_force_relation_selection_frame_fields(state, frame)
    if target == 218334:
        from .business_highbank import append_command_variable_glyph_row_fields
        return append_command_variable_glyph_row_fields(state, frame)
    if target == 218492:
        from .business_highbank import append_command_blank_glyph_row_fields
        return append_command_blank_glyph_row_fields(state, frame)
    if target == 59438:
        from ..high_level_main_flows.business_scene_support import recover_unacted_officer_b200_fields
        return recover_unacted_officer_b200_fields(state, frame)
    if target in (35424, 37080):
        return _window_storage_child_fields(state, frame, target)
    if target == 59312:
        return schedule_transport_debit_fields(state, frame)
    if target == 70022:
        return scan_city_officers_fields(state, frame)
    if target in (60438, 60950):
        from ..high_level_command_actions.contexts_personnel import execute_personnel_scene_fields
        return execute_personnel_scene_fields(state, target, frame)
    if target == 84384:
        from ..high_level_player_commands.business_display import execute_city_group_display_fields
        from ..high_level_player_commands.contexts_display import SpritePacketMemory
        return execute_city_group_display_fields(SpritePacketMemory(state), frame, target)
    if target == 90450:
        from .business_city import initialize_group_route_text_row_fields
        return initialize_group_route_text_row_fields(state, frame)
    raise MovementContinuationBoundary(target, frame, 'actual lowbank child lacks complete returned Scene fields; no device/handler success invented')


# Lowbank53 accounts and allocation: one live algorithm per whole, with explicit entry aliases.
from .services import (first_replace, _movement_frame, _movement_move, _movement_move_long, _movement_compare, _movement_test, _first_compare_long, FirstDeploymentReturnBoundary, MovementContinuationBoundary)

"""Packed resource math and record settlement. No media constants or decoded PC engine."""

def _economy_delta_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, width: int=16, subtract: bool=False) -> FirstDeploymentFrame:
    """Shared fixed-width arithmetic preserves the actual narrow carrier."""
    from .services import _movement_binary_flags
    original=frame.carrier(name)
    mask=(1<<width)-1
    frame,value=_movement_binary_flags(state,frame,original&mask,amount&mask,width,subtract)
    if width==8:
        return first_replace(frame,**{name:replace_byte(original,value)})
    if width==16:
        return first_replace(frame,**{name:replace_word(original,value)})
    if width==32:
        return first_replace(frame,**{name:value})
    raise ValueError('actual resource arithmetic width required')


def _economy_memory_delta_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, amount: int, width: int=16, subtract: bool=False) -> FirstDeploymentFrame:
    from .services import _movement_binary_flags
    frame,value=_movement_binary_flags(state,frame,state.read(address,width//8),amount,width,subtract)
    state.write(address,width//8,value)
    return frame


def schedule_transport_debit_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E7B0: publish the transport order, then debit live city gold and rice.

    Coordinates and prices remain the actual external numeric views. Keep
    separate selected-city/transport-choice rereads, signed WORD indexes and
    unchecked original LONG subtraction. D0/D1 upper WORDs and other registers
    survive; final A0/A1/A2 are the price/gold/rice views, not host snapshots.
    """
    frame = _movement_frame(state, frame)
    from .services import _movement_fixed_shift_word
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)
    frame = first_replace(frame, roster=state.table_at(0xFFFFCDFC).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF688, 2), 16)
    frame = _lowbank_ui_arithmetic_fields(state, frame, 'target_y', 1)
    frame = _economy_logic_fields(state, frame, 'target_y', 16, 8, 'or')
    frame = _lowbank_ui_store_fields(state, frame,
        frame.roster.address(low16(frame.target_x)), low8(frame.target_y), 1)
    frame = first_replace(frame, candidates=state.table_at(0xD4AC6).cursor())
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    for displacement, order_byte in ((2, 1), (0, 2)):
        frame = _movement_move(state, frame, 'unit',
            frame.candidates.word(low16(frame.target_y), displacement), 16)
        frame = _movement_fixed_shift_word(state, frame, 'unit', 4, True)
        frame = _lowbank_ui_store_fields(state, frame,
            frame.roster.address(low16(frame.target_x), order_byte), low8(frame.unit), 1)
    frame = _lowbank_ui_store_fields(state, frame,
        frame.roster.address(low16(frame.target_x), 3), state.read(0xFFFFF393, 1), 1)
    frame = _movement_move(state, frame, 'target_y', state.read(0xFFFFF3A8, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFDFFC).cursor(),
        controller=state.table_at(0xFFFFE09C).cursor())
    frame = _movement_move(state, frame, 'target_x', state.read(0xFFFFF688, 2), 16)
    frame = _movement_fixed_shift_word(state, frame, 'target_x', 3)
    frame = first_replace(frame, roster=state.table_at(0x13B68).cursor())
    for balance, price_offset in ((frame.candidates, 0), (frame.controller, 4)):
        frame = _movement_move_long(state, frame, 'unit', balance.long(low16(frame.target_y)))
        frame = _economy_delta_fields(state, frame, 'unit',
            frame.roster.long(low16(frame.target_x), price_offset), 32, True)
        frame = _lowbank_ui_store_fields(state, frame,
            balance.address(low16(frame.target_y)), frame.unit, 4)
    return frame


def scan_city_officers_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11186: append the tagged-city officers to the caller's actual A0 list.

    D0 is the real city input, D2 the existing count; neither is defaulted.
    Preserve the BYTE MOVE's retained D4 bits on skipped positive assignments,
    the original WORD mask on negative assignments, and D3's DBRA residue.
    The caller, not this leaf, owns the list terminator and physical RTS LONG.
    """
    frame = _movement_frame(state, frame)
    frame = first_replace(frame, candidates=state.table_at(0xFFFFCC00).cursor())
    frame = _movement_move(state, frame, 'count', 255, 16)
    while True:
        frame = _movement_move(state, frame, 'distance',
            frame.candidates.byte(s16(low16(frame.count))), 8)
        if frame.status & 8:
            frame = _economy_logic_fields(state, frame, 'distance', 127)
            frame = _movement_compare(state, frame, low16(frame.distance), low16(frame.target_x), 16)
            if frame.status & 4:
                frame = _lowbank_ui_store_fields(state, frame, frame.roster.base, low16(frame.count))
                frame = first_replace(frame, roster=frame.roster.advance(2))
                frame = _lowbank_ui_arithmetic_fields(state, frame, 'unit', 1)
        frame = _lowbank_ui_counter_fields(frame, 'count')
        if low16(frame.count) == 65535:
            return frame


def _window_storage_child_fields(state: SceneState,
        frame: FirstDeploymentFrame, target: int) -> FirstDeploymentFrame:
    """The title's two real cartridge calls use one complete same-Scene ABI.

    Validation leaves the original carry and checksum-clobbered registers;
    restore keeps both original exits and its nontransactional DATA order.
    This adapter owns no CALL slot, RAM copy, SaveImage, device control or
    default register. The supplied Scene's hardware owns the one live SRAM.
    """
    if target not in (35424, 37080):
        raise ValueError('only actual title restore/header-check entries required')
    frame = _movement_frame(state, frame)
    from ..high_level_storage.contexts_scene_storage import SceneStorageState
    from ..high_level_storage.contexts_storage_fields import StorageFrame
    from ..high_level_storage.business_load import restore_saved_game_state_frame_fields
    from ..high_level_storage.business_streams import validate_saved_header_and_checksum_frame_fields
    storage = SceneStorageState(state)
    entered = StorageFrame(
        d0=frame.target_x, d1=frame.target_y, d2=frame.unit, d3=frame.count,
        d4=frame.distance, d5=frame.offset_x, d6=frame.offset_y, d7=frame.choice,
        a0=frame.roster.base, a1=frame.candidates.base,
        a2=frame.controller.base, a3=frame.scan.base,
        a4=frame.opponent.base, a5=frame.scratch.base, a6=frame.auxiliary.base,
        stack_cursor=frame.stack_cursor.base,
        status_word=(state.sr & 65504) | frame.status)
    if target == 35424:
        returned = restore_saved_game_state_frame_fields(storage, entered)
    else:
        returned = validate_saved_header_and_checksum_frame_fields(storage, entered)
    if type(returned) is not StorageFrame:
        raise MovementContinuationBoundary(target, frame, 'complete actual storage return required')
    returned.validate(storage)
    state.sr = returned.status_word
    return first_replace(frame,
        target_x=returned.d0, target_y=returned.d1, unit=returned.d2, count=returned.d3,
        distance=returned.d4, offset_x=returned.d5, offset_y=returned.d6, choice=returned.d7,
        roster=state.table_at(returned.a0).cursor(), candidates=state.table_at(returned.a1).cursor(),
        controller=state.table_at(returned.a2).cursor(), scan=state.table_at(returned.a3).cursor(),
        opponent=state.table_at(returned.a4).cursor(), scratch=state.table_at(returned.a5).cursor(),
        auxiliary=state.table_at(returned.a6).cursor(),
        stack_cursor=state.table_at(returned.stack_cursor).cursor(), status=returned.status_word & 31)


def _economy_logic_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, mask: int, width: int=16, operation: str='and') -> FirstDeploymentFrame:
    original=frame.carrier(name)&((1<<width)-1)
    if operation=='and':
        value=original&mask
    elif operation=='or':
        value=original|mask
    else:
        raise ValueError('actual resource AND/OR role required')
    if width==32:
        return _movement_move_long(state,frame,name,value)
    return _movement_move(state,frame,name,value,width)


def _economy_memory_logic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, mask: int, width: int=8) -> FirstDeploymentFrame:
    value=state.read(address,width//8)|mask
    return _lowbank_ui_store_fields(state,frame,address,value,width//8)


def _economy_compare_long_fields(state: SceneState, frame: FirstDeploymentFrame,
        left: int, right: int) -> FirstDeploymentFrame:
    frame=_first_compare_long(frame,left,right)
    state.sr=(state.sr&65504)|frame.status
    return frame


def _economy_long_shift_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, amount: int, right: bool=False) -> FirstDeploymentFrame:
    """Reuse the existing live LONG-shift cores; no extra RAM/stack operations."""
    if not right:
        from .services import SceneRefreshMemory
        from ..high_level_scene_flows.business_scene import _glyph_shift_long_fields
        return _glyph_shift_long_fields(SceneRefreshMemory(state),frame,name,amount)
    if amount==8:
        from ..high_level_main_flows.business_movement_support import _movement_shift_long
        return _movement_shift_long(state,frame,name,True)
    from .business_city import _recruitment_right_long
    if amount==5:
        frame=_recruitment_right_long(state,frame,name,4)
        return _recruitment_right_long(state,frame,name,1)
    return _recruitment_right_long(state,frame,name,amount)


def _economy_swap_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str) -> FirstDeploymentFrame:
    return _movement_move_long(state,frame,name,swap_words(frame.carrier(name)))


def _economy_rotate_selector_byte_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1007C rotates only D3.B; X and the other three carrier bytes survive."""
    original=low8(frame.count)
    value=(original>>1)|((original&1)<<7)
    status=(frame.status&16)|(1 if original&1 else 0)|(8 if value&128 else 0)|(4 if value==0 else 0)
    state.sr=(state.sr&65504)|status
    return first_replace(frame,count=replace_byte(frame.count,value),status=status)


def lowbank_update_live_fields_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FC80 is the original empty ordinary RTS, not a fabricated child return."""
    return _movement_frame(state,frame)


def lowbank_update_live_fields_12_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8,True)


def lowbank_update_live_fields_13_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_delta_fields(state,_movement_frame(state,frame),'unit',1,8)


def lowbank_update_live_fields_14_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8)


def lowbank_update_live_fields_15_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_delta_fields(state,_movement_frame(state,frame),'unit',1,8,True)


def lowbank_update_live_fields_16_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8,True)
    return _economy_delta_fields(state,frame,'unit',1,8)


def lowbank_update_live_fields_17_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8)
    return _economy_delta_fields(state,frame,'unit',1,8)


def lowbank_update_live_fields_18_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8)
    return _economy_delta_fields(state,frame,'unit',1,8,True)


def lowbank_update_live_fields_19_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_economy_delta_fields(state,_movement_frame(state,frame),'target_y',1,8,True)
    return _economy_delta_fields(state,frame,'unit',1,8,True)


def lowbank_calculate_live_quotient_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10044: selected-roster trait sum and the original WORD divisor."""
    from .services import _movement_divu_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,controller=state.table_at(0xFFFFC400),scan=state.table_at(0x00FF399E).cursor())
    frame=_movement_move(state,frame,'unit',0,16)
    while True:
        value=frame.scan.word()
        frame=first_replace(frame,scan=frame.scan.advance(2))
        frame=_movement_move(state,frame,'count',value,16)
        if frame.status&8:
            break
        frame=_movement_move(state,frame,'distance',0,16)
        frame=_movement_move(state,frame,'distance',frame.controller.byte(low16(frame.count)),8)
        frame=_economy_delta_fields(state,frame,'unit',low16(frame.distance))
    frame=_economy_logic_fields(state,frame,'target_y',15)
    frame=_economy_logic_fields(state,frame,'unit',65535,32)
    return _movement_divu_word(state,frame,'unit',low16(frame.target_y),0x10068)


def lowbank_coordinate_live_state_110_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1006C: real rotated selector BYTE and immutable WORD instruction-offset table."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(0,1),8)
    frame=_movement_move(state,frame,'unit',frame.roster.byte(0,2),8)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF678,2),16)
    frame=_movement_move(state,frame,'distance',0,16)
    while True:
        frame=_economy_delta_fields(state,frame,'distance',1)
        frame=_economy_rotate_selector_byte_fields(state,frame)
        if not frame.status&1:
            break
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    selected=state.table_at(0x1008A).word(low16(frame.distance))
    frame=_movement_move(state,frame,'distance',selected,16)
    return _lowbank_ui_call_fields(state,frame,0x1009C+s16(selected),0x1008A)


def lowbank_update_record_flags_15_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10234: one packed account settlement, with original BYTE/store order and caps."""
    from .services import _movement_fixed_shift_word, _movement_load_packed_resource, _movement_store_packed_resource
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF57A,1),164,8)
    if not frame.status&4:
        frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
        frame=_movement_load_packed_resource(state,frame,'target_x',5)
        frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF39E,4),32,True)
        frame=_movement_store_packed_resource(state,frame,'target_x',5)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,low16(frame.target_x))
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFB000).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFB200).cursor())
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low16(frame.target_y))
        for address,value in ((0xFFFFF612,520),(0xFFFFF362,40),(0xFFFFF3FE,113)):
            frame=_lowbank_ui_store_fields(state,frame,address,value)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF774,1)
        return _lowbank_ui_store_fields(state,frame,0x00FF7026,1)
    frame=_movement_compare(state,frame,state.read(0xFFFFF57B,1),169,8)
    frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    if not frame.status&4:
        frame=_lowbank_ui_change_bit_fields(state,frame,frame.roster.base,4,True)
        frame=_movement_load_packed_resource(state,frame,'target_x',5)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F0,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',2)
        frame=first_replace(frame,candidates=state.table_at(0xFFFFEF6A).cursor())
        frame=_economy_delta_fields(state,frame,'target_x',frame.candidates.long(low16(frame.target_y)),32,True)
        frame=_movement_store_packed_resource(state,frame,'target_x',5)
        frame=first_replace(frame,roster=state.table_at(0xFFFFEA88).cursor())
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3A6,2))
        frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3F0,2))
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F0,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=first_replace(frame,candidates=state.table_at(0xFFFFEF64).cursor())
        frame=_movement_move(state,frame,'target_y',frame.candidates.word(low16(frame.target_y)),16)
        frame=_economy_delta_fields(state,frame,'target_y',1)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low8(frame.target_y),1)
        for address,value in ((0xFFFFF612,520),(0xFFFFF362,40),(0x00FF7026,9),(0xFFFFF3FE,98)):
            frame=_lowbank_ui_store_fields(state,frame,address,value)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
        return _lowbank_ui_store_fields(state,frame,0xFFFFF774,1)
    frame=_economy_memory_logic_fields(state,frame,frame.roster.base,16)
    frame=_movement_load_packed_resource(state,frame,'target_x',5)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3F4,4),32,True)
    frame=_movement_store_packed_resource(state,frame,'target_x',5)
    frame=_movement_load_packed_resource(state,frame,'target_x',9)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF3BA,4),32)
    frame=_economy_compare_long_fields(state,frame,frame.target_x,999999)
    if not frame.status&5:
        frame=_movement_move_long(state,frame,'target_x',999999)
    frame=_movement_store_packed_resource(state,frame,'target_x',9)
    for address,value in ((0xFFFFF612,520),(0xFFFFF362,40),(0xFFFFF3FE,116),(0x00FF7026,11)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    return frame


def _economy_distribute_resource_fields(state: SceneState, frame: FirstDeploymentFrame,
        first: int, continuation: int, second_tail: bool=False) -> FirstDeploymentFrame:
    """100DA's two resource columns share one division; asymmetric final shifts stay original."""
    from .services import _movement_load_packed_resource, _movement_store_packed_resource, _movement_fixed_shift_word, _movement_multiply_word
    frame=_movement_move_long(state,frame,'target_x',frame.choice)
    frame=_economy_delta_fields(state,frame,'target_x',low16(frame.offset_y))
    frame=_movement_load_packed_resource(state,frame,'target_y',first)
    frame=_movement_move_long(state,frame,'count',frame.target_y)
    frame=_economy_long_shift_fields(state,frame,'target_y',5,True)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.offset_y))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.offset_y))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_economy_delta_fields(state,frame,'target_y',frame.unit,32)
    frame=_movement_move_long(state,frame,'unit',frame.target_x)
    frame=_lowbank_ui_call_fields(state,frame,0x35760,continuation)
    frame=_movement_move_long(state,frame,'unit',frame.count)
    frame=_economy_logic_fields(state,frame,'unit',31,32)
    frame=_movement_fixed_shift_word(state,frame,'unit',1,True)
    frame=_economy_long_shift_fields(state,frame,'target_y',5)
    frame=_economy_delta_fields(state,frame,'target_y',frame.unit,32)
    frame=_economy_delta_fields(state,frame,'count',frame.target_y,32,True)
    frame=_movement_store_packed_resource(state,frame,'target_y',first)
    for displacement,long_shift in ((3,not second_tail),(2,True),(1,False)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+displacement),low8(frame.count),1)
        if long_shift:
            frame=_economy_long_shift_fields(state,frame,'count',8,True)
        else:
            frame=_movement_fixed_shift_word(state,frame,'count',8,True)
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.count),1)
    return first_replace(frame,candidates=frame.candidates.advance(4))


def lowbank_scale_live_record_value_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """100DA: troop-weighted division of two packed resource balances."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,controller=state.table_at(0xFFFFC800),scan=state.table_at(0x00FF399E).cursor())
    frame=_movement_move_long(state,frame,'offset_y',0)
    for name,base in (('offset_y',0x00FF399E),('choice',0x00FF398A)):
        if name=='choice':
            frame=first_replace(frame,scan=state.table_at(base).cursor())
            frame=_movement_move_long(state,frame,name,0)
        while True:
            value=frame.scan.word()
            frame=first_replace(frame,scan=frame.scan.advance(2))
            frame=_movement_move(state,frame,'target_x',value,16)
            if frame.status&8:
                break
            frame=_movement_fixed_shift_word(state,frame,'target_x',2)
            frame=_movement_move_long(state,frame,'target_x',frame.controller.long(low16(frame.target_x)))
            frame=_economy_delta_fields(state,frame,name,frame.target_x,32)
            frame=_economy_delta_fields(state,frame,name,100,32)
        frame=_economy_long_shift_fields(state,frame,name,5,True)
    frame=_economy_distribute_resource_fields(state,frame,5,0x1014C)
    return _economy_distribute_resource_fields(state,frame,9,0x101BA,True)


"""Account transfer, member-roster compaction and the two-column resource commit."""

def _economy_register_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, bit: int, clear: bool=False) -> FirstDeploymentFrame:
    """68000 register bit operations are LONG, unlike memory BYTE bit operations."""
    value=frame.carrier(name)
    mask=1<<(bit&31)
    status=(frame.status&27)|(4 if not value&mask else 0)
    state.sr=(state.sr&65504)|status
    if clear:
        return first_replace(frame,status=status,**{name:value&u32(~mask)})
    return first_replace(frame,status=status)


def lowbank_update_record_flags_13_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FAFC: transfer one scheduled city resource amount; cap the receiver at 999999."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE9F8).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.candidates.byte(low16(frame.target_x),1),8)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE65C).cursor())
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_y)))
    frame=_lowbank_ui_call_fields(state,frame,0xFBAA,0xFB22)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_x),1),8)
    frame=_movement_fixed_shift_word(state,frame,'unit',2)
    frame=first_replace(frame,controller=state.table_at(0xFFFFDFFC))
    frame=_movement_move_long(state,frame,'count',frame.controller.long(low16(frame.unit)))
    frame=_economy_delta_fields(state,frame,'count',frame.target_y,32,True)
    if frame.status&1:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_movement_move(state,frame,'target_x',189,16)
        return _lowbank_ui_call_fields(state,frame,0x676F2,0xFBA8)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.controller.base+s16(low16(frame.unit))),frame.count,4)
    frame=first_replace(frame,scan=state.table_at(0xFFFFE65C).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.scan.base+s16(low16(frame.unit))),0,4,True)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_x)),8)
    frame=_movement_fixed_shift_word(state,frame,'unit',2)
    frame=_movement_move_long(state,frame,'count',frame.controller.long(low16(frame.unit)))
    frame=_economy_delta_fields(state,frame,'count',frame.target_y,32)
    frame=_economy_compare_long_fields(state,frame,frame.count,999999)
    if not frame.status&5:
        frame=_movement_move_long(state,frame,'count',999999)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.controller.base+s16(low16(frame.unit))),frame.count,4)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_x))),0,4,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFE700,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_economy_register_bit_fields(state,frame,'target_x',frame.target_y,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFE700,low16(frame.target_x))
    for address,value in ((0xFFFFF362,40),(0xFFFFF612,520),(0xFFFFF3FE,53),(0x00FF7026,18)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    return frame


def _economy_cleanup_tail_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E822 is a shared BRA tail; preserve the caller LONG, then its real E826 inner slot."""
    frame=_lowbank_ui_call_fields(state,frame,0xE82E,0xE826)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF579,255,1)


def lowbank_coordinate_live_state_106_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_cleanup_tail_fields(state,_movement_frame(state,frame))


def lowbank_coordinate_live_state_106_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_cleanup_tail_fields(state,_movement_frame(state,frame))


def lowbank_coordinate_live_state_108_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF57A,1),33,8)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x10A58,0xFC90)
    return _lowbank_ui_call_fields(state,frame,0x111AC,0xFC96)


def lowbank_calculate_live_quotient_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FC98: replace the city's assigned officer and publish the hundredth-sized value."""
    from .services import _movement_fixed_shift_word, _movement_divu_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),4,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFF392,2))
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE80C).cursor(),candidates=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x),8),16)
    if not frame.status&8:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_y))),0,1,True)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+8),65535)
        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF3A6,2),16)
        if frame.status&4:
            return frame
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+8),state.read(0xFFFFF3A6,2))
    frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF39E,4))
    frame=_movement_divu_word(state,frame,'target_y',100,0xFCDA)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+10),low16(frame.target_y))
    frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,7)
    return _lowbank_ui_call_fields(state,frame,0x1072C,0xFCEE)


# confirmed source operation (recovered_code.s, FD2C..FD76): B400/C000 WORDs
# feed the original randomly weighted growth calculation, whose write is to
# C500 BYTE. The retained "loyalty" docstring is not evidence of a formal UI
# attribute name and must not be used to relabel this destination or formula.
# Keep partial-width arithmetic, the capped BYTE write, the funds-borrow exit
# and original DIVU boundaries; this clarification changes no game rule.
def lowbank_calculate_live_quotient_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FCF4: pay the officer action cost and increase loyalty using the original capped arithmetic."""
    from .services import _movement_fixed_shift_word, _movement_divu_word, _movement_multiply_word
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,0xFCFA)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC800).cursor())
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    frame=_movement_divu_word(state,frame,'target_y',10,0xFD08)
    frame=_economy_logic_fields(state,frame,'target_y',65535,32)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'count',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'unit',frame.roster.long(low16(frame.count)))
    frame=_economy_delta_fields(state,frame,'unit',frame.target_y,32,True)
    if frame.status&1:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,35)
        frame=_movement_move(state,frame,'target_x',189,16)
        frame=_lowbank_ui_call_fields(state,frame,0x676F2,0xFD96)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF608,120)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.count))),frame.unit,4)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB400).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.unit),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',2)
    frame=_economy_delta_fields(state,frame,'unit',low16(frame.target_y))
    frame=first_replace(frame,roster=state.table_at(0xFFFFC000).cursor())
    frame=_economy_delta_fields(state,frame,'unit',frame.roster.word(low16(frame.target_x)))
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF61C,2),16)
    frame=_economy_long_shift_fields(state,frame,'target_y',2)
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_economy_delta_fields(state,frame,'target_y',8)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_y))
    frame=_movement_divu_word(state,frame,'unit',1000,0xFD52)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC500).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x)),8)
    frame=_economy_delta_fields(state,frame,'target_y',low16(frame.unit))
    frame=_movement_compare(state,frame,low16(frame.target_y),100,16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'count',100,16)
        frame=_economy_delta_fields(state,frame,'count',low16(frame.target_y),16,True)
        frame=_economy_delta_fields(state,frame,'unit',low16(frame.count),16,True)
        frame=_movement_move(state,frame,'target_y',100,16)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low8(frame.target_y),1)
    frame=_lowbank_ui_call_fields(state,frame,0xFDD0,0xFD7E)
    frame=_movement_move_long(state,frame,'unit',u32(s16(low16(frame.unit))))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C8,frame.unit,4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
    frame=_movement_move(state,frame,'target_x',102,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0xFDC0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    return _lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),1,1)


def lowbank_update_record_flags_14_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FF1A: find a tagged roster officer; original negative fallback remains live."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x)),16)
    frame=_economy_logic_fields(state,frame,'target_x',16384,16,'or')
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF500).cursor())
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        frame=_economy_register_bit_fields(state,frame,'target_y',14)
        if not frame.status&4:
            break
    frame=_movement_compare(state,frame,low16(frame.target_y),low16(frame.target_x),16)
    if not frame.status&4:
        while True:
            value=frame.candidates.word()
            frame=first_replace(frame,candidates=frame.candidates.advance(2))
            frame=_movement_move(state,frame,'unit',value,16)
            if frame.status&8:
                break
            frame=_movement_compare(state,frame,low16(frame.unit),low16(frame.target_x),16)
            if frame.status&4:
                frame=_movement_move(state,frame,'target_y',low16(frame.unit),16)
                break
    frame=_economy_register_bit_fields(state,frame,'target_y',14,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,low16(frame.target_y))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3A6,low16(frame.target_y))


def lowbank_coordinate_live_state_109_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FE06: debit two balances, append a variable record and compact tagged member words."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF39E,4))
    frame=_economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,32,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE09C).cursor())
    frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF3BA,4))
    frame=_economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,32,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFF9000).cursor())
    while True:
        frame=_movement_move(state,frame,'target_x',0,16)
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
        if frame.status&4:
            break
        frame=_economy_logic_fields(state,frame,'target_x',15)
        frame=_economy_delta_fields(state,frame,'target_x',13)
        frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_movement_move(state,frame,'target_x',state.read(0x00FF382A,2),16)
    frame=_economy_logic_fields(state,frame,'target_x',96,16,'or')
    frame=_lowbank_ui_append_fields(state,frame,low8(frame.target_x),1)
    for address in (0x00FF3828,0x00FF3829,0xFFFFF673,0xFFFFF62E,0xFFFFF39E,0xFFFFF39F,
            0xFFFFF3A0,0xFFFFF3A1,0xFFFFF3BA,0xFFFFF3BB,0xFFFFF3BC,0xFFFFF3BD):
        frame=_lowbank_ui_append_fields(state,frame,state.read(address,1),1)
    frame=_lowbank_ui_call_fields(state,frame,0xFF1A,0xFE7E)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF500).cursor(),scan=state.table_at(0xFFFFCC00).cursor())
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'target_x',value,16)
        frame=_movement_compare(state,frame,low16(frame.target_x),16384,16)
        if not frame.status&1:
            break
    frame=first_replace(frame,candidates=frame.candidates.advance(-2),controller=state.table_at(frame.candidates.base-2))
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low16(frame.target_y),16384,16)
        if frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,low16(frame.target_y))
            frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+2)))
        else:
            frame=_lowbank_ui_append_fields(state,frame,low8(frame.target_y),1)
            frame=_economy_logic_fields(state,frame,'target_y',255)
            frame=_economy_memory_logic_fields(state,frame,u32(frame.scan.base+s16(low16(frame.target_y))),64)
    frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,65535)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,1,True)
    frame=first_replace(frame,roster=state.table_at(0x00FF3000).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0x00FF3826,2))),candidates=state.table_at(0x00FF3800).cursor())
    frame=_lowbank_ui_append_fields(state,frame,0,1,True)
    frame=_lowbank_ui_append_fields(state,frame,low8(frame.target_x),1)
    frame=_lowbank_ui_append_fields(state,frame,state.read(0xFFFFF673,1),1)
    frame=_movement_move(state,frame,'target_y',3,16)
    while True:
        frame=_economy_delta_fields(state,frame,'target_y',1)
        value=frame.candidates.byte()
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=_lowbank_ui_append_fields(state,frame,value,1)
        if frame.status&4:
            break
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,255,1)
    frame=_economy_memory_delta_fields(state,frame,0x00FF3826,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF500,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF630,2),16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
        frame=_lowbank_ui_call_fields(state,frame,0xE1F6,0xFEF4)
    for address,value in ((0x00FF7026,5),(0xFFFFF612,520),(0xFFFFF362,41)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    frame=_movement_move(state,frame,'target_x',108,16)
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0xFF12)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF652,1)


def lowbank_select_live_state_34_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FF58: append the updated record header and its zero-terminated member bytes."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_economy_memory_logic_fields(state,frame,frame.roster.base,80)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(0,3),8)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(0,13),8)
    frame=first_replace(frame,candidates=state.table_at(0x00FF3800).cursor(),controller=state.table_at(0x00FF3000))
    frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+s16(state.read(0x00FF3826,2)))))
    for value,clear in ((0,True),(low8(frame.target_x),False),(low8(frame.target_y),False)):
        frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,value,1,clear)
        frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+1)))
    frame=_movement_move(state,frame,'unit',3,16)
    while True:
        frame=_economy_delta_fields(state,frame,'unit',1)
        value=frame.candidates.byte()
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
        frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,value,1)
        frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+1)))
        if frame.status&4:
            break
    frame=_economy_memory_delta_fields(state,frame,0x00FF3826,low16(frame.unit))
    frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,255,1)
    return first_replace(frame,controller=state.table_at(u32(frame.controller.base+1)))


def lowbank_process_counted_records_37_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """FF98: split roster types, shift following variable records, then distribute balances."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,candidates=state.table_at(state.read(0x00FF382C,4)+13).cursor(),
        roster=state.table_at(0xFFFFF500).cursor(),controller=state.table_at(0x00FF398A),scan=state.table_at(0x00FF399E).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low16(frame.target_y),16384,16)
        if frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.target_y),1)
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
            frame=_lowbank_ui_store_fields(state,frame,frame.scan.base,low16(frame.target_y))
            frame=first_replace(frame,scan=frame.scan.advance(2))
        else:
            frame=_economy_logic_fields(state,frame,'target_y',255)
            frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,low16(frame.target_y))
            frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+2)))
            frame=_economy_delta_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,65535)
    frame=_lowbank_ui_store_fields(state,frame,frame.scan.base,65535)
    frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(),8)
    frame=_economy_logic_fields(state,frame,'target_y',15)
    frame=_economy_delta_fields(state,frame,'target_y',low8(frame.target_x),8,True)
    frame=_economy_logic_fields(state,frame,'target_y',16,8,'or')
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,low8(frame.target_y),1)
    frame=_lowbank_ui_call_fields(state,frame,0x10044,0xFFEE)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+3),low8(frame.unit),1)
    frame=first_replace(frame,controller=state.table_at(u32(frame.candidates.base+s16(low16(frame.target_x)))))
    while True:
        frame=_movement_move(state,frame,'target_y',frame.controller.byte(),8)
        if frame.status&4:
            break
        frame=_economy_logic_fields(state,frame,'target_y',15)
        frame=_economy_delta_fields(state,frame,'target_y',12)
        while True:
            value=frame.controller.byte()
            frame=first_replace(frame,controller=state.table_at(u32(frame.controller.base+1)))
            frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,value,1)
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
            frame=_lowbank_ui_counter_fields(frame,'target_y')
            if low16(frame.target_y)==65535:
                break
    frame=_economy_logic_fields(state,frame,'target_x',16,16,'or')
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.target_x),1)
    frame=first_replace(frame,candidates=frame.candidates.advance(1),roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x1006C,0x1001A)
    for name in ('target_y','unit'):
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.carrier(name)),1)
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_lowbank_ui_call_fields(state,frame,0x101F8,0x10022)
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.unit),1)
    frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,frame.roster.byte(0,4),1)
    frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_lowbank_ui_call_fields(state,frame,0x100DA,0x1002C)
    frame=first_replace(frame,roster=state.table_at(0x00FF398A).cursor())
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',value,16)
        if frame.status&8:
            break
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,low8(frame.target_x),1)
        frame=first_replace(frame,candidates=frame.candidates.advance(1))
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,0,1,True)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,6,True)


def lowbank_coordinate_live_state_111_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1CCBE,0x1022A)


def lowbank_coordinate_live_state_112_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1B246,0x10232)





# Lowbank54 accounts and allocation: one live algorithm per whole, with explicit entry aliases.
from .services import (first_replace, _movement_frame, _movement_move, _movement_move_long, _movement_compare, _movement_test, _first_compare_long, FirstDeploymentReturnBoundary, MovementContinuationBoundary)

"""City allegiance, account expenditure and the original loan-result policies.

The neutral Frame names are the actual D0..D7/A0..A7 carriers. Narrow
operations retain the unmodified upper bits; views always belong to one Scene.
"""

def _campaign_memory_bit_change_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int) -> FirstDeploymentFrame:
    value=state.read(address,1)
    frame=_lowbank_ui_bit_fields(state,frame,value,bit)
    state.write(address,1,value^(1<<(bit&7)))
    return frame


def _campaign_register_set_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, bit: int) -> FirstDeploymentFrame:
    value=frame.carrier(name)
    frame=_lowbank_ui_bit_fields(state,frame,value,bit&31)
    return first_replace(frame,**{name:value|(1<<(bit&31))})


def lowbank_select_live_state_32_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """DE1C: repeat-delay and two-direction selector; original wrap back is retained."""
    frame=_movement_frame(state,frame)
    while True:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
        frame=_economy_logic_fields(state,frame,'target_x',15)
        if frame.status&4:
            return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
        if not frame.status&4:
            return frame
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,0)
        if not frame.status&4:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFAFFD,1),0)
            if frame.status&4:
                return _campaign_memory_bit_change_fields(state,frame,0xFFFFAFF9,0)
            frame=_economy_memory_delta_fields(state,frame,0xFFFFAFFA,1,16,True)
            if not frame.status&1:
                return frame
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFAFFA,2)
            continue
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
        if frame.status&4:
            return _campaign_memory_bit_change_fields(state,frame,0xFFFFAFFD,0)
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFAFFD,1),0)
        if frame.status&4:
            return _campaign_memory_bit_change_fields(state,frame,0xFFFFAFF9,0)
        frame=_economy_memory_delta_fields(state,frame,0xFFFFAFFA,1)
        frame=_movement_compare(state,frame,state.read(0xFFFFAFFA,2),2,16)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFAFFA,0,2,True)
        return frame


def lowbank_coordinate_live_state_103_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E134: pay the defection cost, move allegiance, and replace a departing leader."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3AE,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'unit',frame.roster.long(low16(frame.target_y)))
    frame=_economy_delta_fields(state,frame,'unit',state.read(0xFFFFF39E,4),32,True)
    if frame.status&1:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),frame.unit,4)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low8(frame.target_y),1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),1,1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE45C).cursor())
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=_economy_memory_delta_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_y))),1,32)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3AE,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=_economy_memory_delta_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_y))),1,32,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3AE,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF3A6,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF630,65535)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3AE,2),16)
        frame=_lowbank_ui_call_fields(state,frame,0x5F48,0xE1A0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3AE,2),16)
        frame=_lowbank_ui_call_fields(state,frame,0xE1F6,0xE1A8)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF3A6,2),16)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
            frame=_movement_fixed_shift_word(state,frame,'target_x',1)
            frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low16(frame.target_y))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,state.read(0xFFFFF38A,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
    frame=_movement_move(state,frame,'target_x',14,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0xE1E6)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF652,1)
    return _lowbank_ui_store_fields(state,frame,0x00FF7026,26)


def lowbank_update_live_fields_9_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E3F8 is the actual empty RTS."""
    return _movement_frame(state,frame)


def lowbank_coordinate_live_state_104_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E440 chooses the three actual status actions, preserving each BSR slot."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF57B,1),8)
    frame=_movement_compare(state,frame,low8(frame.target_x),41,8)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xE462,0xE44E)
    frame=_movement_compare(state,frame,low8(frame.target_x),125,8)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xE4A4,0xE45A)
    return _lowbank_ui_call_fields(state,frame,0xE510,0xE460)


def _campaign_officer_notice_fields(state: SceneState, frame: FirstDeploymentFrame,
        notice: int) -> FirstDeploymentFrame:
    """Shared contiguous store sequence, not a replacement for any child call."""
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,40)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3FE,notice)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF774,1)
    return _lowbank_ui_store_fields(state,frame,0x00FF7026,20)


def lowbank_update_record_flags_12_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),128,16)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF3A6,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_campaign_officer_notice_fields(state,frame,22)
    return frame


def lowbank_select_live_state_33_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),130,16)
    if frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    address=u32(frame.roster.base+s16(low16(frame.target_x)))
    frame=_lowbank_ui_bit_fields(state,frame,state.read(address,1),4)
    if frame.status&4:
        frame=_economy_memory_logic_fields(state,frame,address,16)
        frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,20)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,40)
        frame=_movement_move(state,frame,'target_x',24,16)
    else:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,31)
        frame=_movement_move(state,frame,'target_x',173,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3FE,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF774,1)


def lowbank_update_record_flags_12_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E510 is a genuine alternate entry; no fabricated E462 call is inserted."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),132,16)
    if frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3B4,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF580).cursor())
    frame=_movement_move(state,frame,'unit',5,8)
    frame=_economy_delta_fields(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_movement_move(state,frame,'count',frame.roster.byte(low16(frame.target_x)),8)
    frame=_economy_logic_fields(state,frame,'count',16)
    frame=_economy_logic_fields(state,frame,'count',low16(frame.unit),16,'or')
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFC000).cursor())
    frame=_movement_move(state,frame,'distance',frame.candidates.word(low16(frame.unit)),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFBE00).cursor())
    frame=_movement_compare(state,frame,low16(frame.distance),frame.candidates.word(low16(frame.unit)),16)
    if frame.status&1:
        frame=_campaign_register_set_bit_fields(state,frame,'count',3)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low8(frame.count),1)
    return _campaign_officer_notice_fields(state,frame,23)


def lowbank_coordinate_live_state_105_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xE7B0,0xE794)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,40)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3FE,27)
    return _lowbank_ui_store_fields(state,frame,0x00FF7026,10)


def _campaign_gain_loyalty_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
    frame=_economy_delta_fields(state,frame,name,frame.roster.word(low16(frame.target_y)))
    frame=_movement_compare(state,frame,low16(frame.carrier(name)),999,16)
    if not frame.status&5:
        frame=_movement_move(state,frame,name,999,16)
    return _lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.carrier(name)))


def lowbank_calculate_live_quotient_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """E8E6: expenditure effectiveness and its success/failure loyalty consequences."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word, _movement_divu_word
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF57B,1),56,8)
    if frame.status&4:
        return _lowbank_ui_known_child_fields(state,frame,0xEA38)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF39E,4))
    frame=_economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,32,True)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE09C).cursor())
    frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF3BA,4))
    frame=_economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,32,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A0,2),16)
    frame=_economy_delta_fields(state,frame,'target_x',state.read(0xFFFFE774,2))
    frame=_movement_move_long(state,frame,'target_y',0)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFEFD2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'unit',2)
    frame=first_replace(frame,roster=state.table_at(0xDF62).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.unit)),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF61C,2),16)
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_economy_delta_fields(state,frame,'target_y',frame.roster.word(low16(frame.unit),2))
    frame=_movement_multiply_word(state,frame,'target_x',low16(frame.target_y))
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.unit)),8)
    frame=_movement_move(state,frame,'target_y',120,16)
    frame=_economy_delta_fields(state,frame,'target_y',low16(frame.count),16,True)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=_economy_delta_fields(state,frame,'target_y',low16(frame.unit))
    frame=_movement_fixed_shift_word(state,frame,'target_y',3)
    frame=_economy_delta_fields(state,frame,'target_y',low16(frame.unit))
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=_movement_divu_word(state,frame,'target_x',low16(frame.target_y),0xE95C)
    frame=_movement_compare(state,frame,low16(frame.target_x),10,16)
    if not frame.status&1:
        frame=_lowbank_ui_call_fields(state,frame,0xEC16,0xE968)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3FE,39)
        frame=_lowbank_ui_call_fields(state,frame,0x83D4,0xE974)
        frame=_movement_move_long(state,frame,'target_x',0)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
        frame=_movement_move_long(state,frame,'target_y',frame.target_x)
        frame=_economy_long_shift_fields(state,frame,'target_x',1)
        frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
        frame=_economy_long_shift_fields(state,frame,'target_x',1)
        frame=_economy_swap_fields(state,frame,'target_x')
        frame=_economy_delta_fields(state,frame,'target_x',5)
        frame=_campaign_gain_loyalty_fields(state,frame,'target_x')
    else:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3FE,41)
        frame=_lowbank_ui_call_fields(state,frame,0x83D4,0xE9C4)
        frame=_movement_move_long(state,frame,'unit',0)
        frame=_movement_move(state,frame,'unit',state.read(0xFFFFF61C,2),16)
        frame=_movement_move_long(state,frame,'target_y',frame.unit)
        frame=_economy_long_shift_fields(state,frame,'unit',1)
        frame=_economy_delta_fields(state,frame,'unit',frame.target_y,32)
        frame=_economy_swap_fields(state,frame,'unit')
        frame=_economy_delta_fields(state,frame,'unit',1)
        frame=_lowbank_ui_call_fields(state,frame,0x83D4,0xE9DA)
        frame=_economy_logic_fields(state,frame,'target_x',65535,32)
        frame=_movement_move_long(state,frame,'target_y',frame.target_x)
        frame=_economy_long_shift_fields(state,frame,'target_x',1)
        frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
        frame=_economy_swap_fields(state,frame,'target_x')
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
        frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_y)),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
        address=u32(frame.roster.base+s16(low16(frame.target_y)))
        frame=_economy_memory_delta_fields(state,frame,address,low8(frame.target_x),8,True)
        if frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,address,0,1,True)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
        frame=_economy_delta_fields(state,frame,'unit',frame.roster.word(low16(frame.target_y)))
        frame=_movement_compare(state,frame,low16(frame.unit),999,16)
        if not frame.status&5:
            frame=_movement_move(state,frame,'unit',999,16)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.unit))
    frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,14)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF38A,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,40)
    return _lowbank_ui_known_child_fields(state,frame,0xEC0E)


def lowbank_scale_live_record_value_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """EC62: original split-WORD products, signed division and capped debt proceeds."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),106,16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF576,2),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFF578).cursor())
        frame=_movement_compare(state,frame,frame.roster.byte(low16(frame.target_x),-2),63,8)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF38A,520)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE9F8).cursor())
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+1),state.read(0xFFFFF393,1),1)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))+2),state.read(0xFFFFF374,2))
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
        frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
        frame=_economy_delta_fields(state,frame,'target_y',state.read(0xFFFFF39E,4),32)
        frame=_economy_compare_long_fields(state,frame,frame.target_y,999999)
        if not frame.status&5:
            frame=_movement_move_long(state,frame,'target_y',999999)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,4)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE65C).cursor())
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF39E,4),4)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_movement_move(state,frame,'target_x',49,16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF646,state.read(0xFFFFF392,2))
        return _lowbank_ui_call_fields(state,frame,0x676F2,0xEDA2)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF460).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',frame.candidates.byte(low16(frame.target_y)),8)
    frame=_movement_move(state,frame,'unit',u16(s8(low8(frame.unit))),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
    frame=_movement_move(state,frame,'count',low16(frame.target_y),16)
    frame=_movement_multiply_word(state,frame,'count',low16(frame.unit))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.unit))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_economy_delta_fields(state,frame,'target_y',frame.count,32)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_movement_move_long(state,frame,'unit',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=_economy_delta_fields(state,frame,'target_x',frame.unit,32)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_economy_delta_fields(state,frame,'target_x',7)
    frame=_movement_move(state,frame,'unit',low16(frame.target_y),16)
    frame=_movement_multiply_word(state,frame,'unit',low16(frame.target_x))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_movement_multiply_word(state,frame,'target_y',low16(frame.target_x))
    frame=_economy_swap_fields(state,frame,'target_y')
    frame=_economy_delta_fields(state,frame,'target_y',frame.unit,32)
    frame=_movement_move_long(state,frame,'target_x',state.read(0xFFFFF39E,4))
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_movement_multiply_word(state,frame,'unit',200)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_movement_multiply_word(state,frame,'target_x',200)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_economy_delta_fields(state,frame,'unit',frame.target_x,32)
    frame=_lowbank_ui_call_fields(state,frame,0x35760,0xECD2)
    frame=_movement_compare(state,frame,low16(frame.target_y),10,16)
    if frame.status&1:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF740,46)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFE700,2),16)
        frame=_campaign_register_set_bit_fields(state,frame,'target_y',frame.target_x)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFE700,low16(frame.target_y))
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE9F8).cursor())
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF393,1),1)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor())
        frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
        frame=_economy_delta_fields(state,frame,'target_y',state.read(0xFFFFF39E,4),32,True)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),frame.target_y,4)
        frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,16)
        frame=_lowbank_ui_call_fields(state,frame,0x1072C,0xED14)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF740,47)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,33)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF740,2),16)
    return _lowbank_ui_call_fields(state,frame,0x676F2,0xEDD2)


def lowbank_update_live_fields_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _movement_frame(state,frame)


def lowbank_coordinate_live_state_107_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),1,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF57A,1),8)
    frame=_movement_compare(state,frame,low8(frame.target_x),92,8)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0xEE16,0xEDF2)
        return _lowbank_ui_store_fields(state,frame,0x00FF7026,0,2,True)
    frame=_movement_compare(state,frame,low8(frame.target_x),97,8)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xF018,0xEE04)
    return _lowbank_ui_call_fields(state,frame,0xF778,0xEE0A)


"""Conditional-descendant roster partition, counted compaction and asset split.

All 830 CODE bytes have original encoded rows in secondary_dispatch_descendants.s.
The negative list sentinel and DBRA WORD wrap are part of the original contract.
"""

def _campaign_counted_record_copy_fields(state: SceneState, frame: FirstDeploymentFrame,
        source_name: str, destination_name: str) -> FirstDeploymentFrame:
    """Copy repeated 13+low-nibble BYTE records; callers own the live cursors."""
    while True:
        source=getattr(frame,source_name)
        frame=_movement_move(state,frame,'target_x',source.byte(),8)
        frame=_economy_logic_fields(state,frame,'target_x',15)
        if frame.status&4:
            break
        frame=_economy_delta_fields(state,frame,'target_x',12)
        while True:
            source=getattr(frame,source_name)
            destination=getattr(frame,destination_name)
            value=source.byte()
            frame=_lowbank_ui_store_fields(state,frame,destination.base,value,1)
            frame=first_replace(frame,**{source_name:source.advance(1),destination_name:destination.advance(1)})
            remaining=u16(low16(frame.target_x)-1)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,remaining))
            if remaining==65535:
                break
    return _lowbank_ui_store_fields(state,frame,getattr(frame,destination_name).base,0,1,True)


def lowbank_process_counted_records_38_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """103EA: partition officer/embedded member lists, compact records, settle assets."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor(),candidates=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=first_replace(frame,controller=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.controller.byte(low16(frame.target_x)),8)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,controller=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'unit',frame.controller.word(low16(frame.target_y)),16)
    frame=first_replace(frame,controller=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'count',frame.controller.byte(),8)
    frame=_economy_logic_fields(state,frame,'count',15)
    frame=first_replace(frame,scan=frame.controller.advance(13+s16(low16(frame.count))),controller=frame.controller.advance(13))
    frame=_movement_move(state,frame,'offset_x',0,16)
    frame=_movement_move(state,frame,'offset_y',0,16)
    frame=first_replace(frame,scratch=state.table_at(0x00FF398A).cursor(),auxiliary=state.table_at(0x00FF399E).cursor())
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low16(frame.target_y),0x4000,16)
        if frame.status&1:
            frame=_economy_logic_fields(state,frame,'target_y',255)
            frame=_lowbank_ui_store_fields(state,frame,frame.controller.base,low8(frame.target_y),1)
            frame=first_replace(frame,controller=frame.controller.advance(1))
            frame=_lowbank_ui_store_fields(state,frame,frame.scratch.base,low16(frame.target_y))
            frame=first_replace(frame,scratch=frame.scratch.advance(2))
            frame=_economy_delta_fields(state,frame,'offset_x',1)
        else:
            frame=_economy_logic_fields(state,frame,'target_y',255)
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_y))),low8(frame.target_x),1)
            frame=_lowbank_ui_store_fields(state,frame,frame.auxiliary.base,low16(frame.target_y))
            frame=first_replace(frame,auxiliary=frame.auxiliary.advance(2))
            frame=_economy_delta_fields(state,frame,'offset_y',1)
            frame=_movement_compare(state,frame,low16(frame.target_y),low16(frame.unit),16)
            if frame.status&4:
                frame=first_replace(frame,opponent=state.table_at(0xFFFFF45E).cursor())
                frame=_movement_move(state,frame,'distance',low16(frame.target_x),16)
                frame=_movement_fixed_shift_word(state,frame,'distance',1)
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.opponent.base+s16(low16(frame.distance))),low16(frame.unit))
    frame=_lowbank_ui_store_fields(state,frame,frame.scratch.base,65535)
    frame=_lowbank_ui_store_fields(state,frame,frame.auxiliary.base,65535)
    frame=first_replace(frame,opponent=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_lowbank_ui_store_fields(state,frame,frame.opponent.base,low8(frame.offset_x),1)
    frame=_campaign_counted_record_copy_fields(state,frame,'scan','controller')
    frame=_movement_move(state,frame,'target_x',low16(frame.offset_x),16)
    frame=_lowbank_ui_call_fields(state,frame,0x101F8,0x1048E)
    stack=frame.stack_cursor.advance(-2)
    stack.set_word(0,low16(frame.unit))
    frame=first_replace(frame,stack_cursor=stack)
    frame=_lowbank_ui_call_fields(state,frame,0x1058C,0x10494)
    value=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    frame=_movement_move(state,frame,'unit',value,16)
    frame=first_replace(frame,opponent=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.opponent.base+3),low8(frame.unit),1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF630,65535)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFF428).cursor())
    frame=_movement_move(state,frame,'choice',39,16)
    early_notice=False
    while True:
        frame=_movement_move(state,frame,'offset_y',frame.auxiliary.byte(low16(frame.choice)),8)
        frame=_movement_compare(state,frame,low8(frame.offset_y),state.read(0xFFFFF377,1),8)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_x',low16(frame.choice),16)
            frame=_economy_delta_fields(state,frame,'target_x',1)
            frame=_lowbank_ui_call_fields(state,frame,0x5F48,0x104C2)
            frame=_movement_compare(state,frame,low16(frame.count),10,16)
            if frame.status&1:
                early_notice=True
                break
        remaining=u16(low16(frame.choice)-1)
        frame=first_replace(frame,choice=replace_word(frame.choice,remaining))
        if remaining==65535:
            break
    if not early_notice:
        frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
        frame=first_replace(frame,candidates=frame.roster.advance(13))
        frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
        frame=_economy_logic_fields(state,frame,'target_x',15)
        frame=_economy_delta_fields(state,frame,'target_x',1,16,True)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF392,2),16)
        frame=_economy_logic_fields(state,frame,'target_y',128,8,'or')
        frame=_movement_move(state,frame,'unit',0,16)
        frame=first_replace(frame,controller=state.table_at(0xFFFFCC00).cursor())
        while True:
            value=frame.candidates.byte()
            frame=first_replace(frame,candidates=frame.candidates.advance(1))
            frame=_movement_move(state,frame,'unit',value,8)
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.controller.base+s16(low16(frame.unit))),low8(frame.target_y),1)
            remaining=u16(low16(frame.target_x)-1)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,remaining))
            if remaining==65535:
                break
        frame=_campaign_counted_record_copy_fields(state,frame,'candidates','roster')
        while True:
            frame=_movement_move(state,frame,'target_x',state.read(0x00FF398A,2),16)
            if frame.status&8:
                break
            frame=_economy_logic_fields(state,frame,'target_x',255)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,low16(frame.target_x))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF740,155)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,300)
            frame=_lowbank_ui_call_fields(state,frame,0x30A74,0x10536)
            frame=first_replace(frame,roster=state.table_at(0x00FF398A).cursor())
            while True:
                value=frame.roster.word(0,2)
                frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,value)
                frame=first_replace(frame,roster=frame.roster.advance(2))
                if frame.status&8:
                    break
        frame=_movement_move_long(state,frame,'target_x',0xC0000026)
        frame=_movement_move(state,frame,'target_y',7,16)
        frame=_movement_move(state,frame,'unit',0xCA02,16)
        frame=first_replace(frame,roster=state.table_at(0x10570).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0x26BFA,0x1055C)
        value=state.read(0xFFFFF3A4,1)
        frame=_lowbank_ui_bit_fields(state,frame,value,6)
        state.write(0xFFFFF3A4,1,value&191)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,521)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF362,5)


def _campaign_group_asset_column_fields(state: SceneState, frame: FirstDeploymentFrame,
        displacement: int, division_pc: int, target: int, first_column: bool) -> FirstDeploymentFrame:
    """One original four-BYTE asset column; first/second column share the same split."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word, _movement_divu_word
    frame=first_replace(frame,scratch=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'unit',frame.scratch.byte(0,displacement),8)
    frame=_movement_fixed_shift_word(state,frame,'unit',8)
    frame=_movement_move(state,frame,'unit',frame.scratch.byte(0,displacement+1),8)
    frame=_economy_long_shift_fields(state,frame,'unit',8)
    frame=_movement_move(state,frame,'unit',frame.scratch.byte(0,displacement+2),8)
    frame=_economy_long_shift_fields(state,frame,'unit',8)
    frame=_movement_move(state,frame,'unit',frame.scratch.byte(0,displacement+3),8)
    frame=_movement_move_long(state,frame,'count',frame.unit)
    frame=_economy_long_shift_fields(state,frame,'count',8,True)
    frame=_movement_multiply_word(state,frame,'count',low16(frame.target_x))
    frame=_movement_divu_word(state,frame,'count',low16(frame.target_y),division_pc)
    frame=_economy_logic_fields(state,frame,'count',65535,32)
    frame=_economy_long_shift_fields(state,frame,'count',8)
    frame=_economy_delta_fields(state,frame,'unit',frame.count,32,True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.scratch.base+displacement+3),low8(frame.count),1)
    frame=_economy_long_shift_fields(state,frame,'count',8,True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.scratch.base+displacement+2),low8(frame.count),1)
    frame=_economy_long_shift_fields(state,frame,'count',8,True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.scratch.base+displacement+1),low8(frame.count),1)
    frame=_movement_fixed_shift_word(state,frame,'count',8,True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.scratch.base+displacement),low8(frame.count),1)
    if first_column:
        frame=_movement_move(state,frame,'distance',state.read(0xFFFFF364,2),16)
        frame=_movement_fixed_shift_word(state,frame,'distance',2)
    frame=first_replace(frame,auxiliary=state.table_at(target).cursor())
    frame=_movement_move_long(state,frame,'count',frame.auxiliary.long(low16(frame.distance)))
    frame=_economy_delta_fields(state,frame,'count',frame.unit,32)
    frame=_economy_compare_long_fields(state,frame,frame.count,999999)
    if not frame.status&5:
        frame=_movement_move_long(state,frame,'count',999999)
    return _lowbank_ui_store_fields(state,frame,u32(frame.auxiliary.base+s16(low16(frame.distance))),frame.count,4)


def lowbank_calculate_live_quotient_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1058C splits both packed assets by original officer budget weights."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,opponent=state.table_at(0xFFFFC800).cursor(),scratch=state.table_at(0x00FF398A).cursor())
    frame=_movement_move_long(state,frame,'target_x',0)
    while True:
        value=frame.scratch.word()
        frame=first_replace(frame,scratch=frame.scratch.advance(2))
        frame=_movement_move(state,frame,'target_y',value,16)
        if frame.status&8:
            break
        frame=_movement_fixed_shift_word(state,frame,'target_y',2)
        frame=_movement_move_long(state,frame,'target_y',frame.opponent.long(low16(frame.target_y)))
        frame=_economy_long_shift_fields(state,frame,'target_y',5,True)
        frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
        frame=_economy_delta_fields(state,frame,'target_x',100,32)
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=first_replace(frame,auxiliary=state.table_at(0x00FF399E).cursor())
    while True:
        value=frame.auxiliary.word()
        frame=first_replace(frame,auxiliary=frame.auxiliary.advance(2))
        frame=_movement_move(state,frame,'unit',value,16)
        if frame.status&8:
            break
        frame=_movement_fixed_shift_word(state,frame,'unit',2)
        frame=_movement_move_long(state,frame,'unit',frame.opponent.long(low16(frame.unit)))
        frame=_economy_long_shift_fields(state,frame,'unit',5,True)
        frame=_economy_delta_fields(state,frame,'target_y',frame.unit,32)
        frame=_economy_delta_fields(state,frame,'target_y',100,32)
    frame=_campaign_group_asset_column_fields(state,frame,5,0x105EE,0xFFFFDFFC,True)
    return _campaign_group_asset_column_fields(state,frame,9,0x10654,0xFFFFE09C,False)


def lowbank_coordinate_live_state_113_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFEFB0,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low16(frame.target_y))
    frame=first_replace(frame,roster=state.table_at(0xFFFFC300).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),100,1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFA622,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3DA,513)
    frame=_lowbank_ui_call_fields(state,frame,0x106E4,0x106C2)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,524)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,10)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_movement_move(state,frame,'target_x',154,16)
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x106DE)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF65A,0,2,True)


def lowbank_coordinate_live_state_114_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.unit)),8)
    frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(low16(frame.target_y)),8)
    if not frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,6)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF630,65535)
            frame=_lowbank_ui_call_fields(state,frame,0x5F48,0x1070A)
            frame=_lowbank_ui_call_fields(state,frame,0xE1F6,0x1070E)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(low16(frame.target_y)),8)
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,6)
    if frame.status&4:
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_movement_fixed_shift_word(state,frame,'target_x',1)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),low16(frame.target_y))
    return frame


def lowbank_coordinate_live_state_115_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1B59E,0x10A3A)


def lowbank_coordinate_live_state_116_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1B604,0x10A42)


def lowbank_coordinate_live_state_117_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1BFE0,0x10A4A)


"""Three-lane choices, cost editing and original staged confirmation packets.

Text, packet and message children are named live callees; an unbound complete
return keeps its real slot. A zero available-choice mask is not repaired here.
"""

def _campaign_memory_set_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, bit: int, clear: bool=False) -> FirstDeploymentFrame:
    value=state.read(address,1)
    frame=_lowbank_ui_bit_fields(state,frame,value,bit&7)
    mask=1<<(bit&7)
    state.write(address,1,value&u8(~mask) if clear else value|mask)
    return frame


def _campaign_confirmation_fields(state: SceneState, frame: FirstDeploymentFrame,
        command: int, layout: bool=True) -> FirstDeploymentFrame:
    if layout:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,command)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)


def lowbank_update_record_flags_16_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11F1C: publish three selected lane costs and the actual WORD packet."""
    from .services import _movement_fixed_shift_word
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x11F82,0x11F20)
    frame=first_replace(frame,roster=state.table_at(0xD2CA).cursor())
    for selector,displacement,destination in ((0xFFFFEF64,0,0xFFFFEF6A),(0xFFFFEF66,12,0xFFFFEF6E),(0xFFFFEF68,24,0xFFFFEF72)):
        frame=_movement_move(state,frame,'target_x',state.read(selector,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=_lowbank_ui_store_fields(state,frame,destination,frame.roster.long(low16(frame.target_x),displacement),4)
    frame=_movement_move_long(state,frame,'target_x',0xC000000E)
    frame=_movement_move(state,frame,'target_y',10,16)
    frame=_movement_move(state,frame,'unit',0xC3B2,16)
    frame=first_replace(frame,roster=state.table_at(0xD2EE).cursor())
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF692,0xC386)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFEF76,0xC0A1)
    frame=_lowbank_ui_call_fields(state,frame,0x26BFA,0x11F70)
    frame=_campaign_memory_set_bit_fields(state,frame,0xFFFFF3A4,0)
    frame=_lowbank_ui_call_fields(state,frame,0x12008,0x11F7A)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF600,240)


def lowbank_coordinate_live_state_125_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1210C,0x12106)
    return _lowbank_ui_call_fields(state,frame,0x1221C,0x1210A)


def lowbank_coordinate_live_state_126_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1210C: horizontal lane then vertical eligible choice, followed by confirm/cancel."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',3)
    if not frame.status&4:
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,16)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
            if frame.status&4:
                frame=_economy_memory_delta_fields(state,frame,0xFFFFF3F0,1,16,True)
                if frame.status&8:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F0,2)
            else:
                frame=_economy_memory_delta_fields(state,frame,0xFFFFF3F0,1)
                frame=_movement_compare(state,frame,state.read(0xFFFFF3F0,2),3,16)
                if not frame.status&1:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F0,0,2,True)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_economy_logic_fields(state,frame,'target_x',12)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        else:
            frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
            if frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
                frame=first_replace(frame,roster=state.table_at(0xFFFFEF64).cursor(),candidates=state.table_at(0xFFFFEFB2).cursor())
                frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3F0,2),16)
                frame=_movement_fixed_shift_word(state,frame,'target_y',1)
                frame=_movement_move(state,frame,'unit',frame.roster.word(low16(frame.target_y)),16)
                frame=_movement_move(state,frame,'count',frame.candidates.word(low16(frame.target_y)),16)
                frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
                increase=not bool(frame.status&4)
                while True:
                    frame=_economy_delta_fields(state,frame,'unit',1,16,not increase)
                    if increase:
                        frame=_movement_compare(state,frame,low16(frame.unit),3,16)
                        if not frame.status&1:
                            frame=_movement_move(state,frame,'unit',0,16)
                    elif frame.status&1:
                        frame=_movement_move(state,frame,'unit',2,16)
                    frame=_lowbank_ui_bit_fields(state,frame,frame.count,frame.unit&31)
                    if not frame.status&4:
                        break
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.unit))
                return _lowbank_ui_call_fields(state,frame,0x11F1C,0x121B4)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F0,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFEF6A).cursor())
        frame=_movement_move_long(state,frame,'target_x',frame.roster.long(low16(frame.target_x)))
        frame=_economy_compare_long_fields(state,frame,frame.target_x,state.read(0xFFFFF3F8,4))
        if not frame.status&5:
            return frame
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
        frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x121E4)
        frame=_campaign_confirmation_fields(state,frame,3)
        return _lowbank_ui_call_fields(state,frame,0x12292,0x121FA)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_campaign_confirmation_fields(state,frame,2)
        frame=_lowbank_ui_call_fields(state,frame,0x12292,0x1221A)
    return frame


def lowbank_update_record_flags_17_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """125D8 appends all original rows before its still-partial highbank control call."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
    frame=_lowbank_ui_call_fields(state,frame,0x12602,0x125E2)
    frame=_lowbank_ui_call_fields(state,frame,0x12620,0x125E4)
    frame=_lowbank_ui_call_fields(state,frame,0x1268C,0x125E8)
    frame=_lowbank_ui_call_fields(state,frame,0x126D2,0x125EC)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_economy_memory_delta_fields(state,frame,0xFFFFF31A,140)
    frame=_campaign_memory_set_bit_fields(state,frame,0xFFFFF3A4,0)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x12600)


def lowbank_coordinate_live_state_127_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x12F44,0x12EF6)
    frame=_lowbank_ui_call_fields(state,frame,0x12980,0x12EFA)
    frame=_lowbank_ui_call_fields(state,frame,0x12F58,0x12EFE)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,state.read(0xFFFFF3F4,4),4)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,4)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,10)
        return _lowbank_ui_call_fields(state,frame,0x12F44,0x12F22)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_campaign_confirmation_fields(state,frame,2)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,0,4,True)
    return frame


def _campaign_cost_row_prefix_fields(state: SceneState, frame: FirstDeploymentFrame,
        tile: int) -> FirstDeploymentFrame:
    frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,6)
    frame=first_replace(frame,roster=frame.roster.advance(2))
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,tile)
    frame=first_replace(frame,roster=frame.roster.advance(2))
    return _lowbank_ui_known_child_fields(state,frame,0x1293C)


def lowbank_select_live_state_37_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _campaign_cost_row_prefix_fields(state,_movement_frame(state,frame),0xC53E)


def lowbank_update_record_flags_18_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13020,0x12F92)
    frame=_lowbank_ui_call_fields(state,frame,0x12980,0x12F96)
    frame=_lowbank_ui_call_fields(state,frame,0x13034,0x12F9A)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    cancel=False
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,state.read(0xFFFFF3F4,4),4)
        frame=_movement_move_long(state,frame,'target_y',state.read(0xFFFFF3BA,4))
        frame=_economy_logic_fields(state,frame,'target_y',state.read(0xFFFFF39E,4),32,'or')
        if not frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF362,4)
        cancel=True
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        cancel=not bool(frame.status&4)
    if cancel:
        frame=_campaign_confirmation_fields(state,frame,2)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
        frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_x)))
        frame=_movement_move(state,frame,'target_y',1,16)
        frame=_movement_move(state,frame,'unit',0,16)
        frame=first_replace(frame,auxiliary=state.table_at(0xFFFFEF00).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0x1270A,0x12FF8)
        frame=_movement_move_long(state,frame,'target_x',state.read(0xFFFFF39E,4))
        frame=_movement_move(state,frame,'target_y',1,16)
        frame=_movement_move(state,frame,'unit',0,16)
        frame=first_replace(frame,auxiliary=state.table_at(0xFFFFEF0C).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0x1270A,0x1300C)
        frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
        frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)
        frame=_campaign_memory_set_bit_fields(state,frame,0xFFFFF3A5,6,True)
    return frame


def lowbank_select_live_state_38_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _campaign_cost_row_prefix_fields(state,_movement_frame(state,frame),0xC6BE)


def lowbank_calculate_live_quotient_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """132AE: decimal denomination editing and the original cost/loyalty commit."""
    from .services import _movement_fixed_shift_word, _movement_divu_word
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13510,0x132B2)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',12)
    reset_delay=False
    if not frame.status&4:
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
            increase=not bool(frame.status&4)
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF39A,2),16)
            frame=_economy_delta_fields(state,frame,'target_x',1,16,not increase)
            if increase:
                frame=_movement_compare(state,frame,low16(frame.target_x),3,16)
                reset_delay=not bool(frame.status&5)
            else:
                reset_delay=bool(frame.status&8)
                if not reset_delay:
                    frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3EC,2),16)
                    reset_delay=bool(frame.status&1)
            if not reset_delay:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,low16(frame.target_x))
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
        frame=_economy_logic_fields(state,frame,'target_x',3)
        if frame.status&4:
            reset_delay=True
        else:
            frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
            if frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
                frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
                subtract=not bool(frame.status&4)
                frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF39A,2),16)
                if not subtract:
                    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
                    frame=first_replace(frame,roster=state.table_at(0xFFFFEF00).cursor())
                    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
                    frame=first_replace(frame,roster=state.table_at(0x1342C).cursor())
                    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
                    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
                    frame=_economy_delta_fields(state,frame,'target_y',state.read(0xFFFFF39E,4),32)
                    frame=_economy_compare_long_fields(state,frame,frame.target_y,state.read(0xFFFFF3E8,4))
                    reset_delay=not bool(frame.status&5)
                    if not reset_delay:
                        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,frame.target_y,4)
                        frame=first_replace(frame,roster=state.table_at(0x1344C).cursor())
                        frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
                        frame=_economy_memory_delta_fields(state,frame,0xFFFFF3E4,frame.target_y,32)
                else:
                    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
                    frame=first_replace(frame,roster=state.table_at(0x1342C).cursor())
                    frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
                    frame=_movement_move_long(state,frame,'unit',state.read(0xFFFFF39E,4))
                    frame=_economy_delta_fields(state,frame,'unit',frame.target_y,32,True)
                    reset_delay=bool(frame.status&1)
                    if not reset_delay:
                        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,frame.unit,4)
                        frame=first_replace(frame,roster=state.table_at(0x1344C).cursor())
                        frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
                        frame=_economy_memory_delta_fields(state,frame,0xFFFFF3E4,frame.target_y,32,True)
                if not reset_delay:
                    frame=_lowbank_ui_call_fields(state,frame,0x13270,0x13390)
    if reset_delay:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,5)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE774).cursor())
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFCE,state.read(0xFFFFF3E4,4),4)
        frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF3E4,frame.target_y,32)
        frame=_economy_compare_long_fields(state,frame,state.read(0xFFFFF3E4,4),999999)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3E4,999999,4)
        frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x133D2)
        frame=_campaign_confirmation_fields(state,frame,3,False)
        frame=_movement_move_long(state,frame,'target_x',state.read(0xFFFFCFCE,4))
        frame=_economy_delta_fields(state,frame,'target_x',500,32)
        frame=_movement_divu_word(state,frame,'target_x',1000,0x133E8)
        frame=_economy_logic_fields(state,frame,'target_x',65535,32)
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF392,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE13C).cursor())
        frame=_economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),frame.target_x,32,True)
        frame=_lowbank_ui_store_fields(state,frame,0x00FF7026,21)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,192)
        return _lowbank_ui_call_fields(state,frame,0x1347C,0x13412)
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,4)
    if not frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x1353E,0x1341E)
        frame=_campaign_confirmation_fields(state,frame,2,False)
    return frame


def lowbank_coordinate_live_state_128_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x5C98,0x13482)
    for command,count,tile,source,continuation in ((0xC000000B,6,0xC09C,0x134CC,0x1349A),(0xC000000F,7,0xC494,0x134E4,0x134B2),(0xC000000D,4,0xC0B4,0x13500,0x134CA)):
        frame=_movement_move_long(state,frame,'target_x',command)
        frame=_movement_move(state,frame,'target_y',count,16)
        frame=_movement_move(state,frame,'unit',tile,16)
        frame=first_replace(frame,roster=state.table_at(source).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0x26BFA,continuation)
    return frame


def _campaign_selected_troop_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',2)
    return first_replace(frame,roster=state.table_at(0xFFFFC800).cursor())


def lowbank_scale_live_record_value_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1379A: denomination changes and reversible troop-fund transfer; no input repair."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',12)
    process_confirmation=False
    if not frame.status&4:
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
            increase=not bool(frame.status&4)
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF39A,2),16)
            frame=_economy_delta_fields(state,frame,'target_y',1,16,not increase)
            if increase:
                frame=_movement_compare(state,frame,low16(frame.target_y),6,16)
                if frame.status&1:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,low16(frame.target_y))
                else:
                    process_confirmation=True
            else:
                frame=_movement_fixed_shift_word(state,frame,'target_y',1)
                frame=first_replace(frame,roster=state.table_at(0xFFFFEF0C).cursor())
                frame=_movement_compare(state,frame,frame.roster.word(low16(frame.target_y)),0xC001,16)
                blocked=False
                if frame.status&4:
                    frame=first_replace(frame,roster=state.table_at(0xFFFFEF00).cursor())
                    frame=_movement_test(state,frame,frame.roster.word(low16(frame.target_y)),16)
                    blocked=bool(frame.status&4)
                if blocked:
                    process_confirmation=True
                else:
                    frame=_economy_memory_delta_fields(state,frame,0xFFFFF39A,1,16,True)
    else:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
        frame=_economy_logic_fields(state,frame,'target_x',3)
        if frame.status&4:
            process_confirmation=True
        else:
            frame=_economy_memory_delta_fields(state,frame,0xFFFFF608,1,16,True)
            if frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,12)
                frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
                subtract=not bool(frame.status&4)
                frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF39A,2),16)
                frame=_movement_fixed_shift_word(state,frame,'target_x',1)
                frame=_movement_fixed_shift_word(state,frame,'target_x',1)
                frame=first_replace(frame,roster=state.table_at(0x1344C).cursor())
                frame=_movement_move_long(state,frame,'target_y',frame.roster.long(low16(frame.target_x)))
                if not subtract:
                    frame=_movement_move_long(state,frame,'unit',state.read(0xFFFFCFAE,4))
                    frame=_economy_delta_fields(state,frame,'unit',frame.target_y,32,True)
                    process_confirmation=bool(frame.status&1)
                    if not process_confirmation:
                        frame=_movement_move(state,frame,'distance',state.read(0xFFFFF378,2),16)
                        frame=first_replace(frame,candidates=state.table_at(0xFFFFF4FE).cursor())
                        frame=_movement_fixed_shift_word(state,frame,'distance',1)
                        frame=_movement_move(state,frame,'distance',frame.candidates.word(low16(frame.distance)),16)
                        frame=_movement_fixed_shift_word(state,frame,'distance',1)
                        frame=first_replace(frame,candidates=state.table_at(0xFFFFB800).cursor())
                        frame=_movement_move(state,frame,'distance',frame.candidates.word(low16(frame.distance)),16)
                        frame=_movement_multiply_word(state,frame,'distance',100)
                        frame=_movement_move_long(state,frame,'count',state.read(0xFFFFF3EE,4))
                        frame=_economy_delta_fields(state,frame,'count',frame.target_y,32)
                        frame=_economy_compare_long_fields(state,frame,frame.count,frame.distance)
                        process_confirmation=not bool(frame.status&5)
                        if not process_confirmation:
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFAE,frame.unit,4)
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3EE,frame.count,4)
                else:
                    frame=_movement_move_long(state,frame,'unit',state.read(0xFFFFF3EE,4))
                    frame=_economy_delta_fields(state,frame,'unit',frame.target_y,32,True)
                    process_confirmation=bool(frame.status&1)
                    if not process_confirmation:
                        frame=_movement_move_long(state,frame,'count',state.read(0xFFFFCFAE,4))
                        frame=_economy_delta_fields(state,frame,'count',frame.target_y,32)
                        frame=_economy_compare_long_fields(state,frame,frame.count,999999)
                        process_confirmation=not bool(frame.status&5)
                        if not process_confirmation:
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3EE,frame.unit,4)
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFAE,frame.count,4)
                if not process_confirmation:
                    frame=_lowbank_ui_call_fields(state,frame,0x1374A,0x1389E)
    if process_confirmation:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        cancel=not bool(frame.status&4)
        if not cancel:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
            if not frame.status&4:
                frame=_movement_move(state,frame,'target_x',172,16)
                frame=_lowbank_ui_call_fields(state,frame,0x808A,0x138C2)
                frame=_campaign_selected_troop_fields(state,frame)
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF3EE,4),4)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3E4,state.read(0xFFFFCFAE,4),4)
                frame=_campaign_confirmation_fields(state,frame,2)
        else:
            frame=_campaign_selected_troop_fields(state,frame)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3EE,frame.roster.long(low16(frame.target_x)),4)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFAE,state.read(0xFFFFF3E4,4),4)
            frame=_campaign_confirmation_fields(state,frame,2)
            frame=_lowbank_ui_call_fields(state,frame,0x1374A,0x1392E)
    return _lowbank_ui_call_fields(state,frame,0x136F4,0x13932)


def lowbank_coordinate_live_state_129_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13B86,0x13ABA)
    frame=_lowbank_ui_call_fields(state,frame,0x13BDA,0x13ABE)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    cancel_check=True
    if not frame.status&4:
        frame=_economy_memory_delta_fields(state,frame,0xFFFFCFD2,1,16,True)
        frame=_movement_compare(state,frame,state.read(0xFFFFCFD2,2),8,16)
        if not frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
        if not frame.status&4:
            cancel_check=False
            frame=first_replace(frame,roster=state.table_at(0xFFFFDFFC).cursor(),candidates=state.table_at(0xFFFFE09C).cursor())
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
            frame=_movement_fixed_shift_word(state,frame,'target_x',2)
            frame=_movement_move_long(state,frame,'unit',frame.roster.long(low16(frame.target_x)))
            frame=_movement_move_long(state,frame,'count',frame.candidates.long(low16(frame.target_x)))
            frame=first_replace(frame,controller=state.table_at(0x13B68).cursor())
            frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF688,2),16)
            frame=_movement_fixed_shift_word(state,frame,'target_y',3)
            frame=_movement_move(state,frame,'target_x',189,16)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,frame.controller.long(low16(frame.target_y)),4)
            frame=_economy_compare_long_fields(state,frame,frame.unit,state.read(0xFFFFF39E,4))
            sufficient=not bool(frame.status&1)
            if sufficient:
                frame=_movement_move(state,frame,'target_x',199,16)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,frame.controller.long(low16(frame.target_y),4),4)
                frame=_economy_compare_long_fields(state,frame,frame.count,state.read(0xFFFFF3BA,4))
                sufficient=not bool(frame.status&1)
            if sufficient:
                frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x13B2E)
                frame=_campaign_confirmation_fields(state,frame,3,False)
            else:
                frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x13B44)
    if cancel_check:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
        if not frame.status&4:
            frame=_campaign_confirmation_fields(state,frame,2)
            frame=_lowbank_ui_call_fields(state,frame,0x13C7E,0x13B66)
    return frame


def lowbank_process_counted_records_39_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """13D7A: matched two-column row reveal, then the original map result call."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_compare(state,frame,state.read(0xFFFFF36A,2),9,16)
    if not frame.status&1:
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF362,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,108)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF670,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,2)
        frame=_lowbank_ui_call_fields(state,frame,0x5694,0x13DA0)
        frame=_economy_memory_logic_fields(state,frame,0xFFFFF3A4,0x8C0,16)
    else:
        frame=first_replace(frame,roster=state.table_at(0xFFFFD100).cursor())
        frame=first_replace(frame,roster=frame.roster.advance(s16(state.read(0xFFFFF31A,2))))
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),13)
        frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,13)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
        frame=_movement_fixed_shift_word(state,frame,'target_x',8)
        frame=_movement_move(state,frame,'target_y',0xC934,16)
        frame=_economy_delta_fields(state,frame,'target_y',low16(frame.target_x),16,True)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),low16(frame.target_y))
        frame=_economy_delta_fields(state,frame,'target_y',128,16,True)
        frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_y))
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_movement_move(state,frame,'target_x',12,16)
        while True:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0x8000)
            frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0x8000)
            frame=first_replace(frame,roster=frame.roster.advance(2))
            remaining=u16(low16(frame.target_x)-1)
            frame=first_replace(frame,target_x=replace_word(frame.target_x,remaining))
            if remaining==65535:
                break
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+30),0,2,True)
        frame=_economy_memory_delta_fields(state,frame,0xFFFFF36A,1)
    frame=_lowbank_ui_call_fields(state,frame,0xA158,0x13DF0)
    return _lowbank_ui_call_fields(state,frame,0x13DF6,0x13DF4)


def lowbank_coordinate_live_state_130_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13E92,0x13E46)
    frame=_lowbank_ui_call_fields(state,frame,0x13F6C,0x13E4A)
    frame=_lowbank_ui_call_fields(state,frame,0x161D4,0x13E4E)
    frame=_lowbank_ui_call_fields(state,frame,0x13FAA,0x13E52)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),5)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,4)
        frame=_lowbank_ui_call_fields(state,frame,0x13FE4,0x13E6A)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF602,1),4)
        if not frame.status&4:
            frame=_campaign_confirmation_fields(state,frame,2)
            frame=_lowbank_ui_call_fields(state,frame,0x16152,0x13E8A)
    return _lowbank_ui_call_fields(state,frame,0xA158,0x13E90)



"""Trait-based officer allocation and random resource rewards. Tables remain external live RO views."""

def lowbank_coordinate_live_state_118_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10A58/10EE0: command modes choose real reward, transfer or status branches."""
    frame=_movement_frame(state,frame)
    for command in (110,114,115):
        frame=_movement_compare(state,frame,state.read(0xFFFFF38C,2),command,16)
        if frame.status&4:
            if command==115:
                return frame
            if command==110:
                frame=_movement_test(state,frame,state.read(0xFFFFF386,2),16)
                if not frame.status&4:
                    return frame
                frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
                frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF393,1),1)
                frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
                frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),0,1,True)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
                frame=_movement_move(state,frame,'target_x',85,16)
                frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x10F14)
                return _lowbank_ui_store_fields(state,frame,0xFFFFF652,1)
            frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),1,1)
            frame=_lowbank_ui_call_fields(state,frame,0x10F3A,0x10F2E)
            frame=_lowbank_ui_call_fields(state,frame,0x10ADE,0x10F32)
            return _lowbank_ui_call_fields(state,frame,0x10F92,0x10F36)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),1,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_lowbank_ui_call_fields(state,frame,0x1108C,0x10A90)
    frame=_movement_move(state,frame,'choice',low16(frame.target_x),16)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x10D14,0x10AA6)
    frame=_lowbank_ui_call_fields(state,frame,0x10AA8,0x10A98)
    frame=_lowbank_ui_call_fields(state,frame,0x10ADE,0x10A9C)
    return _lowbank_ui_call_fields(state,frame,0x10C74,0x10AA0)


def lowbank_scale_live_record_value_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10AA8: officer trait plus the live random-table factor and its WORD base."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_x)),8)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
    frame=_economy_delta_fields(state,frame,'unit',frame.roster.word(low16(frame.target_x)))
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,0x10AC6)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFEFD2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0x10A4C).cursor())
    frame=_movement_multiply_word(state,frame,'target_x',frame.roster.word(low16(frame.target_y)))
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_economy_delta_fields(state,frame,'target_x',frame.roster.word(low16(frame.target_y),2))
    return _economy_delta_fields(state,frame,'unit',low16(frame.target_x))


def lowbank_resolve_readonly_state_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10ADE: seven ordered score bands select an external 48-byte policy record."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'count',0,16)
    for ceiling in (50,100,150,200,250,300):
        frame=_movement_compare(state,frame,low16(frame.unit),ceiling,16)
        if frame.status&5:
            break
        frame=_economy_delta_fields(state,frame,'count',1)
    frame=_movement_move(state,frame,'distance',low16(frame.count),16)
    frame=_movement_fixed_shift_word(state,frame,'count',1)
    frame=_economy_delta_fields(state,frame,'count',low16(frame.distance))
    frame=_movement_fixed_shift_word(state,frame,'count',4)
    frame=first_replace(frame,roster=state.table_at(0x10B24).cursor())
    return first_replace(frame,roster=frame.roster.advance(s16(low16(frame.count))))


def _economy_trait_band_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Both true entry prefixes converge on these same ordered threshold comparisons."""
    frame=_movement_move(state,frame,'unit',0,16)
    for ceiling in (30,60,80,90,100):
        frame=_movement_compare(state,frame,low16(frame.target_x),ceiling,16)
        if frame.status&5:
            break
        frame=_economy_delta_fields(state,frame,'unit',1)
    return frame


def _economy_policy_offset_fields(state: SceneState, frame: FirstDeploymentFrame,
        continuation: int) -> FirstDeploymentFrame:
    from .services import _movement_fixed_shift_word
    frame=_movement_fixed_shift_word(state,frame,'unit',3)
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,continuation)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_economy_long_shift_fields(state,frame,'target_x',2)
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    return _economy_delta_fields(state,frame,'unit',low16(frame.target_x))


def _economy_normal_allocation_tail_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10CCC: live policy WORD then three real city comparisons and an indexed handler CALL."""
    frame=_economy_policy_offset_fields(state,frame,0x10CD4)
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.unit)),16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF376,2),16)
    matches=False
    for address in (0xFFFFF67A,0xFFFFF67C,0xFFFFF67E):
        frame=_movement_compare(state,frame,low16(frame.unit),state.read(address,2),16)
        if frame.status&4:
            matches=True
            break
    if not matches:
        return frame
    selected=state.table_at(0x10D0C).word(low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',selected,16)
    return _lowbank_ui_call_fields(state,frame,0x10D14+s16(selected),0x10D0A)


def _economy_alternate_allocation_tail_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10FCC: reward on zero policy; otherwise transfer selected officer and present the result."""
    frame=_economy_policy_offset_fields(state,frame,0x10FD4)
    frame=_movement_test(state,frame,frame.roster.word(low16(frame.unit)),16)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x10E12,0x10FEC)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
        frame=_movement_move(state,frame,'target_x',83,16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
        return _lowbank_ui_call_fields(state,frame,0x676F2,0x11008)
    frame=_lowbank_ui_call_fields(state,frame,0x10EB0,0x11010)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCC00).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),state.read(0xFFFFF393,1),1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_x))),0,1,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF740,84)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D2,state.read(0xFFFFF3F2,2))
    saved=state.read(0xFFFFF362,2)
    stack=frame.stack_cursor.advance(-2)
    stack.set_word(0,saved)
    frame=first_replace(frame,stack_cursor=stack)
    frame=_movement_test(state,frame,saved,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
    frame=_lowbank_ui_call_fields(state,frame,0x30A74,0x11046)
    restored=frame.stack_cursor.word()
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,restored)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A6,state.read(0xFFFFF3F2,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_movement_move(state,frame,'target_x',86,16)
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x11074)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF652,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF64E,0,2,True)


def lowbank_scale_live_record_value_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10C74: choose a roster member by the actual random product and policy band."""
    from .services import _movement_fixed_shift_word, _movement_multiply_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'offset_y',low16(frame.choice),16)
    frame=_economy_logic_fields(state,frame,'offset_y',32767)
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,0x10C80)
    frame=_economy_logic_fields(state,frame,'target_x',65535,32)
    frame=_movement_multiply_word(state,frame,'target_x',low16(frame.offset_y))
    frame=_economy_swap_fields(state,frame,'target_x')
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFEF24).cursor())
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x)),16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F2,low16(frame.target_x))
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFB600).cursor())
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x)),16)
    frame=_economy_trait_band_fields(state,frame)
    return _economy_normal_allocation_tail_fields(state,frame)


def lowbank_scale_live_record_value_4_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10F92: first <=30 branch really enters 10CCC, not the later alternate reward tail."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3F2,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_x',1)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFB600).cursor())
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x)),16)
    frame=_economy_trait_band_fields(state,frame)
    if low16(frame.unit)==0:
        return _economy_normal_allocation_tail_fields(state,frame)
    return _economy_alternate_allocation_tail_fields(state,frame)


def _economy_random_gain_fields(state: SceneState, frame: FirstDeploymentFrame,
        continuation: int, multiple: int, bias: int) -> FirstDeploymentFrame:
    """Real RNG call and shared fixed-width gain math; the sampled seed is read at F61C."""
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,continuation)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF61C,2),16)
    frame=_movement_move_long(state,frame,'target_y',frame.target_x)
    frame=_economy_long_shift_fields(state,frame,'target_x',1 if multiple==3 else 2)
    frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    if multiple==20:
        frame=_economy_long_shift_fields(state,frame,'target_x',2)
    frame=_economy_swap_fields(state,frame,'target_x')
    if bias:
        frame=_economy_delta_fields(state,frame,'target_x',bias)
    return frame


def lowbank_coordinate_live_state_120_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10E12: add the three-factor random gain to the actual C000 officer WORD."""
    from .services import _movement_fixed_shift_word
    frame=_economy_random_gain_fields(state,_movement_frame(state,frame),0x10E18,3,1)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC000).cursor())
    return _economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.target_x))


def lowbank_coordinate_live_state_121_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10E8A uses the original four-byte indexing for the BE00 WORD mutation."""
    from .services import _movement_fixed_shift_word
    frame=_economy_random_gain_fields(state,_movement_frame(state,frame),0x10E90,5,1)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',2)
    frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
    return _economy_memory_delta_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.target_x))


def lowbank_coordinate_live_state_122_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10EB0 saturates the WORD reward only on original unsigned carry."""
    from .services import _movement_fixed_shift_word
    frame=_economy_random_gain_fields(state,_movement_frame(state,frame),0x10EB6,5,5)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFBE00).cursor())
    frame=_economy_delta_fields(state,frame,'target_x',frame.roster.word(low16(frame.target_y)))
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',65535,16)
    return _lowbank_ui_store_fields(state,frame,u32(frame.roster.base+s16(low16(frame.target_y))),low16(frame.target_x))


def lowbank_coordinate_live_state_123_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10F3A: career-type base plus twenty-factor random gain and two officer attributes."""
    from .services import _movement_fixed_shift_word
    frame=_economy_random_gain_fields(state,_movement_frame(state,frame),0x10F40,20,0)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC700).cursor())
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    frame=_economy_logic_fields(state,frame,'unit',15)
    frame=_movement_fixed_shift_word(state,frame,'unit',1)
    frame=first_replace(frame,roster=state.table_at(0x10F88).cursor())
    frame=_economy_delta_fields(state,frame,'target_x',frame.roster.word(low16(frame.unit)))
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF3A6,2),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFC200).cursor())
    frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_move(state,frame,'unit',frame.roster.byte(low16(frame.target_y)),8)
    frame=_economy_delta_fields(state,frame,'unit',low16(frame.target_x))
    frame=_movement_fixed_shift_word(state,frame,'target_y',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB600).cursor())
    return _economy_delta_fields(state,frame,'unit',frame.roster.word(low16(frame.target_y)))


def lowbank_coordinate_live_state_119_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """10D14 is also the real shared BRA fallback for both transfer alternatives."""
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x10E12,0x10D18)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,32)
    frame=_movement_move(state,frame,'target_x',77,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    return _lowbank_ui_call_fields(state,frame,0x676F2,0x10D34)


def _economy_transfer_alternative_fields(state: SceneState, frame: FirstDeploymentFrame,
        lane: int) -> FirstDeploymentFrame:
    """10D64/10DB4: only original lane setup differs; same transfer and presentation logic."""
    from .services import _movement_fixed_shift_word
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF392,2),16)
    if lane==0:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF630,65535)
        frame=_lowbank_ui_call_fields(state,frame,0x5F48,0x10D74)
    else:
        frame=first_replace(frame,roster=state.table_at(0xFFFFF45E).cursor())
        frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
        frame=_movement_fixed_shift_word(state,frame,'target_y',1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF630,frame.roster.word(low16(frame.target_y)))
        frame=_lowbank_ui_call_fields(state,frame,0x5F48,0x10DCC)
    frame=_movement_compare(state,frame,low16(frame.count),10,16)
    if not frame.status&1:
        return lowbank_coordinate_live_state_119_fields(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x10EB0 if lane==0 else 0x10E8A,0x10D7E if lane==0 else 0x10DD8)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,520)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,33)
    frame=_movement_move(state,frame,'target_x',79,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D0,state.read(0xFFFFF3A6,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3D2,state.read(0xFFFFF3F2,2))
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x10DA0 if lane==0 else 0x10DFA)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,lane,2,lane==0)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A6,state.read(0xFFFFF3F2,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF64E,lane,2,lane==0)


def lowbank_coordinate_live_state_119_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_transfer_alternative_fields(state,_movement_frame(state,frame),0)


def lowbank_coordinate_live_state_119_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _economy_transfer_alternative_fields(state,_movement_frame(state,frame),1)


def lowbank_coordinate_live_state_124_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """1108C: build allocation candidates, retaining physical D2-D5/A0-A3 MOVEM saves."""
    from ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_restore_longs
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    saved=('unit','count','distance','offset_x','roster','candidates','controller','scan')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFEFE4,2),16)
    frame=_movement_fixed_shift_word(state,frame,'count',2)
    pointer=state.table_at(0x11080).long(low16(frame.count))
    frame=first_replace(frame,auxiliary=state.table_at(pointer))
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFCC00).cursor())
    frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.target_y)),8)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF427).cursor())
    frame=_movement_move(state,frame,'count',frame.candidates.byte(low16(frame.count)),8)
    frame=first_replace(frame,roster=state.table_at(0xFFFFEF24).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x110CE,0x110B6)
    frame=_movement_test(state,frame,low16(frame.unit),16)
    if not frame.status&8:
        frame=_lowbank_ui_call_fields(state,frame,0x11122,0x110BE)
        frame=_lowbank_ui_call_fields(state,frame,0x11186,0x110C2)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,65535)
    frame=_movement_move(state,frame,'target_x',low16(frame.unit),16)
    return _movement_restore_longs(state,frame,saved)


def lowbank_select_live_state_35_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """110CE: four trait-specific external candidate tables; tagged count stays WORD."""
    frame=_movement_frame(state,frame)
    selected=None
    for trait,displacement in ((1,0),(5,4),(10,8),(2,12)):
        frame=_movement_compare(state,frame,low16(frame.count),trait,16)
        if frame.status&4:
            selected=displacement
            break
    if selected is None:
        return frame
    pointer=state.read(u32(frame.auxiliary.base+selected),4)
    frame=first_replace(frame,candidates=state.table_at(pointer).cursor(),controller=state.table_at(0xFFFFCC00))
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'distance',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low8(frame.distance),state.read(0xFFFFF374,1),8)
        if not frame.status&5:
            frame=first_replace(frame,candidates=frame.candidates.advance(2))
            continue
        frame=_movement_move(state,frame,'distance',frame.candidates.word(),16)
        frame=_movement_test(state,frame,frame.controller.byte(low16(frame.distance)),8)
        if frame.status&4:
            frame=_lowbank_ui_append_fields(state,frame,low16(frame.distance))
            frame=_economy_logic_fields(state,frame,'unit',32768,16,'or')
            frame=_economy_delta_fields(state,frame,'unit',1)
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
    return frame


# B56 Lowbank mode selection, record layout and scene setting: sole complete fields.
from .services import (first_replace, _movement_frame, _movement_move, _movement_move_long, _movement_compare, _movement_test, _first_compare_long, FirstDeploymentReturnBoundary, MovementContinuationBoundary)
from ..high_level_main_flows.business_movement_support import _movement_save_longs, _movement_restore_longs

"""B56 mode/selection control, with closed real prefixes and live field carriers.

Directory WORDs, flags and message rows stay in their original memories. Child
calls retain the caller's existing physical LONG slot, including unknown cores.
"""


def _menu_window_reject_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,5)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B0,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def _menu_window_action_mask_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str='target_x', mask: int=0x640) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,name,state.read(0xFFFFF3A4,2),16)
    return _economy_logic_fields(state,frame,name,mask)


def _menu_window_action_notice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Common 2972/29E6 stores do not overwrite the already selected D0 value."""
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3DA,0x208)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3DC,2)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x19)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,3,False)


def _menu_window_action_setup_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """25BC shared mode choice; the 25B8 CLR prefix is separately owned."""
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
        if not frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C4,state.read(0xFFFFF362,2))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x13)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF3C2,state.read(0xFFFFF612,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x205)
    else:
        frame=_menu_window_action_mask_fields(state,frame,'target_x',0x3FF0)
        if not frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,7)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,9)
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
            if frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,13)
            return frame
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x201)
        frame=_lowbank_ui_call_fields(state,frame,0x676C4,0x2626)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,3,False)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_movement_move(state,frame,'target_y',3,16)
    frame=_lowbank_ui_call_fields(state,frame,0x506C,0x263A)
    return _lowbank_ui_call_fields(state,frame,0x5ABC,0x2640)


def _menu_window_action_reset_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A8,0,2,True)
    return _menu_window_action_setup_fields(state,frame)


def _menu_window_current_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2930 policy branch shares the original setup tail, not a second algorithm."""
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,0x1A)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
        frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE640).cursor())
        frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFCD00).cursor())
        frame=_movement_test(state,frame,frame.roster.byte(low16(frame.target_x)),8)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',1,16)
        else:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
            frame=_lowbank_ui_call_fields(state,frame,0xCFB8,0x29B6)
            frame=_movement_test(state,frame,low16(frame.target_x),16)
            if not frame.status&4:
                frame=_lowbank_ui_call_fields(state,frame,0xD028,0x296E)
                return _menu_window_action_reset_fields(state,frame)
            frame=_movement_move(state,frame,'target_x',0,16)
    else:
        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF376,2),16)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFE700,2),16)
        frame=_economy_register_bit_fields(state,frame,'target_x',frame.target_y)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',0x33,16)
        else:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
            frame=_lowbank_ui_call_fields(state,frame,0xCFB8,0x295A)
            frame=_movement_test(state,frame,low16(frame.target_x),16)
            if not frame.status&4:
                frame=_lowbank_ui_call_fields(state,frame,0xD028,0x296E)
                return _menu_window_action_reset_fields(state,frame)
            frame=_movement_move(state,frame,'target_x',0x2A,16)
    frame=_menu_window_action_notice_fields(state,frame)
    return _lowbank_ui_call_fields(state,frame,0x676F2,0x2990)


def lowbank_select_live_state_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """0200: two NOPs and the original unconditional spin; no invented exit."""
    frame=_movement_frame(state,frame)
    while True:
        pass


def lowbank_coordinate_live_state_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2268 menu fade stages retain each true call token and RAM access order."""
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF352,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF352,2),16)
        frame=_movement_move(state,frame,'target_y',0x40,16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0xDEA6,0x2284)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
        frame=_movement_test(state,frame,state.read(0xFFFFF77A,2),16)
        if not frame.status&4:
            frame=_lowbank_ui_call_fields(state,frame,0x23F6,0x2294)
        return frame
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF600,0x24)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF352,0x21)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',0x20,16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF352,2),True)
        frame=_movement_move(state,frame,'target_y',0x40,16)
        frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
        frame=_lowbank_ui_call_fields(state,frame,0xDEA6,0x22C6)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF352,1)
        return _lowbank_ui_call_fields(state,frame,0x23F6,0x22CE)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _lowbank_ui_call_fields(state,frame,0x23F6,0x22DA)


def lowbank_coordinate_live_state_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """22DC input selection publishes only actual WORD writes and full carriers."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFEFDE,0,2,True)
    frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_economy_logic_fields(state,frame,'target_x',0x60)
        if not frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFEFDE,1)
            return _menu_window_confirm_input_fields(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        return _menu_window_confirm_input_fields(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF77A,1)
    frame=_lowbank_ui_call_fields(state,frame,0x23F6,0x2344)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF636,1)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),0)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1,True)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF636,2),16)
    else:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),1)
        if frame.status&4:
            return frame
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
        frame=_movement_compare(state,frame,frame.target_x,state.read(0xFFFFF636,2),16)
        if not frame.status&5:
            frame=_movement_move(state,frame,'target_x',1,16)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF378,low16(frame.target_x))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF4FE).cursor())
    frame=_movement_move(state,frame,'target_x',frame.roster.word(low16(frame.target_x)),16)
    frame=_economy_logic_fields(state,frame,'target_x',0xFF)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF372,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x207)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF352,0,2,True)


def _menu_window_confirm_input_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,frame,0x23AC,0x230C)
    frame=_movement_move(state,frame,'target_x',0x200,16)
    frame=_window_compare_memory_fields(state,frame,0xFFFFEFE0,1)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',0x400,16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0,2,True)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF378,1,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF352,0,2,True)
    frame=_lowbank_ui_call_fields(state,frame,0x23F6,0x2332)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3DE,0,2,True)


def lowbank_select_live_state_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """23AC visible roster offset uses the original signed then unsigned tests."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF378,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',3,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_y',7,16)
    frame=_movement_test(state,frame,state.read(0xFFFFF6C4,2),16)
    reduced=not frame.status&4
    if not reduced:
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        reduced=not frame.status&4
        if not reduced:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
            reduced=not frame.status&4
    if reduced:
        frame=_movement_move(state,frame,'target_y',5,16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF636,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',frame.target_y,True)
    if frame.status&8:
        frame=_movement_move(state,frame,'unit',0,16)
    frame=_movement_compare(state,frame,low16(frame.target_x),low16(frame.unit),16)
    if not frame.status&5:
        frame=_movement_move(state,frame,'target_x',low16(frame.unit),16)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF658,low16(frame.target_x))


def lowbank_update_record_flags_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2490 two original PC-relative WORD directories select real child entries."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF380,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),0x60,16)
    if frame.status&1:
        frame=_menu_window_action_mask_fields(state,frame,'target_y',0xE40)
        if not frame.status&4:
            return _menu_window_flagged_mode_fields(state,frame)
        frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
        frame=_movement_move(state,frame,'target_x',state.read(u32(0x24D4+s16(low16(frame.target_x))),2),16)
        return _lowbank_ui_call_fields(state,frame,u32(0x24DC+s16(low16(frame.target_x))),0x24D2)
    frame=_movement_compare(state,frame,low16(frame.target_x),0xFF,16)
    if frame.status&4:
        frame=_menu_window_action_mask_fields(state,frame,'target_x',0x3FFF)
        if not frame.status&4:
            return _menu_window_flagged_mode_fields(state,frame)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C2,0x208)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF38A,0x208)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x60)
        frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,3,False)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF3A4,0,2,True)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',0x60,True)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.read(u32(0x254E+s16(low16(frame.target_x))),2),16)
    return _lowbank_ui_call_fields(state,frame,u32(0x25B8+s16(low16(frame.target_x))),0x254C)


def _menu_window_flagged_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,7)
    frame=_movement_move(state,frame,'target_x',9,16)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',13,16)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,low16(frame.target_x))


def lowbank_coordinate_live_state_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF650,0,2,True)
    return _lowbank_ui_call_fields(state,frame,0xBBB8,0x24E6)


def lowbank_coordinate_live_state_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xBBDA,0x24EE)


def lowbank_coordinate_live_state_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xBC00,0x24F6)


def lowbank_coordinate_live_state_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xBBDA,0x24FE)


def lowbank_update_record_flags_2_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x26B6) -> FirstDeploymentFrame:
    """Whole 25B8/26B6 family shares its tail and six actual public prefixes."""
    frame=_movement_frame(state,frame)
    if entry in (0x2930,):
        return _menu_window_current_choice_fields(state,frame)
    if entry==0x29CA:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF378,1)
        return _menu_window_action_reset_fields(state,frame)
    if entry in (0x291C,0x2920,0x2B3C):
        return _menu_window_action_reset_fields(state,frame)
    if entry!=0x26B6:
        raise ValueError('actual flag-mode entry required')
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        for source,destination in ((0xFFFFF392,0xFFFFF3A8),(0xFFFFF35E,0xFFFFF3AA),
                (0xFFFFF360,0xFFFFF3AC),(0xFFFFF364,0xFFFFF3AE)):
            frame=_lowbank_ui_store_fields(state,frame,destination,state.read(source,2))
    return _menu_window_action_setup_fields(state,frame)


def lowbank_update_record_flags_2_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_2_fields(state,frame,0x291C)


def lowbank_update_record_flags_2_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_2_fields(state,frame,0x2920)


def lowbank_update_record_flags_2_alternate_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_2_fields(state,frame,0x2930)


def lowbank_update_record_flags_2_alternate_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_2_fields(state,frame,0x29CA)


def lowbank_update_record_flags_2_alternate_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_2_fields(state,frame,0x2B3C)


def lowbank_select_live_state_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame))
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x38)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF362,11)
    return _menu_window_reject_mode_fields(state,frame)


def lowbank_select_live_state_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """273A BRA enters the complete 270A setup body without another call slot."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x206)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,8)
    for address in (0xFFFFF36A,0xFFFFF368,0xFFFFF36E):
        frame=_lowbank_ui_store_fields(state,frame,address,0,2,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF378,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF656,0,2,True)


def lowbank_coordinate_live_state_9_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,14)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B4,0,2,True)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x274C)


def lowbank_coordinate_live_state_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame))
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x12A98,0x2760)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,15)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B8,1)
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
        frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
        frame=first_replace(frame,roster=state.table_at(0xFFFFE3BC).cursor())
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B6,frame.roster.word(low16(frame.target_x),2))
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x278A)


def lowbank_select_live_state_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame))
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x44)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,20)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3E0,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3E2,0,2,True)
    return frame


def _menu_window_trait_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,frame,'target_y')
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,7)
        frame=_movement_move(state,frame,'target_x',9,16)
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),6)
        if frame.status&4:
            frame=_movement_move(state,frame,'target_x',12,16)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x5C)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)


def lowbank_update_record_flags_3_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x28DA) -> FirstDeploymentFrame:
    """Three real action prefixes share one flag/trait and budget-tail algorithm."""
    frame=_movement_frame(state,frame)
    if entry==0x28DA:
        return _menu_window_trait_choice_fields(state,frame)
    if entry==0x2DD2:
        return _menu_window_budget_tail_fields(state,frame)
    if entry!=0x29D4:
        raise ValueError('actual trait-mode entry required')
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFE700,2),16)
    frame=_economy_register_bit_fields(state,frame,'target_y',frame.target_x)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',0x34,16)
        frame=_menu_window_action_notice_fields(state,frame)
        return _lowbank_ui_call_fields(state,frame,0x676F2,0x2A04)
    frame=first_replace(frame,roster=state.table_at(0xFFFFE9F8).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF376,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(low16(frame.target_x),1),8)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF646,low16(frame.target_y))
    return _menu_window_trait_choice_fields(state,frame)


def lowbank_update_record_flags_3_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_3_fields(state,frame,0x29D4)


def lowbank_update_record_flags_3_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_update_record_flags_3_fields(state,frame,0x2DD2)


def _menu_window_budget_tail_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2DD2 ordered LONG arithmetic and packed budget BYTE reads retain D0/D1."""
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A6,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB000).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFB200).cursor())
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',frame.roster.word(low16(frame.target_x)),True)
    frame=_economy_logic_fields(state,frame,'target_y',0xFFFF,32)
    frame=_movement_move_long(state,frame,'target_x',frame.target_y)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_long_shift_fields(state,frame,'target_x',3)
    frame=_economy_delta_fields(state,frame,'target_x',frame.target_y,32)
    frame=_economy_long_shift_fields(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(state.read(0x00FF382C,4)).cursor())
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(5),8)
    frame=_lowbank_ui_shift_fields(state,frame,'target_y',8)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(6),8)
    frame=_economy_long_shift_fields(state,frame,'target_y',8)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(7),8)
    frame=_economy_long_shift_fields(state,frame,'target_y',8)
    frame=_movement_move(state,frame,'target_y',frame.roster.byte(8),8)
    frame=_movement_compare(state,frame,frame.target_x,frame.target_y,16)
    if not frame.status&5:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0x12)
        frame=_movement_move(state,frame,'target_x',0xBD,16)
        return _lowbank_ui_call_fields(state,frame,0x676F2,0x2E32)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C8,frame.target_x,4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,frame.target_x,4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x12)
    frame=_lowbank_ui_call_fields(state,frame,0x125D8,0x2E4A)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)


def lowbank_select_live_state_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,0x36)
    if not frame.status&4:
        frame=_menu_window_action_mask_fields(state,frame)
        if not frame.status&4:
            return _menu_window_reject_mode_fields(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x48)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x17)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)


def lowbank_coordinate_live_state_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """2924 BRA to 279E shares the whole physical body, not another call slot."""
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,5)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B0,0x10)
    else:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x10)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_x)))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F8,frame.target_x,4)
    frame=first_replace(frame,roster=state.table_at(0x27F6).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x12878,0x27DA)
    frame=_movement_move_long(state,frame,'target_x',state.read(0xFFFFF3F8,4))
    frame=_movement_move(state,frame,'target_y',0xC0D8,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFEF00).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x1270A,0x27EE)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3F4,state.read(0xFFFFF39E,4),4)


def lowbank_coordinate_live_state_8_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x2928) -> FirstDeploymentFrame:
    """2928/2A54 prefixes join the sole complete 2664 selection-list body."""
    frame=_movement_frame(state,frame)
    if entry==0x2A54:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,5)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x4C)
    elif entry!=0x2928:
        raise ValueError('actual roster-choice entry required')
    frame=_lowbank_ui_call_fields(state,frame,0x5694,0x266A)
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x2670)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x206)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,8)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36E,0,2,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_call_fields(state,frame,0x5F48,0x268E)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF636,low16(frame.count))
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF378,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF372,state.read(0xFFFFF500,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F2,state.read(0xFFFFF3A6,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF658,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF656,0,2,True)


def lowbank_coordinate_live_state_8_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_coordinate_live_state_8_fields(state,frame,0x2A54)


def lowbank_coordinate_live_state_12_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE09C).cursor())
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_x)))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F8,frame.target_x,4)
    frame=first_replace(frame,roster=state.table_at(0x27F6).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x12878,0x2822)
    frame=_movement_move_long(state,frame,'target_x',state.read(0xFFFFF3F8,4))
    frame=_movement_move(state,frame,'target_y',1,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFEF00).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x1270A,0x2836)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F4,state.read(0xFFFFF3BA,4),4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,5)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF362,17)


def lowbank_coordinate_live_state_7_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x5694,0x2648)
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x264E)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,5)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3B0,6)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F4,0,4,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF39E,0,4,True)


def lowbank_coordinate_live_state_13_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame))
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xC28A,0x2A34)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x1A)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF600,0x4C)


def lowbank_select_live_state_7_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x50)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x1C)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)


def lowbank_coordinate_live_state_14_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame))
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xC28A,0x2AB4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x54)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x1D)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3F0,0,2,True)


def lowbank_select_live_state_8_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x58)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF384,0,2,True)


def lowbank_select_live_state_9_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame),'target_x',0x3FFF)
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF600,0x60)
    return _menu_window_flagged_mode_fields(state,frame)


def lowbank_select_live_state_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame),'target_x',0x3FFF)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,7)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,9)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x64)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF362,0x22)


def lowbank_coordinate_live_state_15_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x206)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,8)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36E,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF656,1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF65A,0,2,True)
    frame=_lowbank_ui_call_fields(state,frame,0xA332,0x2B64)
    frame=_lowbank_ui_call_fields(state,frame,0xA34E,0x2B6A)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF636,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1,True)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF686,low16(frame.target_x))


"""B56 selected-record transitions, row packets and bounded live camera steps."""


def _menu_window_store_plan_fields(state: SceneState, frame: FirstDeploymentFrame,
        plan: tuple) -> FirstDeploymentFrame:
    """Closed original WORD-store sequences distinguish MOVE from real CLR reads."""
    for address,value,clear in plan:
        frame=_lowbank_ui_store_fields(state,frame,address,value,2,clear)
    return frame


def _menu_window_notice_value_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int, continuation: int) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',value,16)
    return _lowbank_ui_call_fields(state,frame,0x676F2,continuation)


def _menu_window_blocked_action_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,7)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,9)


def lowbank_update_live_fields_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _menu_window_store_plan_fields(state,_movement_frame(state,frame),
        ((0xFFFFF612,0x209,False),(0xFFFFF362,0,True),(0xFFFFF39A,2,False)))


def lowbank_coordinate_live_state_16_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame),'target_x',0x3FF0)
    if not frame.status&4:
        return _menu_window_blocked_action_fields(state,frame)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF612,0x209,False),(0xFFFFF362,2,False)))
    frame=_lowbank_ui_store_fields(state,frame,0x00FF3820,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF674,state.read(0xFFFFF672,2))
    return _menu_window_notice_value_fields(state,frame,0x6B,0x2BC6)


def lowbank_update_record_flags_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_action_mask_fields(state,_movement_frame(state,frame),'target_x',0x3FFC)
    if not frame.status&4:
        return _menu_window_blocked_action_fields(state,frame)
    frame=_menu_window_store_plan_fields(state,frame,
        ((0xFFFFF600,0x70,False),(0xFFFFF612,0x209,False),(0xFFFFF362,3,False)))
    frame=_lowbank_ui_call_fields(state,frame,0x163E0,0x2BEC)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF676,0,2,True)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,3,False)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3F4,0,4,True)


def lowbank_coordinate_live_state_17_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x165AC,0x2C12)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF600,0x40,False),
        (0xFFFFF612,0x206,False),(0xFFFFF362,8,False),(0xFFFFF378,1,False),
        (0xFFFFF658,0,True),(0xFFFFF656,1,False),(0xFFFFF684,0,True),(0xFFFFF686,10,False)))
    return _lowbank_ui_call_fields(state,frame,0x5ABC,0x2C44)


def lowbank_update_live_fields_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _menu_window_store_plan_fields(state,_movement_frame(state,frame),
        ((0xFFFFF612,0x206,False),(0xFFFFF362,7,False),(0xFFFFF36A,13,False)))


def lowbank_update_live_fields_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _menu_window_store_plan_fields(state,_movement_frame(state,frame),
        ((0xFFFFF600,0x40,False),(0xFFFFF612,0x206,False),(0xFFFFF362,0,True),
        (0xFFFFF3A4,1,False),(0xFFFFF378,1,False),(0xFFFFF658,0,True),(0xFFFFF656,1,False)))


def lowbank_coordinate_live_state_18_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),1)
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF612,0x209,False),(0xFFFFF362,8,False)))
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x2C9E)
    frame=_lowbank_ui_call_fields(state,frame,0x11CF2,0x2CA4)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _menu_window_notice_value_fields(state,frame,3,0x2CB2)


def lowbank_coordinate_live_state_19_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_store_plan_fields(state,_movement_frame(state,frame),
        ((0xFFFFF612,0x209,False),(0xFFFFF362,8,False),(0xFFFFF386,0,True)))
    frame=_lowbank_ui_call_fields(state,frame,0x11E3C,0x2CDC)
    return _menu_window_notice_value_fields(state,frame,0x72,0x2CE6)


def lowbank_coordinate_live_state_20_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),1)
    if not frame.status&4:
        return _menu_window_reject_mode_fields(state,frame)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF612,0x209,False),(0xFFFFF362,9,False)))
    frame=_lowbank_ui_call_fields(state,frame,0x11F1C,0x2D04)
    frame=_lowbank_ui_call_fields(state,frame,0xEA6,0x2D0A)
    frame=_window_status_word_fields(state,frame,0x2500)
    frame=_menu_window_notice_value_fields(state,frame,0x60,0x2D18)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF3F0,0,2,True)


def lowbank_coordinate_live_state_21_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,0xAB)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x149A0,0x2D40)
        frame=_movement_test(state,frame,frame.target_x,16)
        if frame.status&4:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF576,1,True)
            frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF38C,0xA3,False),(0xFFFFF380,0x89,False)))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3DA,state.read(0xFFFFF612,2))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3DC,state.read(0xFFFFF362,2))
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x24)
            return _menu_window_notice_value_fields(state,frame,0xBC,0x2D72)
    else:
        frame=_lowbank_ui_call_fields(state,frame,0x165AC,0x2D7C)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF600,0x40,False),
        (0xFFFFF612,0x206,False),(0xFFFFF362,8,False),(0xFFFFF378,1,False),
        (0xFFFFF658,0,True),(0xFFFFF656,0,True)))


def lowbank_coordinate_live_state_22_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_menu_window_store_plan_fields(state,_movement_frame(state,frame),
        ((0xFFFFF612,0x209,False),(0xFFFFF362,10,False)))
    frame=_lowbank_ui_call_fields(state,frame,0x12314,0x2DB0)
    frame=_menu_window_notice_value_fields(state,frame,0x73,0x2DBA)
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3F4,0,4,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39A,5)
    return frame


def lowbank_coordinate_live_state_23_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x5ABC,0x2E5C)
    frame=_lowbank_ui_call_fields(state,frame,0x5694,0x2E62)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF362,5,False),
        (0xFFFFF3B0,0x26,False),(0xFFFFF688,0,True)))


def lowbank_coordinate_live_state_24_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1B19C,0x2E7A)


def lowbank_coordinate_live_state_25_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x665E6,0x2E82)


def lowbank_coordinate_live_state_26_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1CD00,0x2E8A)


def lowbank_coordinate_live_state_27_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1CD88,0x2E92)


def lowbank_coordinate_live_state_28_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1CE06,0x2E9A)


def lowbank_coordinate_live_state_29_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF380,2),16)
    special=bool(frame.status&4)
    if special:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),6)
        special=not frame.status&4
    if not special:
        frame=_lowbank_ui_call_fields(state,frame,0xC138,0x2EB4)
        return _lowbank_ui_call_fields(state,frame,0xBFA2,0x2EBA)
    frame=_movement_move(state,frame,'target_x',0xAC,16)
    frame=_lowbank_ui_call_fields(state,frame,0x808A,0x2EC8)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF600,0xEC,False),(0xFFFFF362,0x2A,False)))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFAFF8,state.read(0xFFFFEFD6,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFAFFA,state.read(0xFFFFEFD8,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFAFFC,0,2,True)


def lowbank_update_record_flags_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
    frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF322,2,True)
        return _lowbank_ui_call_fields(state,frame,0x9F7C,0x2F04)
    return _lowbank_ui_call_fields(state,frame,0xBE44,0x2F0E)


def lowbank_coordinate_live_state_30_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x662E4,0x2F16)
    if not frame.status&1:
        return _lowbank_ui_call_fields(state,frame,0xBF5A,0x2F20)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x2B)
    frame=_menu_window_notice_value_fields(state,frame,0x9C,0x2F34)
    return _lowbank_ui_store_fields(state,frame,0x00FF7026,0xFFFF)


def lowbank_update_record_flags_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF603,7,False)
        return _lowbank_ui_call_fields(state,frame,0x9E5E,0x2F6E)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF386,0,True),(0xFFFFF388,0,True)))
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x2F54)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF362,3,False),(0xFFFFF36A,0x12,False)))


def lowbank_coordinate_live_state_31_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5ABC,0x2F80)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),4)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5694,0x2F94)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36A,13)
    if frame.status&1:
        return _lowbank_ui_call_fields(state,frame,0xC1E4,0x2FCC)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,state.read(0xFFFFF3B0,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
    frame=_window_memory_logic_fields(state,frame,0xFFFFF3A4,0xF9B7,operation='and',width=16)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF380,0x8F)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0x78)
    return frame


def lowbank_coordinate_live_state_32_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xC28A,0x2FD4)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF362,8)


def lowbank_update_record_flags_7_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1D18,0x2FE0)
    matched=False
    for value in (0x63,0x60,0x84):
        frame=_window_compare_memory_fields(state,frame,0xFFFFF380,value)
        if frame.status&4:
            matched=True
            break
    if matched:
        frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x3004)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1,True)
    if frame.status&8:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF362,0,True),(0xFFFFF36A,0,True)))
        frame=_menu_window_action_mask_fields(state,frame,'target_x',0x4000)
        if not frame.status&4:
            frame=_window_register_bit_fields(state,frame,'target_x',15,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A4,low16(frame.target_x))
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36A,9)
    if not frame.status&5:
        frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A4,6,False)
    return frame


def lowbank_coordinate_live_state_33_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x1278C,0x3040)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x304A)


def lowbank_coordinate_live_state_34_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x128E2,0x3052)


def lowbank_update_record_flags_8_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF603,7,False)
    frame=_lowbank_ui_call_fields(state,frame,0x9E5E,0x305E)
    frame=_lowbank_ui_call_fields(state,frame,0x16B4,0x3062)
    frame=_lowbank_ui_call_fields(state,frame,0x309A,0x3066)
    frame=_movement_test(state,frame,frame.target_x,16)
    if not frame.status&4:
        return frame
    frame=_movement_test(state,frame,state.read(0xFFFFF322,2),16)
    if not frame.status&4:
        return frame
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF612,0x208,False),
        (0xFFFFF362,2,False),(0xFFFFF36A,0x12,False),(0xFFFFF600,0x34,False)))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF364,state.read(0xFFFFF3AE,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF392,state.read(0xFFFFF3A8,2))


def _menu_window_advance_axis_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, target: int, limit: int) -> FirstDeploymentFrame:
    """309A/30D6 clamp the unsigned borrow branches without assuming a signed delta."""
    frame=_movement_move(state,frame,'target_y',state.read(address,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',state.read(target,2),True)
    if frame.status&4:
        return frame
    if frame.status&1:
        frame=_movement_compare(state,frame,low16(frame.target_y),u16(-limit),16)
        if frame.status&1:
            frame=_movement_move(state,frame,'target_y',u16(-limit),16)
    else:
        frame=_movement_compare(state,frame,low16(frame.target_y),limit,16)
        if not frame.status&5:
            frame=_movement_move(state,frame,'target_y',limit,16)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,address,frame.target_y,True)
    return _movement_move(state,frame,'target_x',1,16)


def lowbank_select_live_state_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """309A retains D0 unchanged when both original axis differences are zero."""
    frame=_movement_frame(state,frame)
    frame=_menu_window_advance_axis_fields(state,frame,0xFFFFF35E,0xFFFFF3AA,3)
    return _menu_window_advance_axis_fields(state,frame,0xFFFFF360,0xFFFFF3AC,4)


def lowbank_coordinate_live_state_35_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xC3CE,0x311A)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF388,0,True),(0xFFFFF384,0,True)))
    frame=_movement_test(state,frame,state.read(0xFFFFF3A2,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x3138)


def lowbank_coordinate_live_state_36_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xC494,0x3140)


def lowbank_coordinate_live_state_37_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xC590,0x3148)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF362,2,False),(0xFFFFF36A,0x12,False)))


def lowbank_coordinate_live_state_38_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x63E6,0x315C)
    return _lowbank_ui_call_fields(state,frame,0x4CFA,0x3162)


def lowbank_coordinate_live_state_39_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x12C0C,0x316A)
    frame=_lowbank_ui_call_fields(state,frame,0x12BC0,0x3170)
    frame=_lowbank_ui_call_fields(state,frame,0x12C84,0x3176)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF362,2,False),(0xFFFFF36A,0x12,False)))
        return _lowbank_ui_call_fields(state,frame,0x12B6A,0x3192)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x31A6)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF362,3,False),(0xFFFFF36A,0x12,False)))


def lowbank_coordinate_live_state_40_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5ABC,0x31C4)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),4)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5694,0x31D8)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),6)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x12EF2,0x31FC)
    frame=_lowbank_ui_call_fields(state,frame,0x12CBE,0x31EC)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x31F2)


def lowbank_coordinate_live_state_41_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5ABC,0x320E)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),4)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5694,0x3222)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),6)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x12F8E,0x3240)
    return _lowbank_ui_call_fields(state,frame,0x12CBE,0x3236)


def lowbank_coordinate_live_state_42_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),0)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xC6F6,0x3280)
    selected=False
    for value in (0xB1,0xBA):
        frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,value)
        if frame.status&4:
            selected=True
            break
    if selected:
        frame=_lowbank_ui_call_fields(state,frame,0x1626C,0x3270)
    else:
        frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x3266)
    return _lowbank_ui_call_fields(state,frame,0xC5C2,0x3276)


def lowbank_process_counted_records_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3282 publishes two real row packets, with DBRA low-WORD and CLR prior read."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_movement_compare(state,frame,low16(frame.target_x),4,16)
    if frame.status&1:
        frame=_lowbank_ui_packet_start_fields(state,frame)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+0x50),0x26)
        frame=_lowbank_ui_append_fields(state,frame,0x26)
        frame=_lowbank_ui_shift_fields(state,frame,'target_x',8)
        frame=_movement_move(state,frame,'target_y',0xCD82,16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',frame.target_x,True)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+0x50),low16(frame.target_y))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0x80,True)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_y))
        frame=_movement_move(state,frame,'target_x',0x12,16)
        while True:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+0x50),0x80008000,4)
            frame=_lowbank_ui_append_fields(state,frame,0x80008000,4)
            frame=_lowbank_ui_counter_fields(frame,'target_x')
            if low16(frame.target_x)==0xFFFF:
                break
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+0x50),0,2,True)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,0xA0)
        return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,state.read(0xFFFFF3C4,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,state.read(0xFFFFF3C2,2))
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,3,False)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A4,0,2,True)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF612,0x208)
    if frame.status&4:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF362,0x13)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x201)
    return frame


"""B56 complete scene-setting controls; actual child slots and device writes remain real."""


def _menu_window_restore_parent_mode_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C2,state.read(0xFFFFF3DA,2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C4,state.read(0xFFFFF3DC,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF362,0x13)


def _menu_window_confirmation_due_fields(state: SceneState, frame: FirstDeploymentFrame) -> tuple[FirstDeploymentFrame, bool]:
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return frame,True
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    return frame,bool(frame.status&4)


def lowbank_coordinate_live_state_43_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0x5ABC,0x331C)
    frame=_lowbank_ui_call_fields(state,frame,0xC9A6,0x3326)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)


def lowbank_coordinate_live_state_44_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xCB58,0x3332)


def lowbank_coordinate_live_state_45_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),3)
    if frame.status&4:
        frame=_movement_move(state,frame,'target_x',1,16)
        frame=_movement_move(state,frame,'target_y',3,16)
        frame=_lowbank_ui_call_fields(state,frame,0x506C,0x334C)
        frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x3352)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',0xF)
    if not frame.status&4:
        return _menu_window_restore_parent_mode_fields(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return _menu_window_restore_parent_mode_fields(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF362,2,False),(0xFFFFF36A,0x12,False)))
    return frame


def lowbank_coordinate_live_state_46_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0xCD72,0x339C)
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x33A2)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,0x36)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A5,1),4)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xC9A6,0x33BC)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def lowbank_coordinate_live_state_47_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0xCE5E,0x33C8)


def lowbank_select_live_state_12_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_menu_window_restore_parent_mode_fields(state,frame)
    return frame


def lowbank_coordinate_live_state_48_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),0)
    if not frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x1321C,0x341A)
        return _lowbank_ui_call_fields(state,frame,0x132AE,0x3420)
    frame=_lowbank_ui_call_fields(state,frame,0x1306A,0x33F8)
    frame=_lowbank_ui_call_fields(state,frame,0x13188,0x33FE)
    frame=_lowbank_ui_call_fields(state,frame,0x1321C,0x3404)
    frame=_lowbank_ui_call_fields(state,frame,0x13270,0x340A)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x3410)


def lowbank_coordinate_live_state_49_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13934,0x3428)
    return _lowbank_ui_call_fields(state,frame,0x1379A,0x342E)


def lowbank_coordinate_live_state_50_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF600,2),16)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),0)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xD14E,0x345E)
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x3448)
    frame=_lowbank_ui_call_fields(state,frame,0xD054,0x344E)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x3454)


def lowbank_coordinate_live_state_51_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),0)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xD368,0x3480)
    frame=_lowbank_ui_call_fields(state,frame,0xD270,0x3470)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x3476)


def lowbank_coordinate_live_state_52_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF3A4,1),0)
    if not frame.status&4:
        return _lowbank_ui_call_fields(state,frame,0xD624,0x34A8)
    frame=_lowbank_ui_call_fields(state,frame,0x5ABC,0x3492)
    frame=_lowbank_ui_call_fields(state,frame,0xD560,0x3498)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x349E)


def lowbank_coordinate_live_state_53_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x20)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36C,2)
    if not frame.status&1:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,0x25)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3FE,2),16)
    if frame.status&8:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0x676F2,0x34D6)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF652,state.read(0xFFFFF774,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF774,0,2,True)


def lowbank_coordinate_live_state_54_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36C,3)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xC11E,0x3502)
    frame=_lowbank_ui_call_fields(state,frame,0x133A,0x3506)
    frame=_movement_test(state,frame,state.read(0x00FF7026,2),16)
    if not frame.status&8:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,0xC0)
    return frame


def lowbank_coordinate_live_state_55_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,0x48)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF64E,2),16)
        if not frame.status&4:
            frame=_menu_window_notice_value_fields(state,frame,0x51,0x353E)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF64E,0,2,True)
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x354C)
    return _menu_window_store_plan_fields(state,frame,((0xFFFFF362,3,False),(0xFFFFF36A,0xC,False),(0xFFFFF36C,1,False)))


def lowbank_coordinate_live_state_56_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,_movement_frame(state,frame),0xFFFFF362,0x21)
    frame=_lowbank_ui_call_fields(state,frame,0xD8AE,0x356C)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0x3572)


def lowbank_select_live_state_13_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,due=_menu_window_confirmation_due_fields(state,_movement_frame(state,frame))
    if due:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF362,2,False),(0xFFFFF36A,0xC,False)))
    return frame


def lowbank_select_live_state_14_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame,due=_menu_window_confirmation_due_fields(state,_movement_frame(state,frame))
    if due:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,state.read(0xFFFFF3DA,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,state.read(0xFFFFF3DC,2))
    return frame


def lowbank_select_live_state_15_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF612,0x206,False),(0xFFFFF362,7,False),(0xFFFFF36A,0xD,False)))
    return frame


def lowbank_coordinate_live_state_57_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13958,0x35D8)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _menu_window_notice_value_fields(state,frame,0x19,0x35E6)


def lowbank_coordinate_live_state_58_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x13AB6,0x35EE)


def lowbank_update_live_fields_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _menu_window_store_plan_fields(state,_movement_frame(state,frame),((0xFFFFF600,0xC0,False),(0xFFFFF362,0x1F,False),(0xFFFFF608,2,False)))


def lowbank_select_live_state_16_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF600,0xC0,False),(0xFFFFF612,0x206,False),(0xFFFFF362,7,False),(0xFFFFF36A,0xD,False)))
    return frame


def lowbank_process_device_control_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3628 retains all thirteen-by-nine real LONG VDP writes, without device success fiction."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',0x30)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0xDE1C,0x36C2)
        return _lowbank_ui_call_fields(state,frame,0xDCF0,0x36C8)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,3,True)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,1,True)
    frame=_lowbank_ui_change_bit_fields(state,frame,0xFFFFF31C,2,False)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF38E,2,False),(0xFFFFF576,0,True),(0xFFFFF396,0,True),(0xFFFFF36C,1,False)))
    frame=_lowbank_ui_call_fields(state,frame,0x133A,0x365E)
    frame=_menu_window_store_plan_fields(state,frame,((0xFFFFF65A,0,True),(0xFFFFF600,0x30,False),(0xFFFFF38C,0,True)))
    frame=_movement_move(state,frame,'target_x',0xC,16)
    frame=_movement_move_long(state,frame,'unit',0x42980003)
    while True:
        frame=_lowbank_ui_store_fields(state,frame,0x00C00004,frame.unit,4)
        frame=_economy_delta_fields(state,frame,'unit',0x800000,32)
        frame=_movement_move(state,frame,'target_y',8,16)
        while True:
            frame=_lowbank_ui_store_fields(state,frame,0x00C00000,0xC000C000,4)
            frame=_lowbank_ui_counter_fields(frame,'target_y')
            if low16(frame.target_y)==0xFFFF:
                break
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==0xFFFF:
            break
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',0xAC,16)
    frame=_lowbank_ui_call_fields(state,frame,0x808A,0x36AC)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFEFD6,state.read(0xFFFFAFF8,2))
    return _lowbank_ui_store_fields(state,frame,0xFFFFEFD8,state.read(0xFFFFAFFA,2))


def lowbank_select_live_state_17_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
    return frame






# B55 Lowbank text packets, record windows and scene control: sole complete fields.
from .services import (first_replace, _movement_frame, _movement_move, _movement_move_long, _movement_compare, _movement_test, _first_compare_long, FirstDeploymentReturnBoundary, MovementContinuationBoundary)

"""Lowbank counted text rows and packet composition; fonts and directory words stay external."""


def _window_append_view_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, value: int, size: int=2, clear: bool=False) -> FirstDeploymentFrame:
    view=getattr(frame,name)
    frame=_lowbank_ui_store_fields(state,frame,view.base,value,size,clear)
    return first_replace(frame,**{name:view.advance(size)})


def _window_memory_logic_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, mask: int, operation: str='or', width: int=16) -> FirstDeploymentFrame:
    original=state.read(address,width//8)
    if operation=='or':
        result=original|mask
    elif operation=='and':
        result=original&mask
    elif operation=='xor':
        result=original^mask
    else:
        raise ValueError('closed original window AND/OR/EOR role required')
    return _lowbank_ui_store_fields(state,frame,address,result,width//8)


def _window_compare_memory_fields(state: SceneState, frame: FirstDeploymentFrame,
        address: int, operand: int, width: int=16) -> FirstDeploymentFrame:
    return _movement_compare(state,frame,state.read(address,width//8),operand,width)


def _window_blank_row_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """591C shared tail: seven blanks, including each real MOVE and final DBRA WORD."""
    frame=_movement_move(state,frame,'target_x',6,16)
    return _lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC001)


def lowbank_update_live_fields_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5864 sets the actual D3 WORD then falls through the existing Main cursor core."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'count',0xC308,16)
    return _lowbank_ui_known_child_fields(state,frame,0x5868)


def lowbank_select_live_state_22_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """5884 alternate cursor tile, with a real BRA rather than another return slot."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'count',0xC314,16)
    return _lowbank_ui_known_child_fields(state,frame,0x5868)


def lowbank_coordinate_live_state_72_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,auxiliary=frame.roster.advance(30))
    frame=_window_append_view_fields(state,frame,'auxiliary',0xC001)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE65C).cursor())
    frame=_movement_move(state,frame,'choice',0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x58E4,0x589C)
    return _lowbank_ui_call_fields(state,frame,0x591C,0x58A0)


def lowbank_coordinate_live_state_73_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,auxiliary=frame.roster.advance(30))
    frame=_window_append_view_fields(state,frame,'auxiliary',0xC001)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFDFFC).cursor())
    frame=_movement_move(state,frame,'choice',0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x58E4,0x58B4)
    return _lowbank_ui_call_fields(state,frame,0x591C,0x58B8)


def _window_numeric_cell_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """58E4 numeric lane: the actual dynamic offset is D7.W, not a mode guess."""
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF364,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.target_x)))
    frame=_movement_move(state,frame,'target_y',0xC386,16)
    frame=_movement_move(state,frame,'unit',0xC001,16)
    frame=_movement_move(state,frame,'distance',0,16)
    target=u32(0x58FE+s16(low16(frame.choice)))
    return _lowbank_ui_call_fields(state,frame,target,0x58FC)


def lowbank_process_counted_records_7_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x58BA) -> FirstDeploymentFrame:
    """58BA/58E4 share one formatting core; the BYTE-count prefix is truly optional."""
    frame=_movement_frame(state,frame)
    if entry not in (0x58BA,0x58E4):
        raise ValueError('actual complete numeric-lane entry required')
    if entry==0x58BA:
        frame=_movement_test(state,frame,state.read(0xFFFFF62E,1),8)
        if frame.status&8:
            frame=_movement_move(state,frame,'target_x',0,16)
            frame=_movement_move(state,frame,'target_y',0,16)
            frame=_movement_move(state,frame,'target_x',state.read(u32(0x58DE+s16(low16(frame.offset_y))),1),8)
            frame=_movement_move(state,frame,'target_y',state.read(u32(0x58DF+s16(low16(frame.offset_y))),1),8)
            while True:
                frame=_window_append_view_fields(state,frame,'auxiliary',0xC001)
                frame=_lowbank_ui_counter_fields(frame,'target_x')
                if low16(frame.target_x)==65535:
                    break
            while True:
                frame=_window_append_view_fields(state,frame,'auxiliary',0xC385)
                frame=_lowbank_ui_counter_fields(frame,'target_y')
                if low16(frame.target_y)==65535:
                    return frame
    return _window_numeric_cell_fields(state,frame)


def lowbank_process_counted_records_7_alternate_1_fields(state: SceneState,
        frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_7_fields(state,frame,0x58E4)


def lowbank_select_live_state_23_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """58FE BRA/590A JMP leaves the parent's real slot in place."""
    return _lowbank_ui_known_child_fields(state,_movement_frame(state,frame),0x1270A)


def lowbank_select_live_state_24_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_known_child_fields(state,_movement_frame(state,frame),0x12734)


def lowbank_select_live_state_25_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_known_child_fields(state,_movement_frame(state,frame),0x1273C)


def lowbank_process_counted_records_8_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x591C) -> FirstDeploymentFrame:
    """Six true text-lane prefixes share the 591C seven-cell tail, not six codecs."""
    frame=_movement_frame(state,frame)
    if entry==0x591C:
        return _window_blank_row_fields(state,frame)
    if entry==0x592A:
        source,selector,continuation=(0xFFFFE09C,0,0x593A)
    elif entry==0x593C:
        source,selector,continuation=(0xFFFFE13C,8,0x594A)
    elif entry==0x5958:
        source,selector,continuation=(0xFFFFE3BC,0,0x596A)
    elif entry==0x596C:
        source,selector,continuation=(0xFFFFE45C,0,0x5980)
    elif entry==0x5982:
        source,selector,continuation=(0xFFFFE4FC,0,0x5998)
    else:
        raise ValueError('actual whole text-row prefix required')
    frame=first_replace(frame,auxiliary=frame.roster.advance(30))
    if entry!=0x593C:
        frame=_window_append_view_fields(state,frame,'auxiliary',0xC001)
    frame=first_replace(frame,candidates=state.table_at(source).cursor())
    frame=_movement_move(state,frame,'choice',selector,16)
    target=0x58E4
    if entry in (0x596C,0x5982):
        frame=_movement_move(state,frame,'offset_y',0 if entry==0x596C else 4,16)
        target=0x58BA
    frame=_lowbank_ui_call_fields(state,frame,target,continuation)
    if entry==0x593C:
        for value in (0xC386,0xC386,0xC386):
            frame=_window_append_view_fields(state,frame,'auxiliary',value)
    return _window_blank_row_fields(state,frame)


def lowbank_process_counted_records_8_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_8_fields(state,frame,0x592A)


def lowbank_process_counted_records_8_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_8_fields(state,frame,0x593C)


def lowbank_process_counted_records_8_alternate_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_8_fields(state,frame,0x5958)


def lowbank_process_counted_records_8_alternate_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_8_fields(state,frame,0x596C)


def lowbank_process_counted_records_8_alternate_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_8_fields(state,frame,0x5982)


def lowbank_process_counted_records_9_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x599A) -> FirstDeploymentFrame:
    """Four stored-choice prefixes retain their true Main child and tail slots."""
    frame=_movement_frame(state,frame)
    if entry==0x599A:
        tile,stored_return,source,numeric_return=(0xC001,0x59A2,0xFFFFE1DC,0x59B2)
    elif entry==0x59D8:
        tile,stored_return,source,numeric_return=(0xC05D,0x59E0,0xFFFFE27C,0x59F0)
    elif entry==0x59F2:
        tile,stored_return,source,numeric_return=(0xC025,0x59FA,0xFFFFE31C,0x5A0E)
    elif entry==0x5A10:
        tile,stored_return,source,numeric_return=(0xC031,0x5A18,0xFFFFE59C,0x5A28)
    else:
        raise ValueError('actual stored-choice prefix required')
    frame=_movement_move(state,frame,'count',tile,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5A2A,stored_return)
    frame=first_replace(frame,auxiliary=frame.roster.advance(30),candidates=state.table_at(source).cursor())
    frame=_movement_move(state,frame,'choice',4,16)
    if entry==0x59F2:
        frame=_movement_move(state,frame,'offset_y',2,16)
    frame=_lowbank_ui_call_fields(state,frame,0x58BA if entry==0x59F2 else 0x58E4,numeric_return)
    frame=_movement_move(state,frame,'target_x',4,16)
    return _lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC001)


def lowbank_process_counted_records_9_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_9_fields(state,frame,0x59D8)


def lowbank_process_counted_records_9_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_9_fields(state,frame,0x59F2)


def lowbank_process_counted_records_9_alternate_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_9_fields(state,frame,0x5A10)


def lowbank_coordinate_live_state_76_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0x5DCC) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    if entry==0x5DCC:
        frame=_movement_test(state,frame,state.read(0xFFFFF36C,2),16)
        if not frame.status&4:
            return frame
    elif entry!=0x5DD2:
        raise ValueError('actual panel entry required')
    frame=_lowbank_ui_packet_start_fields(state,frame)
    for target,continuation in ((0x5DFC,0x5DDE),(0x5E5A,0x5DE4),(0x5EEA,0x5DEA)):
        frame=_lowbank_ui_call_fields(state,frame,target,continuation)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,168)
    return _window_memory_logic_fields(state,frame,0xFFFFF3A4,0xA000,operation='or',width=16)


def lowbank_coordinate_live_state_76_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_coordinate_live_state_76_fields(state,frame,0x5DD2)


def lowbank_process_counted_records_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    for tile in (10,0xC084,0xC380):
        values={10:(10,10),0xC084:(0xC384,0xC204),0xC380:(0xD380,0xC382)}[tile]
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+48),values[0])
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),values[1])
        frame=_lowbank_ui_append_fields(state,frame,tile)
    frame=_movement_move(state,frame,'target_x',7,16)
    while True:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+48),0xD381)
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xC001)
        frame=_lowbank_ui_append_fields(state,frame,0xC381)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+48),0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    return first_replace(frame,roster=frame.roster.advance(48))


def lowbank_coordinate_live_state_77_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    for top,bottom in ((10,10),(0xC184,0xC104),(0xC382,0xC382)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),top)
        frame=_lowbank_ui_append_fields(state,frame,bottom)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF374,1),8)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',184)
    frame=_movement_move(state,frame,'target_y',1,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFD300).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x12744,0x5E92)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',2,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5ED2,0x5E9E)
    frame=_movement_move(state,frame,'target_y',0xC0D0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5EBA,0x5EA8)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    return first_replace(frame,roster=frame.roster.advance(24))


def lowbank_update_live_fields_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,low16(frame.target_y))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),low16(frame.target_y))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+2),low16(frame.target_y))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+26),low16(frame.target_y))
    return first_replace(frame,roster=frame.roster.advance(4))


def lowbank_process_counted_records_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    while True:
        frame=_movement_move(state,frame,'target_y',frame.candidates.word(),16)
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        if frame.status&4:
            frame=_movement_move(state,frame,'target_y',0xC001,16)
        else:
            frame=_lowbank_ui_shift_fields(state,frame,'target_y',2)
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',0xC0D4)
        frame=_lowbank_ui_call_fields(state,frame,0x5EBA,0x5EE4)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            return frame


def lowbank_coordinate_live_state_78_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    for top,bottom in ((10,10),(0xC304,0xC284),(0xC382,0xC382)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),top)
        frame=_lowbank_ui_append_fields(state,frame,bottom)
    frame=_movement_move(state,frame,'target_y',0xC001,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5EBA,0x5F0E)
    frame=_movement_move_long(state,frame,'target_x',0)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF375,1),8)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_y',1,16)
    frame=_movement_move(state,frame,'unit',0,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x1274C,0x5F28)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5ED2,0x5F32)
    frame=_movement_move(state,frame,'target_y',0xC0D4,16)
    frame=_lowbank_ui_call_fields(state,frame,0x5EBA,0x5F38)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+24),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    return first_replace(frame,roster=frame.roster.advance(24))


def lowbank_process_counted_records_12_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF61A,1,True)
    if not frame.status&8:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF61A,3)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF618,2),16)
    if frame.status&8:
        return frame
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF618,2,True)
    frame=first_replace(frame,roster=state.table_at(u32(0x94CA+s16(low16(frame.target_x)))).cursor(),
        candidates=state.table_at(0xFFFFFB04).cursor())
    frame=_movement_move_long(state,frame,'target_x',10)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31E,1)


def lowbank_select_live_state_26_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor())
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        if frame.status&8:
            return _lowbank_ui_store_fields(state,frame,0xFFFFF684,low16(frame.target_x))
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_y,14)
        if not frame.status&4:
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)


def lowbank_coordinate_live_state_79_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',1,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFF500).cursor())
    while True:
        frame=_movement_move(state,frame,'target_y',frame.roster.word(),16)
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_y,14)
        if frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF378,low16(frame.target_x))
            return _lowbank_ui_call_fields(state,frame,0x23F6,0xA36E)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)


def lowbank_process_counted_records_13_fields(state: SceneState, frame: FirstDeploymentFrame,
        entry: int=0xAAB4) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    if entry==0xAAB4:
        source=0xFFFFE1DC
    elif entry==0xAB2A:
        source=0xFFFFE31C
    elif entry==0xAB34:
        source=0xFFFFE3BC
    else:
        raise ValueError('actual description-row prefix required')
    frame=_movement_move(state,frame,'unit',2,16)
    frame=first_replace(frame,candidates=state.table_at(source).cursor())
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'unit',0x483)
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'unit',2)
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.unit)))
    frame=_movement_move(state,frame,'target_y',0x400,16)
    frame=_movement_move(state,frame,'unit',0x483,16)
    frame=first_replace(frame,auxiliary=frame.roster)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x12744,0xAADE)
    return first_replace(frame,roster=frame.auxiliary)


def lowbank_process_counted_records_13_alternate_1_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_13_fields(state,frame,0xAB2A)


def lowbank_process_counted_records_13_alternate_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return lowbank_process_counted_records_13_fields(state,frame,0xAB34)


def lowbank_process_counted_records_14_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'unit',3,16)
    frame=first_replace(frame,candidates=state.table_at(0xFFFFE45C).cursor())
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'unit',0x483)
    frame=_movement_move(state,frame,'unit',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'unit',2)
    frame=_movement_move_long(state,frame,'target_x',frame.candidates.long(low16(frame.unit)))
    frame=_movement_move(state,frame,'target_y',0x400,16)
    frame=_movement_move(state,frame,'unit',0x483,16)
    frame=first_replace(frame,auxiliary=frame.roster)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_lowbank_ui_call_fields(state,frame,0x1274C,0xAB0C)
    return first_replace(frame,roster=frame.auxiliary)


"""Lowbank roster windows: paired rows, real directory dispatch and retained input quirks."""


def _window_dispatch_row_fields(state: SceneState, frame: FirstDeploymentFrame,
        directory: int, continuation: int) -> FirstDeploymentFrame:
    frame=_lowbank_ui_packet_start_fields(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.read(u32(directory+s16(low16(frame.target_x))),2),16)
    frame=first_replace(frame,candidates=state.table_at(0xBC24).cursor())
    return _lowbank_ui_call_fields(state,frame,u32(frame.candidates.base+s16(low16(frame.target_x))),continuation)


def lowbank_coordinate_live_state_80_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _window_dispatch_row_fields(state,_movement_frame(state,frame),0xBBD4,0xBBD2)


def lowbank_coordinate_live_state_81_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _window_dispatch_row_fields(state,_movement_frame(state,frame),0xBBF6,0xBBF4)


def lowbank_coordinate_live_state_82_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _window_dispatch_row_fields(state,_movement_frame(state,frame),0xBC1C,0xBC1A)


def lowbank_process_counted_records_15_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    for value in (16,0xC318,0xC380):
        frame=_lowbank_ui_append_fields(state,frame,value)
    frame=_movement_move(state,frame,'target_x',13,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xC381)
    frame=_lowbank_ui_append_fields(state,frame,0xCB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,24)


def _window_index_three_fields(state: SceneState, frame: FirstDeploymentFrame,
        shift: int, origin: int) -> FirstDeploymentFrame:
    """The repeated source expressions retain every reread and the D1 WORD carrier."""
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1,True)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',shift)
    return _lowbank_ui_arithmetic_fields(state,frame,'target_x',origin)


def lowbank_coordinate_live_state_83_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),16)
    frame=_lowbank_ui_append_fields(state,frame,16)
    frame=_window_index_three_fields(state,frame,7,0xC418)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),low16(frame.target_x))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',128,True)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),0xC382)
    frame=_lowbank_ui_append_fields(state,frame,0xC382)
    frame=_window_index_three_fields(state,frame,3,0xC005)
    for first_return,second_return in ((0xBC94,0xBC98),(0xBCA6,0xBCAA),(0xBCB8,0xBCBC)):
        frame=_lowbank_ui_call_fields(state,frame,0xBCDA,first_return)
        frame=_lowbank_ui_call_fields(state,frame,0xBCDA,second_return)
        if second_return!=0xBCBC:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),0xC001)
            frame=_lowbank_ui_append_fields(state,frame,0xC001)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),0,2,True)
    frame=first_replace(frame,roster=frame.roster.advance(36))
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,48)


def lowbank_update_live_fields_7_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BCDA incrementing paired glyphs ends on the fourth ADD, not the last MOVE."""
    frame=_movement_frame(state,frame)
    for offset in (0,36,2,38):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),low16(frame.target_x))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
    return first_replace(frame,roster=frame.roster.advance(4))


def lowbank_process_counted_records_16_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_append_fields(state,frame,16)
    frame=_window_index_three_fields(state,frame,7,0xC318)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
    frame=_lowbank_ui_append_fields(state,frame,0xD380)
    frame=_movement_move(state,frame,'target_x',13,16)
    frame=_lowbank_ui_repeat_cells_fields(state,frame,'target_x',0xD381)
    frame=_lowbank_ui_append_fields(state,frame,0xDB80)
    frame=_lowbank_ui_store_fields(state,frame,frame.roster.base,0,2,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,36)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF380,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',2)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF382,state.read(u32(0xBD66+s16(low16(frame.target_x))),2))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF384,state.read(u32(0xBD68+s16(low16(frame.target_x))),2))
    frame=_lowbank_ui_call_fields(state,frame,0xBE24,0xBD3E)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3A4,2),16)
    frame=_window_register_bit_fields(state,frame,'target_x',13,False)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A4,low16(frame.target_x))
    frame=_movement_test(state,frame,state.read(0xFFFFF38C,2),16)
    if frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x5DD2,0xBD58)
    frame=_window_memory_logic_fields(state,frame,0xFFFFF3A4,0x8100,operation='or',width=16)
    return _lowbank_ui_call_fields(state,frame,0x676C4,0xBD64)


def lowbank_process_counted_records_17_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    for offset in (72,36):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),16)
    frame=_lowbank_ui_append_fields(state,frame,16)
    frame=_window_index_three_fields(state,frame,7,0xC498)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+72),low16(frame.target_x))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',128,True)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),low16(frame.target_x))
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',128,True)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
    for offset in (72,36):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),0xC382)
    frame=_lowbank_ui_append_fields(state,frame,0xC382)
    frame=_movement_move(state,frame,'target_x',13,16)
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+72+s16(low16(frame.target_y))),0xC001)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',2)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_window_index_three_fields(state,frame,3,0xC005)
    for first_return,second_return in ((0xBDE2,0xBDE6),(0xBDF4,0xBDF8),(0xBE06,0xBE0A)):
        frame=_lowbank_ui_call_fields(state,frame,0xBCDA,first_return)
        frame=_lowbank_ui_call_fields(state,frame,0xBCDA,second_return)
        if second_return!=0xBE0A:
            frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+36),0xC001)
            frame=_lowbank_ui_append_fields(state,frame,0xC001)
    for offset in (72,36):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+offset),0xCB82)
    frame=_lowbank_ui_append_fields(state,frame,0xCB82)
    frame=_lowbank_ui_store_fields(state,frame,u32(frame.roster.base+72),0,2,True)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)


def lowbank_select_live_state_27_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BE24 original subtract-until-borrow, including its zero-divisor nontermination."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF396,2),16)
    frame=_movement_move(state,frame,'target_y',0,16)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF384,2),16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'unit',1)
    while True:
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit),True)
        if frame.status&1:
            break
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.unit))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,low16(frame.target_x))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF386,low16(frame.target_y))


def _window_descriptor_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """Read the real long descriptor base, then the actual signed WORD displacement."""
    frame=first_replace(frame,candidates=state.table_at(0x92878).cursor())
    frame=first_replace(frame,roster=state.table_at(frame.candidates.long()).cursor())
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x),4),16)
    return first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))


def lowbank_coordinate_live_state_84_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0xBEE6,0xBE48)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36A,18)
    if frame.status&1:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A2,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF576,1,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF38C,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3C2,state.read(0xFFFFF38A,2))
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,19)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF36C,0,2,True)
    frame=_window_descriptor_fields(state,frame)
    frame=_movement_move(state,frame,'target_x',0,16)
    frame=_movement_move(state,frame,'target_x',frame.roster.byte(),8)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF38C,low16(frame.target_x))
    # This second lookup intentionally reads the same long descriptor base again.
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=first_replace(frame,roster=state.table_at(frame.candidates.long()).cursor())
    frame=_movement_move(state,frame,'target_x',frame.candidates.word(low16(frame.target_x),4),16)
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.target_x))))
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF381,frame.roster.byte(1),1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,48)
    frame=_window_memory_logic_fields(state,frame,0xFFFFF3A4,0xFEDA,operation='and',width=16)
    frame=_movement_test(state,frame,state.read(0xFFFFF38C,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF576,0,2,True)
        frame=_movement_move(state,frame,'target_x',0,16)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF578,1),8)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1,True)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF396,low16(frame.target_x))
    frame=first_replace(frame,candidates=state.table_at(0xFFFFF578).cursor())
    frame=first_replace(frame,candidates=frame.candidates.advance(s16(state.read(0xFFFFF576,2))))
    frame=_movement_move(state,frame,'target_x',frame.candidates.byte(),8)
    frame=_movement_move(state,frame,'target_y',0,16)
    while True:
        frame=_movement_compare(state,frame,low8(frame.target_x),frame.roster.byte(low16(frame.target_y),2),8)
        if frame.status&4:
            return _lowbank_ui_store_fields(state,frame,0xFFFFF396,low16(frame.target_y))
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',1)


def lowbank_process_counted_records_18_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_packet_start_fields(state,frame)
    frame=_lowbank_ui_append_fields(state,frame,26)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF36A,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',7)
    frame=_movement_move(state,frame,'target_y',0xC904,16)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',low16(frame.target_x),True)
    frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_y))
    frame=_movement_move(state,frame,'target_x',26,16)
    frame=_lowbank_ui_clear_cells_fields(state,frame,'target_x')
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31A,56)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF38F,1),2)
    if frame.status&4:
        return frame
    frame=_movement_move_long(state,frame,'target_x',0xC0000006)
    frame=_movement_move(state,frame,'target_y',8,16)
    frame=_movement_move(state,frame,'unit',0xC3A0,16)
    frame=first_replace(frame,roster=state.table_at(0xBF3A).cursor())
    frame=_lowbank_ui_call_fields(state,frame,0x26BFA,0xBF32)
    return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A5,3,False)


def lowbank_update_record_flags_9_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF36A,18)
    if frame.status&1:
        frame=_lowbank_ui_call_fields(state,frame,0xBEE6,0xBF96)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF36A,1)
        return _lowbank_ui_change_bit_fields(state,frame,0xFFFFF3A5,0,False)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3A2,0,2,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF38C,2),16)
    frame=_window_descriptor_fields(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF381,frame.roster.byte(1),1)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,48)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF396,0,2,True)
    return _window_memory_logic_fields(state,frame,0xFFFFF3A4,0xFEDA,operation='and',width=16)


def _window_reset_choice_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF39E,0,4,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF3BA,0,4,True)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


def lowbank_coordinate_live_state_85_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """BFA2 navigation, hold-repeat and confirmation; preserve all fresh reads and wrapped WORDs."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',15)
    update=not bool(frame.status&4)
    if not update:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    else:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
        update=bool(frame.status&4)
        if update:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,16)
            frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,0)
            if not frame.status&4:
                frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1,True)
                if frame.status&8:
                    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,state.read(0xFFFFF382,2))
            else:
                frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
                if not frame.status&4:
                    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF386,1)
                    frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF386,2),16)
                    frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF382,2),16)
                    if not frame.status&5:
                        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF386,0,2,True)
                else:
                    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
                    if not frame.status&4:
                        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF388,1)
                        frame=_movement_move(state,frame,'target_y',state.read(0xFFFFF388,2),16)
                        frame=_movement_compare(state,frame,low16(frame.target_y),state.read(0xFFFFF384,2),16)
                        if not frame.status&5:
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,0,2,True)
                    else:
                        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF388,1,True)
                        if frame.status&8:
                            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,state.read(0xFFFFF384,2))
    frame=_window_compare_memory_fields(state,frame,0xFFFFF380,3)
    restricted=bool(frame.status&4)
    if not restricted:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF380,2)
        restricted=bool(frame.status&4)
    if restricted:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF386,2)
        if not frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,1)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,4)
    confirm=not bool(frame.status&4)
    if confirm:
        frame=_movement_test(state,frame,state.read(0xFFFFF650,2),16)
        confirm=bool(frame.status&4)
    if confirm:
        frame=_movement_test(state,frame,state.read(0xFFFFF380,2),16)
        if not frame.status&4:
            return _window_reset_choice_fields(state,frame)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF388,2),16)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF578,low8(frame.target_x),1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF579,12,1)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF576,2)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF388,3)
    else:
        frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
        if not frame.status&4:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
            frame=_window_compare_memory_fields(state,frame,0xFFFFCFD2,8)
            if not frame.status&5:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
            return frame
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,2),16)
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,5)
        if frame.status&4:
            return frame
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0xC0A8)
    if frame.status&1:
        return _window_reset_choice_fields(state,frame)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF362,2)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,0,2,True)


"""Scene coordination and real hardware controls: no fabricated bus grant, IRQ, or RTE success."""


def _window_status_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        value: int) -> FirstDeploymentFrame:
    state.set_status_word(u16(value))
    return first_replace(frame,status=value&31)


def _window_register_bit_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str, bit: int, enabled: bool) -> FirstDeploymentFrame:
    original=frame.carrier(name)
    frame=_lowbank_ui_bit_fields(state,frame,original,bit)
    mask=1<<(bit%32)
    return first_replace(frame,**{name:u32(original|mask if enabled else original&~mask)})


def _window_neg_word_fields(state: SceneState, frame: FirstDeploymentFrame,
        name: str) -> FirstDeploymentFrame:
    from .services import _movement_binary_flags
    frame,result=_movement_binary_flags(state,frame,0,low16(frame.carrier(name)),16,True)
    return first_replace(frame,**{name:replace_word(frame.carrier(name),result)})


def lowbank_process_counted_records_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3966 subtracts each nonzero palette component once, preserving six actual LONG saves."""
    frame=_movement_frame(state,frame)
    saved=('target_x','target_y','offset_x','offset_y','choice','roster')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_move(state,frame,'offset_x',63,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB00).cursor())
    frame=_movement_move(state,frame,'choice',low16(frame.offset_x),16)
    while True:
        frame=_movement_move(state,frame,'target_x',frame.roster.word(),16)
        for mask,amount in ((14,2),(224,32),(3584,512)):
            frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
            frame=_economy_logic_fields(state,frame,'target_y',mask)
            if not frame.status&4:
                frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',amount,True)
        frame=_lowbank_ui_append_fields(state,frame,low16(frame.target_x))
        frame=_lowbank_ui_counter_fields(frame,'choice')
        if low16(frame.choice)==65535:
            break
    frame=_movement_restore_longs(state,frame,saved)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF31E,1)


def lowbank_process_device_control_2_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3B34 publishes negated vertical position and two real VDP command/data pairs."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF316,2),16)
    frame=_window_neg_word_fields(state,frame,'target_x')
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF318,low16(frame.target_x))
    frame=_lowbank_ui_store_fields(state,frame,0xC00004,0x40000010,4)
    frame=_lowbank_ui_store_fields(state,frame,0xC00000,state.read(0xFFFFF312,4),4)
    frame=_lowbank_ui_store_fields(state,frame,0xC00004,0x7C000002,4)
    return _lowbank_ui_store_fields(state,frame,0xC00000,state.read(0xFFFFF316,4),4)


def _window_leave_intro_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """3CA6 is the same owner's real control tail, without a new CALL."""
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x200)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF352,0,2,True)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF35E,0x160)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF360,0x100)
    frame=_lowbank_ui_call_fields(state,frame,0x15BE,0x3CC2)
    frame=_movement_move(state,frame,'target_x',31,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB00).cursor(),candidates=state.table_at(0xFFFFFB80).cursor())
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_movement_move(state,frame,'target_x',127,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB00).cursor())
    frame=_lowbank_ui_clear_cells_fields(state,frame,'target_x')
    frame=_movement_test(state,frame,state.read(0xFFFFF776,2),16)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,220)
    else:
        frame=_lowbank_ui_call_fields(state,frame,0x3E54,0x3CF8)
        frame=_lowbank_ui_call_fields(state,frame,0x8A60,0x3D00)
        for address,value in ((0xFFFFF376,255),(0xFFFF9F00,65535),(0xFFFFF36C,2)):
            frame=_lowbank_ui_store_fields(state,frame,address,value)
        frame=_lowbank_ui_call_fields(state,frame,0x9390,0x3D18)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF380,133)
    return _window_status_word_fields(state,frame,0x2700)


def _window_intro_literal_planes_fields(state: SceneState, frame: FirstDeploymentFrame,
        first_return: int, second_return: int) -> FirstDeploymentFrame:
    """Two actual decoder tails share their existing owner, never a copied bitmap codec."""
    for source,destination,continuation in ((0x65FF6,0xC000,first_return),(0x66199,0xC040,second_return)):
        frame=first_replace(frame,roster=state.table_at(source).cursor(),candidates=state.table_at(destination).cursor())
        frame=_movement_move_long(state,frame,'offset_x',128)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFF8000,0,2,True)
        frame=_movement_move(state,frame,'offset_y',16,16)
        frame=_lowbank_ui_call_fields(state,frame,0x3AAD6,continuation)
    return frame


def lowbank_process_device_control_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4178/3CA6 full introduction timeline, including both original descriptor packet loops."""
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x3A978,0x417E)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0xA00)
    if frame.status&1:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF32E,1)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFF8430,1)
    frame=_movement_test(state,frame,state.read(0xFFFFF32B,1),8)
    if not frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFF80C4,1),7)
        if not frame.status&4:
            return _window_leave_intro_fields(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x340)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
        frame=_economy_logic_fields(state,frame,'target_x',128,8)
        if not frame.status&4:
            frame=_window_status_word_fields(state,frame,0x2700)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32E,0x33E)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32C,32)
            frame=_movement_move(state,frame,'unit',state.read(0xFFFFF32C,2),16)
            frame=_lowbank_ui_call_fields(state,frame,0x3A00,0x41C4)
            frame=_window_status_word_fields(state,frame,0x2500)
    frame=_movement_test(state,frame,state.read(0xFFFF842E,2),16)
    if frame.status&4:
        frame=_window_compare_memory_fields(state,frame,0xFFFF8430,0x500)
        if frame.status&4:
            for address in (0xFFFF80CA,0xFFFF80CC,0xFFFF80CE,0xFFFF80D0):
                frame=_lowbank_ui_store_fields(state,frame,address,65535)
            frame=_movement_move_long(state,frame,'target_x',1)
            frame=_lowbank_ui_call_fields(state,frame,0x3AA38,0x41FA)
        frame=_window_compare_memory_fields(state,frame,0xFFFF8430,0x500)
        if not frame.status&1:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFF80C4,1),7)
            if not frame.status&4:
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,24)
                frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x303)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x300)
    if frame.status&1:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x280)
        if frame.status&1:
            return frame
        frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x280)
        if frame.status&4:
            frame=_window_status_word_fields(state,frame,0x2700)
            frame=_window_intro_literal_planes_fields(state,frame,0x425C,0x427C)
            frame=_window_status_word_fields(state,frame,0x2500)
        return _lowbank_ui_call_fields(state,frame,0x43BC,0x4284)
    frame=_movement_move(state,frame,'count',1,16)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32C,32)
    if frame.status&1:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF32C,2)
        frame=_window_compare_memory_fields(state,frame,0xFFFFF32C,16)
        if not frame.status&5:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF32C,2)
        frame=_movement_move(state,frame,'unit',state.read(0xFFFFF32C,2),16)
        frame=_lowbank_ui_call_fields(state,frame,0x3A00,0x42AE)
        frame=_movement_move(state,frame,'count',4,16)
    frame=_lowbank_ui_call_fields(state,frame,0x43BC,0x42B6)
    frame=_movement_save_longs(state,frame,('candidates',))
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x340)
    if frame.status&4:
        frame=_window_status_word_fields(state,frame,0x2700)
        frame=_window_intro_literal_planes_fields(state,frame,0x42E6,0x4306)
        frame=_window_status_word_fields(state,frame,0x2500)
    frame=_movement_restore_longs(state,frame,('candidates',))
    frame=first_replace(frame,roster=state.table_at(0x43A0).cursor())
    frame=_movement_move(state,frame,'distance',0xF0B,16)
    frame=_movement_move(state,frame,'target_y',0xE300,16)
    frame=_movement_move(state,frame,'choice',6,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,value)
        for value in (0x200,low16(frame.distance),low16(frame.target_y)):
            frame=_window_append_view_fields(state,frame,'candidates',value)
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'distance',1)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',16)
        frame=_lowbank_ui_counter_fields(frame,'choice')
        if low16(frame.choice)==65535:
            break
    frame=_lowbank_ui_call_fields(state,frame,0x4480,0x433A)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,0x340)
    if frame.status&1:
        return _lowbank_ui_store_fields(state,frame,frame.candidates.base,0,4)
    frame=_movement_test(state,frame,state.read(0xFFFF842E,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x45B6,0x434E)
        frame=_lowbank_ui_call_fields(state,frame,0x4400,0x4352)
        return _lowbank_ui_call_fields(state,frame,0x4420,0x4356)
    frame=_lowbank_ui_call_fields(state,frame,0x45B6,0x435C)
    return _lowbank_ui_call_fields(state,frame,0x4442,0x4360)


def lowbank_process_counted_records_3_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """43BC ten original descriptor records, with the live D7-dependent tile/stride adjustments."""
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,roster=state.table_at(0x4378).cursor(),candidates=state.table_at(0xFFFFF800).cursor())
    frame=_movement_move(state,frame,'target_x',0xD01,16)
    frame=_movement_move(state,frame,'target_y',0xE370,16)
    frame=_movement_move(state,frame,'choice',9,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,value)
        for value in (0x200,low16(frame.target_x),low16(frame.target_y)):
            frame=_window_append_view_fields(state,frame,'candidates',value)
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',8)
        frame=_movement_compare(state,frame,low16(frame.choice),6,16)
        if frame.status&1:
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_y',8)
        frame=_movement_compare(state,frame,low16(frame.choice),7,16)
        if frame.status&1:
            frame=_economy_logic_fields(state,frame,'target_x',0x200,16,'or')
        frame=_lowbank_ui_counter_fields(frame,'choice')
        if low16(frame.choice)==65535:
            return frame


def _window_copy_descriptor_cells_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: int, count: int, increment_distance: bool) -> FirstDeploymentFrame:
    frame=first_replace(frame,roster=state.table_at(source).cursor())
    frame=_movement_move(state,frame,'target_x',low16(frame.distance),16)
    frame=_economy_logic_fields(state,frame,'target_x',255)
    frame=_movement_move(state,frame,'choice',count,16)
    while True:
        value=frame.roster.word()
        frame=first_replace(frame,roster=frame.roster.advance(2))
        frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_window_append_view_fields(state,frame,'candidates',low16(frame.target_x))
        for position in (0,1):
            value=frame.roster.word()
            frame=first_replace(frame,roster=frame.roster.advance(2))
            frame=_window_append_view_fields(state,frame,'candidates',value)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',1)
        if increment_distance:
            frame=_lowbank_ui_arithmetic_fields(state,frame,'distance',1)
        frame=_lowbank_ui_counter_fields(frame,'choice')
        if low16(frame.choice)==65535:
            return frame


def lowbank_process_counted_records_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _window_copy_descriptor_cells_fields(state,_movement_frame(state,frame),0x44D8,12,False)


def lowbank_select_live_state_18_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,0x110)
    frame=_movement_test(state,frame,state.read(0xFFFF842A,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,frame.candidates.base,0x120)
    for offset,value in ((2,0),(4,0x6024),(6,0xF0)):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+offset),value)
    return frame


def lowbank_process_counted_records_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),5)
    if frame.status&4:
        frame=_window_copy_descriptor_cells_fields(state,frame,0x4526,14,False)
    for offset in (0,2,4,6):
        frame=_lowbank_ui_store_fields(state,frame,u32(frame.candidates.base+offset),0)
    return frame


def lowbank_process_counted_records_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_window_copy_descriptor_cells_fields(state,_movement_frame(state,frame),0x4580,8,True)
    frame=_movement_test(state,frame,state.read(0xFFFF843A,2),16)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFF843A,1)
    saved=('target_x','target_y','unit','count','distance','offset_x','offset_y','choice',
        'roster','candidates','controller','scan','opponent','scratch','auxiliary')
    frame=_movement_save_longs(state,frame,saved)
    frame=_window_status_word_fields(state,frame,0x2700)
    frame=first_replace(frame,roster=state.table_at(0x5CDE2).cursor(),candidates=state.table_at(0xCC8C).cursor())
    frame=_movement_move_long(state,frame,'offset_x',128)
    frame=_movement_move(state,frame,'offset_y',1,16)
    frame=_lowbank_ui_call_fields(state,frame,0x3AAB6,0x44CE)
    frame=_window_status_word_fields(state,frame,0x2500)
    return _movement_restore_longs(state,frame,saved)


def lowbank_coordinate_live_state_59_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFF80C4,1),7)
    if frame.status&4:
        return frame
    frame=_movement_test(state,frame,state.read(0xFFFF842E,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_call_fields(state,frame,0x90D8,0x45CC)
        if not frame.status&1:
            frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),0)
            change=not bool(frame.status&4)
            if not change:
                frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),1)
                change=not bool(frame.status&4)
            if change:
                frame=_window_memory_logic_fields(state,frame,0xFFFF842A,1,operation='xor',width=16)
                frame=_window_memory_logic_fields(state,frame,0xFFFF842A,1,operation='and',width=16)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF776,0,2,True)
        frame=_movement_test(state,frame,state.read(0xFFFF842A,2),16)
        if not frame.status&4:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF776,1)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
        frame=_economy_logic_fields(state,frame,'target_x',128,8)
        if frame.status&4:
            return frame
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32B,1,1)
        for address in (0xFFFF80CA,0xFFFF80CC,0xFFFF80CE,0xFFFF80D0):
            frame=_lowbank_ui_store_fields(state,frame,address,65535)
        frame=_movement_move_long(state,frame,'target_x',1)
        return _lowbank_ui_call_fields(state,frame,0x3AA38,0x4634)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',128,8)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFF842E,1)
    frame=_movement_move(state,frame,'target_x',0xAC,8)
    return _lowbank_ui_call_fields(state,frame,0x808A,0x4652)


def lowbank_process_device_control_5_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,24)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF612,0x303)
    return _lowbank_ui_store_fields(state,frame,0xC00004,0x8B00)


def _window_restart_intro_fields(state: SceneState, frame: FirstDeploymentFrame,
        continuation: int) -> FirstDeploymentFrame:
    for address,value in ((0xFFFFF600,16),(0xFFFFF612,0x300),(0xFFFF842A,0),
            (0xFFFF842C,0),(0xFFFF842E,0),(0xFFFF8430,0),(0xFFFF843A,0)):
        frame=_lowbank_ui_store_fields(state,frame,address,value)
    frame=_window_status_word_fields(state,frame,0x2700)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32E,0x33E)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32C,32)
    frame=_movement_move(state,frame,'unit',state.read(0xFFFFF32C,2),16)
    frame=_lowbank_ui_call_fields(state,frame,0x3A00,continuation)
    return _window_status_word_fields(state,frame,0x2500)


def _window_exit_countdown_fields(state: SceneState, frame: FirstDeploymentFrame,
        fade_return: int, restart_return: int) -> FirstDeploymentFrame:
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF32E,1)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF32E,64)
    if not frame.status&1:
        return _window_restart_intro_fields(state,frame,restart_return)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&1:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,4)
    return _lowbank_ui_call_fields(state,frame,0x3966,fade_return)


def lowbank_coordinate_live_state_60_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF32B,1),8)
    if not frame.status&4:
        return _window_exit_countdown_fields(state,frame,0x46F8,0x473C)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,4)
    for position,child,continuation in ((0xFFFFF344,0x354DE,0x4696),(0xFFFFF346,0x3557C,0x46AE)):
        frame=_movement_move(state,frame,'target_x',state.read(position,2),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF316,2),16)
        if frame.status&4:
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',24,True)
            frame=_lowbank_ui_store_fields(state,frame,position,low16(frame.target_x))
            frame=_lowbank_ui_call_fields(state,frame,child,continuation)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF316,1,True)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF316,0xFCA0)
    if frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF612,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,4)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF348,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF34C,15)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFFB80,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFFBA0,0,2,True)
    return frame


def lowbank_coordinate_live_state_61_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_test(state,frame,state.read(0xFFFFF32B,1),8)
    if not frame.status&4:
        return _window_exit_countdown_fields(state,frame,0x47D4,0x4818)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,4)
    frame=_movement_move(state,frame,'target_y',32,16)
    frame=first_replace(frame,roster=state.table_at(0xFFFFFB80).cursor())
    frame=_window_compare_memory_fields(state,frame,0xFFFFF34C,16)
    if frame.status&1:
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF34C,2),16)
        frame=_lowbank_ui_call_fields(state,frame,0xDEA6,0x4772)
    elif frame.status&4:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF348,6)
        if frame.status&4:
            return _lowbank_ui_known_child_fields(state,frame,0x206)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF600,28)
    else:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF34C,33)
        if not frame.status&1:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF34C,0,2,True)
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,0x1C0)
        else:
            frame=_movement_move(state,frame,'target_x',32,16)
            frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',state.read(0xFFFFF34C,2),True)
            frame=_lowbank_ui_call_fields(state,frame,0xDEA6,0x47AE)
    return _lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF34C,1)


def _window_lsr_word_six_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """483E LSR.W #6,D0: retain the high WORD; X/C are the original bit five."""
    value=low16(frame.target_x)
    result=value>>6
    carry=(value>>5)&1
    status=(17 if carry else 0)|(8 if result&0x8000 else 0)|(4 if result==0 else 0)
    state.sr=(state.sr&65504)|status
    return first_replace(frame,target_x=replace_word(frame.target_x,result),status=status)


def lowbank_process_device_control_6_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """481E interrupt entry owns fifteen LONG saves and its real RTE, not an ordinary child RTS."""
    frame=_movement_frame(state,frame)
    saved=('target_x','target_y','unit','count','distance','offset_x','offset_y','choice',
        'roster','candidates','controller','scan','opponent','scratch','auxiliary')
    frame=_movement_save_longs(state,frame,saved)
    frame=_movement_test(state,frame,state.read(0xFFFFF612,1),8)
    if not frame.status&4:
        frame=_movement_move(state,frame,'target_x',state.read(0xC00004,2),16)
        frame=_movement_move(state,frame,'target_x',state.read(0xC00004,2),16)
        frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,3)
        if not frame.status&4:
            frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF612,2),16)
            frame=_window_lsr_word_six_fields(state,frame)
            frame=_economy_logic_fields(state,frame,'target_x',0xFFFC)
            frame=_lowbank_ui_call_fields(state,frame,u32(0x4854+s16(low16(frame.target_x))),0x4848)
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF320,1)
    frame=_lowbank_ui_call_fields(state,frame,0x83D4,0x4852)
    frame=_movement_restore_longs(state,frame,saved)
    # No ordinary caller owns these interrupt words. Read the real exception
    # frame, then report the unbound control transfer instead of fake RTS.
    status=frame.stack_cursor.word()
    target=frame.stack_cursor.long(2)
    frame=first_replace(frame,stack_cursor=frame.stack_cursor.advance(6),status=status&31)
    state.set_status_word(status)
    raise MovementContinuationBoundary(target,frame,'real 4856 RTE target/context is not an ordinary Lowbank child return')


def _window_dma_prefix_fields(state: SceneState, frame: FirstDeploymentFrame,
        alternate: bool) -> FirstDeploymentFrame:
    """Two closed original DMA prefixes retain their actual bus and status reads."""
    frame=first_replace(frame,auxiliary=state.table_at(0xC00004).cursor())
    frame=_movement_move(state,frame,'choice',state.read(0xFFFFF606,2),16)
    frame=_economy_logic_fields(state,frame,'choice',16,8,'or')
    frame=_lowbank_ui_store_fields(state,frame,frame.auxiliary.base,low16(frame.choice))
    frame=_lowbank_ui_store_fields(state,frame,0xA11100,0x100)
    for value,size in (((0x94019340,4),(0x96FC9500,4),(0x977F,2),(0x7800,2)) if alternate
            else ((0x94009340,4),(0x96FD9580,4),(0x977F,2),(0xC000,2))):
        frame=_lowbank_ui_store_fields(state,frame,frame.auxiliary.base,value,size)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF620,0x82 if alternate else 0x80)
    frame=_lowbank_ui_store_fields(state,frame,frame.auxiliary.base,state.read(0xFFFFF620,2))
    frame=_movement_test(state,frame,state.read(0xFF3F00 if alternate else 0xFFFF3F00,1),8)
    if frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xA11100,0)
    return _lowbank_ui_store_fields(state,frame,frame.auxiliary.base,state.read(0xFFFFF606,2))


def lowbank_process_device_control_4_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4860 BRA to full 40B0 hardware/update parent; never push a JMP continuation."""
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',96,16)
    while True:
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_call_fields(state,frame,0x4890,0x40BE)
    frame=_window_dma_prefix_fields(state,frame,False)
    frame=_lowbank_ui_call_fields(state,frame,0x3B34,0x410C)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_economy_logic_fields(state,frame,'target_x',64,8,'or')
    frame=_lowbank_ui_store_fields(state,frame,0xC00004,low16(frame.target_x))
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF603,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',0xF0)
    requested=not bool(frame.status&4)
    if requested:
        frame=_movement_test(state,frame,state.read(0xFFFFF32B,1),8)
        requested=bool(frame.status&4)
    if requested:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF612,0x300)
        requested=not bool(frame.status&4)
    if requested:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF612,0x301)
        requested=not bool(frame.status&4)
    if requested:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32B,1,1)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF608,0,2,True)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFF842C,0,2,True)
        frame=_movement_move(state,frame,'target_x',0xAC,8)
        frame=_lowbank_ui_call_fields(state,frame,0x808A,0x4156)
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF32E,0,2,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF612,2),16)
    frame=_economy_logic_fields(state,frame,'target_x',255)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_movement_move(state,frame,'target_x',state.read(u32(0x416E+s16(low16(frame.target_x))),2),16)
    return _lowbank_ui_call_fields(state,frame,u32(0x4178+s16(low16(frame.target_x))),0x416C)


def lowbank_process_device_control_9_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_window_dma_prefix_fields(state,_movement_frame(state,frame),True)
    frame=_lowbank_ui_call_fields(state,frame,0x4A16,0x4990)
    return _lowbank_ui_call_fields(state,frame,0xAD06,0x4996)


def lowbank_coordinate_live_state_62_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x9508,0x49DC)


def lowbank_select_live_state_19_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_known_child_fields(state,_movement_frame(state,frame),0xF10)


def lowbank_coordinate_live_state_63_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x18CB4,0x49E4)


def lowbank_coordinate_live_state_64_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x3A536,0x49EC)
    return _lowbank_ui_call_fields(state,frame,0xA3DA,0x49F2)


def lowbank_coordinate_live_state_65_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x28936,0x4A14)


def lowbank_coordinate_live_state_66_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    return _lowbank_ui_call_fields(state,_movement_frame(state,frame),0x2B2FE,0x4A32)


def _window_vdp_commit_exit_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_economy_logic_fields(state,frame,'target_x',64,8,'or')
    frame=_lowbank_ui_store_fields(state,frame,0xC00004,low16(frame.target_x))
    return _lowbank_ui_store_fields(state,frame,0xFFFFF612,0,2,True)


def lowbank_process_device_control_7_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x3A89C,0x49FA)
    return _window_vdp_commit_exit_fields(state,frame)


def lowbank_process_device_control_8_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_lowbank_ui_call_fields(state,_movement_frame(state,frame),0x4890,0x4A38)
    return _window_vdp_commit_exit_fields(state,frame)


def lowbank_select_live_state_20_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """4A4C original masked-interrupt infinite loop; never present a fabricated RTS."""
    frame=_movement_frame(state,frame)
    while True:
        frame=_window_status_word_fields(state,frame,0x2700)


def lowbank_coordinate_live_state_67_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_call_fields(state,frame,0x4D54,0x4CFE)
    frame=_lowbank_ui_call_fields(state,frame,0x4D98,0x4D02)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),4)
    if not frame.status&4:
        frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,2)
        return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)
    frame=_movement_test(state,frame,state.read(0xFFFFCFD2,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFCFD2,1,True)
        frame=_window_compare_memory_fields(state,frame,0xFFFFCFD2,8)
        if not frame.status&5:
            frame=_lowbank_ui_store_fields(state,frame,0xFFFFCFD2,8)
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if frame.status&4:
        return frame
    frame=_lowbank_ui_call_fields(state,frame,0xC0B6,0x4D46)
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF362,3)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF36A,18)


def lowbank_select_live_state_21_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',3)
    if frame.status&4:
        return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    if not frame.status&4:
        return frame
    frame=_lowbank_ui_bit_fields(state,frame,frame.target_x,1)
    if frame.status&4:
        frame=_movement_test(state,frame,state.read(0xFFFFF3B4,2),16)
        if frame.status&4:
            return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3B4,1,True)
    else:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3B4,1)
        frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3B4,2),16)
        frame=_movement_compare(state,frame,low16(frame.target_x),state.read(0xFFFFF3B2,2),16)
        if not frame.status&1:
            frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF3B4,1,True)
            return _lowbank_ui_store_fields(state,frame,0xFFFFF608,1)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF608,12)


def lowbank_coordinate_live_state_68_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),5)
    if not frame.status&4:
        return frame
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF602,1),8)
    frame=_economy_logic_fields(state,frame,'target_x',3)
    if frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF321,1),3)
        if not frame.status&4:
            return frame
    frame=first_replace(frame,roster=state.table_at(0x4DD6).cursor())
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF3B4,2),16)
    frame=_movement_move(state,frame,'target_y',low16(frame.target_x),16)
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',1)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',low16(frame.target_y))
    frame=_lowbank_ui_shift_fields(state,frame,'target_x',3)
    frame=_lowbank_ui_arithmetic_fields(state,frame,'target_x',64)
    frame=_movement_move(state,frame,'target_y',120,16)
    return _lowbank_ui_call_fields(state,frame,0xAC08,0x4DD4)


def _window_write_font_fields(state: SceneState, frame: FirstDeploymentFrame,
        source: int, count: int, continuation: int) -> FirstDeploymentFrame:
    frame=first_replace(frame,roster=state.table_at(source).cursor())
    frame=_movement_move(state,frame,'count',count,16)
    return _lowbank_ui_call_fields(state,frame,0xAE8A,continuation)


def lowbank_coordinate_live_state_69_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_window_write_font_fields(state,_movement_frame(state,frame),0x8A1F4,3,0x50D6)
    return _movement_move(state,frame,'distance',127,16)


def lowbank_process_device_control_10_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF612,0x20A)
    if frame.status&4:
        frame=_window_write_font_fields(state,frame,0x8A380,2,0x5144)
        return _movement_move(state,frame,'distance',95,16)
    frame=first_replace(frame,auxiliary=state.table_at(0xC00000).cursor(),candidates=state.table_at(0xFFFFD300).cursor())
    frame=_movement_move(state,frame,'unit',1,16)
    frame=_movement_move(state,frame,'count',0,16)
    frame=_movement_move(state,frame,'distance',0,16)
    frame=_movement_move(state,frame,'offset_y',0,16)
    frame=first_replace(frame,controller=state.table_at(0xFFFFF578))
    while True:
        frame=_movement_move(state,frame,'offset_x',0,16)
        frame=_movement_move(state,frame,'offset_x',frame.controller.byte(),8)
        frame=first_replace(frame,controller=frame.controller.advance(1),scan=state.table_at(0x5149))
        frame=_movement_move(state,frame,'offset_x',frame.scan.byte(low16(frame.offset_x)),8)
        frame=_movement_move(state,frame,'offset_x',u16(s8(low8(frame.offset_x))),16)
        frame=_lowbank_ui_shift_fields(state,frame,'offset_x',2)
        frame=first_replace(frame,roster=state.table_at(0x8A304).cursor())
        frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.offset_x))))
        frame=_movement_move(state,frame,'count',1,16)
        frame=_lowbank_ui_call_fields(state,frame,0xAE8A,0x5120)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'distance',64)
        frame=_lowbank_ui_arithmetic_fields(state,frame,'offset_y',1)
        frame=_lowbank_ui_counter_fields(frame,'unit')
        if low16(frame.unit)==65535:
            break
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF390,low16(frame.offset_y))
    return _lowbank_ui_arithmetic_fields(state,frame,'distance',1,True)


def lowbank_coordinate_live_state_70_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_window_write_font_fields(state,_movement_frame(state,frame),0x6BF0A,1,0x5174)
    frame=_movement_move(state,frame,'count',state.read(0xFFFFF65A,2),16)
    frame=_lowbank_ui_shift_fields(state,frame,'count',2)
    frame=first_replace(frame,roster=state.table_at(0x6BF0E).cursor())
    frame=first_replace(frame,roster=frame.roster.advance(s16(low16(frame.count))))
    frame=_movement_move(state,frame,'count',1,16)
    frame=_lowbank_ui_call_fields(state,frame,0xAE8A,0x518C)
    return _movement_move(state,frame,'distance',127,16)


def lowbank_coordinate_live_state_71_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_window_compare_memory_fields(state,frame,0xFFFFF38C,161)
    special=bool(frame.status&4)
    if not special:
        frame=_window_compare_memory_fields(state,frame,0xFFFFF612,0x209)
        if frame.status&4:
            frame=_window_compare_memory_fields(state,frame,0xFFFFF362,5)
            special=bool(frame.status&4)
            if not special:
                frame=_window_compare_memory_fields(state,frame,0xFFFFF362,6)
                special=bool(frame.status&4)
    if special:
        frame=_window_write_font_fields(state,frame,0x8A386,2,0x51CA)
        return _movement_move(state,frame,'distance',95,16)
    frame=_window_write_font_fields(state,frame,0x6BF0A,1,0x51E2)
    frame=first_replace(frame,roster=state.table_at(0x6BF1A).cursor())
    frame=_window_compare_memory_fields(state,frame,0xFFFFF65A,18)
    if frame.status&4:
        frame=first_replace(frame,roster=frame.roster.advance(4))
    frame=_movement_move(state,frame,'count',1,16)
    frame=_lowbank_ui_call_fields(state,frame,0xAE8A,0x51FE)
    return _movement_move(state,frame,'distance',127,16)


def lowbank_process_device_control_11_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    frame=_movement_frame(state,frame)
    frame=_movement_move(state,frame,'target_x',128,16)
    while True:
        frame=_lowbank_ui_counter_fields(frame,'target_x')
        if low16(frame.target_x)==65535:
            break
    frame=_lowbank_ui_call_fields(state,frame,0x4890,0x9516)
    frame=_lowbank_ui_call_fields(state,frame,0x4998,0x951C)
    frame=_movement_test(state,frame,state.read(0xFFFFF608,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_memory_arithmetic_fields(state,frame,0xFFFFF608,1,True)
    frame=_movement_move(state,frame,'target_x',state.read(0xFFFFF606,2),16)
    frame=_economy_logic_fields(state,frame,'target_x',64,8,'or')
    frame=_lowbank_ui_store_fields(state,frame,0xC00004,low16(frame.target_x))
    frame=_lowbank_ui_call_fields(state,frame,0x949E,0x953A)
    frame=_movement_test(state,frame,state.read(0xFFFFF608,2),16)
    if not frame.status&4:
        frame=_lowbank_ui_bit_fields(state,frame,state.read(0xFFFFF603,1),7)
        if frame.status&4:
            return frame
    frame=_lowbank_ui_store_fields(state,frame,0xFFFFF600,12)
    return _lowbank_ui_store_fields(state,frame,0xFFFFF776,0,2,True)




def lowbank_select_live_state_36_fields(state: SceneState, frame: FirstDeploymentFrame) -> FirstDeploymentFrame:
    """11122: per-city ordered candidate triples and actual alternative trait tests."""
    from .services import _movement_fixed_shift_word
    frame=_movement_frame(state,frame)
    frame=first_replace(frame,candidates=state.table_at(state.read(u32(frame.auxiliary.base+16),4)).cursor())
    frame=_movement_move(state,frame,'distance',low16(frame.target_x),16)
    frame=_movement_fixed_shift_word(state,frame,'distance',1)
    frame=_movement_move(state,frame,'distance',frame.candidates.word(low16(frame.distance)),16)
    frame=first_replace(frame,candidates=state.table_at(state.read(u32(frame.auxiliary.base+20),4)).cursor())
    frame=first_replace(frame,candidates=frame.candidates.advance(s16(low16(frame.distance))),controller=state.table_at(0xFFFFCC00),scan=state.table_at(0xFFFFF427).cursor())
    while True:
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'distance',value,16)
        if frame.status&8:
            break
        frame=_movement_compare(state,frame,low8(frame.distance),state.read(0xFFFFF374,1),8)
        if not frame.status&5:
            break
        value=frame.candidates.word()
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
        frame=_movement_move(state,frame,'distance',value,16)
        allowed=not bool(frame.status&8)
        if allowed:
            frame=_movement_compare(state,frame,low16(frame.distance),222,16)
            if frame.status&4:
                frame=_movement_compare(state,frame,state.read(0xFFFFF374,1),5,8)
                allowed=bool(frame.status&5)
        if allowed:
            frame=_movement_test(state,frame,frame.controller.byte(low16(frame.distance)),8)
            allowed=bool(frame.status&4)
        if allowed:
            frame=_movement_move(state,frame,'offset_x',frame.candidates.word(),16)
            if not frame.status&8:
                frame=_economy_register_bit_fields(state,frame,'offset_x',14)
                if frame.status&4:
                    frame=_movement_move(state,frame,'offset_x',frame.controller.byte(low16(frame.offset_x)),8)
                    frame=_economy_logic_fields(state,frame,'offset_x',255)
                    frame=_movement_compare(state,frame,low8(frame.count),frame.scan.byte(low16(frame.offset_x)),8)
                else:
                    frame=_movement_compare(state,frame,low8(frame.offset_x),low8(frame.count),8)
                allowed=bool(frame.status&4)
        if allowed:
            frame=_lowbank_ui_append_fields(state,frame,low16(frame.distance))
            frame=_economy_delta_fields(state,frame,'unit',1)
        frame=first_replace(frame,candidates=frame.candidates.advance(2))
    return frame
