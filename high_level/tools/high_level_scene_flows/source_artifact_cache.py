"""Current-epoch immutable source artifacts, never a live continuation cache.

Every caller supplies freshly read complete source and the actual transformer
CodeTypes/contracts. Only one epoch per family/module/group is retained. A miss
runs its original admission builder; errors are never hidden by an older hit.
"""
from pathlib import Path
from threading import RLock
from types import CodeType


_CURRENT = {}
_LOCK = RLock()
_SCALARS = (str, bytes, int, bool, float, complex, type(None))


def read_source_text(module):
    """Read the real whole file, preserving newlines; no linecache/mtime gate."""
    filename = module.__file__
    if type(filename) is not str or not filename:
        raise ValueError('an actual source module filename is required')
    with Path(filename).open('r', encoding='utf-8-sig', newline='') as stream:
        return filename, stream.read()


def _freeze(value):
    if type(value) in _SCALARS or type(value) is CodeType:
        return ('leaf', type(value), value)
    if type(value) is dict:
        return ('dict', tuple((_freeze(key), _freeze(item)) for key, item in value.items()))
    if type(value) in (list, tuple):
        return ('list' if type(value) is list else 'tuple', tuple(map(_freeze, value)))
    if type(value) in (set, frozenset):
        return ('set' if type(value) is set else 'frozenset', frozenset(map(_freeze, value)))
    raise ValueError('source artifacts may contain only CodeTypes and immutable declarations')


def _thaw(value):
    kind = value[0]
    if kind == 'leaf':
        return value[2]
    if kind == 'dict':
        return {_thaw(key): _thaw(item) for key, item in value[1]}
    items = (_thaw(item) for item in value[1])
    return {'list': list, 'tuple': tuple, 'set': set, 'frozenset': frozenset}[kind](items)


def _same_epoch(left, right):
    return (left[:2] == right[:2] and left[3] == right[3]
        and len(left[2]) == len(right[2])
        and all(before is after for before, after in zip(left[2], right[2])))


def get_source_artifacts(family, module_name, group, *, source_text, filename,
        transformer_codes, expected_contract, prepare):
    """Get fresh containers holding admitted immutable code, or build one miss.

    The builder is called but never retained. ASTs, functions, bound methods,
    modules, namespaces, Scenes and Frames cannot pass the artifact freezer.
    Source text is compared exactly; CodeType epoch members compare by identity.
    """
    if any(type(value) is not str or not value for value in (family, module_name, group, filename)):
        raise ValueError('explicit source artifact family/module/group/filename required')
    if type(source_text) is not str or type(transformer_codes) is not tuple:
        raise ValueError('fresh complete source text and transformer CodeType tuple required')
    if not transformer_codes or any(type(code) is not CodeType for code in transformer_codes):
        raise ValueError('actual transformer/validator CodeType identities required')
    epoch = filename, source_text, transformer_codes, _freeze(expected_contract)
    key = family, module_name, group
    with _LOCK:
        retained = _CURRENT.get(key)
    if retained is not None and _same_epoch(retained[0], epoch):
        return _thaw(retained[1])
    artifact = _freeze(prepare())
    with _LOCK:
        _CURRENT[key] = epoch, artifact
    return _thaw(artifact)
