# Original game behavior

[简体中文](ORIGINAL_GAME_BUGS.md) · [繁體中文](ORIGINAL_GAME_BUGS.zh-TW.md) · [日本語](ORIGINAL_GAME_BUGS.ja.md) · **English**

The reconstruction retains the following cartridge behaviors and edge cases, including counter wraparound, stale table entries, overwritten pointers, and partial writes. IDs identify the same cases across editions.

| ID | Original behavior |
| --- | --- |
| BUG-001 | A grain shipment total above the cap drops to 99,999. |
| BUG-002 | One city adjacency branch has an always-false match condition. |
| BUG-003 | Removing an adjacent candidate uses a shorter compaction range. |
| BUG-004 | AI pathfinding overwrites city table pointers still used by selection. |
| BUG-005 | Both adjacency cost reads use the grid index. |
| BUG-006 | The arriving unit's leader search stops at the next-to-last slot; removal skips moving the first entry. |
| BUG-007 | Faction roster cleanup uses the incremented source pointer and can erase an unread terminator. |
| BUG-008 | AI weapon purchase reads a BYTE but compares a WORD; a stale high byte can skip the purchase. |
| BUG-009 | AI weapon purchases write to the first officer slot. |
| BUG-010 | AI development discards the random ratio and budgets with four times the city ID. |
| BUG-011 | The training cap correction increases progress by more than the original increment. |
| BUG-012 | AI recruitment checks memory relative to the roster cursor instead of the troop table. |
| BUG-013 | The AI's third player ownership check uses the previous city selection instead of the current owner. |
| BUG-014 | Pathfinding keeps taking the search branch after exhausting the frontier. |
| BUG-015 | The AI city adjacency table contains two one-way links. |
| BUG-016 | An army resource decision ends at action 13; one path writes 12 earlier in the same call. |
| BUG-017 | Two random branch tests always return zero, but the RNG seed still changes. |
| BUG-018 | Strongest-enemy selection starts with the largest unsigned value. |
| BUG-019 | Every roster ID and the terminator overwrite the strength accumulator's low WORD. |
| BUG-020 | The city strength scan overwrites the target city with its officer counter. |
| BUG-021 | Army equipment purchase prepares the equipment pointer but writes to the attribute table. |
| BUG-022 | A missing city-linked officer leaves execution looping at one address. |
| BUG-023 | An economic support subroutine changes the base for later processed-city checks. |
| BUG-024 | The support roster appends after the old terminator. |
| BUG-025 | Army roster sorting uses the exhausted FFFF count as the WORD offset. |
| BUG-026 | A nonzero provisioning price LONG becomes zero as a WORD divisor. |
| BUG-027 | Marching costs for two officers use average speed directly as divisor, even when zero. |
| BUG-028 | Eight iterations clear the same slot before selecting the special battlefield tail group. |
| BUG-029 | Battlefield deduplication can scan past the candidate area into adjacent output. |
| BUG-030 | The battlefield budget reloads the old value after computing the quotient. |
| BUG-031 | Terrain filtering prepares a coordinate table pointer but reads from the map base. |
| BUG-032 | One battlefield budget formula uses the full updated RNG state. |
| BUG-033 | The officer ID scaled by four for coordinates is written back to the roster. |
| BUG-034 | Two roster reordering paths copy forward into adjacent overlapping memory. |
| BUG-035 | Roster training divides by the selected member count, even when zero. |
| BUG-036 | After reading the sprite size, the horizontal flip adjustment always equals 8. |
| BUG-037 | The second side's battlefield strength denominator repeats the B400 factor. |
| BUG-038 | The fixed-field save encoder writes a nonzero trailing byte at the input cursor. |
| BUG-039 | The first monthly event type runs the June branch twice. |
| BUG-040 | The postbattle total for the second city resource goes back to the battlefield buffer. |
| BUG-041 | Average speed for an empty army packet exhausts a WORD counter and passes zero to division. |
| BUG-042 | For certain totals, the scene headcount oscillates between 15 and 16. |
| BUG-043 | Offset 3 is the third extended vertical probe for object movement. |
| BUG-044 | Palette transformation loops when the low WORD exceeds 15. |
| BUG-045 | The second side's headcount can also oscillate between 15 and 16. |
| BUG-046 | An intervening MOVE overwrites the comparison flags for object pursuit. |
| BUG-047 | Loyalty aggregation reads a BYTE from the loyalty table and uses it as a packet offset. |
| BUG-048 | Loyalty aggregation uses its count directly as divisor, even when zero. |
| BUG-049 | Action budget divides directly by the officer's C400 attribute BYTE, even when zero. |

See the [cartridge address index](../PENDING_SOURCE_INDEX.en.md) and the [editing guide](../EDITING.en.md) for the corresponding code.
