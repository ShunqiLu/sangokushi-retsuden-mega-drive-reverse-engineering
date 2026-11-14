"""Explicit external original-intro restart plans; import has no game effects.

This does not extend the runtime configuration schema. Callers opt in with a
separate path after a new application opens and before any frame operation.
"""
import json
from pathlib import Path

from .config import ConfigurationError, _object, _list, _integer, _path, _no_duplicate_keys


FORMAT = 'g5510-original-intro-restart-plans-v1'
MAX_JSON_BYTES = 65536
MAX_PLANS = 256
MAX_CLOCK = (1 << 63) - 1


def _read_intro_restart_plans(path):
    if not isinstance(path, (str, Path)):
        raise ConfigurationError('片头复位计划必须是调用者明确指定的文件路径。')
    source = _path(str(path), Path.cwd(), 'intro_restarts', existing='file')
    with source.open('rb') as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ConfigurationError('片头复位计划超过明确的64KiB文件上限。')
    try:
        row = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_no_duplicate_keys)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ConfigurationError('片头复位计划不是有效的UTF-8 JSON：' + str(source)) from error
    _object(row, ('format', 'plans'), 'intro_restarts')
    if row['format'] != FORMAT:
        raise ConfigurationError('片头复位计划format不匹配；不能加载其它事件或资源文件。')
    rows = _list(row['plans'], 'intro_restarts.plans')
    if not 1 <= len(rows) <= MAX_PLANS:
        raise ConfigurationError('必须明确提供1..256项有限复位计划；没有自动补充。')
    # This import and typed construction occur only for an explicit supplied
    # plan. No application, Scene, IRQ, clock grant or hardware is run here.
    from .intro_restart import IntroRestartSpec
    result = []
    for index, item in enumerate(rows):
        context = 'intro_restarts.plans[' + str(index) + ']'
        _object(item, ('reset_pulse_clocks', 'irq_clock_hz', 'startup_im1_offsets'), context)
        pulses = _list(item['reset_pulse_clocks'], context + '.reset_pulse_clocks')
        offsets = _list(item['startup_im1_offsets'], context + '.startup_im1_offsets')
        if len(pulses) != 2 or len(offsets) != 3:
            raise ConfigurationError(context + '必须提供恰好两次RESET脉冲和三次启动IM1时刻偏移。')
        pulse_values = tuple(_integer(value, context + '.reset_pulse_clocks', 3, MAX_CLOCK)
            for value in pulses)
        clock_hz = _integer(item['irq_clock_hz'], context + '.irq_clock_hz', 1, MAX_CLOCK)
        offset_values = tuple(_integer(value, context + '.startup_im1_offsets', 1, MAX_CLOCK)
            for value in offsets)
        if any(left >= right for left, right in zip(offset_values, offset_values[1:])):
            raise ConfigurationError(context + '.startup_im1_offsets必须严格递增，不能猜测或复用时刻。')
        result.append(IntroRestartSpec(pulse_values, clock_hz, offset_values))
    return source, tuple(result)


def load_intro_restart_plans(path):
    """Read one exact external plan; no default path, plans, pulse or timestamp."""
    return _read_intro_restart_plans(path)[1]


def enable_configured_intro_restarts(app, path):
    """Bind exactly once after fresh App.open, before any frame/audio operation."""
    from .application import GameApplication
    from .intro_restart import enable_intro_restarts
    if type(app) is not GameApplication or app.operations != 0:
        raise ConfigurationError('可选片头复位计划只能在新应用打开后、任何运行操作之前绑定。')
    if getattr(app, 'ordered_restarts', None) is not None:
        raise ConfigurationError('联合复位计划已绑定，不能追加互斥的旧片头计划。')
    source, plans = _read_intro_restart_plans(path)
    owner = enable_intro_restarts(app, plans=plans)
    owner.configuration_source = str(source)
    return owner


def describe_intro_restart_owner(owner):
    """Small exact declaration and live counters, without RAM or device reads."""
    from .intro_restart import OriginalIntroRestartOwner
    if type(owner) is not OriginalIntroRestartOwner:
        raise ConfigurationError('必须是实际绑定的同应用片头复位所有者。')
    return dict(format=FORMAT, source=getattr(owner, 'configuration_source', None),
        plans=[dict(reset_pulse_clocks=list(plan.reset_pulse_clocks), irq_clock_hz=plan.irq_clock_hz,
            startup_im1_offsets=list(plan.startup_im1_offsets)) for plan in owner.plans],
        explicit_opt_in=True, default_automatic_restart=False,
        other_frame_BUS_DMA_R_Busy_read_budgets_extended=False,
        actual_restart_owner=owner.diagnostics())
