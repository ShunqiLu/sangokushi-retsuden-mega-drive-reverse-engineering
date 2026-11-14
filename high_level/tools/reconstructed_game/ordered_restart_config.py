"""External ordered reset plans with explicit warm/cold paths; no game on import."""
import json
from pathlib import Path

from .config import ConfigurationError, _object, _list, _integer, _path, _no_duplicate_keys
from .intro_restart_config import MAX_JSON_BYTES, MAX_PLANS, MAX_CLOCK


FORMAT = 'g5510-original-ordered-restart-plans-v2'
LEGACY_FORMAT = 'g5510-original-ordered-restart-plans-v1'


def _read_ordered_restart_plans(path):
    if not isinstance(path, (str, Path)):
        raise ConfigurationError('联合复位计划必须是调用者明确指定的文件路径。')
    source = _path(str(path), Path.cwd(), 'restarts', existing='file')
    with source.open('rb') as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ConfigurationError('联合复位计划超过明确的64KiB文件上限。')
    try:
        row = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError('联合复位计划不是有效的UTF-8 JSON：' + str(source)) from error
    _object(row, ('format','plans'), 'restarts')
    if row['format'] not in (FORMAT, LEGACY_FORMAT):
        raise ConfigurationError('联合计划format不匹配，不能按文件内容猜测重启类型。')
    legacy = row['format'] == LEGACY_FORMAT
    rows = _list(row['plans'], 'restarts.plans')
    if not 1 <= len(rows) <= MAX_PLANS:
        raise ConfigurationError('必须明确提供1..256项有序有限复位计划。')
    from .intro_restart import IntroRestartSpec
    from .ordered_restart import ColdRestartSpec, OrderedRestartPlan
    plans = []
    for index, item in enumerate(rows):
        context = 'restarts.plans[' + str(index) + ']'
        fields = ('kind','reset_pulse_clocks','irq_clock_hz','startup_im1_offsets')
        _object(item, fields if legacy else fields + ('reset_path',), context)
        if type(item['kind']) is not str or item['kind'] not in ('intro','narrative'):
            raise ConfigurationError(context+'.kind必须明确为intro或narrative。')
        # Version1 has only its original strict warm contract. Pulse length
        # never determines a reset path; version2 must declare it explicitly.
        reset_path = 'warm' if legacy else item['reset_path']
        if type(reset_path) is not str or reset_path not in ('warm','cold'):
            raise ConfigurationError(context+'.reset_path必须明确为warm或cold。')
        pulses = _list(item['reset_pulse_clocks'], context+'.reset_pulse_clocks')
        offsets = _list(item['startup_im1_offsets'], context+'.startup_im1_offsets')
        pulse_count = 2 if reset_path == 'warm' else 3
        if len(pulses) != pulse_count or len(offsets) != 3:
            raise ConfigurationError(context+'的'+reset_path+'计划必须提供恰好'
                +str(pulse_count)+'次RESET脉冲和三次启动IM1时刻偏移。')
        values = tuple(_integer(value, context+'.reset_pulse_clocks', 3, MAX_CLOCK) for value in pulses)
        clock = _integer(item['irq_clock_hz'], context+'.irq_clock_hz', 1, MAX_CLOCK)
        stamps = tuple(_integer(value, context+'.startup_im1_offsets', 1, MAX_CLOCK) for value in offsets)
        if any(left >= right for left, right in zip(stamps, stamps[1:])):
            raise ConfigurationError(context+'.startup_im1_offsets必须严格递增。')
        supply = IntroRestartSpec(values, clock, stamps) if reset_path == 'warm' else ColdRestartSpec(values, clock, stamps)
        plans.append(OrderedRestartPlan(item['kind'], supply, reset_path=reset_path))
    return source, tuple(plans)


def load_ordered_restart_plans(path):
    """No default path, kind, RESET clocks, event count or timestamp."""
    return _read_ordered_restart_plans(path)[1]


def enable_configured_ordered_restarts(app, path):
    from .application import GameApplication
    from .ordered_restart import enable_ordered_restarts
    if type(app) is not GameApplication or app.operations != 0:
        raise ConfigurationError('联合复位计划只能在新应用打开后、任何运行操作之前绑定。')
    source, plans = _read_ordered_restart_plans(path)
    owner = enable_ordered_restarts(app, plans=plans)
    owner.configuration_source = str(source)
    return owner


def describe_ordered_restart_owner(owner):
    """Finite declarations and actual counters only; no game RAM or chip read."""
    from .ordered_restart import OrderedRestartOwner
    if type(owner) is not OrderedRestartOwner:
        raise ConfigurationError('必须是实际绑定的同应用有序联合复位所有者。')
    return dict(format=FORMAT, source=getattr(owner, 'configuration_source', None),
        plans=[dict(kind=row.kind, reset_path=row.reset_path,
            reset_pulse_clocks=list(row.supply.reset_pulse_clocks),
            reset_pulse_count=len(row.supply.reset_pulse_clocks),
            irq_clock_hz=row.supply.irq_clock_hz, startup_im1_offsets=list(row.supply.startup_im1_offsets))
            for row in owner.steps],
        explicit_opt_in=True, automatic_kind_selection=False, automatic_supply_refill=False,
        original_intro_and_narrative_protocols_distinct=True, other_event_budgets_extended=False,
        actual_restart_owner=owner.diagnostics())
