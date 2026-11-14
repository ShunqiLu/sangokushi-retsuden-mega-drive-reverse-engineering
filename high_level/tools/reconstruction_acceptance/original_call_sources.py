"""Pure explicit original-CALL text parsing, without executable bindings.

Only the existing three direct CALL spellings and their fixed widths are
recognized. Unsupported cells remain rejected; no source or width is guessed.
"""
from pathlib import Path
import re


class OriginalCallSourceError(ValueError):
    """An explicit original source violates the finite text-parser contract."""


def _require(condition, message):
    if not condition:
        raise OriginalCallSourceError(message)


def read_original_call_sources(paths, wanted):
    """Read selected CALL cells, or explicitly enumerate calls with wanted=None.

    Enumeration still uses these same three decoders. Other CALL spellings are
    rejected; ordinary non-CALL instructions are not fabricated as failures or
    candidates. Existing explicit-address requests retain their old behavior.
    """
    found, rejected = {}, {}
    for supplied in paths:
        path = Path(supplied).resolve(strict=True)
        _require(path.suffix == '.s' and path.is_file() and path.stat().st_size <= 16_000_000,
            'bounded explicit editable original assembly required')
        address = None
        for number, raw in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            line = raw.split('|', 1)[0].strip()
            label = re.fullmatch(r'm68k_([0-9a-fA-F]{6}):', line)
            if label:
                address = int(label[1], 16)
                continue
            if not line or line.startswith('.') or line.endswith(':'):
                continue
            if address is not None and (wanted is None or address in wanted):
                relative = re.fullmatch(r'jsr\s+(-?[0-9]+)\(%pc\)', line)
                branch = re.fullmatch(r'bsr\.w\s+\(\.\s*\+\s*(-?[0-9]+)\)', line)
                absolute = re.fullmatch(r'jsr\s+0x([0-9a-fA-F]+):l', line)
                if relative:
                    target, width = address + 2 + int(relative[1]), 4
                elif branch:
                    target, width = address + int(branch[1]), 4
                elif absolute:
                    target, width = int(absolute[1], 16), 6
                else:
                    if wanted is None and not re.match(r'(?:jsr|bsr)(?:\.[a-z]+)?(?:\s|$)', line):
                        address = None
                        continue
                    rejected[address] = dict(source=str(path), line=number, statement=line,
                        reason='original cell is not a supported explicit direct CALL')
                    address = None
                    continue
                row = dict(source=str(path), line=number, statement=line, caller=address,
                    target=target, continuation=address + width,
                    physical_effect='original caller owns its one LONG; binding neither pushes nor pops it')
                _require(address not in found and address not in rejected,
                    'competing original CALL sources at ' + hex(address))
                found[address] = row
            address = None
    return found, rejected
