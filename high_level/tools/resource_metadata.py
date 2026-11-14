"""Compare the structural fields of editable resource packages."""
from tools.resource_reference import reference_pattern


def compare_fixed_fields(row, expected, editable, label):
    """Validate metadata with exact field types and values."""
    if type(row) is not dict or row.keys() != set(expected) | set(editable):
        raise ValueError(f"{label}: fields differ")
    compare({key: row[key] for key in expected}, expected, label)


def compare(value, expected, label):
    """Validate typed metadata, including the shape of optional source references."""
    if type(value) is not type(expected):
        raise ValueError(f"{label}: field type differs")
    if type(expected) is dict:
        if value.keys() != expected.keys():
            raise ValueError(f"{label}: fields differ")
        for key in expected:
            compare(value[key], expected[key], f"{label}.{key}")
    elif type(expected) in (list, tuple):
        if len(value) != len(expected):
            raise ValueError(f"{label}: element count differs")
        for index, (item, other) in enumerate(zip(value, expected)):
            compare(item, other, f"{label}[{index}]")
    elif value != expected:
        pattern = reference_pattern(expected)
        if pattern is None or not pattern.fullmatch(value):
            raise ValueError(f"{label}: field value differs")
