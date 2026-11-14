"""Explicit finite original narrative-reset plans; imports have no game effects."""
import json
from pathlib import Path

from .config import ConfigurationError, _object, _list, _integer, _path, _no_duplicate_keys
from .intro_restart_config import MAX_JSON_BYTES, MAX_PLANS, MAX_CLOCK


FORMAT = 'g5510-original-narrative-restart-plans-v1'


def _read_narrative_restart_plans(path):
    if not isinstance(path, (str, Path)):
        raise ConfigurationError('剧情复位计划必须是调用者明确指定的文件路径。')
    source = _path(str(path), Path.cwd(), 'narrative_restarts', existing='file')
    with source.open('rb') as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ConfigurationError('剧情复位计划超过明确的64KiB文件上限。')
    try:
        row = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError('剧情复位计划不是有效的UTF-8 JSON：' + str(source)) from error
    _object(row, ('format', 'plans'), 'narrative_restarts')
    if row['format'] != FORMAT:
        raise ConfigurationError('剧情复位计划format不匹配；不能将片头IRQ计划当作剧情跳转计划。')
    rows = _list(row['plans'], 'narrative_restarts.plans')
    if not 1 <= len(rows) <= MAX_PLANS:
        raise ConfigurationError('必须明确提供1..256项有限剧情复位计划；没有自动补充。')
    # Reuse only the existing typed supply contract, not its IRQ restart owner.
    from .intro_restart import IntroRestartSpec
    plans = []
    for index, item in enumerate(rows):
        context = 'narrative_restarts.plans[' + str(index) + ']'
        _object(item, ('reset_pulse_clocks', 'irq_clock_hz', 'startup_im1_offsets'), context)
        pulses = _list(item['reset_pulse_clocks'], context + '.reset_pulse_clocks')
        offsets = _list(item['startup_im1_offsets'], context + '.startup_im1_offsets')
        if len(pulses) != 2 or len(offsets) != 3:
            raise ConfigurationError(context + '必须提供恰好两次RESET脉冲和三次启动IM1时刻偏移。')
        pulse_values = tuple(_integer(value, context + '.reset_pulse_clocks', 3, MAX_CLOCK) for value in pulses)
        irq_clock_hz = _integer(item['irq_clock_hz'], context + '.irq_clock_hz', 1, MAX_CLOCK)
        offset_values = tuple(_integer(value, context + '.startup_im1_offsets', 1, MAX_CLOCK) for value in offsets)
        if any(left >= right for left, right in zip(offset_values, offset_values[1:])):
            raise ConfigurationError(context + '.startup_im1_offsets必须严格递增。')
        plans.append(IntroRestartSpec(pulse_values, irq_clock_hz, offset_values))
    return source, tuple(plans)


def load_narrative_restart_plans(path):
    """Read a supplied plan only; no default path, pulse, device event or timestamp."""
    return _read_narrative_restart_plans(path)[1]


def enable_configured_narrative_restarts(app, path):
    """Bind after fresh App.open, before any operation; no mixed pulse ordering."""
    from .application import GameApplication
    from .narrative_restart import enable_narrative_restarts
    if type(app) is not GameApplication or app.operations != 0:
        raise ConfigurationError('剧情复位计划只能在新应用打开后、任何运行操作之前绑定。')
    if getattr(app, 'ordered_restarts', None) is not None:
        raise ConfigurationError('联合复位计划已绑定，不能追加互斥的旧剧情计划。')
    if getattr(app, 'intro_restarts', None) is not None:
        raise ConfigurationError('剧情与片头IRQ复位计划目前必须明确择一，不能猜测两类脉冲顺序。')
    source, plans = _read_narrative_restart_plans(path)
    owner = enable_narrative_restarts(app, plans=plans)
    owner.configuration_source = str(source)
    return owner


def describe_narrative_restart_owner(owner):
    """Small declaration and observations, without reading RAM, devices or assets."""
    from .narrative_restart import NarrativeRestartOwner
    if type(owner) is not NarrativeRestartOwner:
        raise ConfigurationError('必须是实际绑定的同应用剧情复位所有者。')
    return dict(format=FORMAT, source=getattr(owner, 'configuration_source', None),
        plans=[dict(reset_pulse_clocks=list(plan.reset_pulse_clocks), irq_clock_hz=plan.irq_clock_hz,
            startup_im1_offsets=list(plan.startup_im1_offsets)) for plan in owner.plans],
        explicit_opt_in=True, default_automatic_restart=False,
        intro_restart_protocol_widened=False, other_event_budgets_extended=False,
        actual_restart_owner=owner.diagnostics())
