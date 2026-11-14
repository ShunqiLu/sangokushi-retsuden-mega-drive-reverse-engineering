# Original game behavior

[简体中文](ORIGINAL_GAME_BUGS.md) · [繁體中文](ORIGINAL_GAME_BUGS.zh-TW.md) · [日本語](ORIGINAL_GAME_BUGS.ja.md) · **English**

These entries record operation order, field widths, and branch outcomes preserved by the assembly reconstruction. Instruction addresses are 68000 addresses in the linear cartridge image. Register and RAM addresses are noted separately. Whether a case occurs in play depends on the save, scene, and command inputs.

| ID | Behavior | Instruction address | Result |
| --- | --- | --- | --- |
| BUG-001 | Grain shipments over the cap | `01554A，015552` | The sum is compared with 999,999. Above it, grain is set to 99,999. The gold branch uses a cap of 999,999. |
| BUG-002 | Always-false city adjacency test | `016538，01653A，01653E` | The branch compares the original 16-bit value with that value minus 16, so equality is impossible. |
| BUG-003 | Copy range after removing an adjacent candidate | `017E14，017E1E` | The upper bound uses the decremented count, so some removals leave a duplicate. |
| BUG-004 | City table pointers after AI pathfinding | `034260，034266` | Pathfinding can leave frontier and grid pointers in A1 and A2. The city scan still uses those registers. |
| BUG-005 | Grid index for adjacency cost | `017ECE，017ED8` | Both terrain and cost are read with the same signed 16-bit grid index. The second read supplies the return value. |
| BUG-006 | Leader removal from arriving units | `01596C，01598E` | After a match, copying starts at the next index. The search stops before the last slot. |
| BUG-007 | Incremented roster pointer during cleanup | `00E3E2` | Clearing uses A0 after incrementing it. Aliased pointers can zero a later terminator. |
| BUG-008 | Upper byte in AI equipment comparison | `03372E，033732` | The read updates only D5's low byte. The level check compares the full word, so a stale high byte affects the purchase. |
| BUG-009 | AI equipment writeback by category | `033758` | The read indexes by officer and category. Only the category determines the write address. |
| BUG-010 | AI development budget uses four times the city ID | `03238E，032392` | The city ID replaces the random ratio, then shifts left by two for the budget calculation. |
| BUG-011 | Training progress at the cap | `00FD6A–00FD72` | When the new value exceeds 100, progress becomes the original increment minus the difference between 100 and the new value. |
| BUG-012 | AI recruitment cap uses the roster cursor | `033790–0337C6` | The comparison address uses the advancing roster cursor and the officer offset. |
| BUG-013 | Third player's ownership check uses the previous selection | `032918` | It compares the low byte of the previously selected city register with the third player slot. |
| BUG-014 | Branch after exhausting the pathfinding frontier | `006544–006554，00664E` | The outer loop continues along the original control path after the frontier runs out. |
| BUG-015 | Two one-way city adjacencies | `0D4BE2–0D4D22` | The 40 rows contain 182 directed links. The links 20→33 and 34→36 have no reverse link. |
| BUG-016 | Army resource decision ends with action 13 | `0346B0–0346BE` | Both paths write action 13. One writes action 12 to the same address first. |
| BUG-017 | Two random-sample tests always read zero | `034620，03510A` | After updating the seed, clearing upper bits, shifting the low word, and swapping leave the tested low word at zero. |
| BUG-018 | Initial strength for the strongest enemy candidate | `03498A–0349B0` | The maximum starts at the largest unsigned integer, so every candidate skips the update. |
| BUG-019 | Roster strength loses its low word to member IDs | `035092–0350A2` | Reading an ID overwrites the accumulator's low word each iteration. Reading the terminator overwrites it again. |
| BUG-020 | Countdown in the city strength scan | `0350B2，0350C2` | After reading the target city, the scan writes 255 to the same register and uses the countdown for comparison. |
| BUG-021 | Army equipment purchase writes to attributes | `034EC8–034EE6` | The routine prepares both tables, then writes byte 4 to the member attributes at B400. |
| BUG-022 | Self-loop in the city officer lookup | `034676–034680` | If none of the 256 entries match, the code branches to an instruction that loops at its own address. |
| BUG-023 | Processed-table base in economic support | `03245E，032484，0324AC` | The subroutine leaves CC00 in A4. Subsequent checks for already processed cities use that base. |
| BUG-024 | Support roster append after the terminator | `033F5C，033F8C` | Reading the terminator advances the cursor. The added officer and new terminator are written from that next address. |
| BUG-025 | Army roster sort uses an exhausted count | `034798，0347FA` | The loop leaves FFFF in D3's low word. Sorting uses it as the offset, so base C800 can yield odd address C801. |
| BUG-026 | Zero low word in the provisioning divisor | `034E5C，034E76` | Division uses only the product's low word. A cost of 16,384 is one example that yields a zero low word. |
| BUG-027 | Two officers' average speed as divisor | `033BE8，033C32` | The computed average of the two speed bytes goes directly into the 16-bit divisor. |
| BUG-028 | Final battlefield group clears the same slot | `025B44–025B4E` | All eight clears target D300. The two final candidates then go to D300 and D302. |
| BUG-029 | Battlefield candidate scan crosses slots | `025B88，025BA2` | Consecutive matches keep advancing the candidate address and can read into the adjacent region. |
| BUG-030 | Battlefield budget returns the old value | `0263FA，026402` | After division, the routine reloads the original budget from F39E. The caller compares against that return value. |
| BUG-031 | Terrain filter reads coordinates from the map base | `026B34–026B42` | A1 receives the coordinate table pointer. Both reads use the retained A0 map context. |
| BUG-032 | Battlefield budget uses the full RNG state | `0267C2，0267C6` | The formula adds the complete updated random state twice. |
| BUG-033 | Scaled officer ID written back to the roster | `025F86，025FBE，025FCC` | The ID shifts left by two for coordinates. Roster comparison and writeback keep using the scaled value. |
| BUG-034 | Forward copy across overlapping roster regions | `025EC8–025EDA，025FA4–025FBA` | Both destinations start one word past the source. The read and write cursors move together toward higher addresses. |
| BUG-035 | Selected member count as training divisor | `013FE4–014048` | The loop counts selected members. Division uses that count directly, including zero. |
| BUG-036 | Fixed horizontal sprite flip adjustment | `00AC68–00AC82` | The mask, shift, and swap after reading the size always produce a correction of 8. |
| BUG-037 | Side two's strength repeats the B400 factor | `01C272–01C28E` | Both multiplications use the first attribute accumulated into D3. |
| BUG-038 | Save encoder writes the remainder at the input cursor | `00928E–009296` | If the remainder is nonzero, the final write targets A1 and advances that input pointer. |
| BUG-039 | June event filters the same cities twice | `0170A8，0170CE` | Both June branches call the same event routine for cities 5, 8, and 14. |
| BUG-040 | Second postbattle resource goes to the battlefield buffer | `01CBE6–01CC06` | The capped sum of city and battlefield resources is written to the buffer at EE24. |
| BUG-041 | Average speed of an empty unit | `018158–018184` | A zero count wraps the loop's word counter. The final division still uses the original count. |
| BUG-042 | Side one's headcount oscillates between 15 and 16 | `03F4C2–03F4F0` | If the average at 15 exceeds 1,000, the count rises to 16, then the cap drops it back to 15. |
| BUG-043 | Vertical probe includes offset 3 | `041402，041406` | Extended vertical checks read offsets 10, 20, 3, and 40 in that order. |
| BUG-044 | Palette transformation self-loop | `00DEA6–00DEAC` | When the low word exceeds 15, control stays at a branch to itself. |
| BUG-045 | Side two's headcount oscillates between 15 and 16 | `03F45E–03F48C` | The same adjustment loop uses fields 80E6 and 80EA for side two. |
| BUG-046 | Pursuit branches use flags from the action write | `040FEE，04107E` | The instruction writing the action ID updates the flags used by the branch. |
| BUG-047 | Loyalty byte indexes the current unit packet | `067184，067188` | A byte read from the loyalty table becomes an offset into the current unit packet. |
| BUG-048 | Headcount as average loyalty divisor | `067148，0671A0` | The deployment roster and unit packets contribute members. Division uses the resulting count directly. |
| BUG-049 | Officer attribute byte as action budget divisor | `00091A–00092C` | The C400 attribute byte is zero-extended to 16 bits and used directly as the divisor. |

Look up the addresses in the [68000 source](../src/m68k/). See also the [editing guide](../EDITING.en.md) and [assembly build instructions](../README.en.md).
