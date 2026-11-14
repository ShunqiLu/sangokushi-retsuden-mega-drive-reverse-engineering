"""Restricted business-text admission and ordinary mnemonic lowering.
An intermediate fixed-structure compiler, not arbitrary Python or CPU proof.
"""
from .compiler_common import semantic_functions, lower_declared
from .target import BUSINESS_SCENE_SUPPORT_BINDINGS

APPROVED={'business_gameplay': {'advance_setup_dismissal',
                       'advance_setup_reveal',
                       'cycle_setup_option',
                       'initialize_setup_video',
                       'settle_city_projects_and_refresh_map',
                       'update_first_setup_option',
                       'update_fourth_setup_option',
                       'update_second_setup_option',
                       'update_setup_player_choices',
                       'update_third_setup_option',
                       'write_setup_video_address'},
 'business_highbank': {'advance_officer_growth_levels'},
 'contexts_gameplay': {'ProjectValues', 'GameplayCall', 'SetupPlane', 'SetupValues'},
 'contexts_highbank': {'GrowthValues'},
 'contexts_scene_support': {'CityCommandValues',
                            'GlyphTileLayout',
                            'SceneCall',
                            'ScenePresentation',
                            'checked_context'},
 'dataclasses': {'replace'},
 'domain': {'Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
            'data_view',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_byte',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'},
 'services': {'SceneRenderFrame',
              'append_map_sprites',
              'call_target',
              'clear_video_sprite_plane',
              'enqueue_sound_command',
              'initialize_video_registers_and_planes',
              'sample_random_pair',
              'sample_random_preserving_seed_carrier',
              'set_vram_write_address',
              'snapshot_and_clear_scene_palette',
              'upload_portrait_tiles',
              'wait_for_scene_sound_byte'}}

DECLARATIONS={'_ram': {'signature': 'state, name', 'returns': None, 'flow': "return ram_view(state, 'ram_' + name)"},
 '_word': {'signature': 'state, name', 'returns': None, 'flow': 'return _ram(state, name).word()'},
 '_put': {'signature': 'state, name, value',
          'returns': None,
          'flow': '_ram(state, name).set_word(0, low16(value))'},
 '_call': {'signature': 'state, target, values, continuation',
           'returns': None,
           'flow': 'from .services import call_target\n'
                   'context = GameplayCall(values, continuation) if type(values) is SetupValues else '
                   'SceneCall(values, continuation)\n'
                   'result = call_target(state, u32(target), context)\n'
                   'if type(result) is not type(values):\n'
                   "    raise Boundary('actual scene call must return its typed operands')\n"
                   'return result.validate(state)'},
 '_vector': {'signature': 'state, values, selector, parameters, base, continuation',
             'returns': None,
             'flow': 'offset = data_view(state, parameters).word(low16(selector))\n'
                     'return _call(state, u32(base + s16(offset)), values, continuation)'},
 '_setup_checked': {'signature': 'state, values',
                    'returns': None,
                    'flow': 'checked_state(state)\n'
                            'if type(values) is not SetupValues:\n'
                            "    raise ValueError('setup operands required')\n"
                            'return values.validate(state)'},
 '_setup_sprite': {'signature': 'state, values',
                   'returns': None,
                   'flow': 'from .services import append_map_sprites\n'
                           'if values.source is None:\n'
                           "    raise Boundary('real setup sprite source required')\n"
                           'sprite = append_map_sprites(state, values.source, values.value, '
                           'values.position, values.attributes, reset_scroll=True, '
                           'initialize_clip=True)\n'
                           'return replace(values, value=sprite.x, position=sprite.y, '
                           'attributes=sprite.attributes, source=sprite.source)'},
 'refresh_setup_option_labels': {'signature': 'state: SceneState, values: SetupValues',
                                 'returns': 'SetupValues',
                                 'flow': '_setup_checked(state, values)\n'
                                         "value = replace_word(values.value, _word(state, '7032'))\n"
                                         'position = replace_word(values.position, _word(state, '
                                         "'7026'))\n"
                                         'if low16(position) == low16(value):\n'
                                         '    return replace(values, value=value, position=position)\n'
                                         'position = replace_word(position, u16(low16(position) << 2))\n'
                                         'pointer = data_view(state, '
                                         "'data_0300de').long(low16(position))\n"
                                         'source = state.table_at(pointer).cursor()\n'
                                         'while True:\n'
                                         '    value = replace_word(value, source.word())\n'
                                         '    if low16(value) == 65535:\n'
                                         "        _put(state, '7032', _word(state, '7026'))\n"
                                         '        return replace(values, value=value, '
                                         'position=position, source=source)\n'
                                         '    from .business_gameplay import write_setup_video_address\n'
                                         '    plane = SetupPlane(value, position, values.attributes, '
                                         'values.rows, values.tile, values.option, source, '
                                         'VideoPlaneAddress(low16(value)))\n'
                                         '    value = write_setup_video_address(state, plane).command\n'
                                         '    value = 0\n'
                                         '    option = replace_word(values.option, source.next_word())\n'
                                         '    option = 0\n'
                                         '    while True:\n'
                                         '        value = replace_word(value, source.next_word())\n'
                                         '        if low16(value) == 65535:\n'
                                         '            break\n'
                                         '        value = replace_word(value, low16(value) & 255 | '
                                         '33536)\n'
                                         '        state.write(12582912, 2, low16(value))\n'
                                         '    values = replace(values, value=value, option=option)'},
 'render_packed_sprite_position': {'signature': 'state: SceneState, values: SetupValues',
                                   'returns': 'SetupValues',
                                   'flow': '_setup_checked(state, values)\n'
                                           'position = replace_word(values.position, '
                                           'low16(values.value) & 255)\n'
                                           'value = replace_word(values.value, low16(values.value) >> 8 '
                                           '& 255)\n'
                                           'return _setup_sprite(state, replace(values, value=value, '
                                           'position=position, attributes=0))'},
 'render_setup_player_position': {'signature': 'state: SceneState, values: SetupValues',
                                  'returns': 'SetupValues',
                                  'flow': '_setup_checked(state, values)\n'
                                          'value = replace_word(values.value, u16(low16(values.value) '
                                          '<< 1))\n'
                                          'position = replace_word(values.position, data_view(state, '
                                          "'data_03046a').word(low16(value)))\n"
                                          'return _setup_sprite(state, replace(values, '
                                          'value=replace_word(value, 176), position=position, '
                                          'attributes=0))'},
 'render_selected_setup_options': {'signature': 'state: SceneState, values: SetupValues',
                                   'returns': 'SetupValues',
                                   'flow': '_setup_checked(state, values)\n'
                                           "choices = ((0, '7026', 'data_030456', 'data_02b116'), (1, "
                                           "'7024', 'data_03045c', 'data_02b122'), (2, '7028', "
                                           "'data_030462', 'data_02b128'), (3, '702a', 'data_030466', "
                                           "'data_02b130'))\n"
                                           'for selected, field, positions, sprites in choices:\n'
                                           "    if _word(state, '7022') == selected and _ram(state, "
                                           "'f321').byte() & 8:\n"
                                           '        continue\n'
                                           '    position = replace_word(values.position, '
                                           'u16(_word(state, field) << 1))\n'
                                           '    value = replace_word(values.value, data_view(state, '
                                           'positions).word(low16(position)))\n'
                                           '    values = render_packed_sprite_position(state, '
                                           'replace(values, value=value, position=position, '
                                           'source=data_view(state, sprites).cursor()))\n'
                                           "skip = _word(state, '7022') == 4 and _ram(state, "
                                           "'f321').byte() & 8\n"
                                           'if not skip:\n'
                                           "    if _word(state, '7026') == 2 and _word(state, '702c') "
                                           '>= 3:\n'
                                           "        _put(state, '702c', 0)\n"
                                           '    value = replace_word(values.value, u16(_word(state, '
                                           "'702c') << 1))\n"
                                           '    position = replace_word(values.position, '
                                           "data_view(state, 'data_03046c').word(low16(value)))\n"
                                           '    values = _setup_sprite(state, replace(values, '
                                           'value=replace_word(value, 176), position=position, '
                                           'attributes=0, source=data_view(state, '
                                           "'data_02b132').cursor()))\n"
                                           "if not _word(state, '7034') or _word(state, '7022') < 5:\n"
                                           '    return values\n'
                                           "if not (_word(state, '7022') == 5 and _ram(state, "
                                           "'f321').byte() & 8):\n"
                                           '    value = replace_word(values.value, _word(state, '
                                           "'702e'))\n"
                                           '    values = render_setup_player_position(state, '
                                           'replace(values, value=value, source=data_view(state, '
                                           "'data_02b13a').cursor()))\n"
                                           '    values = replace(values, value=value)\n'
                                           "if _word(state, '7034') != 2 or _word(state, '7022') < 6:\n"
                                           '    return values\n'
                                           "if not (_word(state, '7022') == 6 and _ram(state, "
                                           "'f321').byte() & 8):\n"
                                           '    value = replace_word(values.value, _word(state, '
                                           "'7030'))\n"
                                           '    values = render_setup_player_position(state, '
                                           'replace(values, value=value, source=data_view(state, '
                                           "'data_02b140').cursor()))\n"
                                           '    values = replace(values, value=value)\n'
                                           'return values'},
 '_cycle_player_choice': {'signature': 'state, values, excluded_second',
 'returns': None,
 'flow': "if _word(state, '7038') < 16 or _word(state, '703a') < 16:\n"
         '    return values\n'
         'option = values.tile\n'
         "if _ram(state, 'f605').byte() & 4:\n"
         '    while True:\n'
         '        if not low16(option):\n'
         "            option = 2 if _word(state, '7026') == 2 else 6\n"
         '        else:\n'
         '            option = replace_word(option, u16(low16(option) - 1))\n'
         "        if low16(option) != _word(state, '702c') and (not excluded_second or "
         "low16(option) != _word(state, '702e')):\n"
         '            break\n'
         "elif _ram(state, 'f605').byte() & 8:\n"
         '    while True:\n'
         "        limit = 2 if _word(state, '7026') >= 2 else 6\n"
         '        option = replace_word(option, 0 if low16(option) == limit else '
         'u16(low16(option) + 1))\n'
         "        if low16(option) != _word(state, '702c') and (not excluded_second or "
         "low16(option) != _word(state, '702e')):\n"
         '            break\n'
         'return replace(values, tile=option)'},
 'cycle_second_player_choice': {'signature': 'state: SceneState, values: SetupValues',
                                'returns': 'SetupValues',
                                'flow': '_setup_checked(state, values)\n'
                                        'return _cycle_player_choice(state, values, False)'},
 'cycle_third_player_choice': {'signature': 'state: SceneState, values: SetupValues',
                               'returns': 'SetupValues',
                               'flow': '_setup_checked(state, values)\n'
                                       'return _cycle_player_choice(state, values, True)'},
 'read_controller_identity': {'signature': 'state: SceneState, values: SetupValues',
                              'returns': 'SetupValues',
                              'flow': '_setup_checked(state, values)\n'
                                      'if values.source is None:\n'
                                      "    raise Boundary('actual controller I/O port required')\n"
                                      'port = values.source\n'
                                      'port.set_byte(0, 64)\n'
                                      'value = replace_byte(values.value, port.byte())\n'
                                      'position = replace_byte(values.position, low8(value))\n'
                                      'position = replace_byte(position, u8(low8(position) << 1))\n'
                                      'value = replace_byte(value, (low8(value) | low8(position)) & '
                                      '10)\n'
                                      'port.set_byte(0, 0)\n'
                                      'position = replace_byte(position, port.byte())\n'
                                      'attributes = replace_byte(values.attributes, low8(position) >> '
                                      '1)\n'
                                      'position = replace_byte(position, (low8(position) | '
                                      'low8(attributes)) & 5)\n'
                                      'value = replace_byte(value, low8(value) | low8(position))\n'
                                      'return replace(values, value=value, position=position, '
                                      'attributes=attributes)'},
 'update_connected_controller_option': {'signature': 'state: SceneState, values: SetupValues',
 'returns': 'SetupValues',
 'flow': '_setup_checked(state, values)\n'
         "if _word(state, '703e'):\n"
         '    return values\n'
         'values = read_controller_identity(state, replace(values, '
         'source=state.table_at(10551301).cursor()))\n'
         'if low8(values.value) != 11:\n'
         "    _put(state, '7034', 0)\n"
         'else:\n'
         '    from .business_gameplay import cycle_setup_option\n'
         '    values = cycle_setup_option(state, replace(values, '
         "tile=replace_word(values.tile, _word(state, '7034')), "
         'stride=replace_word(values.stride, 2)))\n'
         "    _put(state, '7034', values.tile)\n"
         "position = replace_word(values.position, u16(_word(state, '7034') << 1))\n"
         'value = replace_word(values.value, data_view(state, '
         "'data_03047c').word(low16(position)))\n"
         'return _setup_sprite(state, replace(values, value=value, '
         'position=replace_word(position, 112), attributes=0, source=data_view(state, '
         "'data_02b14a').cursor()))"},
 'advance_controller_setup_reveal': {'signature': 'state: SceneState, values: SetupValues',
                                     'returns': 'SetupValues',
                                     'flow': '_setup_checked(state, values)\n'
                                             "if _word(state, '7038') >= 16:\n"
                                             '    return values\n'
                                             'value = replace_word(values.value, u16(15 - _word(state, '
                                             "'7038')))\n"
                                             'values = _call(state, 56998, replace(values, value=value, '
                                             'position=replace_word(values.position, 64), '
                                             "source=data_view(state, 'data_02b46e').cursor()), "
                                             '198418)\n'
                                             "_put(state, '7038', u16(_word(state, '7038') + 1))\n"
                                             'return values'},
 'advance_controller_setup_dismissal': {'signature': 'state: SceneState, values: SetupValues',
                                        'returns': 'SetupValues',
                                        'flow': '_setup_checked(state, values)\n'
                                                "if _word(state, '703a') >= 16:\n"
                                                '    return values\n'
                                                'values = _call(state, 56998, replace(values, '
                                                'value=replace_word(values.value, _word(state, '
                                                "'703a')), position=replace_word(values.position, 64), "
                                                "source=data_view(state, 'data_02b46e').cursor()), "
                                                '198458)\n'
                                                "_put(state, '703a', u16(_word(state, '703a') + 1))\n"
                                                'return values'},
 'commit_setup_options': {'signature': 'state: SceneState, values: SetupValues',
                          'returns': 'SetupValues',
                          'flow': '_setup_checked(state, values)\n'
                                  "_put(state, 'efd2', _word(state, '7024'))\n"
                                  "value = replace_word(values.value, _word(state, '7026'))\n"
                                  "_put(state, 'efd4', value)\n"
                                  "_put(state, 'efe4', value)\n"
                                  "_ram(state, 'f374').set_byte(0, data_view(state, "
                                  "'data_0307e0').byte(low16(value)))\n"
                                  "_ram(state, 'f375').set_byte(0, 0)\n"
                                  "_put(state, 'efd6', _word(state, '7028'))\n"
                                  "_put(state, 'efd8', _word(state, '702a'))\n"
                                  "_put(state, 'f67c', 128)\n"
                                  "_put(state, 'f67e', 128)\n"
                                  "value = replace_word(value, _word(state, '7034'))\n"
                                  "choices = _ram(state, '702c').cursor()\n"
                                  "position = replace_word(values.position, u16(_word(state, 'efd4') * "
                                  '14))\n'
                                  "directory = data_view(state, 'data_0307e4').cursor(low16(position))\n"
                                  "destination = _ram(state, 'f67a').cursor()\n"
                                  'for _ in descending_inclusive(low16(value)):\n'
                                  '    position = replace_word(position, u16(choices.next_word() << '
                                  '1))\n'
                                  '    destination.append_word(directory.word(low16(position)))\n'
                                  'return replace(values, value=replace_word(value, 65535), '
                                  'position=position, source=choices, destination=destination)'},
 '_setup_transfer_control': {'signature': 'state, values, width, source_address',
                             'returns': None,
                             'flow': 'state.set_status_word(9984)\n'
                                     'state.write(12582916, 2, 36610)\n'
                                     'state.write(12582916, 4, 1610612738)\n'
                                     'stride, selector = (replace_word(values.stride, 13107), '
                                     'replace_word(values.selector, 3455))\n'
                                     'for _ in descending_inclusive(low16(selector)):\n'
                                     '    state.write(12582912, 2, low16(stride))\n'
                                     "_put(state, '700c', width)\n"
                                     "_ram(state, '700e').set_long(0, source_address)\n"
                                     "_put(state, '7014', 3)\n"
                                     "_put(state, '7016', 1)\n"
                                     'state.set_status_word(9472)\n'
                                     'return replace(values, stride=stride, '
                                     'selector=replace_word(selector, 65535))'},
 '_run_configuration_choices': {'signature': 'state, values',
                                'returns': None,
                                'flow': 'from .business_gameplay import initialize_setup_video, '
                                        'advance_setup_reveal, advance_setup_dismissal, '
                                        'update_first_setup_option, update_second_setup_option, '
                                        'update_third_setup_option, update_fourth_setup_option, '
                                        'update_setup_player_choices\n'
                                        'from .services import clear_video_sprite_plane, '
                                        'initialize_video_registers_and_planes, enqueue_sound_command\n'
                                        'while True:\n'
                                        '    state.set_status_word(9984)\n'
                                        "    value = replace_word(values.value, _word(state, 'f606'))\n"
                                        '    value = replace_byte(value, low8(value) & 191)\n'
                                        '    state.write(12582916, 2, low16(value))\n'
                                        "    _put(state, 'f612', 0)\n"
                                        '    clear_video_sprite_plane(state)\n'
                                        '    initialize_video_registers_and_planes(state)\n'
                                        "    _put(state, '7036', 0)\n"
                                        '    values = initialize_setup_video(state, replace(values, '
                                        'value=value))\n'
                                        "    _put(state, '7022', 0)\n"
                                        "    _put(state, '7040', 0)\n"
                                        "    _put(state, '7042', 0)\n"
                                        "    _put(state, '703e', 0)\n"
                                        '    values = advance_setup_reveal(state, values)\n'
                                        '    values = _setup_transfer_control(state, values, 41472, '
                                        '174758)\n'
                                        "    _put(state, 'f612', 2048)\n"
                                        "    while _ram(state, 'f612').byte():\n"
                                        "        state.progress('configuration-sound')\n"
                                        '    restart = False\n'
                                        '    while True:\n'
                                        '        values = advance_setup_reveal(state, values)\n'
                                        '        values = advance_setup_dismissal(state, values)\n'
                                        "        if not _word(state, '703e'):\n"
                                        '            values = refresh_setup_option_labels(state, '
                                        'values)\n'
                                        '            values = update_first_setup_option(state, values)\n'
                                        '            values = update_second_setup_option(state, '
                                        'values)\n'
                                        '            values = update_third_setup_option(state, values)\n'
                                        '            values = update_fourth_setup_option(state, '
                                        'values)\n'
                                        '            values = update_setup_player_choices(state, '
                                        'values)\n'
                                        '            values = render_selected_setup_options(state, '
                                        'values)\n'
                                        "            controllers = _word(state, '7034')\n"
                                        "            stage = _word(state, '7022')\n"
                                        '            if controllers == 1 and stage == 5 or (controllers '
                                        '>= 2 and stage in (5, 6)):\n'
                                        "                _ram(state, 'f603').set_byte(0, _ram(state, "
                                        "'f605').byte())\n"
                                        "            if _ram(state, 'f603').byte() & 32:\n"
                                        '                value = replace_byte(values.value, 172)\n'
                                        '                enqueue_sound_command(state, low8(value))\n'
                                        '                final = 5 if not controllers else 6 if '
                                        'controllers == 1 else 7\n'
                                        '                position = final - 1\n'
                                        '                values = replace(values, value=final, '
                                        'position=position)\n'
                                        '                if final == stage:\n'
                                        '                    return values\n'
                                        '                if position == stage:\n'
                                        '                    values = _setup_transfer_control(state, '
                                        'values, 41408, 174782)\n'
                                        "                _put(state, '7022', u16(_word(state, '7022') + "
                                        '1))\n'
                                        "            elif _ram(state, 'f603').byte() & 16:\n"
                                        '                final = 5 if not controllers else 6 if '
                                        'controllers == 1 else 7\n'
                                        '                values = replace(values, value=final)\n'
                                        '                if stage == final:\n'
                                        "                    _put(state, '7022', 0)\n"
                                        '                    values = _setup_transfer_control(state, '
                                        'values, 41472, 174758)\n'
                                        '                elif stage:\n'
                                        "                    _put(state, '7022', u16(stage - 1))\n"
                                        '            value = replace_byte(values.value, _ram(state, '
                                        "'f603').byte())\n"
                                        '            value = replace_byte(value, low8(value) & 128)\n'
                                        '            values = replace(values, value=value)\n'
                                        '            if low8(value):\n'
                                        "                _put(state, '703e', 1)\n"
                                        "        if _word(state, '7042') >= 16:\n"
                                        '            restart = True\n'
                                        '            break\n'
                                        "        state.progress('configuration-frame')\n"
                                        '    if not restart:\n'
                                        '        return values'},
 'run_controller_setup_and_configuration': {'signature': 'state: SceneState, values: SetupValues',
                                            'returns': 'SetupValues',
                                            'flow': 'from .business_gameplay import '
                                                    'initialize_setup_video\n'
                                                    'from .services import clear_video_sprite_plane, '
                                                    'initialize_video_registers_and_planes, '
                                                    'enqueue_sound_command\n'
                                                    '_setup_checked(state, values)\n'
                                                    'state.set_status_word(9984)\n'
                                                    'value = replace_word(values.value, _word(state, '
                                                    "'f606'))\n"
                                                    'value = replace_byte(value, low8(value) & 191)\n'
                                                    'state.write(12582916, 2, low16(value))\n'
                                                    "_put(state, 'f612', 0)\n"
                                                    'clear_video_sprite_plane(state)\n'
                                                    'initialize_video_registers_and_planes(state)\n'
                                                    "_put(state, '7036', 1)\n"
                                                    'values = initialize_setup_video(state, '
                                                    'replace(values, value=value))\n'
                                                    "_put(state, '7038', 0)\n"
                                                    "_put(state, '703a', 0)\n"
                                                    "_put(state, '703e', 0)\n"
                                                    'values = advance_controller_setup_reveal(state, '
                                                    'values)\n'
                                                    'values = _setup_transfer_control(state, values, '
                                                    '41152, 174736)\n'
                                                    "_put(state, 'f612', 2048)\n"
                                                    "while _ram(state, 'f612').byte():\n"
                                                    "    state.progress('controller-sound')\n"
                                                    "while _word(state, '703a') < 16:\n"
                                                    '    values = '
                                                    'advance_controller_setup_reveal(state, values)\n'
                                                    '    values = '
                                                    'update_connected_controller_option(state, values)\n'
                                                    '    value = replace_byte(values.value, _ram(state, '
                                                    "'f603').byte())\n"
                                                    '    value = replace_byte(value, low8(value) & 32)\n'
                                                    '    values = replace(values, value=value)\n'
                                                    '    if low8(value):\n'
                                                    "        _put(state, '703e', 1)\n"
                                                    '        enqueue_sound_command(state, 172)\n'
                                                    '        values = replace(values, '
                                                    'value=replace_byte(value, 172))\n'
                                                    "    if _word(state, '703e'):\n"
                                                    '        values = '
                                                    'advance_controller_setup_dismissal(state, values)\n'
                                                    "    state.progress('controller-frame')\n"
                                                    'return _run_configuration_choices(state, values)'},
 '_carry': {'signature': 'state, value',
            'returns': None,
            'flow': 'status = state.read_status_word()\n'
                    'state.set_status_word(status | 1 if value else status & 65534)'},
 'locate_selected_ruler_city': {'signature': 'state: SceneState, values: CityCommandValues',
                                'returns': 'CityCommandValues',
                                'flow': 'checked_context(values, CityCommandValues, state)\n'
                                        "value = replace_word(values.value, u16(_word(state, 'f376') << "
                                        '1))\n'
                                        'value = replace_word(value, _ram(state, '
                                        "'e640').word(low16(value)))\n"
                                        'field = replace_byte(values.field, _ram(state, '
                                        "'cc00').byte(low16(value)))\n"
                                        'field = replace_word(field, low16(field) & 63)\n'
                                        'if low16(field) <= 40:\n'
                                        '    field = replace_word(field, u16(low16(field) << 2))\n'
                                        "    positions = data_view(state, 'data_0d4ac6')\n"
                                        "    _put(state, 'f35e', positions.word(low16(field), "
                                        'displacement=2))\n'
                                        "    _put(state, 'f360', positions.word(low16(field)))\n"
                                        '    _carry(state, False)\n'
                                        '    return replace(values, value=value, field=field, '
                                        'scratch=positions)\n'
                                        "owners = _ram(state, 'f428')\n"
                                        "field = replace_word(field, _word(state, 'f376'))\n"
                                        'found = False\n'
                                        'for city in descending_inclusive(39):\n'
                                        '    value = replace_word(value, city)\n'
                                        '    if owners.byte(city) == low8(field):\n'
                                        '        found = True\n'
                                        '        break\n'
                                        'if found:\n'
                                        '    value = replace_word(value, u16(low16(value) << 2))\n'
                                        "    positions = data_view(state, 'data_0d4aca')\n"
                                        "    _put(state, 'f35e', positions.word(low16(value), "
                                        'displacement=2))\n'
                                        "    _put(state, 'f360', positions.word(low16(value)))\n"
                                        '    _carry(state, False)\n'
                                        '    return replace(values, value=value, field=field, '
                                        'scratch=positions)\n'
                                        '_carry(state, True)\n'
                                        'return replace(values, value=replace_word(value, 65535), '
                                        'field=field, scratch=owners)'},
 '_packet_location': {'signature': 'state, values, packet',
                      'returns': None,
                      'flow': 'value = replace_byte(replace_word(values.value, 0), packet.byte(1))\n'
                              'value = replace_word(value, u16(low16(value) << 4))\n'
                              "_put(state, 'f35e', value)\n"
                              'value = replace_byte(replace_word(value, 0), packet.byte(2))\n'
                              'value = replace_word(value, u16(low16(value) << 4))\n'
                              "_put(state, 'f360', value)\n"
                              '_carry(state, False)\n'
                              'return replace(values, value=value, packet=packet)'},
 'locate_selected_force_packet': {'signature': 'state: SceneState, values: CityCommandValues',
                                  'returns': 'CityCommandValues',
                                  'flow': 'checked_context(values, CityCommandValues, state)\n'
                                          "value = replace_word(values.value, u16(_word(state, 'f376') "
                                          '<< 1))\n'
                                          'value = replace_word(value, _ram(state, '
                                          "'e640').word(low16(value)))\n"
                                          "if _ram(state, 'a050').byte(low16(value)):\n"
                                          "    value = replace_word(value, _word(state, 'f376'))\n"
                                          "    packet = _ram(state, '9000').cursor()\n"
                                          '    field = values.field\n'
                                          '    while True:\n'
                                          '        field = replace_byte(field, packet.byte())\n'
                                          '        field = replace_word(field, low16(field) & 15)\n'
                                          '        if not low16(field):\n'
                                          '            _carry(state, True)\n'
                                          '            return replace(values, value=value, field=field, '
                                          'packet=packet)\n'
                                          '        if packet.byte(4) == low8(value):\n'
                                          '            return _packet_location(state, replace(values, '
                                          'value=value, field=field), packet)\n'
                                          '        packet.base = u32(packet.base + 13 + '
                                          's16(low16(field)))\n'
                                          "packet = _ram(state, '9000').cursor()\n"
                                          'member, count = (values.member, values.count)\n'
                                          'while True:\n'
                                          '    member = replace_byte(member, packet.byte())\n'
                                          '    member = replace_word(member, low16(member) & 15)\n'
                                          '    if not low16(member):\n'
                                          '        _carry(state, True)\n'
                                          '        return replace(values, value=value, member=member, '
                                          'count=count, packet=packet)\n'
                                          '    if packet.byte(4) == low8(values.field):\n'
                                          '        for index in descending_inclusive(u16(low16(member) '
                                          '- 1)):\n'
                                          '            count = replace_word(count, index)\n'
                                          '            if packet.byte(u16(13 + index)) == low8(value):\n'
                                          '                return _packet_location(state, '
                                          'replace(values, value=value, member=member, count=count), '
                                          'packet)\n'
                                          '        count = replace_word(count, 65535)\n'
                                          '    packet.base = u32(packet.base + 13 + '
                                          's16(low16(member)))'},
 '_require_packet': {'signature': 'values',
                     'returns': None,
                     'flow': 'if values.packet is None:\n'
                             "    raise Boundary('live packed-force packet required')\n"
                             'return values.packet'},
 'calculate_map_packet_supply': {'signature': 'state: SceneState, values: CityCommandValues',
                                 'returns': 'CityCommandValues',
                                 'flow': 'checked_context(values, CityCommandValues, state)\n'
                                         'packet, troops = (_require_packet(values), _ram(state, '
                                         "'c800'))\n"
                                         'field = replace_word(values.field, u16(low16(values.value) - '
                                         '1))\n'
                                         'member, count = (replace_word(values.member, 0), 0)\n'
                                         'for index in descending_inclusive(low16(field)):\n'
                                         '    field = replace_word(field, index)\n'
                                         '    member = replace_byte(member, packet.byte(u16(13 + '
                                         'index)))\n'
                                         '    member = replace_word(member, u16(low16(member) << 2))\n'
                                         '    count = u32(count + troops.long(low16(member)))\n'
                                         '    count = u32(count + 100)\n'
                                         'count = divu_retained(count, 10)\n'
                                         'member = replace_word(member, low16(count))\n'
                                         'count = replace_word(count, u16((low16(count) << 1) + '
                                         'low16(member))) & 65535\n'
                                         'return replace(values, field=replace_word(field, 65535), '
                                         'member=member, count=count, troops=troops)'},
 'sample_map_packet_loss_factors': {'signature': 'state: SceneState, values: CityCommandValues',
                                    'returns': 'CityCommandValues',
                                    'flow': 'from .services import sample_random_pair\n'
                                            'checked_context(values, CityCommandValues, state)\n'
                                            'sample = sample_random_pair(state).sample & 65535\n'
                                            'member = replace_word(values.member, '
                                            'u16(low16(swap_words(u32(sample * 6))) + 5))\n'
                                            'sample = sample_random_pair(state).sample & 65535\n'
                                            'count = replace_word(values.count, '
                                            'u16(low16(swap_words(u32(sample * 501))) + 500))\n'
                                            'return replace(values, member=member, count=count)'},
 'apply_map_packet_supply_losses': {'signature': 'state: SceneState, values: CityCommandValues',
                                    'returns': 'CityCommandValues',
                                    'flow': 'checked_context(values, CityCommandValues, state)\n'
                                            'packet = _require_packet(values)\n'
                                            "_put(state, 'cfc8', 0)\n"
                                            "_ram(state, 'cfc9').set_byte(0, packet.byte(13))\n"
                                            'selected = replace_word(values.selected, 0)\n'
                                            "troops, readiness, assignments = (_ram(state, 'c800'), "
                                            "_ram(state, 'b200'), _ram(state, 'cc00'))\n"
                                            "survivors = _ram(state, 'cfb2').cursor()\n"
                                            'values = replace(values, selected=selected, troops=troops, '
                                            'readiness=readiness, assignments=assignments, '
                                            'roster=survivors, field=replace_word(values.field, '
                                            'u16(low16(values.value) - 1)))\n'
                                            'for index in descending_inclusive(low16(values.field)):\n'
                                            '    values = sample_map_packet_loss_factors(state, '
                                            'replace(values, field=replace_word(values.field, index)))\n'
                                            '    officer = '
                                            'replace_byte(replace_word(values.readiness_loss, 0), '
                                            'packet.byte(u16(13 + index)))\n'
                                            '    troop_rate = replace_word(values.troop_rate, '
                                            'u16(low16(officer) << 1))\n'
                                            '    force_index = replace_word(values.force_index, '
                                            'readiness.word(low16(troop_rate)))\n'
                                            '    old = low16(force_index)\n'
                                            '    force_index = replace_word(force_index, u16(old - '
                                            'low16(values.member)))\n'
                                            '    values = replace(values, readiness_loss=officer, '
                                            'troop_rate=troop_rate, force_index=force_index)\n'
                                            '    if old > low16(values.member):\n'
                                            '        readiness.set_word(low16(troop_rate), '
                                            'low16(force_index))\n'
                                            '        troop_rate = replace_word(troop_rate, '
                                            'u16(low16(troop_rate) << 1))\n'
                                            '        force_index = replace_word(force_index, '
                                            'troops.word(low16(troop_rate), displacement=2))\n'
                                            '        old = low16(force_index)\n'
                                            '        force_index = replace_word(force_index, u16(old - '
                                            'low16(values.count)))\n'
                                            '        if old < low16(values.count):\n'
                                            '            force_index = replace_word(force_index, 0)\n'
                                            '        troops.set_word(low16(troop_rate), '
                                            'low16(force_index), displacement=2)\n'
                                            '        selected = replace_word(values.selected, '
                                            'u16(low16(values.selected) + 1))\n'
                                            '        survivors.append_byte(low8(officer))\n'
                                            '        values = replace(values, selected=selected, '
                                            'troop_rate=troop_rate, force_index=force_index)\n'
                                            '    else:\n'
                                            '        assignments.set_byte(low16(officer), 255)\n'
                                            '        member = replace_byte(values.member, '
                                            'packet.byte(4))\n'
                                            '        member = replace_word(member, low16(member) & 15)\n'
                                            '        values = replace(values, member=member)\n'
                                            "        if low16(member) in (_word(state, 'f67a'), "
                                            "_word(state, 'f67c'), _word(state, 'f67e')):\n"
                                            '            saved_stage, saved_force = (_word(state, '
                                            "'f362'), _word(state, 'f376'))\n"
                                            "            _put(state, 'f376', member)\n"
                                            "            _put(state, 'f3d0', officer)\n"
                                            "            _put(state, 'f740', 202)\n"
                                            "            _put(state, 'f362', 0)\n"
                                            '            _call(state, 199284, values, 200032)\n'
                                            "            _put(state, 'f376', saved_force)\n"
                                            "            _put(state, 'f362', saved_stage)\n"
                                            'values = replace(values, field=replace_word(values.field, '
                                            '65535))\n'
                                            'if low16(values.value) != low16(values.selected):\n'
                                            '    values = compact_map_packet_survivors(state, values)\n'
                                            'return replace(values, value=replace_word(values.value, '
                                            'low16(values.selected)))'},
 'replace_map_queue_leader': {'signature': 'state: SceneState, values: CityCommandValues',
                              'returns': 'CityCommandValues',
                              'flow': 'checked_context(values, CityCommandValues, state)\n'
                                      'packet = _require_packet(values)\n'
                                      "leader, old_leader = (packet.byte(13), _word(state, 'cfc8'))\n"
                                      "ranked = _ram(state, '39b2').cursor()\n"
                                      'while ranked.byte():\n'
                                      '    if ranked.byte(1) == low8(old_leader):\n'
                                      '        ranked.set_byte(1, leader)\n'
                                      "        queue = _ram(state, '3000').cursor(1)\n"
                                      '        while queue.byte() != low8(old_leader):\n'
                                      '            queue.base = u32(queue.base + 1)\n'
                                      '            while queue.next_byte():\n'
                                      '                pass\n'
                                      '            queue.base = u32(queue.base + 1)\n'
                                      '        queue.set_byte(0, leader)\n'
                                      '        break\n'
                                      '    ranked.base = u32(ranked.base + 2)\n'
                                      'return values'},
 'remove_map_queue_leader': {'signature': 'state: SceneState, values: CityCommandValues',
                             'returns': 'CityCommandValues',
                             'flow': 'checked_context(values, CityCommandValues, state)\n'
                                     "ranked, leader = (_ram(state, '39b2').cursor(), _word(state, "
                                     "'cfc8'))\n"
                                     'while ranked.byte():\n'
                                     '    if ranked.byte(1) == low8(leader):\n'
                                     '        while True:\n'
                                     '            priority = ranked.byte(2)\n'
                                     '            ranked.set_byte(0, priority)\n'
                                     '            if not priority:\n'
                                     '                return values\n'
                                     '            ranked.set_byte(1, ranked.byte(3))\n'
                                     '            ranked.base = u32(ranked.base + 2)\n'
                                     '    ranked.base = u32(ranked.base + 2)\n'
                                     'return values'},
 'compact_map_packet_survivors': {'signature': 'state: SceneState, values: CityCommandValues',
                                  'returns': 'CityCommandValues',
                                  'flow': 'checked_context(values, CityCommandValues, state)\n'
                                          'packet = _require_packet(values)\n'
                                          'force_index = replace_word(values.force_index, '
                                          'low16(values.selected))\n'
                                          'if low16(force_index):\n'
                                          '    force_index = replace_word(force_index, '
                                          'u16(low16(force_index) - 1))\n'
                                          "    source = _ram(state, 'cfb2').cursor()\n"
                                          '    for index in descending_inclusive(low16(force_index)):\n'
                                          '        packet.set_byte(u16(13 + index), '
                                          'source.next_byte())\n'
                                          '    packet.set_byte(0, low8(values.selected))\n'
                                          '    values = replace_map_queue_leader(state, values)\n'
                                          '    source = state.table_at(u32(packet.base + 13 + '
                                          's16(low16(values.value)))).cursor()\n'
                                          '    destination = state.table_at(u32(packet.base + 13 + '
                                          's16(low16(values.selected)))).cursor()\n'
                                          'else:\n'
                                          '    values = remove_map_queue_leader(state, values)\n'
                                          '    source = state.table_at(u32(packet.base + 13 + '
                                          's16(low16(values.value)))).cursor()\n'
                                          '    destination = state.table_at(packet.base).cursor()\n'
                                          'field = values.field\n'
                                          'while True:\n'
                                          '    field = replace_byte(field, source.byte())\n'
                                          '    field = replace_word(field, low16(field) & 15)\n'
                                          '    if not low16(field):\n'
                                          '        break\n'
                                          '    field = replace_word(field, u16(low16(field) + 12))\n'
                                          '    for _ in descending_inclusive(low16(field)):\n'
                                          '        destination.append_byte(source.next_byte())\n'
                                          '    field = replace_word(field, 65535)\n'
                                          'destination.set_byte(0, 0)\n'
                                          'member, count = (values.member, values.count)\n'
                                          'if low16(values.selected):\n'
                                          "    radius = _ram(state, 'c400')\n"
                                          '    force_index = replace_word(force_index, '
                                          'u16(low16(values.selected) - 1))\n'
                                          '    member, count = (0, replace_word(count, 0))\n'
                                          '    for index in descending_inclusive(low16(force_index)):\n'
                                          '        count = replace_byte(count, packet.byte(u16(13 + '
                                          'index)))\n'
                                          '        member = replace_byte(member, u8(low8(member) + '
                                          'radius.byte(low16(count))))\n'
                                          '    member = divu_retained(member, low16(values.selected))\n'
                                          '    packet.set_byte(3, low8(member))\n'
                                          '    force_index = replace_word(force_index, 65535)\n'
                                          '    source = radius.cursor()\n'
                                          'return replace(values, field=field, member=member, '
                                          'count=count, force_index=force_index, roster=source, '
                                          'destination=destination)'},
 'deduct_all_map_packet_supply': {'signature': 'state: SceneState, values: CityCommandValues',
                                  'returns': 'CityCommandValues',
                                  'flow': 'checked_context(values, CityCommandValues, state)\n'
                                          "packet = _ram(state, '9000').cursor()\n"
                                          'while True:\n'
                                          '    value = replace_byte(values.value, packet.byte())\n'
                                          '    value = replace_word(value, low16(value) & 15)\n'
                                          '    values = replace(values, value=value, packet=packet)\n'
                                          '    if not low16(value):\n'
                                          '        return values\n'
                                          '    values = calculate_map_packet_supply(state, values)\n'
                                          '    member = replace_byte(values.member, packet.byte(9))\n'
                                          '    member = replace_word(member, u16(low16(member) << 8))\n'
                                          '    member = replace_byte(member, packet.byte(10))\n'
                                          '    member = u32(member << 8)\n'
                                          '    member = replace_byte(member, packet.byte(11))\n'
                                          '    member = u32(member << 8)\n'
                                          '    member = replace_byte(member, packet.byte(12))\n'
                                          '    old_supply = member\n'
                                          '    member = u32(member - values.count)\n'
                                          '    values = replace(values, member=member)\n'
                                          '    if old_supply < values.count:\n'
                                          '        values = apply_map_packet_supply_losses(state, '
                                          'values)\n'
                                          '        if not low16(values.value):\n'
                                          '            continue\n'
                                          '        member = 0\n'
                                          '    packet.set_byte(12, low8(member))\n'
                                          '    member >>= 8\n'
                                          '    packet.set_byte(11, low8(member))\n'
                                          '    member >>= 8\n'
                                          '    packet.set_byte(10, low8(member))\n'
                                          '    member = replace_word(member, low16(member) >> 8)\n'
                                          '    packet.set_byte(9, low8(member))\n'
                                          '    packet.base = u32(packet.base + 13 + '
                                          's16(low16(values.value)))\n'
                                          '    values = replace(values, member=member)'},
 'initialize_force_turn_order': {'signature': 'state: SceneState, values: CityCommandValues',
                                 'returns': 'CityCommandValues',
                                 'flow': 'checked_context(values, CityCommandValues, state)\n'
                                         'source, destination = (data_view(state, '
                                         "'data_030ed8').cursor(), _ram(state, 'f714').cursor())\n"
                                         'for _ in descending_inclusive(15):\n'
                                         '    destination.append_byte(source.next_byte())\n'
                                         'values = shuffle_force_turn_order(state, replace(values, '
                                         'value=replace_word(values.value, 65535), packet=destination, '
                                         'roster=source))\n'
                                         "_put(state, 'f724', 0)\n"
                                         "_put(state, 'f600', 176)\n"
                                         'return values'},
 'shuffle_force_turn_order': {'signature': 'state: SceneState, values: CityCommandValues',
                              'returns': 'CityCommandValues',
                              'flow': 'from .services import sample_random_pair\n'
                                      'checked_context(values, CityCommandValues, state)\n'
                                      "order = _ram(state, 'f714')\n"
                                      'value, field, member, count = (values.value, values.field, '
                                      'values.member, values.count)\n'
                                      'for iteration in descending_inclusive(15):\n'
                                      '    sample = sample_random_pair(state)\n'
                                      "    value = replace_word(sample.sample, _word(state, 'f61c') & "
                                      '15)\n'
                                      '    field = replace_word(sample.updated_state, _word(state, '
                                      "'f61c') >> 8 & 15)\n"
                                      '    member = replace_byte(member, order.byte(low16(value)))\n'
                                      '    if negative_byte(low8(member)):\n'
                                      '        continue\n'
                                      '    count = replace_byte(count, order.byte(low16(field)))\n'
                                      '    if negative_byte(low8(count)):\n'
                                      '        continue\n'
                                      '    order.set_byte(low16(value), low8(count))\n'
                                      '    order.set_byte(low16(field), low8(member))\n'
                                      'return replace(values, value=value, field=field, member=member, '
                                      'count=count, selected=replace_word(values.selected, 65535), '
                                      'packet=order.cursor())'},
 'select_next_force_turn': {'signature': 'state: SceneState, values: CityCommandValues',
                            'returns': 'CityCommandValues',
                            'flow': 'checked_context(values, CityCommandValues, state)\n'
                                    "value = replace_word(values.value, _word(state, 'f724'))\n"
                                    'field = values.field\n'
                                    "order, rulers = (_ram(state, 'f714'), _ram(state, 'e640'))\n"
                                    'while True:\n'
                                    '    field = replace_byte(field, order.byte(low16(value)))\n'
                                    '    field = replace_word(field, u16(low8(field) - 256 if '
                                    'negative_byte(low8(field)) else low8(field)))\n'
                                    '    if negative_word(low16(field)):\n'
                                    '        break\n'
                                    '    value = replace_word(value, u16(low16(value) + 1))\n'
                                    '    field = replace_word(field, u16(low16(field) << 1))\n'
                                    '    if not negative_word(rulers.word(low16(field))):\n'
                                    '        field = replace_word(field, low16(field) >> 1)\n'
                                    '        break\n'
                                    "_put(state, 'f724', value)\n"
                                    "_put(state, 'f376', field)\n"
                                    "_put(state, 'f364', 0)\n"
                                    'return replace(values, value=value, field=field, '
                                    'packet=order.cursor(), roster=rulers.cursor())'},
 'recover_idle_officer_readiness': {'signature': 'state: SceneState, values: CityCommandValues',
                                    'returns': 'CityCommandValues',
                                    'flow': 'checked_context(values, CityCommandValues, state)\n'
                                            'assignments, readiness, maximum, active = (_ram(state, '
                                            "'cc00'), _ram(state, 'b200'), _ram(state, 'b000'), "
                                            "_ram(state, 'ea38'))\n"
                                            'field = replace_word(values.field, 0)\n'
                                            'member, count = (values.member, values.count)\n'
                                            'for officer in descending_inclusive(255):\n'
                                            '    field = replace_byte(field, '
                                            'assignments.byte(officer))\n'
                                            '    if low8(field) > 40:\n'
                                            '        continue\n'
                                            '    if active.byte(low16(field)):\n'
                                            '        continue\n'
                                            '    field = replace_word(field, u16(officer << 1))\n'
                                            '    member = divu_retained(u32(maximum.word(low16(field)) '
                                            '* 15), 100)\n'
                                            '    count = replace_word(count, '
                                            'readiness.word(low16(field)))\n'
                                            '    count = replace_word(count, u16(low16(count) + '
                                            'low16(member)))\n'
                                            '    if low16(count) > maximum.word(low16(field)):\n'
                                            '        count = replace_word(count, '
                                            'maximum.word(low16(field)))\n'
                                            '    readiness.set_word(low16(field), low16(count))\n'
                                            'return replace(values, value=replace_word(values.value, '
                                            '65535), field=field, member=member, count=count, '
                                            'assignments=assignments, readiness=readiness, '
                                            'troops=maximum, scratch=active)'},
 'clear_unassigned_officer_commands': {'signature': 'state: SceneState, values: CityCommandValues',
                                       'returns': 'CityCommandValues',
                                       'flow': 'checked_context(values, CityCommandValues, state)\n'
                                               "flags = _ram(state, 'cd00').cursor()\n"
                                               'field = values.field\n'
                                               'for _ in descending_inclusive(255):\n'
                                               '    field = replace_byte(field, flags.next_byte())\n'
                                               '    if low8(field) < 2:\n'
                                               '        flags.set_byte(65535, 0)\n'
                                               'return replace(values, value=replace_word(values.value, '
                                               '65535), field=field, packet=flags)'},
 'select_next_force_city': {'signature': 'state: SceneState, values: CityCommandValues',
                            'returns': 'CityCommandValues',
                            'flow': 'checked_context(values, CityCommandValues, state)\n'
                                    "owners, gates = (_ram(state, 'f427'), _ram(state, 'ea37'))\n"
                                    "value = replace_word(values.value, u16(_word(state, 'f364') + 1))\n"
                                    "member = replace_word(values.member, _word(state, 'f376'))\n"
                                    'field = values.field\n'
                                    'while low16(value) <= 40:\n'
                                    '    if not gates.byte(low16(value)):\n'
                                    '        field = replace_byte(field, owners.byte(low16(value)))\n'
                                    '        if low8(field) == low8(member):\n'
                                    "            _put(state, 'f364', value)\n"
                                    '            return replace(values, value=value, field=field, '
                                    'member=member, packet=owners.cursor(), roster=gates.cursor())\n'
                                    '    value = replace_word(value, u16(low16(value) + 1))\n'
                                    'value = replace_word(value, 65535)\n'
                                    "_put(state, 'f364', value)\n"
                                    'return replace(values, value=value, field=field, member=member, '
                                    'packet=owners.cursor(), roster=gates.cursor())'},
 'select_next_force_map_packet': {'signature': 'state: SceneState, values: CityCommandValues',
                                  'returns': 'CityCommandValues',
                                  'flow': 'checked_context(values, CityCommandValues, state)\n'
                                          "packet = _ram(state, '9000').cursor(_word(state, 'f75a'))\n"
                                          "value = replace_word(values.value, _word(state, 'f376'))\n"
                                          'field = values.field\n'
                                          'while True:\n'
                                          '    field = replace_byte(field, packet.byte())\n'
                                          '    if not field & 32:\n'
                                          '        field = replace_word(field, low16(field) & 15)\n'
                                          '        if not low16(field):\n'
                                          '            break\n'
                                          '        if packet.byte(4) == low8(value):\n'
                                          '            value = replace_byte(replace_word(value, 0), '
                                          'packet.byte(1))\n'
                                          "            _put(state, 'f75c', value)\n"
                                          '            value = replace_byte(value, packet.byte(2))\n'
                                          "            _put(state, 'f75e', value)\n"
                                          '            value = replace_byte(value, packet.byte(3))\n'
                                          "            _put(state, 'f760', value)\n"
                                          '            return replace(values, value=value, field=field, '
                                          'packet=packet)\n'
                                          '    field = replace_word(field, low16(field) & 15)\n'
                                          '    if not low16(field):\n'
                                          '        break\n'
                                          '    packet.base = u32(packet.base + 13 + s16(low16(field)))\n'
                                          '    field = replace_word(field, u16(low16(field) + 13))\n'
                                          "    _put(state, 'f75a', u16(_word(state, 'f75a') + "
                                          'low16(field)))\n'
                                          "_put(state, 'f75a', 65535)\n"
                                          'return replace(values, value=value, field=field, '
                                          'packet=packet)'},
 'sample_city_command_policy': {'signature': 'state: SceneState, values: CityCommandValues',
                                'returns': 'CityCommandValues',
                                'flow': 'from .services import sample_random_pair\n'
                                        'checked_context(values, CityCommandValues, state)\n'
                                        'sample = sample_random_pair(state)\n'
                                        "value = replace_word(sample.sample, u16(_word(state, 'efd2') "
                                        '<< 6))\n'
                                        'parameters = data_view(state, '
                                        "'data_0311fc').cursor(low16(value))\n"
                                        "value = replace_word(value, u16(_word(state, 'f376') << 2))\n"
                                        "field = swap_words(u32(_word(state, 'f61c') << 4))\n"
                                        'member = replace_word(values.member, 0)\n'
                                        'if low16(field) >= parameters.word(low16(value)):\n'
                                        '    member = replace_word(member, u16(low16(member) + 4))\n'
                                        '    if low16(field) >= parameters.word(low16(value), '
                                        'displacement=2):\n'
                                        '        member = replace_word(member, u16(low16(member) + 4))\n'
                                        'sample = sample_random_pair(state)\n'
                                        "thresholds = data_view(state, 'data_0312bc')\n"
                                        'value = swap_words(u32((sample.sample & 65535) << 3))\n'
                                        'field = replace_word(sample.updated_state, 0)\n'
                                        'if low16(value) >= thresholds.word(low16(member)):\n'
                                        '    field = replace_word(field, u16(low16(field) + 1))\n'
                                        '    if low16(value) >= thresholds.word(low16(member), '
                                        'displacement=2):\n'
                                        '        field = replace_word(field, u16(low16(field) + 1))\n'
                                        "_put(state, 'f726', field)\n"
                                        'return replace(values, value=value, field=field, '
                                        'member=member, packet=parameters, scratch=thresholds)'},
 'clear_current_city_project_orders': {'signature': 'state: SceneState, values: CityCommandValues',
                                       'returns': 'CityCommandValues',
                                       'flow': 'checked_context(values, CityCommandValues, state)\n'
                                               'value = replace_word(values.value, u16(_word(state, '
                                               "'f364') * 12))\n"
                                               "projects = _ram(state, 'e80c')\n"
                                               'projects.set_long(low16(value), 4294967295)\n'
                                               'projects.set_long(low16(value), 4294967295, '
                                               'displacement=4)\n'
                                               'projects.set_long(low16(value), 4294967295, '
                                               'displacement=8)\n'
                                               'return replace(values, value=value, '
                                               'packet=projects.cursor())'},
 'build_current_city_officer_roster': {'signature': 'state: SceneState, values: CityCommandValues',
                                       'returns': 'CityCommandValues',
                                       'flow': 'checked_context(values, CityCommandValues, state)\n'
                                               'destination, assignments, flags = (_ram(state, '
                                               "'f72a').cursor(), _ram(state, 'cc00'), _ram(state, "
                                               "'cd00'))\n"
                                               'value = replace_word(values.value, _word(state, '
                                               "'f364'))\n"
                                               'field, member, count, found = (values.field, '
                                               'values.member, values.count, '
                                               'replace_word(values.readiness_loss, 0))\n'
                                               'for officer in descending_inclusive(255):\n'
                                               '    field = replace_word(field, officer)\n'
                                               '    member = replace_byte(member, '
                                               'assignments.byte(officer))\n'
                                               '    if low16(member) != low16(value):\n'
                                               '        continue\n'
                                               '    count = replace_word(count, officer)\n'
                                               '    if flags.byte(low16(count)):\n'
                                               '        count |= 16384\n'
                                               '    destination.append_word(low16(count))\n'
                                               '    found = replace_word(found, u16(low16(found) + 1))\n'
                                               'destination.put_word(65535)\n'
                                               "_put(state, 'f762', found)\n"
                                               'return replace(values, value=value, '
                                               'field=replace_word(field, 65535), member=member, '
                                               'count=count, readiness_loss=found, '
                                               'destination=destination, assignments=assignments, '
                                               'scratch=flags)'},
 'run_city_command_assignment': {'signature': 'state: SceneState, values: CityCommandValues',
                                 'returns': 'CityCommandValues',
                                 'flow': 'checked_context(values, CityCommandValues, state)\n'
                                         'values = sample_city_command_policy(state, values)\n'
                                         'while True:\n'
                                         '    values = select_next_force_city(state, values)\n'
                                         "    if negative_word(_word(state, 'f364')):\n"
                                         '        break\n'
                                         '    values = clear_current_city_project_orders(state, '
                                         'values)\n'
                                         '    values = build_current_city_officer_roster(state, '
                                         'values)\n'
                                         "    _put(state, 'f728', 1)\n"
                                         '    value = replace_word(values.value, u16(_word(state, '
                                         "'f726') << 1))\n"
                                         '    values = _vector(state, replace(values, value=value), '
                                         "value, 'data_031006', 200716, 200662)\n"
                                         'values = _call(state, 59438, values, 200670)\n'
                                         'values = clear_unassigned_officer_commands(state, values)\n'
                                         'from .business_highbank import advance_officer_growth_levels\n'
                                         'from .contexts_highbank import GrowthValues\n'
                                         'growth = advance_officer_growth_levels(state, '
                                         'GrowthValues(values.value, values.field, values.member))\n'
                                         'return replace(values, value=growth.values.selected, '
                                         'field=growth.values.value, member=growth.values.category, '
                                         'assignments=growth.assignments)'},
 'run_city_command_states': {'signature': 'state: SceneState, values: CityCommandValues',
                             'returns': 'CityCommandValues',
                             'flow': 'checked_context(values, CityCommandValues, state)\n'
                                     'while True:\n'
                                     '    values = select_next_force_city(state, values)\n'
                                     "    if negative_word(_word(state, 'f364')):\n"
                                     '        return values\n'
                                     '    values = build_current_city_officer_roster(state, values)\n'
                                     "    _put(state, 'f728', 1)\n"
                                     '    values = dispatch_city_command_stage(state, values)'},
 'run_map_packet_command_states': {'signature': 'state: SceneState, values: CityCommandValues',
                                   'returns': 'CityCommandValues',
                                   'flow': 'checked_context(values, CityCommandValues, state)\n'
                                           'while True:\n'
                                           '    values = select_next_force_map_packet(state, values)\n'
                                           "    if negative_word(_word(state, 'f75a')):\n"
                                           '        return values\n'
                                           "    _put(state, 'f728', 1)\n"
                                           '    values = dispatch_map_packet_command_stage(state, '
                                           'values)\n'
                                           "    packet = _ram(state, '9000').cursor(_word(state, "
                                           "'f75a'))\n"
                                           '    value = replace_byte(replace_word(values.value, 0), '
                                           'packet.byte())\n'
                                           '    value = replace_word(value, u16(low16(value) + 13))\n'
                                           "    _put(state, 'f75a', u16(_word(state, 'f75a') + "
                                           'low16(value)))\n'
                                           '    values = replace(values, value=value, packet=packet)'},
 'finish_city_command_assignment': {'signature': 'state: SceneState, values: CityCommandValues',
                                    'returns': 'CityCommandValues',
                                    'flow': 'checked_context(values, CityCommandValues, state)\n'
                                            'values = _call(state, 59552, values, 201196)\n'
                                            'from .business_gameplay import '
                                            'settle_city_projects_and_refresh_map\n'
                                            'from .contexts_gameplay import ProjectValues\n'
                                            'projects = ProjectValues(values.member, values.count, '
                                            'values.readiness_loss, values.troop_rate, values.selected, '
                                            'values.value, values.field, values.force_index, '
                                            "_ram(state, 'cc00'), _ram(state, 'cd00'), "
                                            'state.table_at(values.packet.base) if values.packet is not '
                                            'None else None)\n'
                                            'projects = settle_city_projects_and_refresh_map(state, '
                                            'projects)\n'
                                            "_put(state, 'f36c', 1)\n"
                                            'return replace(values, value=projects.city_index, '
                                            'field=projects.record_index, member=projects.officer, '
                                            'count=projects.budget, readiness_loss=projects.value, '
                                            'troop_rate=projects.scale, '
                                            'force_index=projects.city_offset, '
                                            'selected=projects.effect, '
                                            'assignments=projects.assignments, '
                                            'scratch=projects.task_flags, '
                                            'packet=projects.orders.cursor() if projects.orders is not '
                                            'None else values.packet)'},
 'retain_city_command_stage': {'signature': 'state: SceneState, values: CityCommandValues',
                               'returns': 'CityCommandValues',
                               'flow': 'checked_context(values, CityCommandValues, state)\n'
                                       'return values'},
 'dispatch_city_assignment_state': {'signature': 'state: SceneState, values: CityCommandValues',
                                    'returns': 'CityCommandValues',
                                    'flow': 'checked_context(values, CityCommandValues, state)\n'
                                            'value = replace_word(values.value, u16(_word(state, '
                                            "'f362') << 1))\n"
                                            'return _vector(state, replace(values, value=value), value, '
                                            "'data_0312d8', 201464, 201430)"},
 '_run_command_stage': {'signature': 'state, values, parameters, base, continuation',
                        'returns': None,
                        'flow': 'while True:\n'
                                "    value = replace_word(values.value, _word(state, 'f728'))\n"
                                '    values = replace(values, value=value)\n'
                                '    if negative_word(low16(value)):\n'
                                '        return values\n'
                                '    value = replace_word(value, u16(low16(value) - 1 << 1))\n'
                                '    values = _vector(state, replace(values, value=value), value, '
                                'parameters, base, continuation)'},
 'dispatch_city_command_stage': {'signature': 'state: SceneState, values: CityCommandValues',
                                 'returns': 'CityCommandValues',
                                 'flow': 'checked_context(values, CityCommandValues, state)\n'
                                         "return _run_command_stage(state, values, 'data_0338da', "
                                         '211180, 211158)'},
 'dispatch_map_packet_command_stage': {'signature': 'state: SceneState, values: CityCommandValues',
                                       'returns': 'CityCommandValues',
                                       'flow': 'checked_context(values, CityCommandValues, state)\n'
                                               "return _run_command_stage(state, values, 'data_034110', "
                                               '213312, 213260)'},
 'dispatch_auxiliary_command_stage': {'signature': 'state: SceneState, values: CityCommandValues',
                                      'returns': 'CityCommandValues',
                                      'flow': 'checked_context(values, CityCommandValues, state)\n'
                                              "return _run_command_stage(state, values, 'data_034f7c', "
                                              '216980, 216952)'},
 'begin_auxiliary_command_stage': {'signature': 'state: SceneState, values: CityCommandValues',
                                   'returns': 'CityCommandValues',
                                   'flow': 'checked_context(values, CityCommandValues, state)\n'
                                           'values = _call(state, 216886, values, 216874)\n'
                                           "_put(state, 'f728', 1)\n"
                                           'return dispatch_auxiliary_command_stage(state, values)'},
 '_glyph_cursor': {'signature': 'state, cursor, role',
                   'returns': None,
                   'flow': 'if cursor is None:\n'
                           "    raise Boundary('actual live ' + role + ' cursor required')\n"
                           'checked_cursor(cursor, state)\n'
                           'return cursor'},
 'upload_glyph_tile_sequence': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                'returns': 'GlyphTileLayout',
                                'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                        'state.write(12582916, 4, 1075838976)\n'
                                        'layout = replace(layout, counts=data_view(state, '
                                        "'data_08991c').cursor(), identifiers=data_view(state, "
                                        "'data_089932').cursor())\n"
                                        'return expand_glyph_tile_sequence(state, layout)'},
 'expand_glyph_tile_sequence': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                'returns': 'GlyphTileLayout',
                                'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                        "counts = _glyph_cursor(state, layout.counts, 'glyph count')\n"
                                        "identifiers = _glyph_cursor(state, layout.identifiers, 'glyph "
                                        "identifier')\n"
                                        'while True:\n'
                                        "    destination = ram_view(state, 'ram_d300').cursor()\n"
                                        '    count_carrier = replace_word(layout.value, 0)\n'
                                        '    count_carrier = replace_byte(count_carrier, '
                                        'counts.next_byte())\n'
                                        '    layout = replace(layout, value=count_carrier, '
                                        'destination=destination)\n'
                                        '    if low8(count_carrier) & 128:\n'
                                        '        return layout\n'
                                        '    if low8(count_carrier) == 0:\n'
                                        '        continue\n'
                                        '    layout = calculate_glyph_row_layout(state, layout)\n'
                                        '    while True:\n'
                                        '        layout = replace(layout, '
                                        'glyph=replace_word(layout.glyph, identifiers.next_word()))\n'
                                        '        layout = select_glyph_bitmap(state, layout)\n'
                                        '        layout = replace(layout, '
                                        'rows=replace_word(layout.rows, 15))\n'
                                        '        while True:\n'
                                        '            layout = expand_monochrome_glyph_byte(state, '
                                        'layout)\n'
                                        '            destination.set_long(0, layout.pixels)\n'
                                        '            layout = expand_monochrome_glyph_byte(state, '
                                        'layout)\n'
                                        '            '
                                        'state.write(destination.address(low16(layout.row_stride)), 4, '
                                        'layout.pixels)\n'
                                        '            destination = destination.advance(4)\n'
                                        '            layout = replace(layout, destination=destination, '
                                        'remaining=replace_word(layout.remaining, '
                                        'u16(low16(layout.remaining) - 1)), '
                                        'rows=replace_word(layout.rows, u16(low16(layout.rows) - 1)))\n'
                                        '            if low16(layout.rows) == 65535:\n'
                                        '                break\n'
                                        '        layout = replace(layout, '
                                        'value=replace_word(layout.value, u16(low16(layout.value) - '
                                        '1)))\n'
                                        '        if low16(layout.value) == 0:\n'
                                        '            break\n'
                                        '        layout = replace(layout, pixels=0)\n'
                                        '        destination.set_long(0, 0)\n'
                                        '        destination.set_long(0, 0, displacement=4)\n'
                                        '        '
                                        'state.write(destination.address(low16(layout.row_stride)), 4, '
                                        '0)\n'
                                        '        '
                                        'state.write(destination.address(low16(layout.row_stride), 4), '
                                        '4, 0)\n'
                                        '        destination = destination.advance(8)\n'
                                        '        layout = replace(layout, destination=destination, '
                                        'remaining=replace_word(layout.remaining, '
                                        'u16(low16(layout.remaining) - 2)))\n'
                                        '    if low16(layout.remaining) != 0:\n'
                                        '        layout = replace(layout, '
                                        'remaining=replace_word(layout.remaining, '
                                        'u16(low16(layout.remaining) - 1)))\n'
                                        '        while True:\n'
                                        '            layout = replace(layout, pixels=0)\n'
                                        '            destination.set_long(0, 0)\n'
                                        '            '
                                        'state.write(destination.address(low16(layout.row_stride)), 4, '
                                        '0)\n'
                                        '            destination = destination.advance(4)\n'
                                        '            layout = replace(layout, destination=destination, '
                                        'remaining=replace_word(layout.remaining, '
                                        'u16(low16(layout.remaining) - 1)))\n'
                                        '            if low16(layout.remaining) == 65535:\n'
                                        '                break\n'
                                        '    layout = upload_expanded_glyph_rows(state, layout)'},
 'calculate_glyph_row_layout': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                'returns': 'GlyphTileLayout',
                                'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                        'padding = u16(low16(layout.value) << 3)\n'
                                        'padding = u16(padding + 20) & 65504\n'
                                        'stride = u16(low16(layout.value) << 6)\n'
                                        'stride = u16(stride + padding)\n'
                                        'return replace(layout, '
                                        'row_stride=replace_word(layout.row_stride, stride), '
                                        'remaining=replace_word(layout.remaining, stride >> 2))'},
 'select_glyph_bitmap': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                         'returns': 'GlyphTileLayout',
                         'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                 'saved_glyph = low16(layout.glyph)\n'
                                 'upper_page = u32((layout.glyph & 65280) << 3)\n'
                                 'row_index = u16((saved_glyph & 255) << 5)\n'
                                 'bitmap_offset = replace_word(upper_page, u16(low16(upper_page) + '
                                 'row_index))\n'
                                 'bitmap = data_view(state, '
                                 "'data_08159c').cursor(low16(bitmap_offset))\n"
                                 'return replace(layout, glyph=saved_glyph, '
                                 'rows=replace_word(layout.rows, row_index), bitmap=bitmap)'},
 'expand_monochrome_glyph_byte': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                  'returns': 'GlyphTileLayout',
                                  'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                          "bitmap = _glyph_cursor(state, layout.bitmap, 'glyph "
                                          "bitmap')\n"
                                          'packed = replace_byte(layout.packed_bits, '
                                          'bitmap.next_byte())\n'
                                          'pixels = 0\n'
                                          'shift_count = replace_word(layout.shift_count, 7)\n'
                                          'while True:\n'
                                          '    incoming_extend = 1 if pixels & 268435456 else 0\n'
                                          '    pixels = u32(pixels << 4)\n'
                                          '    emitted_bit = bool(low8(packed) & 128)\n'
                                          '    packed = replace_byte(packed, (low8(packed) << 1 | '
                                          'incoming_extend) & 255)\n'
                                          '    if emitted_bit:\n'
                                          '        pixels = replace_byte(pixels, low8(pixels) | 1)\n'
                                          '    shift_count = replace_word(shift_count, '
                                          'u16(low16(shift_count) - 1))\n'
                                          '    if low16(shift_count) == 65535:\n'
                                          '        return replace(layout, packed_bits=packed, '
                                          'pixels=pixels, shift_count=shift_count)'},
 'upload_expanded_glyph_rows': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                'returns': 'GlyphTileLayout',
                                'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                        "destination = ram_view(state, 'ram_d300').cursor()\n"
                                        'stride = replace_word(layout.row_stride, '
                                        'low16(layout.row_stride) >> 1)\n'
                                        'stride = replace_word(stride, u16(low16(stride) - 1))\n'
                                        'while True:\n'
                                        '    state.write(12582912, 4, destination.next_long())\n'
                                        '    stride = replace_word(stride, u16(low16(stride) - 1))\n'
                                        '    if low16(stride) == 65535:\n'
                                        '        return replace(layout, destination=destination, '
                                        'row_stride=stride)'},
 'initialize_auxiliary_text_panel': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                     'returns': 'GlyphTileLayout',
                                     'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                             'selection = replace_word(layout.value, ram_view(state, '
                                             "'ram_f348').word())\n"
                                             'selection = replace_byte(selection, data_view(state, '
                                             "'data_03563e').byte(low16(selection)))\n"
                                             "ram_view(state, 'ram_f34a').set_word(0, "
                                             'low16(selection))\n'
                                             'stride = replace_word(layout.row_stride, 5)\n'
                                             'from .services import upload_portrait_tiles, '
                                             'SceneRenderFrame\n'
                                             'uploaded = upload_portrait_tiles(state, '
                                             'SceneRenderFrame(selection, stride, layout.remaining, '
                                             'layout.glyph, layout.rows))\n'
                                             'layout = replace(layout, value=uploaded.frame.x, '
                                             'row_stride=uploaded.frame.y, '
                                             'remaining=uploaded.frame.attributes, '
                                             'glyph=uploaded.frame.palette, rows=uploaded.frame.tile)\n'
                                             "counts = ram_view(state, 'ram_fb00').cursor()\n"
                                             "identifiers = ram_view(state, 'ram_fb80').cursor()\n"
                                             'value = replace_word(layout.value, 7)\n'
                                             'while True:\n'
                                             '    identifiers.append_long(counts.next_long())\n'
                                             '    value = replace_word(value, u16(low16(value) - 1))\n'
                                             '    if low16(value) == 65535:\n'
                                             '        break\n'
                                             'identifiers.set_long(0, 3822)\n'
                                             'layout = replace(layout, counts=counts, '
                                             'identifiers=identifiers, value=value, '
                                             'row_stride=1103757315)\n'
                                             'state.write(12582916, 2, 36736)\n'
                                             'layout = draw_auxiliary_text_panel_border(state, layout)\n'
                                             'layout = replace(layout, row_stride=u32(layout.row_stride '
                                             '- 8650752), remaining=replace_word(layout.remaining, '
                                             '8477))\n'
                                             'layout = draw_auxiliary_text_panel_rows(state, layout)\n'
                                             'state.write(12582916, 2, 36610)\n'
                                             'layout = upload_auxiliary_text_panel_glyphs(state, '
                                             'layout)\n'
                                             'return draw_auxiliary_text_panel_markers(state, layout)'},
 'draw_auxiliary_text_panel_border': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                      'returns': 'GlyphTileLayout',
                                      'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                              'value = replace_word(layout.value, 10)\n'
                                              'remaining = replace_word(layout.remaining, 5)\n'
                                              'stride, glyph, rows, shift = (layout.row_stride, '
                                              'layout.glyph, layout.rows, layout.shift_count)\n'
                                              'while True:\n'
                                              '    rows = replace_word(rows, low16(value))\n'
                                              '    state.write(12582916, 4, stride)\n'
                                              '    glyph = replace_word(glyph, 7)\n'
                                              '    while True:\n'
                                              '        state.write(12582912, 2, low16(rows))\n'
                                              '        rows = replace_word(rows, u16(low16(rows) + 6))\n'
                                              '        glyph = replace_word(glyph, u16(low16(glyph) - '
                                              '1))\n'
                                              '        if low16(glyph) == 65535:\n'
                                              '            break\n'
                                              '    if low16(remaining) in (3, 2):\n'
                                              '        shift = replace_word(shift, 8463 if '
                                              'low16(remaining) == 3 else 8449)\n'
                                              '        state.write(12582912, 2, 0)\n'
                                              '        state.write(12582912, 2, 0)\n'
                                              '        glyph = replace_word(glyph, 13)\n'
                                              '        while True:\n'
                                              '            state.write(12582912, 2, low16(shift))\n'
                                              '            shift = replace_word(shift, u16(low16(shift) '
                                              '+ 1))\n'
                                              '            glyph = replace_word(glyph, u16(low16(glyph) '
                                              '- 1))\n'
                                              '            if low16(glyph) == 65535:\n'
                                              '                break\n'
                                              '    value = replace_word(value, u16(low16(value) - 1))\n'
                                              '    stride = u32(stride - 131072)\n'
                                              '    remaining = replace_word(remaining, '
                                              'u16(low16(remaining) - 1))\n'
                                              '    if low16(remaining) == 65535:\n'
                                              '        return replace(layout, value=value, '
                                              'row_stride=stride, remaining=remaining, glyph=glyph, '
                                              'rows=rows, shift_count=shift)'},
 'draw_auxiliary_text_panel_rows': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                    'returns': 'GlyphTileLayout',
                                    'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                            'value = replace_word(layout.value, ram_view(state, '
                                            "'ram_f348').word())\n"
                                            'value = replace_word(value, u16(low16(value) << 2))\n'
                                            'pointer = data_view(state, '
                                            "'data_035710').long(low16(value))\n"
                                            'counts = state.table_at(pointer).cursor()\n'
                                            'glyph = replace_word(layout.glyph, 8)\n'
                                            'stride, remaining = (layout.row_stride, layout.remaining)\n'
                                            'rows, shift, packed = (layout.rows, layout.shift_count, '
                                            'layout.packed_bits)\n'
                                            'while True:\n'
                                            '    counts = counts.advance(1)\n'
                                            '    rows = replace_byte(rows, counts.next_byte())\n'
                                            '    rows = replace_word(rows, low16(rows) & 255)\n'
                                            '    shift = replace_word(shift, low16(rows))\n'
                                            '    shift = replace_word(shift, u16(low16(shift) << 1))\n'
                                            '    shift = replace_word(shift, u16(low16(shift) + 5))\n'
                                            '    shift = replace_word(shift, low16(shift) >> 3)\n'
                                            '    rows = replace_word(rows, u16(low16(rows) << 1))\n'
                                            '    rows = replace_word(rows, u16(low16(rows) + '
                                            'low16(shift)))\n'
                                            '    shift = replace_word(shift, low16(remaining))\n'
                                            '    shift = replace_word(shift, u16(low16(shift) + '
                                            'low16(rows)))\n'
                                            '    packed = replace_word(packed, u16(low16(rows) - 1))\n'
                                            '    state.write(12582916, 4, stride)\n'
                                            '    while True:\n'
                                            '        state.write(12582912, 2, low16(shift))\n'
                                            '        shift = replace_word(shift, u16(low16(shift) + '
                                            '1))\n'
                                            '        packed = replace_word(packed, u16(low16(packed) - '
                                            '1))\n'
                                            '        if low16(packed) == 65535:\n'
                                            '            break\n'
                                            '    stride = u32(stride - 131072)\n'
                                            '    state.write(12582916, 4, stride)\n'
                                            '    packed = replace_word(packed, u16(low16(rows) - 1))\n'
                                            '    while True:\n'
                                            '        state.write(12582912, 2, low16(remaining))\n'
                                            '        remaining = replace_word(remaining, '
                                            'u16(low16(remaining) + 1))\n'
                                            '        packed = replace_word(packed, u16(low16(packed) - '
                                            '1))\n'
                                            '        if low16(packed) == 65535:\n'
                                            '            break\n'
                                            '    stride = u32(stride - 262144)\n'
                                            '    remaining = replace_word(remaining, '
                                            'u16(low16(remaining) + low16(rows)))\n'
                                            '    glyph = replace_word(glyph, u16(low16(glyph) - 1))\n'
                                            '    if low16(glyph) == 65535:\n'
                                            '        return replace(layout, value=value, '
                                            'row_stride=stride, remaining=remaining, glyph=glyph, '
                                            'rows=rows, shift_count=shift, packed_bits=packed, '
                                            'counts=counts)'},
 'upload_auxiliary_text_panel_glyphs': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                        'returns': 'GlyphTileLayout',
                                        'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                                'state.write(12582916, 4, 1612709888)\n'
                                                'value = replace_word(layout.value, ram_view(state, '
                                                "'ram_f348').word())\n"
                                                'value = replace_word(value, u16(low16(value) << 2))\n'
                                                'counts = state.table_at(data_view(state, '
                                                "'data_035710').long(low16(value))).cursor()\n"
                                                'identifiers = state.table_at(data_view(state, '
                                                "'data_035728').long(low16(value))).cursor()\n"
                                                'return expand_glyph_tile_sequence(state, '
                                                'replace(layout, value=value, counts=counts, '
                                                'identifiers=identifiers))'},
 'draw_auxiliary_text_panel_markers': {'signature': 'state: SceneState, layout: GlyphTileLayout',
                                       'returns': 'GlyphTileLayout',
                                       'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                               'state.write(12582916, 4, 1128398851)\n'
                                               'state.write(12582912, 4, 3473462)\n'
                                               'state.write(12582912, 4, 3604536)\n'
                                               'state.write(12582916, 4, 1145307139)\n'
                                               'state.write(12582912, 4, 3997758)\n'
                                               'return layout'},
 '_presentation_word': {'signature': 'state, name',
                        'returns': None,
                        'flow': "return ram_view(state, 'ram_' + name).word()"},
 '_presentation_store': {'signature': 'state, name, value',
                         'returns': None,
                         'flow': "ram_view(state, 'ram_' + name).set_word(0, low16(value))"},
 '_presentation_call': {'signature': 'state, target, frame, continuation',
                        'returns': None,
                        'flow': 'from .services import call_target\n'
                                'result = call_target(state, uint(target, 32), SceneCall(frame, '
                                'continuation))\n'
                                'if type(result) is not ScenePresentation:\n'
                                "    raise Boundary('presentation service must return its declared "
                                "operands')\n"
                                'return result.validate(state)'},
 '_presentation_video': {'signature': 'frame',
                         'returns': None,
                         'flow': 'if type(frame.video_address) is not VideoPlaneAddress:\n'
                                 "    raise Boundary('this plane entry requires its actual A1 video "
                                 "carrier')\n"
                                 'return frame.video_address'},
 '_presentation_plane_row': {'signature': 'state, frame, decoder_continuation',
                             'returns': None,
                             'flow': 'from .services import set_vram_write_address\n'
                                     'column = replace_word(frame.tile, u16(low16(frame.tile) + 1))\n'
                                     'frame = replace(frame, tile=column)\n'
                                     'if low8(column) < 32:\n'
                                     '    return (frame, False)\n'
                                     'rows = replace_word(frame.palette, u16(low16(frame.palette) - '
                                     '1))\n'
                                     'frame = replace(frame, palette=rows)\n'
                                     'if low16(rows) == 0:\n'
                                     '    return (replace(frame, command=decoder_continuation), True)\n'
                                     'address = _presentation_video(frame).advance_full(frame.stride)\n'
                                     'command = set_vram_write_address(state, address)\n'
                                     'return (replace(frame, command=command, tile=0, '
                                     'video_address=address), False)'},
 '_presentation_decode_plane_tail': {'signature': 'state, frame',
                                     'returns': None,
                                     'flow': 'from .services import set_vram_write_address\n'
                                             'source = frame.source\n'
                                             'checked_cursor(source, state)\n'
                                             'address = _presentation_video(frame)\n'
                                             'state.write(12582916, 2, 36610)\n'
                                             'frame = replace(frame, '
                                             'command=set_vram_write_address(state, address), tile=0)\n'
                                             "if _presentation_word(state, '8002') == 0:\n"
                                             '    frame = replace(frame, '
                                             'foreground=replace_byte(frame.foreground, '
                                             'source.next_byte()))\n'
                                             'while True:\n'
                                             '    value = replace_byte(frame.mode, source.next_byte())\n'
                                             '    frame = replace(frame, mode=value)\n'
                                             "    literal = _presentation_word(state, '8002') != 0 or "
                                             'low8(frame.foreground) != low8(value)\n'
                                             '    if literal:\n'
                                             '        value = replace_word(value, u16(low16(value) << '
                                             '8))\n'
                                             '        value = replace_byte(value, source.next_byte())\n'
                                             '        value = replace_word(value, low16(value) | '
                                             "_presentation_word(state, '8000'))\n"
                                             '        state.write(12582912, 2, low16(value))\n'
                                             '        frame, escaped = _presentation_plane_row(state, '
                                             'replace(frame, mode=value), 240400)\n'
                                             '        if escaped:\n'
                                             '            return frame\n'
                                             '    else:\n'
                                             '        count = source.next_byte()\n'
                                             '        frame = replace(frame, rows=count)\n'
                                             '        if count == 0:\n'
                                             '            return frame\n'
                                             '        value = replace_byte(frame.mode, '
                                             'source.next_byte())\n'
                                             '        value = replace_word(value, u16(low16(value) << '
                                             '8))\n'
                                             '        value = replace_byte(value, source.next_byte())\n'
                                             '        frame = replace(frame, mode=value)\n'
                                             '        while True:\n'
                                             '            value = replace_word(frame.mode, '
                                             "low16(frame.mode) | _presentation_word(state, '8000'))\n"
                                             '            state.write(12582912, 2, low16(value))\n'
                                             '            frame, escaped = '
                                             '_presentation_plane_row(state, replace(frame, '
                                             'mode=value), 240428)\n'
                                             '            if escaped:\n'
                                             '                return frame\n'
                                             '            count = u16(low16(frame.rows) - 1)\n'
                                             '            frame = replace(frame, '
                                             'rows=replace_word(frame.rows, count))\n'
                                             '            if count == 65535:\n'
                                             '                break'},
 'decode_unmasked_literal_plane': {'signature': 'state: SceneState, frame: ScenePresentation',
                                   'returns': 'ScenePresentation',
                                   'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                           "_presentation_store(state, '8000', 0)\n"
                                           "_presentation_store(state, '8002', 1)\n"
                                           'return _presentation_decode_plane_tail(state, frame)'},
 'decode_high_plane_rows': {'signature': 'state: SceneState, frame: ScenePresentation',
                            'returns': 'ScenePresentation',
                            'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                    "_presentation_store(state, '8000', 32768)\n"
                                    'frame = replace(frame, palette=replace_word(frame.palette, 32))\n'
                                    "_presentation_store(state, '8002', 0)\n"
                                    'return _presentation_decode_plane_tail(state, frame)'},
 '_presentation_full_plane': {'signature': 'state, frame',
                              'returns': None,
                              'flow': "_presentation_store(state, '8000', 0)\n"
                                      'frame = replace(frame, palette=replace_word(frame.palette, 32))\n'
                                      "_presentation_store(state, '8002', 0)\n"
                                      'return _presentation_decode_plane_tail(state, frame)'},
 '_presentation_swapped_tiles': {'signature': 'state, frame',
                                 'returns': None,
                                 'flow': 'from .services import set_vram_write_address\n'
                                         'source = frame.source\n'
                                         'checked_cursor(source, state)\n'
                                         'state.write(12582916, 2, 36610)\n'
                                         'command = set_vram_write_address(state, '
                                         'VideoPlaneAddress(low16(frame.command)))\n'
                                         'marker = replace_byte(frame.foreground, source.next_byte())\n'
                                         'frame = replace(frame, command=command, foreground=marker)\n'
                                         'while True:\n'
                                         '    low = replace_byte(frame.mode, source.next_byte())\n'
                                         '    frame = replace(frame, mode=low)\n'
                                         '    if low8(marker) != low8(low):\n'
                                         '        pixels = replace_byte(frame.tile, '
                                         'source.next_byte())\n'
                                         '        pixels = replace_word(pixels, u16(low16(pixels) << '
                                         '8))\n'
                                         '        pixels = replace_byte(pixels, low8(low))\n'
                                         '        state.write(12582912, 2, low16(pixels))\n'
                                         '        frame = replace(frame, tile=pixels)\n'
                                         '    else:\n'
                                         '        count = source.next_byte()\n'
                                         '        frame = replace(frame, rows=count)\n'
                                         '        if count == 0:\n'
                                         '            return frame\n'
                                         '        low = replace_byte(frame.mode, source.next_byte())\n'
                                         '        pixels = replace_byte(frame.tile, '
                                         'source.next_byte())\n'
                                         '        pixels = replace_word(pixels, u16(low16(pixels) << '
                                         '8))\n'
                                         '        pixels = replace_byte(pixels, low8(low))\n'
                                         '        frame = replace(frame, mode=low, tile=pixels)\n'
                                         '        while True:\n'
                                         '            state.write(12582912, 2, low16(pixels))\n'
                                         '            count = u16(low16(frame.rows) - 1)\n'
                                         '            frame = replace(frame, '
                                         'rows=replace_word(frame.rows, count))\n'
                                         '            if count == 65535:\n'
                                         '                break'},
 '_presentation_select_tiles': {'signature': 'state, frame, directory_name, video_word',
                                'returns': None,
                                'flow': 'selected = replace_word(frame.command, '
                                        "_presentation_word(state, '80da'))\n"
                                        'selected = replace_word(selected, u16(low16(selected) << 2))\n'
                                        'directory = data_view(state, directory_name)\n'
                                        'source = '
                                        'state.table_at(directory.long(low16(selected))).cursor()\n'
                                        'frame = replace(frame, source=source, '
                                        'command=replace_word(selected, video_word))\n'
                                        'return _presentation_swapped_tiles(state, frame)'},
 '_presentation_select_plane': {'signature': 'state, frame, directory_name, video_address',
                                'returns': None,
                                'flow': 'selected = replace_word(frame.command, '
                                        "_presentation_word(state, '80da'))\n"
                                        'selected = replace_word(selected, u16(low16(selected) << 2))\n'
                                        'directory = data_view(state, directory_name)\n'
                                        'source = '
                                        'state.table_at(directory.long(low16(selected))).cursor()\n'
                                        'frame = replace(frame, source=source, command=selected, '
                                        'destination=None, '
                                        'video_address=VideoPlaneAddress(video_address), stride=128)\n'
                                        'return _presentation_full_plane(state, frame)'},
 '_presentation_copy_palette': {'signature': 'state, frame',
                                'returns': None,
                                'flow': 'index = replace_word(frame.command, u16(low16(frame.command) '
                                        '<< 3))\n'
                                        'directory = data_view(state, '
                                        "'data_03abac').cursor(low16(index))\n"
                                        'source = state.table_at(directory.next_long()).cursor()\n'
                                        'destination = '
                                        'state.table_at(u32(s16(directory.next_word()))).cursor()\n'
                                        'count = replace_word(frame.remaining, directory.next_word())\n'
                                        'while True:\n'
                                        '    destination.append_long(source.next_long())\n'
                                        '    count = replace_word(count, u16(low16(count) - 1))\n'
                                        '    if low16(count) == 65535:\n'
                                        '        return replace(frame, command=index, remaining=count, '
                                        'destination=directory, video_address=None, actor=source, '
                                        'opponent=destination)'},
 'initialize_object_scene_video': {'signature': 'state: SceneState, frame: ScenePresentation',
                                   'returns': 'ScenePresentation',
                                   'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                           'state.write(12582916, 2, 36610)\n'
                                           'state.write(12582916, 2, 33328)\n'
                                           'state.write(12582916, 2, 33584)\n'
                                           'state.write(12582916, 2, 33799)\n'
                                           'state.write(12582916, 2, 34152)\n'
                                           'state.write(12582916, 2, 34560)\n'
                                           'state.write(12582916, 2, 35584)\n'
                                           'state.write(12582916, 2, 35969)\n'
                                           'state.write(12582916, 2, 36149)\n'
                                           'state.write(12582916, 2, 36610)\n'
                                           'state.write(12582916, 2, 36881)\n'
                                           'state.write(12582916, 2, 37268)\n'
                                           'state.write(12582916, 2, 37376)\n'
                                           "_presentation_store(state, '8020', 48)\n"
                                           "_presentation_store(state, '8024', 0)\n"
                                           "_presentation_store(state, '8026', 48)\n"
                                           "_presentation_store(state, '8022', 32)\n"
                                           "_presentation_store(state, '8028', 0)\n"
                                           "_presentation_store(state, '802a', 32)\n"
                                           'frame = _presentation_select_tiles(state, frame, '
                                           "'data_03dc54', 0)\n"
                                           'frame = _presentation_select_tiles(state, frame, '
                                           "'data_03dc68', 8192)\n"
                                           'frame = _presentation_select_tiles(state, frame, '
                                           "'data_03dc7c', 16384)\n"
                                           'frame = replace(frame, source=data_view(state, '
                                           "'data_04e090').cursor(), "
                                           'command=replace_word(frame.command, 32768))\n'
                                           'frame = _presentation_swapped_tiles(state, frame)\n'
                                           'frame = replace(frame, source=data_view(state, '
                                           "'data_04fbe4').cursor(), "
                                           'command=replace_word(frame.command, 40960))\n'
                                           'frame = _presentation_swapped_tiles(state, frame)\n'
                                           'frame = _presentation_select_plane(state, frame, '
                                           "'data_03dc90', 57344)\n"
                                           'frame = _presentation_select_plane(state, frame, '
                                           "'data_03dca4', 61440)\n"
                                           'frame = replace(frame, source=data_view(state, '
                                           "'data_045413').cursor(), destination=None, "
                                           'video_address=VideoPlaneAddress(49152), stride=128)\n'
                                           'frame = decode_unmasked_literal_plane(state, frame)\n'
                                           'frame = replace(frame, source=data_view(state, '
                                           "'data_0456ec').cursor(), destination=None, "
                                           'video_address=VideoPlaneAddress(49216), stride=128)\n'
                                           'frame = decode_high_plane_rows(state, frame)\n'
                                           'selected = replace_word(frame.command, '
                                           "_presentation_word(state, '80da'))\n"
                                           'selected = replace_word(selected, u16(low16(selected) + '
                                           '4))\n'
                                           'return _presentation_copy_palette(state, replace(frame, '
                                           'command=selected))'},
 'dispatch_repeating_scene_presentation': {'signature': 'state: SceneState, frame: ScenePresentation',
                                           'returns': 'ScenePresentation',
                                           'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                                   "selection = u16(_presentation_word(state, '80da') "
                                                   '<< 2)\n'
                                                   'frame = replace(frame, '
                                                   'command=replace_word(frame.command, selection))\n'
                                                   'if selection == 0:\n'
                                                   '    target = 243634\n'
                                                   'elif selection == 4:\n'
                                                   '    target = 246162\n'
                                                   'elif selection == 8:\n'
                                                   '    target = 248474\n'
                                                   'elif selection == 12:\n'
                                                   '    target = 250226\n'
                                                   'elif selection == 16:\n'
                                                   '    target = 248176\n'
                                                   'else:\n'
                                                   '    target = u32(243614 + s16(selection))\n'
                                                   'return _presentation_call(state, target, frame, '
                                                   '243582)'},
 'run_repeating_scene_presentation': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                              'state.set_status_word(9984)\n'
                                              'command = replace_word(frame.command, '
                                              "_presentation_word(state, 'f606'))\n"
                                              'command = replace_byte(command, low8(command) & 191)\n'
                                              'state.write(12582916, 2, low16(command))\n'
                                              'frame = _presentation_call(state, 26830, replace(frame, '
                                              'command=command), 243530)\n'
                                              'frame = initialize_object_scene_video(state, frame)\n'
                                              'from .services import snapshot_and_clear_scene_palette\n'
                                              'snapshot = snapshot_and_clear_scene_palette(state)\n'
                                              'frame = replace(frame, source=snapshot.source, '
                                              'destination=snapshot.destination, video_address=None, '
                                              'foreground=65535)\n'
                                              'command = replace_word(frame.command, '
                                              "_presentation_word(state, '80da'))\n"
                                              'offset = u16(low16(command) << 1)\n'
                                              'command = replace_word(command, data_view(state, '
                                              "'data_03b788').word(offset))\n"
                                              'frame = _presentation_call(state, 32906, replace(frame, '
                                              'command=command), 243554)\n'
                                              'state.set_status_word(9472)\n'
                                              'while True:\n'
                                              "    _presentation_store(state, 'f612', 1280)\n"
                                              '    from .services import wait_for_scene_sound_byte\n'
                                              '    wait_for_scene_sound_byte(state)\n'
                                              '    frame = _presentation_call(state, 242312, frame, '
                                              '243574)\n'
                                              '    frame = _presentation_call(state, 239992, frame, '
                                              '243578)\n'
                                              '    frame = dispatch_repeating_scene_presentation(state, '
                                              'frame)\n'
                                              '    frame = _presentation_call(state, 242236, frame, '
                                              '243588)'},
 'set_uniform_conservative_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                     'returns': 'ScenePresentation',
                                     'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                             "_presentation_store(state, '812a', 5)\n"
                                             "_presentation_store(state, '812c', 5)\n"
                                             "_presentation_store(state, '812e', 5)\n"
                                             'return frame'},
 'set_first_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                              "order = 1 if _presentation_word(state, '8160') < 4 else "
                                              '5\n'
                                              "_presentation_store(state, '812a', order)\n"
                                              "_presentation_store(state, '812c', order)\n"
                                              "_presentation_store(state, '812e', order)\n"
                                              'return frame'},
 'set_mixed_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                              "if _presentation_word(state, '8160') < 5:\n"
                                              "    _presentation_store(state, '812a', 1)\n"
                                              "    _presentation_store(state, '812c', 1)\n"
                                              "    _presentation_store(state, '812e', 4)\n"
                                              'else:\n'
                                              "    _presentation_store(state, '812a', 5)\n"
                                              "    _presentation_store(state, '812c', 5)\n"
                                              "    _presentation_store(state, '812e', 5)\n"
                                              'return frame'},
 'set_third_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                              "order = 1 if _presentation_word(state, '8160') < 5 else "
                                              '5\n'
                                              "_presentation_store(state, '812a', order)\n"
                                              "_presentation_store(state, '812c', order)\n"
                                              "_presentation_store(state, '812e', order)\n"
                                              'return frame'},
 'set_uniform_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                        'returns': 'ScenePresentation',
                                        'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                                "order = 4 if _presentation_word(state, '8160') < 6 "
                                                'else 5\n'
                                                "_presentation_store(state, '812a', order)\n"
                                                "_presentation_store(state, '812c', order)\n"
                                                "_presentation_store(state, '812e', order)\n"
                                                'return frame'},
 '_presentation_random': {'signature': 'state, frame, mask',
                          'returns': None,
                          'flow': 'from .services import sample_random_preserving_seed_carrier\n'
                                  'value = sample_random_preserving_seed_carrier(state)\n'
                                  'return replace(frame, command=replace_word(value, low16(value) & '
                                  'mask))'},
 'choose_first_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                        "if _presentation_word(state, '8160') < 6:\n"
                                        "    _presentation_store(state, '8130', 4)\n"
                                        '    frame = _presentation_random(state, frame, 3)\n'
                                        '    if low16(frame.command) == 0:\n'
                                        "        _presentation_store(state, '8130', 5)\n"
                                        '    return frame\n'
                                        "_presentation_store(state, '8130', 5)\n"
                                        "if _presentation_word(state, '8178') > 40:\n"
                                        '    return frame\n'
                                        'frame = _presentation_random(state, frame, 7)\n'
                                        'if low16(frame.command) != 0:\n'
                                        "    _presentation_store(state, '8130', 4)\n"
                                        'return frame'},
 'choose_alternate_first_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                          'returns': 'ScenePresentation',
                                          'flow': 'return choose_first_leader_action(state, frame)'},
 'choose_second_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                 'returns': 'ScenePresentation',
                                 'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                         "_presentation_store(state, '8130', 4)\n"
                                         "if _presentation_word(state, '8160') < 6:\n"
                                         '    return frame\n'
                                         "_presentation_store(state, '8130', 1)\n"
                                         "if _presentation_word(state, '8160') >= 10:\n"
                                         "    _presentation_store(state, '8130', 5)\n"
                                         "if _presentation_word(state, '8178') > 40:\n"
                                         '    return frame\n'
                                         'frame = _presentation_random(state, frame, 1)\n'
                                         'if low16(frame.command) == 0:\n'
                                         "    _presentation_store(state, '8130', 4)\n"
                                         'return frame'},
 'choose_third_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                        'frame = _presentation_random(state, frame, 1)\n'
                                        'if low16(frame.command) == 0 and _presentation_word(state, '
                                        "'8160') >= 5:\n"
                                        "    _presentation_store(state, '8130', 5)\n"
                                        'else:\n'
                                        "    _presentation_store(state, '8130', 4)\n"
                                        'return frame'},
 'choose_fifth_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                        'frame = _presentation_random(state, frame, 1)\n'
                                        'if low16(frame.command) == 0 and _presentation_word(state, '
                                        "'8160') >= 6:\n"
                                        "    _presentation_store(state, '8130', 5)\n"
                                        'else:\n'
                                        "    _presentation_store(state, '8130', 4)\n"
                                        'return frame'}}

def _lower_refresh_setup_option_labels(emitter,rules):
    emitter.segment(0x30088,0x300de)
    emitter.ins('move.w','0xff7032:l,%d0',6)
    emitter.ins('move.w','0xff7026:l,%d1',6)
    emitter.ins('cmp.w','%d0,%d1',2)
    emitter.ins('beq.w','main_pc_0300dc',4)
    emitter.ins('lea.l','66(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('asl.w','#0x2,%d1',2)
    emitter.ins('movea.l','(%a0, %d1.w),%a0',4)
    emitter.ins('move.w','(%a0),%d0',2)
    emitter.ins('cmpi.w','#0xffff,%d0',4)
    emitter.ins('beq.w','main_pc_0300d2',4)
    emitter.ins('jsr','-19564(%pc)',4)
    emitter.ins('moveq','#0,%d0',2)
    emitter.ins('move.w','(%a0)+,%d5',2)
    emitter.ins('clr.l','%d5',2)
    emitter.ins('move.w','(%a0)+,%d0',2)
    emitter.ins('cmpi.w','#0xffff,%d0',4)
    emitter.ins('beq.b','main_pc_0300a6',2)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('ori.w','#0x8300,%d0',4)
    emitter.ins('move.w','%d0,0xc00000:l',6)
    emitter.ins('bra.b','main_pc_0300ba',2)
    emitter.ins('move.w','0xff7026:l,0xff7032:l',10)
    emitter.ins('rts','',2)

def _lower_render_packed_sprite_position(emitter,rules):
    emitter.segment(0x302ac,0x302c2)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('asr.w','#0x8,%d0',2)
    emitter.ins('andi.w','#0xff,%d0',4)
    emitter.ins('andi.w','#0xff,%d1',4)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('rts','',2)

def _lower_render_selected_setup_options(emitter,rules):
    emitter.segment(0x302c2,0x30456)
    emitter.ins('tst.w','0xff7022:l',6)
    emitter.ins('bne.w','main_pc_0302d6',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_0302f0',4)
    emitter.ins('move.w','0xff7026:l,%d1',6)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','374(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a0, %d1.w),%d0',4)
    emitter.ins('lea.l','-20948(%pc),%a0',4)
    emitter.ins('jsr','-66(%pc)',4)
    emitter.ins('cmpi.w','#0x1,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_030306',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_030320',4)
    emitter.ins('move.w','0xff7024:l,%d1',6)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','332(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a0, %d1.w),%d0',4)
    emitter.ins('lea.l','-20982(%pc),%a0',4)
    emitter.ins('jsr','-114(%pc)',4)
    emitter.ins('cmpi.w','#0x2,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_030336',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_030350',4)
    emitter.ins('move.w','0xff7028:l,%d1',6)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','290(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a0, %d1.w),%d0',4)
    emitter.ins('lea.l','-21030(%pc),%a0',4)
    emitter.ins('jsr','-162(%pc)',4)
    emitter.ins('cmpi.w','#0x3,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_030366',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_030380',4)
    emitter.ins('move.w','0xff702a:l,%d1',6)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','246(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a0, %d1.w),%d0',4)
    emitter.ins('lea.l','-21078(%pc),%a0',4)
    emitter.ins('jsr','-210(%pc)',4)
    emitter.ins('cmpi.w','#0x4,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_030396',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_0303c4',4)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('beq.w','main_pc_030440',4)
    emitter.ins('move.w','0xff702c:l,%d0',6)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('lea.l','192(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','(%a0, %d0.w),%d1',4)
    emitter.ins('move.w','#0xb0,%d0',4)
    emitter.ins('lea.l','-21128(%pc),%a0',4)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('tst.w','0xff7034:l',6)
    emitter.ins('beq.w','main_pc_03043e',4)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('bcs.w','main_pc_03043e',4)
    emitter.ins('bne.w','main_pc_0303e8',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_030400',4)
    emitter.ins('lea.l','-21168(%pc),%a0',4)
    emitter.ins('move.w','0xff702e:l,%d0',6)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('jsr','140(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('cmpi.w','#0x2,0xff7034:l',8)
    emitter.ins('bne.w','main_pc_03043e',4)
    emitter.ins('cmpi.w','#0x6,0xff7022:l',8)
    emitter.ins('bcs.w','main_pc_03043e',4)
    emitter.ins('bne.w','main_pc_030426',4)
    emitter.ins('btst.b','#0x3,0xf321:w',6)
    emitter.ins('bne.w','main_pc_03043e',4)
    emitter.ins('lea.l','-21222(%pc),%a0',4)
    emitter.ins('move.w','0xff7030:l,%d0',6)
    emitter.ins('movem.l','%d0,-(%a7)',4)
    emitter.ins('jsr','78(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('movem.l','(%a7)+,%d0',4)
    emitter.ins('rts','',2)
    emitter.ins('cmpi.w','#0x3,0xff702c:l',8)
    emitter.ins('bcs.w','main_pc_0303a2',4)
    emitter.ins('clr.w','0xff702c:l',6)
    emitter.ins('bra.w','main_pc_0303a2',4)

def _lower_render_setup_player_position(emitter,rules):
    emitter.segment(0x30484,0x3049c)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('lea.l','-28(%pc),%a3',4)
    emitter.ins('move.w','(%a3, %d0.w),%d1',4)
    emitter.ins('move.w','#0xb0,%d0',4)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('rts','',2)

def _lower_cycle_second_player_choice(emitter,rules):
    emitter.segment(0x3049c,0x3051e)
    emitter.ins('cmpi.w','#0x10,0xff7038:l',8)
    emitter.ins('bcs.w','main_pc_03051c',4)
    emitter.ins('cmpi.w','#0x10,0xff703a:l',8)
    emitter.ins('bcs.w','main_pc_03051c',4)
    emitter.ins('btst.b','#0x2,0xf605:w',6)
    emitter.ins('beq.w','main_pc_0304e2',4)
    emitter.ins('tst.w','%d5',2)
    emitter.ins('bne.w','main_pc_0304d4',4)
    emitter.ins('moveq','#2,%d5',2)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('beq.b','main_pc_0304d2',2)
    emitter.ins('moveq','#6,%d5',2)
    emitter.ins('bra.b','main_pc_0304d8',2)
    emitter.ins('subi.w','#0x1,%d5',4)
    emitter.ins('cmp.w','0xff702c:l,%d5',6)
    emitter.ins('beq.b','main_pc_0304be',2)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x3,0xf605:w',6)
    emitter.ins('beq.w','main_pc_030514',4)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('bcs.w','main_pc_030504',4)
    emitter.ins('cmpi.w','#0x2,%d5',4)
    emitter.ins('beq.w','main_pc_030512',4)
    emitter.ins('bra.w','main_pc_03050c',4)
    emitter.ins('cmpi.w','#0x6,%d5',4)
    emitter.ins('beq.w','main_pc_030512',4)
    emitter.ins('addi.w','#0x1,%d5',4)
    emitter.ins('bra.b','main_pc_030514',2)
    emitter.ins('clr.w','%d5',2)
    emitter.ins('cmp.w','0xff702c:l,%d5',6)
    emitter.ins('beq.b','main_pc_0304ec',2)
    emitter.ins('rts','',2)

def _lower_cycle_third_player_choice(emitter,rules):
    emitter.segment(0x3051e,0x305b0)
    emitter.ins('cmpi.w','#0x10,0xff7038:l',8)
    emitter.ins('bcs.w','main_pc_0305ae',4)
    emitter.ins('cmpi.w','#0x10,0xff703a:l',8)
    emitter.ins('bcs.w','main_pc_0305ae',4)
    emitter.ins('btst.b','#0x2,0xf605:w',6)
    emitter.ins('beq.w','main_pc_03056c',4)
    emitter.ins('tst.w','%d5',2)
    emitter.ins('bne.w','main_pc_030556',4)
    emitter.ins('moveq','#2,%d5',2)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('beq.b','main_pc_030554',2)
    emitter.ins('moveq','#6,%d5',2)
    emitter.ins('bra.b','main_pc_03055a',2)
    emitter.ins('subi.w','#0x1,%d5',4)
    emitter.ins('cmp.w','0xff702c:l,%d5',6)
    emitter.ins('beq.b','main_pc_030540',2)
    emitter.ins('cmp.w','0xff702e:l,%d5',6)
    emitter.ins('beq.b','main_pc_030540',2)
    emitter.ins('rts','',2)
    emitter.ins('btst.b','#0x3,0xf605:w',6)
    emitter.ins('beq.w','main_pc_03059e',4)
    emitter.ins('cmpi.w','#0x2,0xff7026:l',8)
    emitter.ins('bcs.w','main_pc_03058e',4)
    emitter.ins('cmpi.w','#0x2,%d5',4)
    emitter.ins('beq.w','main_pc_03059c',4)
    emitter.ins('bra.w','main_pc_030596',4)
    emitter.ins('cmpi.w','#0x6,%d5',4)
    emitter.ins('beq.w','main_pc_03059c',4)
    emitter.ins('addi.w','#0x1,%d5',4)
    emitter.ins('bra.b','main_pc_03059e',2)
    emitter.ins('clr.w','%d5',2)
    emitter.ins('cmp.w','0xff702c:l,%d5',6)
    emitter.ins('beq.b','main_pc_030576',2)
    emitter.ins('cmp.w','0xff702e:l,%d5',6)
    emitter.ins('beq.b','main_pc_030576',2)
    emitter.ins('rts','',2)

def _lower_run_controller_setup_and_configuration(emitter,rules):
    emitter.segment(0x2aa8e,0x2aa90)
    emitter.ins('rts','',2)
    emitter.segment(0x2aace,0x2ad5a)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('clr.w','0xf612:w',4)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('jsr','main_pc_006826:l',6)
    emitter.ins('clr.w','0xff7036:l',6)
    emitter.ins('jsr','1638(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('clr.w','0xff7022:l',6)
    emitter.ins('clr.w','0xff7040:l',6)
    emitter.ins('clr.w','0xff7042:l',6)
    emitter.ins('clr.w','0xff703e:l',6)
    emitter.ins('jsr','1186(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,main_pc_02ab3a',4)
    emitter.ins('move.w','#0xa200,0xff700c:l',8)
    emitter.ins('move.l','#0x2aaa6,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x800,0xf612:w',6)
    emitter.ins('tst.b','0xf612:w',4)
    emitter.ins('bne.b','main_pc_02ab6c',2)
    emitter.ins('jsr','1092(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','1132(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('tst.w','0xff703e:l',6)
    emitter.ins('bne.w','main_pc_02ad4a',4)
    emitter.ins('jsr','22328(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','458(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','498(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','540(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','582(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','624(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','21722(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('tst.w','0xff7034:l',6)
    emitter.ins('beq.w','main_pc_02abf4',4)
    emitter.ins('cmpi.w','#0x1,0xff7034:l',8)
    emitter.ins('beq.w','main_pc_02abe2',4)
    emitter.ins('cmpi.w','#0x6,0xff7022:l',8)
    emitter.ins('beq.w','main_pc_02abee',4)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('beq.w','main_pc_02abee',4)
    emitter.ins('bra.b','main_pc_02abf4',2)
    emitter.ins('cmpi.w','#0x5,0xff7022:l',8)
    emitter.ins('bne.w','main_pc_02abf4',4)
    emitter.ins('move.b','0xf605:w,0xf603:w',6)
    emitter.ins('btst.b','#0x5,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02ac98',4)
    emitter.ins('move.b','#0xac,%d0',4)
    emitter.ins('jsr','main_pc_00808a:l',6)
    emitter.ins('moveq','#5,%d0',2)
    emitter.ins('moveq','#4,%d1',2)
    emitter.ins('tst.w','0xff7034:l',6)
    emitter.ins('beq.w','main_pc_02ac2a',4)
    emitter.ins('moveq','#6,%d0',2)
    emitter.ins('moveq','#5,%d1',2)
    emitter.ins('cmpi.w','#0x1,0xff7034:l',8)
    emitter.ins('beq.w','main_pc_02ac2a',4)
    emitter.ins('moveq','#7,%d0',2)
    emitter.ins('moveq','#6,%d1',2)
    emitter.ins('cmp.w','0xff7022:l,%d0',6)
    emitter.ins('beq.w','main_pc_02ad42',4)
    emitter.ins('cmp.w','0xff7022:l,%d1',6)
    emitter.ins('bne.w','main_pc_02ac8e',4)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,main_pc_02ac62',4)
    emitter.ins('move.w','#0xa1c0,0xff700c:l',8)
    emitter.ins('move.l','#0x2aabe,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('addq.w','#0x1,0xff7022:l',6)
    emitter.ins('bra.w','main_pc_02ad36',4)
    emitter.ins('btst.b','#0x4,0xf603:w',6)
    emitter.ins('beq.w','main_pc_02ad36',4)
    emitter.ins('moveq','#5,%d0',2)
    emitter.ins('tst.w','0xff7034:l',6)
    emitter.ins('beq.w','main_pc_02acbe',4)
    emitter.ins('moveq','#6,%d0',2)
    emitter.ins('cmpi.w','#0x1,0xff7034:l',8)
    emitter.ins('beq.w','main_pc_02acbe',4)
    emitter.ins('moveq','#7,%d0',2)
    emitter.ins('cmp.w','0xff7022:l,%d0',6)
    emitter.ins('bne.w','main_pc_02ad22',4)
    emitter.ins('clr.w','0xff7022:l',6)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,main_pc_02acf2',4)
    emitter.ins('move.w','#0xa200,0xff700c:l',8)
    emitter.ins('move.l','#0x2aaa6,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('bra.w','main_pc_02ad36',4)
    emitter.ins('tst.w','0xff7022:l',6)
    emitter.ins('bne.w','main_pc_02ad30',4)
    emitter.ins('bra.w','main_pc_02ad36',4)
    emitter.ins('subq.w','#0x1,0xff7022:l',6)
    emitter.ins('move.b','0xf603:w,%d0',4)
    emitter.ins('andi.b','#0x80,%d0',4)
    emitter.ins('beq.w','main_pc_02ad4a',4)
    emitter.ins('move.w','#0x1,0xff703e:l',8)
    emitter.ins('cmpi.w','#0x10,0xff7042:l',8)
    emitter.ins('bcc.w','main_pc_02aa8e',4)
    emitter.ins('bra.w','main_pc_02ab66',4)
    emitter.segment(0x305b0,0x30696)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('clr.w','0xf612:w',4)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('jsr','main_pc_006826:l',6)
    emitter.ins('move.w','#0x1,0xff7036:l',8)
    emitter.ins('jsr','-21630(%pc)',4)
    emitter.ins('clr.w','0xff7038:l',6)
    emitter.ins('clr.w','0xff703a:l',6)
    emitter.ins('clr.w','0xff703e:l',6)
    emitter.ins('jsr','252(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.l','#0x60000002,0xc00004:l',10)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.w','#0x3333,%d6',4)
    emitter.ins('move.w','#0xd7f,%d7',4)
    emitter.ins('move.w','%d6,(%a5)',2)
    emitter.ins('dbra','%d7,main_pc_030616',4)
    emitter.ins('move.w','#0xa0c0,0xff700c:l',8)
    emitter.ins('move.l','#0x2aa90,0xff700e:l',10)
    emitter.ins('move.w','#0x3,0xff7014:l',8)
    emitter.ins('move.w','#0x1,0xff7016:l',8)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x800,0xf612:w',6)
    emitter.ins('tst.b','0xf612:w',4)
    emitter.ins('bne.b','main_pc_030648',2)
    emitter.ins('cmpi.w','#0x10,0xff703a:l',8)
    emitter.ins('bcc.w','main_pc_02aace',4)
    emitter.ins('jsr','146(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','52(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('move.b','0xf603:w,%d0',4)
    emitter.ins('andi.b','#0x20,%d0',4)
    emitter.ins('beq.w','main_pc_030684',4)
    emitter.ins('move.w','#0x1,0xff703e:l',8)
    emitter.ins('move.b','#0xac,%d0',4)
    emitter.ins('jsr','main_pc_00808a:l',6)
    emitter.ins('tst.w','0xff703e:l',6)
    emitter.ins('beq.w','main_pc_030694',4)
    emitter.ins('jsr','138(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('bra.b','main_pc_030642',2)

def _lower_update_connected_controller_option(emitter,rules):
    emitter.segment(0x30696,0x306ee)
    emitter.ins('tst.w','0xff703e:l',6)
    emitter.ins('bne.w','main_pc_0306cc',4)
    emitter.ins('lea.l','0xa10005:l,%a0',6)
    emitter.ins('bsr.w','main_pc_030742',4)
    emitter.ins('cmpi.b','#0xb,%d0',4)
    emitter.ins('beq.b','main_pc_0306b8',2)
    emitter.ins('clr.w','0xff7034:l',6)
    emitter.ins('bra.b','main_pc_0306cc',2)
    emitter.ins('move.w','0xff7034:l,%d5',6)
    emitter.ins('move.w','#0x2,%d6',4)
    emitter.ins('jsr','-22186(%pc)',4)
    emitter.ins('move.w','%d5,0xff7034:l',6)
    emitter.ins('move.w','0xff7034:l,%d1',6)
    emitter.ins('asl.w','#0x1,%d1',2)
    emitter.ins('lea.l','-602(%pc),%a3',4)
    emitter.ins('move.w','(%a3, %d1.w),%d0',4)
    emitter.ins('lea.l','-21908(%pc),%a0',4)
    emitter.ins('move.w','#0x70,%d1',4)
    emitter.ins('clr.l','%d2',2)
    emitter.ins('jsr','main_pc_00ac08:l',6)
    emitter.ins('rts','',2)

def _lower_advance_controller_setup_reveal(emitter,rules):
    emitter.segment(0x306ee,0x3071a)
    emitter.ins('cmpi.w','#0x10,0xff7038:l',8)
    emitter.ins('bcc.w','main_pc_030718',4)
    emitter.ins('move.w','#0xf,%d0',4)
    emitter.ins('sub.w','0xff7038:l,%d0',6)
    emitter.ins('move.w','#0x40,%d1',4)
    emitter.ins('lea.l','-21148(%pc),%a0',4)
    emitter.ins('jsr','main_pc_00dea6:l',6)
    emitter.ins('addq.w','#0x1,0xff7038:l',6)
    emitter.ins('rts','',2)

def _lower_advance_controller_setup_dismissal(emitter,rules):
    emitter.segment(0x3071a,0x30742)
    emitter.ins('cmpi.w','#0x10,0xff703a:l',8)
    emitter.ins('bcc.w','main_pc_030740',4)
    emitter.ins('move.w','0xff703a:l,%d0',6)
    emitter.ins('move.w','#0x40,%d1',4)
    emitter.ins('lea.l','-21188(%pc),%a0',4)
    emitter.ins('jsr','main_pc_00dea6:l',6)
    emitter.ins('addq.w','#0x1,0xff703a:l',6)
    emitter.ins('rts','',2)

def _lower_read_controller_identity(emitter,rules):
    emitter.segment(0x30742,0x3076e)
    emitter.ins('move.b','#0x40,(%a0)',4)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('move.b','(%a0),%d0',2)
    emitter.ins('move.b','%d0,%d1',2)
    emitter.ins('asl.b','#0x1,%d1',2)
    emitter.ins('or.b','%d1,%d0',2)
    emitter.ins('andi.b','#0xa,%d0',4)
    emitter.ins('move.b','#0x0,(%a0)',4)
    emitter.ins('nop','',2)
    emitter.ins('nop','',2)
    emitter.ins('move.b','(%a0),%d1',2)
    emitter.ins('move.b','%d1,%d2',2)
    emitter.ins('lsr.b','#0x1,%d2',2)
    emitter.ins('or.b','%d2,%d1',2)
    emitter.ins('andi.b','#0x5,%d1',4)
    emitter.ins('or.b','%d1,%d0',2)
    emitter.ins('rts','',2)

def _lower_commit_setup_options(emitter,rules):
    emitter.segment(0x3076e,0x307e0)
    emitter.ins('move.w','0xff7024:l,0xefd2:w',8)
    emitter.ins('move.w','0xff7026:l,%d0',6)
    emitter.ins('move.w','%d0,0xefd4:w',4)
    emitter.ins('move.w','%d0,0xefe4:w',4)
    emitter.ins('move.b','90(%pc, %d0.w),0xf374:w',6)
    emitter.ins('clr.b','0xf375:w',4)
    emitter.ins('move.w','0xff7028:l,0xefd6:w',8)
    emitter.ins('move.w','0xff702a:l,0xefd8:w',8)
    emitter.ins('move.w','#0x80,0xf67c:w',6)
    emitter.ins('move.w','#0x80,0xf67e:w',6)
    emitter.ins('move.w','0xff7034:l,%d0',6)
    emitter.ins('lea.l','0xff702c:l,%a0',6)
    emitter.ins('lea.l','44(%pc),%a1',4)
    emitter.ins('move.w','0xefd4:w,%d1',4)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('add.w','0xefd4:w,%d1',4)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('add.w','0xefd4:w,%d1',4)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('adda.w','%d1,%a1',2)
    emitter.ins('lea.l','0xf67a:w,%a2',4)
    emitter.ins('move.w','(%a0)+,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('move.w','(%a1, %d1.w),(%a2)+',4)
    emitter.ins('dbra','%d0,main_pc_0307d2',4)
    emitter.ins('rts','',2)

def _lower_locate_selected_ruler_city(emitter,rules):
    emitter.segment(0x309fc,0x30a74)
    emitter.ins('lea.l','0xe640:w,%a0',4)
    emitter.ins('move.w','0xf376:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','(%a0, %d0.w),%d0',4)
    emitter.ins('lea.l','0xcc00:w,%a0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('andi.w','#0x3f,%d1',4)
    emitter.ins('cmpi.w','#0x28,%d1',4)
    emitter.ins('bhi.w','main_pc_030a3a',4)
    emitter.ins('lsl.w','#0x2,%d1',2)
    emitter.ins('lea.l','0xd4ac6:l,%a0',6)
    emitter.ins('move.w','0x2(%a0, %d1.w),0xf35e:w',6)
    emitter.ins('move.w','(%a0, %d1.w),0xf360:w',6)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('bra.w','main_pc_030a72',4)
    emitter.ins('lea.l','0xf428:w,%a0',4)
    emitter.ins('move.w','#0x27,%d0',4)
    emitter.ins('move.w','0xf376:w,%d1',4)
    emitter.ins('cmp.b','(%a0, %d0.w),%d1',4)
    emitter.ins('beq.w','main_pc_030a5a',4)
    emitter.ins('dbra','%d0,main_pc_030a46',4)
    emitter.ins('ori.w','#0x1,%sr',4)
    emitter.ins('bra.w','main_pc_030a72',4)
    emitter.ins('lea.l','0xd4aca:l,%a0',6)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('move.w','0x2(%a0, %d0.w),0xf35e:w',6)
    emitter.ins('move.w','(%a0, %d0.w),0xf360:w',6)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('rts','',2)

def _lower_locate_selected_force_packet(emitter,rules):
    emitter.segment(0x30b8e,0x30c3a)
    emitter.ins('move.w','0xf376:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('lea.l','0xe640:w,%a0',4)
    emitter.ins('move.w','(%a0, %d0.w),%d0',4)
    emitter.ins('lea.l','0xa050:w,%a0',4)
    emitter.ins('tst.b','(%a0, %d0.w)',4)
    emitter.ins('bne.w','main_pc_030bf4',4)
    emitter.ins('lea.l','0x9000:w,%a0',4)
    emitter.ins('move.b','(%a0),%d2',2)
    emitter.ins('andi.w','#0xf,%d2',4)
    emitter.ins('beq.w','main_pc_030c34',4)
    emitter.ins('cmp.b','0x4(%a0),%d1',4)
    emitter.ins('bne.w','main_pc_030bce',4)
    emitter.ins('move.w','%d2,%d3',2)
    emitter.ins('subq.w','#0x1,%d3',2)
    emitter.ins('cmp.b','0xd(%a0, %d3.w),%d0',4)
    emitter.ins('beq.w','main_pc_030bd4',4)
    emitter.ins('dbra','%d3,main_pc_030bc2',4)
    emitter.ins('lea.l','0xd(%a0, %d2.w),%a0',4)
    emitter.ins('bra.b','main_pc_030bac',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a0),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('move.w','%d0,0xf35e:w',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x2(%a0),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('move.w','%d0,0xf360:w',4)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('bra.w','main_pc_030c38',4)
    emitter.ins('lea.l','0x9000:w,%a0',4)
    emitter.ins('move.w','0xf376:w,%d0',4)
    emitter.ins('move.b','(%a0),%d1',2)
    emitter.ins('andi.w','#0xf,%d1',4)
    emitter.ins('beq.w','main_pc_030c34',4)
    emitter.ins('cmp.b','0x4(%a0),%d0',4)
    emitter.ins('beq.w','main_pc_030c14',4)
    emitter.ins('lea.l','0xd(%a0, %d1.w),%a0',4)
    emitter.ins('bra.b','main_pc_030bfc',2)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a0),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('move.w','%d0,0xf35e:w',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x2(%a0),%d0',4)
    emitter.ins('lsl.w','#0x4,%d0',2)
    emitter.ins('move.w','%d0,0xf360:w',4)
    emitter.ins('andi.w','#0xfffe,%sr',4)
    emitter.ins('bra.w','main_pc_030c38',4)
    emitter.ins('ori.w','#0x1,%sr',4)
    emitter.ins('rts','',2)

def _lower_deduct_all_map_packet_supply(emitter,rules):
    emitter.segment(0x30c3a,0x30c90)
    emitter.ins('lea.l','0x9000:w,%a0',4)
    emitter.ins('move.b','(%a0),%d0',2)
    emitter.ins('andi.w','#0xf,%d0',4)
    emitter.ins('beq.w','main_pc_030c8e',4)
    emitter.ins('bsr.w','main_pc_030c90',4)
    emitter.ins('move.b','0x9(%a0),%d2',4)
    emitter.ins('lsl.w','#0x8,%d2',2)
    emitter.ins('move.b','0xa(%a0),%d2',4)
    emitter.ins('lsl.l','#0x8,%d2',2)
    emitter.ins('move.b','0xb(%a0),%d2',4)
    emitter.ins('lsl.l','#0x8,%d2',2)
    emitter.ins('move.b','0xc(%a0),%d2',4)
    emitter.ins('sub.l','%d3,%d2',2)
    emitter.ins('bcc.w','main_pc_030c72',4)
    emitter.ins('bsr.w','main_pc_030cc2',4)
    emitter.ins('tst.w','%d0',2)
    emitter.ins('beq.b','main_pc_030c3e',2)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('move.b','%d2,0xc(%a0)',4)
    emitter.ins('lsr.l','#0x8,%d2',2)
    emitter.ins('move.b','%d2,0xb(%a0)',4)
    emitter.ins('lsr.l','#0x8,%d2',2)
    emitter.ins('move.b','%d2,0xa(%a0)',4)
    emitter.ins('lsr.w','#0x8,%d2',2)
    emitter.ins('move.b','%d2,0x9(%a0)',4)
    emitter.ins('lea.l','0xd(%a0, %d0.w),%a0',4)
    emitter.ins('bra.b','main_pc_030c3e',2)
    emitter.ins('rts','',2)

def _lower_calculate_map_packet_supply(emitter,rules):
    emitter.segment(0x30c90,0x30cc2)
    emitter.ins('lea.l','0xc800:w,%a1',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('subq.w','#0x1,%d1',2)
    emitter.ins('moveq','#0,%d3',2)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('move.b','0xd(%a0, %d1.w),%d2',4)
    emitter.ins('lsl.w','#0x2,%d2',2)
    emitter.ins('add.l','(%a1, %d2.w),%d3',4)
    emitter.ins('addi.l','#0x64,%d3',6)
    emitter.ins('dbra','%d1,main_pc_030c9a',4)
    emitter.ins('divu.w','#0xa,%d3',4)
    emitter.ins('move.w','%d3,%d2',2)
    emitter.ins('lsl.w','#0x1,%d3',2)
    emitter.ins('add.w','%d2,%d3',2)
    emitter.ins('andi.l','#0xffff,%d3',6)
    emitter.ins('rts','',2)

def _lower_apply_map_packet_supply_losses(emitter,rules):
    emitter.segment(0x30cc2,0x30d7e)
    emitter.ins('clr.w','0xcfc8:w',4)
    emitter.ins('move.b','0xd(%a0),0xcfc9:w',6)
    emitter.ins('clr.w','%d7',2)
    emitter.ins('lea.l','0xc800:w,%a1',4)
    emitter.ins('lea.l','0xb200:w,%a2',4)
    emitter.ins('lea.l','0xcfb2:w,%a3',4)
    emitter.ins('lea.l','0xcc00:w,%a4',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('subq.w','#0x1,%d1',2)
    emitter.ins('bsr.w','main_pc_030d7e',4)
    emitter.ins('clr.w','%d4',2)
    emitter.ins('move.b','0xd(%a0, %d1.w),%d4',4)
    emitter.ins('move.w','%d4,%d5',2)
    emitter.ins('lsl.w','#0x1,%d5',2)
    emitter.ins('move.w','(%a2, %d5.w),%d6',4)
    emitter.ins('sub.w','%d2,%d6',2)
    emitter.ins('bls.w','main_pc_030d18',4)
    emitter.ins('move.w','%d6,(%a2, %d5.w)',4)
    emitter.ins('lsl.w','#0x1,%d5',2)
    emitter.ins('move.w','0x2(%a1, %d5.w),%d6',4)
    emitter.ins('sub.w','%d3,%d6',2)
    emitter.ins('bcc.w','main_pc_030d0c',4)
    emitter.ins('clr.w','%d6',2)
    emitter.ins('move.w','%d6,0x2(%a1, %d5.w)',4)
    emitter.ins('addq.w','#0x1,%d7',2)
    emitter.ins('move.b','%d4,(%a3)+',2)
    emitter.ins('bra.w','main_pc_030d6c',4)
    emitter.ins('move.b','#0xff,(%a4, %d4.w)',6)
    emitter.ins('move.b','0x4(%a0),%d2',4)
    emitter.ins('andi.w','#0xf,%d2',4)
    emitter.ins('cmp.w','0xf67a:w,%d2',4)
    emitter.ins('beq.w','main_pc_030d3e',4)
    emitter.ins('cmp.w','0xf67c:w,%d2',4)
    emitter.ins('beq.w','main_pc_030d3e',4)
    emitter.ins('cmp.w','0xf67e:w,%d2',4)
    emitter.ins('bne.w','main_pc_030d6c',4)
    emitter.ins('move.w','0xf362:w,-(%a7)',4)
    emitter.ins('move.w','0xf376:w,-(%a7)',4)
    emitter.ins('movem.l','%d0-%d7/%a0-%a6,-(%a7)',4)
    emitter.ins('move.w','%d2,0xf376:w',4)
    emitter.ins('move.w','%d4,0xf3d0:w',4)
    emitter.ins('move.w','#0xca,0xf740:w',6)
    emitter.ins('clr.w','0xf362:w',4)
    emitter.ins('jsr','-746(%pc)',4)
    emitter.ins('movem.l','(%a7)+,%d0-%d7/%a0-%a6',4)
    emitter.ins('move.w','(%a7)+,0xf376:w',4)
    emitter.ins('move.w','(%a7)+,0xf362:w',4)
    emitter.ins('dbra','%d1,main_pc_030ce2',4)
    emitter.ins('cmp.w','%d7,%d0',2)
    emitter.ins('beq.w','main_pc_030d7a',4)
    emitter.ins('bsr.w','main_pc_030dc6',4)
    emitter.ins('move.w','%d7,%d0',2)
    emitter.ins('rts','',2)

def _lower_sample_map_packet_loss_factors(emitter,rules):
    emitter.segment(0x30d7e,0x30dc6)
    emitter.ins('movem.l','%d0-%d1,-(%a7)',4)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('add.l','%d1,%d0',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('addq.w','#0x5,%d0',2)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('move.l','%d0,%d1',2)
    emitter.ins('lsl.l','#0x8,%d0',2)
    emitter.ins('lsl.l','#0x1,%d0',2)
    emitter.ins('sub.l','%d1,%d0',2)
    emitter.ins('lsl.l','#0x1,%d1',2)
    emitter.ins('sub.l','%d1,%d0',2)
    emitter.ins('lsl.l','#0x2,%d1',2)
    emitter.ins('sub.l','%d1,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('addi.w','#0x1f4,%d0',4)
    emitter.ins('move.w','%d0,%d3',2)
    emitter.ins('movem.l','(%a7)+,%d0-%d1',4)
    emitter.ins('rts','',2)

def _lower_compact_map_packet_survivors(emitter,rules):
    emitter.segment(0x30dc6,0x30e34)
    emitter.ins('move.w','%d7,%d6',2)
    emitter.ins('beq.w','main_pc_030dec',4)
    emitter.ins('subq.w','#0x1,%d6',2)
    emitter.ins('lea.l','0xcfb2:w,%a1',4)
    emitter.ins('move.b','(%a1)+,0xd(%a0, %d6.w)',4)
    emitter.ins('dbra','%d6,main_pc_030dd2',4)
    emitter.ins('move.b','%d7,(%a0)',2)
    emitter.ins('bsr.w','main_pc_030e34',4)
    emitter.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    emitter.ins('lea.l','0xd(%a0, %d7.w),%a2',4)
    emitter.ins('bra.w','main_pc_030df6',4)
    emitter.ins('bsr.w','main_pc_030e7c',4)
    emitter.ins('lea.l','0xd(%a0, %d0.w),%a1',4)
    emitter.ins('lea.l','(%a0),%a2',2)
    emitter.ins('move.b','(%a1),%d1',2)
    emitter.ins('andi.w','#0xf,%d1',4)
    emitter.ins('beq.w','main_pc_030e0c',4)
    emitter.ins('addi.w','#0xc,%d1',4)
    emitter.ins('move.b','(%a1)+,(%a2)+',2)
    emitter.ins('dbra','%d1,main_pc_030e04',4)
    emitter.ins('bra.b','main_pc_030df6',2)
    emitter.ins('clr.b','(%a2)',2)
    emitter.ins('tst.w','%d7',2)
    emitter.ins('beq.w','main_pc_030e32',4)
    emitter.ins('lea.l','0xc400:w,%a1',4)
    emitter.ins('move.w','%d7,%d6',2)
    emitter.ins('subq.w','#0x1,%d6',2)
    emitter.ins('moveq','#0,%d2',2)
    emitter.ins('clr.w','%d3',2)
    emitter.ins('move.b','0xd(%a0, %d6.w),%d3',4)
    emitter.ins('add.b','(%a1, %d3.w),%d2',4)
    emitter.ins('dbra','%d6,main_pc_030e20',4)
    emitter.ins('divu.w','%d7,%d2',2)
    emitter.ins('move.b','%d2,0x3(%a0)',4)
    emitter.ins('rts','',2)

def _lower_replace_map_queue_leader(emitter,rules):
    emitter.segment(0x30e34,0x30e7c)
    emitter.ins('movem.l','%d0-%d1/%a0,-(%a7)',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0xd(%a0),%d0',4)
    emitter.ins('move.w','0xcfc8:w,%d1',4)
    emitter.ins('lea.l','0xff39b2:l,%a0',6)
    emitter.ins('tst.b','(%a0)',2)
    emitter.ins('beq.w','main_pc_030e76',4)
    emitter.ins('cmp.b','0x1(%a0),%d1',4)
    emitter.ins('beq.w','main_pc_030e5a',4)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('bra.b','main_pc_030e48',2)
    emitter.ins('move.b','%d0,0x1(%a0)',4)
    emitter.ins('lea.l','0xff3000:l,%a0',6)
    emitter.ins('addq.w','#0x1,%a0',2)
    emitter.ins('cmp.b','(%a0),%d1',2)
    emitter.ins('beq.w','main_pc_030e74',4)
    emitter.ins('addq.w','#0x1,%a0',2)
    emitter.ins('tst.b','(%a0)+',2)
    emitter.ins('bne.b','main_pc_030e6e',2)
    emitter.ins('bra.b','main_pc_030e64',2)
    emitter.ins('move.b','%d0,(%a0)',2)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0',4)
    emitter.ins('rts','',2)

def _lower_remove_map_queue_leader(emitter,rules):
    emitter.segment(0x30e7c,0x30eb4)
    emitter.ins('movem.l','%d0-%d1/%a0-%a1,-(%a7)',4)
    emitter.ins('lea.l','0xff39b2:l,%a0',6)
    emitter.ins('move.w','0xcfc8:w,%d0',4)
    emitter.ins('tst.b','(%a0)',2)
    emitter.ins('beq.w','main_pc_030eae',4)
    emitter.ins('cmp.b','0x1(%a0),%d0',4)
    emitter.ins('beq.w','main_pc_030e9c',4)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('bra.b','main_pc_030e8a',2)
    emitter.ins('move.b','0x2(%a0),(%a0)',4)
    emitter.ins('beq.w','main_pc_030eae',4)
    emitter.ins('move.b','0x3(%a0),0x1(%a0)',6)
    emitter.ins('addq.w','#0x2,%a0',2)
    emitter.ins('bra.b','main_pc_030e9c',2)
    emitter.ins('movem.l','(%a7)+,%d0-%d1/%a0-%a1',4)
    emitter.ins('rts','',2)

def _lower_initialize_force_turn_order(emitter,rules):
    emitter.segment(0x30eb4,0x30ed8)
    emitter.ins('lea.l','0xf714:w,%a0',4)
    emitter.ins('lea.l','30(%pc),%a1',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','#0xf,%d0',4)
    emitter.ins('move.b','(%a1)+,(%a0)+',2)
    emitter.ins('dbra','%d0,main_pc_030ec2',4)
    emitter.ins('bsr.w','main_pc_030ee8',4)
    emitter.ins('clr.w','0xf724:w',4)
    emitter.ins('move.w','#0xb0,0xf600:w',6)
    emitter.ins('rts','',2)

def _lower_shuffle_force_turn_order(emitter,rules):
    emitter.segment(0x30ee8,0x30f26)
    emitter.ins('lea.l','0xf714:w,%a0',4)
    emitter.ins('move.w','#0xf,%d7',4)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('move.w','0xf61c:w,%d0',4)
    emitter.ins('andi.w','#0xf,%d0',4)
    emitter.ins('move.w','0xf61c:w,%d1',4)
    emitter.ins('lsr.w','#0x8,%d1',2)
    emitter.ins('andi.w','#0xf,%d1',4)
    emitter.ins('move.b','(%a0, %d0.w),%d2',4)
    emitter.ins('bmi.w','main_pc_030f20',4)
    emitter.ins('move.b','(%a0, %d1.w),%d3',4)
    emitter.ins('bmi.w','main_pc_030f20',4)
    emitter.ins('move.b','%d3,(%a0, %d0.w)',4)
    emitter.ins('move.b','%d2,(%a0, %d1.w)',4)
    emitter.ins('dbra','%d7,main_pc_030ef0',4)
    emitter.ins('rts','',2)

def _lower_select_next_force_turn(emitter,rules):
    emitter.segment(0x30f26,0x30f54)
    emitter.ins('move.w','0xf724:w,%d0',4)
    emitter.ins('lea.l','0xf714:w,%a0',4)
    emitter.ins('lea.l','0xe640:w,%a1',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('ext.w','%d1',2)
    emitter.ins('bmi.b','main_pc_030f46',2)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('tst.w','(%a1, %d1.w)',4)
    emitter.ins('bmi.b','main_pc_030f32',2)
    emitter.ins('lsr.w','#0x1,%d1',2)
    emitter.ins('move.w','%d0,0xf724:w',4)
    emitter.ins('move.w','%d1,0xf376:w',4)
    emitter.ins('clr.w','0xf364:w',4)
    emitter.ins('rts','',2)

def _lower_recover_idle_officer_readiness(emitter,rules):
    emitter.segment(0x30f54,0x30faa)
    emitter.ins('lea.l','0xcc00:w,%a0',4)
    emitter.ins('lea.l','0xb200:w,%a3',4)
    emitter.ins('lea.l','0xb000:w,%a4',4)
    emitter.ins('lea.l','0xea38:w,%a5',4)
    emitter.ins('move.w','#0xff,%d0',4)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('cmpi.b','#0x28,%d1',4)
    emitter.ins('bhi.w','main_pc_030fa4',4)
    emitter.ins('tst.b','(%a5, %d1.w)',4)
    emitter.ins('bne.w','main_pc_030fa4',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x1,%d1',2)
    emitter.ins('move.w','(%a4, %d1.w),%d2',4)
    emitter.ins('mulu.w','#0x'+format(rules['idle_recovery_percent'],'x')+',%d2',4)
    emitter.ins('divu.w','#0x64,%d2',4)
    emitter.ins('move.w','(%a3, %d1.w),%d3',4)
    emitter.ins('add.w','%d2,%d3',2)
    emitter.ins('cmp.w','(%a4, %d1.w),%d3',4)
    emitter.ins('bls.w','main_pc_030fa0',4)
    emitter.ins('move.w','(%a4, %d1.w),%d3',4)
    emitter.ins('move.w','%d3,(%a3, %d1.w)',4)
    emitter.ins('dbra','%d0,main_pc_030f68',4)
    emitter.ins('rts','',2)

def _lower_run_city_command_assignment(emitter,rules):
    emitter.segment(0x30faa,0x30fea)
    emitter.ins('bsr.w','main_pc_031110',4)
    emitter.ins('bsr.w','main_pc_031074',4)
    emitter.ins('tst.w','0xf364:w',4)
    emitter.ins('bmi.w','main_pc_030fd8',4)
    emitter.ins('bsr.w','main_pc_03117c',4)
    emitter.ins('bsr.w','main_pc_0311a6',4)
    emitter.ins('move.w','#0x1,0xf728:w',6)
    emitter.ins('move.w','0xf726:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','54(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','56(%pc, %d0.w)',4)
    emitter.ins('bra.b','main_pc_030fae',2)
    emitter.ins('jsr','main_pc_00e82e:l',6)
    emitter.ins('bsr.w','main_pc_030fea',4)
    emitter.ins('jsr','main_pc_0662e4:l',6)
    emitter.ins('rts','',2)

def _lower_clear_unassigned_officer_commands(emitter,rules):
    emitter.segment(0x30fea,0x31006)
    emitter.ins('lea.l','0xcd00:w,%a0',4)
    emitter.ins('move.w','#0xff,%d0',4)
    emitter.ins('move.b','(%a0)+,%d1',2)
    emitter.ins('cmpi.b','#0x2,%d1',4)
    emitter.ins('bcc.w','main_pc_031000',4)
    emitter.ins('clr.b','-0x1(%a0)',4)
    emitter.ins('dbra','%d0,main_pc_030ff2',4)
    emitter.ins('rts','',2)

def _lower_run_city_command_states(emitter,rules):
    emitter.segment(0x31024,0x31044)
    emitter.ins('bsr.w','main_pc_031074',4)
    emitter.ins('tst.w','0xf364:w',4)
    emitter.ins('bmi.w','main_pc_031042',4)
    emitter.ins('bsr.w','main_pc_0311a6',4)
    emitter.ins('move.w','#0x1,0xf728:w',6)
    emitter.ins('jsr','main_pc_0338c2:l',6)
    emitter.ins('bra.b','main_pc_031024',2)
    emitter.ins('rts','',2)

def _lower_run_map_packet_command_states(emitter,rules):
    emitter.segment(0x31044,0x31074)
    emitter.ins('bsr.w','main_pc_0310ae',4)
    emitter.ins('tst.w','0xf75a:w',4)
    emitter.ins('bmi.w','main_pc_031072',4)
    emitter.ins('move.w','#0x1,0xf728:w',6)
    emitter.ins('jsr','main_pc_0340f8:l',6)
    emitter.ins('lea.l','0x9000:w,%a0',4)
    emitter.ins('adda.w','0xf75a:w,%a0',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','(%a0),%d0',2)
    emitter.ins('addi.w','#0xd,%d0',4)
    emitter.ins('add.w','%d0,0xf75a:w',4)
    emitter.ins('bra.b','main_pc_031044',2)
    emitter.ins('rts','',2)

def _lower_select_next_force_city(emitter,rules):
    emitter.segment(0x31074,0x310ae)
    emitter.ins('lea.l','0xf427:w,%a0',4)
    emitter.ins('lea.l','0xea37:w,%a1',4)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('move.w','0xf376:w,%d2',4)
    emitter.ins('cmpi.w','#0x28,%d0',4)
    emitter.ins('bhi.w','main_pc_0310a4',4)
    emitter.ins('tst.b','(%a1, %d0.w)',4)
    emitter.ins('bne.w','main_pc_0310a0',4)
    emitter.ins('move.b','(%a0, %d0.w),%d1',4)
    emitter.ins('cmp.b','%d2,%d1',2)
    emitter.ins('beq.w','main_pc_0310a8',4)
    emitter.ins('addq.w','#0x1,%d0',2)
    emitter.ins('bra.b','main_pc_031086',2)
    emitter.ins('move.w','#0xffff,%d0',4)
    emitter.ins('move.w','%d0,0xf364:w',4)
    emitter.ins('rts','',2)

def _lower_select_next_force_map_packet(emitter,rules):
    emitter.segment(0x310ae,0x31110)
    emitter.ins('lea.l','0x9000:w,%a0',4)
    emitter.ins('adda.w','0xf75a:w,%a0',4)
    emitter.ins('move.w','0xf376:w,%d0',4)
    emitter.ins('move.b','(%a0),%d1',2)
    emitter.ins('btst.l','#0x5,%d1',4)
    emitter.ins('bne.w','main_pc_0310d4',4)
    emitter.ins('andi.w','#0xf,%d1',4)
    emitter.ins('beq.w','main_pc_0310ea',4)
    emitter.ins('cmp.b','0x4(%a0),%d0',4)
    emitter.ins('beq.w','main_pc_0310f4',4)
    emitter.ins('andi.w','#0xf,%d1',4)
    emitter.ins('beq.w','main_pc_0310ea',4)
    emitter.ins('lea.l','0xd(%a0, %d1.w),%a0',4)
    emitter.ins('addi.w','#0xd,%d1',4)
    emitter.ins('add.w','%d1,0xf75a:w',4)
    emitter.ins('bra.b','main_pc_0310ba',2)
    emitter.ins('move.w','#0xffff,0xf75a:w',6)
    emitter.ins('bra.w','main_pc_03110e',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','0x1(%a0),%d0',4)
    emitter.ins('move.w','%d0,0xf75c:w',4)
    emitter.ins('move.b','0x2(%a0),%d0',4)
    emitter.ins('move.w','%d0,0xf75e:w',4)
    emitter.ins('move.b','0x3(%a0),%d0',4)
    emitter.ins('move.w','%d0,0xf760:w',4)
    emitter.ins('rts','',2)

def _lower_sample_city_command_policy(emitter,rules):
    emitter.segment(0x31110,0x3117c)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('lea.l','228(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('move.w','0xefd2:w,%d0',4)
    emitter.ins('lsl.w','#0x6,%d0',2)
    emitter.ins('adda.w','%d0,%a0',2)
    emitter.ins('move.w','0xf376:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('moveq','#0,%d1',2)
    emitter.ins('move.w','0xf61c:w,%d1',4)
    emitter.ins('lsl.l','#0x4,%d1',2)
    emitter.ins('swap','%d1',2)
    emitter.ins('clr.w','%d2',2)
    emitter.ins('cmp.w','(%a0, %d0.w),%d1',4)
    emitter.ins('bcs.w','main_pc_03114a',4)
    emitter.ins('addq.w','#0x4,%d2',2)
    emitter.ins('cmp.w','0x2(%a0, %d0.w),%d1',4)
    emitter.ins('bcs.w','main_pc_03114a',4)
    emitter.ins('addq.w','#0x4,%d2',2)
    emitter.ins('jsr','main_pc_0083d4:l',6)
    emitter.ins('lea.l','362(%pc),%a2',4)
    emitter.ins('nop','',2)
    emitter.ins('andi.l','#0xffff,%d0',6)
    emitter.ins('lsl.l','#0x3,%d0',2)
    emitter.ins('swap','%d0',2)
    emitter.ins('clr.w','%d1',2)
    emitter.ins('cmp.w','(%a2, %d2.w),%d0',4)
    emitter.ins('bcs.w','main_pc_031176',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('cmp.w','0x2(%a2, %d2.w),%d0',4)
    emitter.ins('bcs.w','main_pc_031176',4)
    emitter.ins('addq.w','#0x1,%d1',2)
    emitter.ins('move.w','%d1,0xf726:w',4)
    emitter.ins('rts','',2)

def _lower_clear_current_city_project_orders(emitter,rules):
    emitter.segment(0x3117c,0x311a6)
    emitter.ins('lea.l','0xe80c:w,%a0',4)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('add.w','0xf364:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('move.l','#0xffffffff,(%a0, %d0.w)',8)
    emitter.ins('move.l','#0xffffffff,0x4(%a0, %d0.w)',8)
    emitter.ins('move.l','#0xffffffff,0x8(%a0, %d0.w)',8)
    emitter.ins('rts','',2)

def _lower_build_current_city_officer_roster(emitter,rules):
    emitter.segment(0x311a6,0x311e6)
    emitter.ins('lea.l','0xf72a:w,%a0',4)
    emitter.ins('lea.l','0xcc00:w,%a1',4)
    emitter.ins('lea.l','0xcd00:w,%a2',4)
    emitter.ins('move.w','0xf364:w,%d0',4)
    emitter.ins('clr.w','%d4',2)
    emitter.ins('move.w','#0xff,%d1',4)
    emitter.ins('move.b','(%a1, %d1.w),%d2',4)
    emitter.ins('cmp.w','%d0,%d2',2)
    emitter.ins('bne.w','main_pc_0311d8',4)
    emitter.ins('move.w','%d1,%d3',2)
    emitter.ins('tst.b','(%a2, %d3.w)',4)
    emitter.ins('beq.w','main_pc_0311d4',4)
    emitter.ins('bset.l','#0xe,%d3',4)
    emitter.ins('move.w','%d3,(%a0)+',2)
    emitter.ins('addq.w','#0x1,%d4',2)
    emitter.ins('dbra','%d1,main_pc_0311bc',4)
    emitter.ins('move.w','#0xffff,(%a0)',4)
    emitter.ins('move.w','%d4,0xf762:w',4)
    emitter.ins('rts','',2)

def _lower_finish_city_command_assignment(emitter,rules):
    emitter.segment(0x311e6,0x311fa)
    emitter.ins('jsr','main_pc_00e8a0:l',6)
    emitter.ins('jsr','main_pc_01190e:l',6)
    emitter.ins('move.w','#0x1,0xf36c:w',6)
    emitter.ins('rts','',2)

def _lower_retain_city_command_stage(emitter,rules):
    emitter.segment(0x311fa,0x311fc)
    emitter.ins('rts','',2)

def _lower_dispatch_city_assignment_state(emitter,rules):
    emitter.segment(0x312c8,0x312d8)
    emitter.ins('move.w','0xf362:w,%d0',4)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','8(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','36(%pc, %d0.w)',4)
    emitter.ins('rts','',2)

def _lower_dispatch_city_command_stage(emitter,rules):
    emitter.segment(0x338c2,0x338da)
    emitter.ins('move.w','0xf728:w,%d0',4)
    emitter.ins('bmi.w','main_pc_0338d8',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','10(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','24(%pc, %d0.w)',4)
    emitter.ins('bra.b','main_pc_0338c2',2)
    emitter.ins('rts','',2)

def _lower_dispatch_map_packet_command_stage(emitter,rules):
    emitter.segment(0x340f8,0x34110)
    emitter.ins('move.w','0xf728:w,%d0',4)
    emitter.ins('bmi.w','main_pc_03410e',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','10(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','54(%pc, %d0.w)',4)
    emitter.ins('bra.b','main_pc_0340f8',2)
    emitter.ins('rts','',2)

def _lower_begin_auxiliary_command_stage(emitter,rules):
    emitter.segment(0x34f26,0x34f36)
    emitter.ins('bsr.w','main_pc_034f36',4)
    emitter.ins('move.w','#0x1,0xf728:w',6)
    emitter.ins('bsr.w','main_pc_034f64',4)
    emitter.ins('rts','',2)

def _lower_dispatch_auxiliary_command_stage(emitter,rules):
    emitter.segment(0x34f64,0x34f7c)
    emitter.ins('move.w','0xf728:w,%d0',4)
    emitter.ins('bmi.w','main_pc_034f7a',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('lsl.w','#0x1,%d0',2)
    emitter.ins('move.w','10(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','30(%pc, %d0.w)',4)
    emitter.ins('bra.b','main_pc_034f64',2)
    emitter.ins('rts','',2)

def _lower_upload_glyph_tile_sequence(emitter,rules):
    emitter.segment(0x353fc,0x35478)
    emitter.ins('move.l','#0x40200000,0xc00004:l',10)
    emitter.ins('lea.l','0x8991c:l,%a0',6)
    emitter.ins('lea.l','0x89932:l,%a1',6)
    emitter.ins('lea.l','0xd300:w,%a2',4)
    emitter.ins('clr.w','%d0',2)
    emitter.ins('move.b','(%a0)+,%d0',2)
    emitter.ins('bmi.b','main_pc_035476',2)
    emitter.ins('beq.b','main_pc_035412',2)
    emitter.ins('bsr.w','main_pc_035478',4)
    emitter.ins('move.w','(%a1)+,%d3',2)
    emitter.ins('bsr.w','main_pc_035490',4)
    emitter.ins('move.w','#0xf,%d4',4)
    emitter.ins('bsr.w','main_pc_0354b2',4)
    emitter.ins('move.l','%d7,(%a2)',2)
    emitter.ins('bsr.w','main_pc_0354b2',4)
    emitter.ins('move.l','%d7,(%a2, %d1.w)',4)
    emitter.ins('addq.w','#0x4,%a2',2)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('dbra','%d4,main_pc_03542c',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('beq.b','main_pc_03545c',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.l','%d7,(%a2)',2)
    emitter.ins('move.l','%d7,0x4(%a2)',4)
    emitter.ins('move.l','%d7,(%a2, %d1.w)',4)
    emitter.ins('move.l','%d7,0x4(%a2, %d1.w)',4)
    emitter.ins('addq.w','#0x8,%a2',2)
    emitter.ins('subq.w','#0x2,%d2',2)
    emitter.ins('bra.b','main_pc_035422',2)
    emitter.ins('tst.w','%d2',2)
    emitter.ins('beq.b','main_pc_035470',2)
    emitter.ins('subq.w','#0x1,%d2',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.l','%d7,(%a2)',2)
    emitter.ins('move.l','%d7,(%a2, %d1.w)',4)
    emitter.ins('addq.l','#0x4,%a2',2)
    emitter.ins('dbra','%d2,main_pc_035464',4)
    emitter.ins('bsr.w','main_pc_0354ca',4)
    emitter.ins('bra.b','main_pc_035412',2)
    emitter.ins('rts','',2)

def _lower_calculate_glyph_row_layout(emitter,rules):
    emitter.segment(0x35478,0x35490)
    emitter.ins('move.w','%d0,%d2',2)
    emitter.ins('lsl.w','#0x3,%d2',2)
    emitter.ins('addi.w','#0x14,%d2',4)
    emitter.ins('andi.w','#0xffe0,%d2',4)
    emitter.ins('move.w','%d0,%d1',2)
    emitter.ins('lsl.w','#0x6,%d1',2)
    emitter.ins('add.w','%d2,%d1',2)
    emitter.ins('move.w','%d1,%d2',2)
    emitter.ins('lsr.w','#0x2,%d2',2)
    emitter.ins('rts','',2)

def _lower_select_glyph_bitmap(emitter,rules):
    emitter.segment(0x35490,0x354b2)
    emitter.ins('move.w','%d3,-(%a7)',2)
    emitter.ins('move.w','%d3,%d4',2)
    emitter.ins('andi.l','#0xff00,%d3',6)
    emitter.ins('lsl.l','#0x3,%d3',2)
    emitter.ins('andi.w','#0xff,%d4',4)
    emitter.ins('lsl.w','#0x5,%d4',2)
    emitter.ins('add.w','%d4,%d3',2)
    emitter.ins('lea.l','0x8159c:l,%a3',6)
    emitter.ins('lea.l','(%a3, %d3.w),%a3',4)
    emitter.ins('move.w','(%a7)+,%d3',2)
    emitter.ins('rts','',2)

def _lower_expand_monochrome_glyph_byte(emitter,rules):
    emitter.segment(0x354b2,0x354ca)
    emitter.ins('move.b','(%a3)+,%d6',2)
    emitter.ins('moveq','#0,%d7',2)
    emitter.ins('move.w','#0x7,%d5',4)
    emitter.ins('lsl.l','#0x4,%d7',2)
    emitter.ins('roxl.b','#0x1,%d6',2)
    emitter.ins('bcc.b','main_pc_0354c4',2)
    emitter.ins('ori.b','#0x1,%d7',4)
    emitter.ins('dbra','%d5,main_pc_0354ba',4)
    emitter.ins('rts','',2)

def _lower_upload_expanded_glyph_rows(emitter,rules):
    emitter.segment(0x354ca,0x354de)
    emitter.ins('lea.l','0xd300:w,%a2',4)
    emitter.ins('lsr.w','#0x1,%d1',2)
    emitter.ins('subq.w','#0x1,%d1',2)
    emitter.ins('move.l','(%a2)+,0xc00000:l',6)
    emitter.ins('dbra','%d1,main_pc_0354d2',4)
    emitter.ins('rts','',2)

def _lower_initialize_auxiliary_text_panel(emitter,rules):
    emitter.segment(0x355da,0x3563e)
    emitter.ins('move.w','0xf348:w,%d0',4)
    emitter.ins('move.b','94(%pc, %d0.w),%d0',4)
    emitter.ins('move.w','%d0,0xf34a:w',4)
    emitter.ins('move.w','#0x5,%d1',4)
    emitter.ins('jsr','main_pc_0661d4:l',6)
    emitter.ins('lea.l','0xfb00:w,%a0',4)
    emitter.ins('lea.l','0xfb80:w,%a1',4)
    emitter.ins('move.w','#0x7,%d0',4)
    emitter.ins('move.l','(%a0)+,(%a1)+',2)
    emitter.ins('dbra','%d0,main_pc_0355fc',4)
    emitter.ins('move.l','#0xeee,(%a1)',6)
    emitter.ins('lea.l','0xc00004:l,%a6',6)
    emitter.ins('lea.l','0xc00000:l,%a5',6)
    emitter.ins('move.l','#0x41ca0003,%d1',6)
    emitter.ins('move.w','#0x8f80,(%a6)',4)
    emitter.ins('bsr.w','main_pc_035644',4)
    emitter.ins('subi.l','#0x840000,%d1',6)
    emitter.ins('move.w','#0x211d,%d2',4)
    emitter.ins('bsr.w','main_pc_03569a',4)
    emitter.ins('move.w','#0x8f02,(%a6)',4)
    emitter.ins('bsr.w','main_pc_0356f2',4)
    emitter.ins('bsr.w','main_pc_035740',4)
    emitter.ins('rts','',2)

def _lower_draw_auxiliary_text_panel_border(emitter,rules):
    emitter.segment(0x35644,0x3569a)
    emitter.ins('move.w','#0xa,%d0',4)
    emitter.ins('move.w','#0x5,%d2',4)
    emitter.ins('move.w','%d0,%d4',2)
    emitter.ins('move.l','%d1,(%a6)',2)
    emitter.ins('move.w','#0x7,%d3',4)
    emitter.ins('move.w','%d4,(%a5)',2)
    emitter.ins('addq.w','#0x6,%d4',2)
    emitter.ins('dbra','%d3,main_pc_035654',4)
    emitter.ins('cmpi.w','#0x3,%d2',4)
    emitter.ins('beq.w','main_pc_035674',4)
    emitter.ins('cmpi.w','#0x2,%d2',4)
    emitter.ins('bne.w','main_pc_03568c',4)
    emitter.ins('move.w','#0x2101,%d5',4)
    emitter.ins('bra.w','main_pc_035678',4)
    emitter.ins('move.w','#0x210f,%d5',4)
    emitter.ins('move.w','#0x0,(%a5)',4)
    emitter.ins('move.w','#0x0,(%a5)',4)
    emitter.ins('move.w','#0xd,%d3',4)
    emitter.ins('move.w','%d5,(%a5)',2)
    emitter.ins('addq.w','#0x1,%d5',2)
    emitter.ins('dbra','%d3,main_pc_035684',4)
    emitter.ins('subq.w','#0x1,%d0',2)
    emitter.ins('subi.l','#0x20000,%d1',6)
    emitter.ins('dbra','%d2,main_pc_03564c',4)
    emitter.ins('rts','',2)

def _lower_draw_auxiliary_text_panel_rows(emitter,rules):
    emitter.segment(0x3569a,0x356f2)
    emitter.ins('move.w','0xf348:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('movea.l','110(%pc, %d0.w),%a0',4)
    emitter.ins('move.w','#0x8,%d3',4)
    emitter.ins('addq.l','#0x1,%a0',2)
    emitter.ins('move.b','(%a0)+,%d4',2)
    emitter.ins('andi.w','#0xff,%d4',4)
    emitter.ins('move.w','%d4,%d5',2)
    emitter.ins('lsl.w','#0x1,%d5',2)
    emitter.ins('addi.w','#0x5,%d5',4)
    emitter.ins('lsr.w','#0x3,%d5',2)
    emitter.ins('lsl.w','#0x1,%d4',2)
    emitter.ins('add.w','%d5,%d4',2)
    emitter.ins('move.w','%d2,%d5',2)
    emitter.ins('add.w','%d4,%d5',2)
    emitter.ins('move.w','%d4,%d6',2)
    emitter.ins('subq.w','#0x1,%d6',2)
    emitter.ins('move.l','%d1,(%a6)',2)
    emitter.ins('move.w','%d5,(%a5)',2)
    emitter.ins('addq.w','#0x1,%d5',2)
    emitter.ins('dbra','%d6,main_pc_0356c8',4)
    emitter.ins('subi.l','#0x20000,%d1',6)
    emitter.ins('move.l','%d1,(%a6)',2)
    emitter.ins('move.w','%d4,%d6',2)
    emitter.ins('subq.w','#0x1,%d6',2)
    emitter.ins('move.w','%d2,(%a5)',2)
    emitter.ins('addq.w','#0x1,%d2',2)
    emitter.ins('dbra','%d6,main_pc_0356dc',4)
    emitter.ins('subi.l','#0x40000,%d1',6)
    emitter.ins('add.w','%d4,%d2',2)
    emitter.ins('dbra','%d3,main_pc_0356aa',4)
    emitter.ins('rts','',2)

def _lower_upload_auxiliary_text_panel_glyphs(emitter,rules):
    emitter.segment(0x356f2,0x35710)
    emitter.ins('move.l','#0x60200000,0xc00004:l',10)
    emitter.ins('move.w','0xf348:w,%d0',4)
    emitter.ins('lsl.w','#0x2,%d0',2)
    emitter.ins('movea.l','12(%pc, %d0.w),%a0',4)
    emitter.ins('movea.l','32(%pc, %d0.w),%a1',4)
    emitter.ins('bsr.w','main_pc_035412',4)
    emitter.ins('rts','',2)

def _lower_draw_auxiliary_text_panel_markers(emitter,rules):
    emitter.segment(0x35740,0x35760)
    emitter.ins('move.l','#0x43420003,(%a6)',6)
    emitter.ins('move.l','#0x350036,(%a5)',6)
    emitter.ins('move.l','#0x370038,(%a5)',6)
    emitter.ins('move.l','#0x44440003,(%a6)',6)
    emitter.ins('move.l','#0x3d003e,(%a5)',6)
    emitter.ins('rts','',2)

def _lower_decode_unmasked_literal_plane(emitter,rules):
    emitter.segment(0x3aab6,0x3aac2)
    emitter.ins('clr.w','0x8000:w',4)
    emitter.ins('move.w','#0x1,0x8002:w',6)
    emitter.ins('bra.b','main_pc_03aada',2)

def _lower_decode_high_plane_rows(emitter,rules):
    emitter.segment(0x3aac2,0x3aace)
    emitter.ins('move.w','#0x8000,0x8000:w',6)
    emitter.ins('move.w','#0x20,%d6',4)
    emitter.ins('bra.b','main_pc_03aad6',2)

def _lower_run_repeating_scene_presentation(emitter,rules):
    emitter.segment(0x3b732,0x3b788)
    emitter.ins('move.w','#0x2700,%sr',4)
    emitter.ins('move.w','0xf606:w,%d0',4)
    emitter.ins('andi.b','#0xbf,%d0',4)
    emitter.ins('move.w','%d0,0xc00004:l',6)
    emitter.ins('jsr','main_pc_0068ce:l',6)
    emitter.ins('bsr.w','main_pc_03daec',4)
    emitter.ins('jsr','-3270(%pc)',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x1,%d0',2)
    emitter.ins('move.w','46(%pc, %d0.w),%d0',4)
    emitter.ins('jsr','main_pc_00808a:l',6)
    emitter.ins('move.w','#0x2500,%sr',4)
    emitter.ins('move.w','#0x500,0xf612:w',6)
    emitter.ins('jsr','main_pc_0083c8:l',6)
    emitter.ins('jsr','-1260(%pc)',4)
    emitter.ins('jsr','-3584(%pc)',4)
    emitter.ins('jsr','24(%pc)',4)
    emitter.ins('nop','',2)
    emitter.ins('jsr','-1350(%pc)',4)
    emitter.ins('bra.w','main_pc_03b766',4)

def _lower_dispatch_repeating_scene_presentation(emitter,rules):
    emitter.segment(0x3b794,0x3b79e)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('jmp','2(%pc, %d0.w)',4)

def _lower_initialize_object_scene_video(emitter,rules):
    emitter.segment(0x3daec,0x3dc54)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','#0x8230,0xc00004:l',8)
    emitter.ins('move.w','#0x8330,0xc00004:l',8)
    emitter.ins('move.w','#0x8407,0xc00004:l',8)
    emitter.ins('move.w','#0x8568,0xc00004:l',8)
    emitter.ins('move.w','#0x8700,0xc00004:l',8)
    emitter.ins('move.w','#0x8b00,0xc00004:l',8)
    emitter.ins('move.w','#0x8c81,0xc00004:l',8)
    emitter.ins('move.w','#0x8d35,0xc00004:l',8)
    emitter.ins('move.w','#0x8f02,0xc00004:l',8)
    emitter.ins('move.w','#0x9011,0xc00004:l',8)
    emitter.ins('move.w','#0x9194,0xc00004:l',8)
    emitter.ins('move.w','#0x9200,0xc00004:l',8)
    emitter.ins('move.w','#0x30,0x8020:w',6)
    emitter.ins('move.w','#0x0,0x8024:w',6)
    emitter.ins('move.w','#0x30,0x8026:w',6)
    emitter.ins('move.w','#0x20,0x8022:w',6)
    emitter.ins('move.w','#0x0,0x8028:w',6)
    emitter.ins('move.w','#0x20,0x802a:w',6)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','212(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('move.w','#0x0,%d0',4)
    emitter.ins('bsr.w','main_pc_03ab52',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','208(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('move.w','#0x2000,%d0',4)
    emitter.ins('bsr.w','main_pc_03ab52',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','204(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('move.w','#0x4000,%d0',4)
    emitter.ins('bsr.w','main_pc_03ab52',4)
    emitter.ins('lea.l','0x4e090:l,%a0',6)
    emitter.ins('move.w','#0x8000,%d0',4)
    emitter.ins('bsr.w','main_pc_03ab52',4)
    emitter.ins('lea.l','0x4fbe4:l,%a0',6)
    emitter.ins('move.w','#0xa000,%d0',4)
    emitter.ins('bsr.w','main_pc_03ab52',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','172(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('lea.l','0xe000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('jsr','-12588(%pc)',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('asl.w','#0x2,%d0',2)
    emitter.ins('lea.l','160(%pc),%a0',4)
    emitter.ins('nop','',2)
    emitter.ins('movea.l','(%a0, %d0.w),%a0',4)
    emitter.ins('lea.l','0xf000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('jsr','-12620(%pc)',4)
    emitter.ins('lea.l','0x45413:l,%a0',6)
    emitter.ins('lea.l','0xc000:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('jsr','-12654(%pc)',4)
    emitter.ins('lea.l','0x456ec:l,%a0',6)
    emitter.ins('lea.l','0xc040:l,%a1',6)
    emitter.ins('move.l','#0x80,%d5',6)
    emitter.ins('jsr','-12676(%pc)',4)
    emitter.ins('move.w','0x80da:w,%d0',4)
    emitter.ins('addq.w','#0x4,%d0',2)
    emitter.ins('jsr','-12476(%pc)',4)
    emitter.ins('rts','',2)

def _lower_set_uniform_conservative_orders(emitter,rules):
    emitter.segment(0x41bee,0x41bf2)
    emitter.ins('bra.w','main_pc_041c02',4)
    emitter.segment(0x41c02,0x41c16)
    emitter.ins('move.w','#0x5,0x812a:w',6)
    emitter.ins('move.w','#0x5,0x812c:w',6)
    emitter.ins('move.w','#0x5,0x812e:w',6)
    emitter.ins('rts','',2)

def _lower_set_first_timed_formation_orders(emitter,rules):
    emitter.segment(0x41bf2,0x41bf6)
    emitter.ins('bra.w','main_pc_041c16',4)
    emitter.segment(0x41c16,0x41c46)
    emitter.ins('cmpi.w','#0x4,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041c32',2)
    emitter.ins('move.w','#0x5,0x812a:w',6)
    emitter.ins('move.w','#0x5,0x812c:w',6)
    emitter.ins('move.w','#0x5,0x812e:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x1,0x812a:w',6)
    emitter.ins('move.w','#0x1,0x812c:w',6)
    emitter.ins('move.w','#0x1,0x812e:w',6)
    emitter.ins('rts','',2)

def _lower_set_mixed_timed_formation_orders(emitter,rules):
    emitter.segment(0x41bf6,0x41bfa)
    emitter.ins('bra.w','main_pc_041c46',4)
    emitter.segment(0x41c46,0x41c76)
    emitter.ins('cmpi.w','#0x5,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041c62',2)
    emitter.ins('move.w','#0x5,0x812a:w',6)
    emitter.ins('move.w','#0x5,0x812c:w',6)
    emitter.ins('move.w','#0x5,0x812e:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x1,0x812a:w',6)
    emitter.ins('move.w','#0x1,0x812c:w',6)
    emitter.ins('move.w','#0x4,0x812e:w',6)
    emitter.ins('rts','',2)

def _lower_set_third_timed_formation_orders(emitter,rules):
    emitter.segment(0x41bfa,0x41bfe)
    emitter.ins('bra.w','main_pc_041c76',4)
    emitter.segment(0x41c76,0x41ca6)
    emitter.ins('cmpi.w','#0x5,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041c92',2)
    emitter.ins('move.w','#0x5,0x812a:w',6)
    emitter.ins('move.w','#0x5,0x812c:w',6)
    emitter.ins('move.w','#0x5,0x812e:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x1,0x812a:w',6)
    emitter.ins('move.w','#0x1,0x812c:w',6)
    emitter.ins('move.w','#0x1,0x812e:w',6)
    emitter.ins('rts','',2)

def _lower_set_uniform_timed_formation_orders(emitter,rules):
    emitter.segment(0x41bfe,0x41c02)
    emitter.ins('bra.w','main_pc_041ca6',4)
    emitter.segment(0x41ca6,0x41cd6)
    emitter.ins('cmpi.w','#0x6,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041cc2',2)
    emitter.ins('move.w','#0x5,0x812a:w',6)
    emitter.ins('move.w','#0x5,0x812c:w',6)
    emitter.ins('move.w','#0x5,0x812e:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x4,0x812a:w',6)
    emitter.ins('move.w','#0x4,0x812c:w',6)
    emitter.ins('move.w','#0x4,0x812e:w',6)
    emitter.ins('rts','',2)

def _lower_choose_first_leader_action(emitter,rules):
    emitter.segment(0x41cea,0x41cee)
    emitter.ins('bra.w','main_pc_041cfe',4)
    emitter.segment(0x41cf6,0x41cfa)
    emitter.ins('bra.w','main_pc_041cfe',4)
    emitter.segment(0x41cfe,0x41d3c)
    emitter.ins('cmpi.w','#0x6,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041d26',2)
    emitter.ins('move.w','#0x5,0x8130:w',6)
    emitter.ins('cmpi.w','#0x28,0x8178:w',6)
    emitter.ins('bhi.b','main_pc_041d3c',2)
    emitter.ins('jsr','-26100(%pc)',4)
    emitter.ins('andi.w','#0x7,%d0',4)
    emitter.ins('beq.b','main_pc_041d3c',2)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('jsr','-26124(%pc)',4)
    emitter.ins('andi.w','#0x3,%d0',4)
    emitter.ins('bne.b','main_pc_041d3c',2)
    emitter.ins('move.w','#0x5,0x8130:w',6)

def _lower_choose_second_leader_action(emitter,rules):
    emitter.segment(0x41cee,0x41cf2)
    emitter.ins('bra.w','main_pc_041d3e',4)
    emitter.segment(0x41d3e,0x41d7a)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('cmpi.w','#0x6,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041d7a',2)
    emitter.ins('move.w','#0x1,0x8130:w',6)
    emitter.ins('cmpi.w','#0xa,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041d60',2)
    emitter.ins('move.w','#0x5,0x8130:w',6)
    emitter.ins('cmpi.w','#0x28,0x8178:w',6)
    emitter.ins('bhi.b','main_pc_041d7a',2)
    emitter.ins('jsr','-26184(%pc)',4)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('bne.b','main_pc_041d7a',2)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('rts','',2)

def _lower_choose_third_leader_action(emitter,rules):
    emitter.segment(0x41cf2,0x41cf6)
    emitter.ins('bra.w','main_pc_041d7c',4)
    emitter.segment(0x41d7c,0x41d9e)
    emitter.ins('jsr','-26204(%pc)',4)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('bne.b','main_pc_041d96',2)
    emitter.ins('cmpi.w','#0x5,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041d96',2)
    emitter.ins('move.w','#0x5,0x8130:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('rts','',2)

def _lower_choose_fifth_leader_action(emitter,rules):
    emitter.segment(0x41cfa,0x41cfe)
    emitter.ins('bra.w','main_pc_041d9e',4)
    emitter.segment(0x41d9e,0x41dc0)
    emitter.ins('jsr','-26238(%pc)',4)
    emitter.ins('andi.w','#0x1,%d0',4)
    emitter.ins('bne.b','main_pc_041db8',2)
    emitter.ins('cmpi.w','#0x6,0x8160:w',6)
    emitter.ins('bcs.b','main_pc_041db8',2)
    emitter.ins('move.w','#0x5,0x8130:w',6)
    emitter.ins('rts','',2)
    emitter.ins('move.w','#0x4,0x8130:w',6)
    emitter.ins('rts','',2)

LOWERERS={
    'refresh_setup_option_labels':_lower_refresh_setup_option_labels,
    'render_packed_sprite_position':_lower_render_packed_sprite_position,
    'render_selected_setup_options':_lower_render_selected_setup_options,
    'render_setup_player_position':_lower_render_setup_player_position,
    'cycle_second_player_choice':_lower_cycle_second_player_choice,
    'cycle_third_player_choice':_lower_cycle_third_player_choice,
    'run_controller_setup_and_configuration':_lower_run_controller_setup_and_configuration,
    'update_connected_controller_option':_lower_update_connected_controller_option,
    'advance_controller_setup_reveal':_lower_advance_controller_setup_reveal,
    'advance_controller_setup_dismissal':_lower_advance_controller_setup_dismissal,
    'read_controller_identity':_lower_read_controller_identity,
    'commit_setup_options':_lower_commit_setup_options,
    'locate_selected_ruler_city':_lower_locate_selected_ruler_city,
    'locate_selected_force_packet':_lower_locate_selected_force_packet,
    'deduct_all_map_packet_supply':_lower_deduct_all_map_packet_supply,
    'calculate_map_packet_supply':_lower_calculate_map_packet_supply,
    'apply_map_packet_supply_losses':_lower_apply_map_packet_supply_losses,
    'sample_map_packet_loss_factors':_lower_sample_map_packet_loss_factors,
    'compact_map_packet_survivors':_lower_compact_map_packet_survivors,
    'replace_map_queue_leader':_lower_replace_map_queue_leader,
    'remove_map_queue_leader':_lower_remove_map_queue_leader,
    'initialize_force_turn_order':_lower_initialize_force_turn_order,
    'shuffle_force_turn_order':_lower_shuffle_force_turn_order,
    'select_next_force_turn':_lower_select_next_force_turn,
    'recover_idle_officer_readiness':_lower_recover_idle_officer_readiness,
    'run_city_command_assignment':_lower_run_city_command_assignment,
    'clear_unassigned_officer_commands':_lower_clear_unassigned_officer_commands,
    'run_city_command_states':_lower_run_city_command_states,
    'run_map_packet_command_states':_lower_run_map_packet_command_states,
    'select_next_force_city':_lower_select_next_force_city,
    'select_next_force_map_packet':_lower_select_next_force_map_packet,
    'sample_city_command_policy':_lower_sample_city_command_policy,
    'clear_current_city_project_orders':_lower_clear_current_city_project_orders,
    'build_current_city_officer_roster':_lower_build_current_city_officer_roster,
    'finish_city_command_assignment':_lower_finish_city_command_assignment,
    'retain_city_command_stage':_lower_retain_city_command_stage,
    'dispatch_city_assignment_state':_lower_dispatch_city_assignment_state,
    'dispatch_city_command_stage':_lower_dispatch_city_command_stage,
    'dispatch_map_packet_command_stage':_lower_dispatch_map_packet_command_stage,
    'begin_auxiliary_command_stage':_lower_begin_auxiliary_command_stage,
    'dispatch_auxiliary_command_stage':_lower_dispatch_auxiliary_command_stage,
    'upload_glyph_tile_sequence':_lower_upload_glyph_tile_sequence,
    'calculate_glyph_row_layout':_lower_calculate_glyph_row_layout,
    'select_glyph_bitmap':_lower_select_glyph_bitmap,
    'expand_monochrome_glyph_byte':_lower_expand_monochrome_glyph_byte,
    'upload_expanded_glyph_rows':_lower_upload_expanded_glyph_rows,
    'initialize_auxiliary_text_panel':_lower_initialize_auxiliary_text_panel,
    'draw_auxiliary_text_panel_border':_lower_draw_auxiliary_text_panel_border,
    'draw_auxiliary_text_panel_rows':_lower_draw_auxiliary_text_panel_rows,
    'upload_auxiliary_text_panel_glyphs':_lower_upload_auxiliary_text_panel_glyphs,
    'draw_auxiliary_text_panel_markers':_lower_draw_auxiliary_text_panel_markers,
    'decode_unmasked_literal_plane':_lower_decode_unmasked_literal_plane,
    'decode_high_plane_rows':_lower_decode_high_plane_rows,
    'run_repeating_scene_presentation':_lower_run_repeating_scene_presentation,
    'dispatch_repeating_scene_presentation':_lower_dispatch_repeating_scene_presentation,
    'initialize_object_scene_video':_lower_initialize_object_scene_video,
    'set_uniform_conservative_orders':_lower_set_uniform_conservative_orders,
    'set_first_timed_formation_orders':_lower_set_first_timed_formation_orders,
    'set_mixed_timed_formation_orders':_lower_set_mixed_timed_formation_orders,
    'set_third_timed_formation_orders':_lower_set_third_timed_formation_orders,
    'set_uniform_timed_formation_orders':_lower_set_uniform_timed_formation_orders,
    'choose_first_leader_action':_lower_choose_first_leader_action,
    'choose_second_leader_action':_lower_choose_second_leader_action,
    'choose_third_leader_action':_lower_choose_third_leader_action,
    'choose_fifth_leader_action':_lower_choose_fifth_leader_action,
}

def compile_source(source):
    records=semantic_functions(source,DECLARATIONS,APPROVED)
    sole_formation_fields = {name:records[name]['effects'] for name in ('_scene_formation_legacy_fields', '_scene_formation_random_fields', 'choose_alternate_first_leader_action_fields', 'choose_fifth_leader_action_fields', 'choose_first_leader_action_fields', 'choose_scene_object_leader_action_fields', 'choose_second_leader_action_fields', 'choose_third_leader_action_fields', 'set_first_timed_formation_orders_fields', 'set_mixed_timed_formation_orders_fields', 'set_scene_object_formation_orders_fields', 'set_third_timed_formation_orders_fields', 'set_uniform_conservative_orders_fields', 'set_uniform_timed_formation_orders_fields')}
    for owner in ('set_uniform_conservative_orders', 'set_first_timed_formation_orders', 'set_mixed_timed_formation_orders', 'set_third_timed_formation_orders', 'set_uniform_timed_formation_orders', 'choose_first_leader_action', 'choose_second_leader_action', 'choose_third_leader_action', 'choose_fifth_leader_action'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'],sole_formation_fields=sole_formation_fields)
    sole_packet_fields = {name:records[name]['effects'] for name in ('_map_packet_call_fields', '_map_packet_divu_fields', '_map_packet_legacy_entry_fields', '_map_packet_legacy_result_fields', '_map_packet_lost_message_fields', '_map_packet_survivor_store_fields', 'apply_map_packet_supply_losses_fields', 'calculate_map_packet_supply_fields', 'compact_map_packet_survivors_fields', 'deduct_all_map_packet_supply_fields', 'initialize_force_turn_order_fields', 'recover_idle_officer_readiness_fields', 'remove_map_queue_leader_fields', 'replace_map_queue_leader_fields', 'sample_map_packet_loss_factors_fields', 'select_next_force_turn_fields', 'shuffle_force_turn_order_fields')}
    for owner in ('apply_map_packet_supply_losses', 'calculate_map_packet_supply', 'compact_map_packet_survivors', 'deduct_all_map_packet_supply', 'initialize_force_turn_order', 'recover_idle_officer_readiness', 'remove_map_queue_leader', 'replace_map_queue_leader', 'sample_map_packet_loss_factors', 'select_next_force_turn', 'shuffle_force_turn_order'):
        records[owner]['effects'] = dict(previous=records[owner]['effects'],sole_map_packet_fields=sole_packet_fields)
    records['recover_idle_officer_readiness']['rules'].update(records['recover_idle_officer_readiness_fields']['rules'])
    sole_map_presentation_fields = {name: records[name]['effects'] for name in ('_assignment_location_carry_fields', '_assignment_location_store_fields', 'locate_selected_force_packet_fields', 'locate_selected_ruler_city_fields')}
    for owner in ('locate_selected_ruler_city', 'locate_selected_force_packet'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_map_fields=sole_map_presentation_fields)
    sole_setup_assignment_fields = {name: records[name]['effects'] for name in ('_city_assignment_child_fields', '_city_assignment_vector_fields', '_controller_setup_begin_fields', '_controller_setup_byte_shift_fields', '_controller_setup_child_fields', '_controller_setup_cycle_player_fields', '_controller_setup_fill_descriptor_fields', '_controller_setup_interrupt_status_fields', '_controller_setup_last_button_fields', '_controller_setup_main_iteration_fields', '_controller_setup_option_sprite_fields', '_controller_setup_palette_fields', '_controller_setup_visible_fields', '_controller_setup_wait_irq_fields', 'advance_controller_setup_dismissal_fields', 'advance_controller_setup_reveal_fields', 'build_current_city_officer_roster_fields', 'clear_current_city_project_orders_fields', 'clear_unassigned_officer_commands_fields', 'commit_setup_options_fields', 'cycle_second_player_choice_fields', 'cycle_third_player_choice_fields', 'dispatch_city_assignment_state_fields', 'finish_city_command_assignment_fields', 'read_controller_identity_fields', 'refresh_setup_option_labels_fields', 'render_packed_sprite_position_fields', 'render_selected_setup_options_fields', 'render_setup_player_position_fields', 'retain_city_command_stage_fields', 'run_city_command_assignment_fields', 'run_city_command_states_fields', 'run_controller_setup_and_configuration_fields', 'run_map_packet_command_states_fields', 'sample_city_command_policy_fields', 'select_next_force_city_fields', 'select_next_force_map_packet_fields', 'update_connected_controller_option_fields', 'recover_unacted_officer_b200_fields', '_clear_invalid_debt_record_fields', 'clear_unowned_debt_records_fields')}
    for owner in ('refresh_setup_option_labels', 'render_packed_sprite_position', 'render_selected_setup_options', 'render_setup_player_position', 'cycle_second_player_choice', 'cycle_third_player_choice', 'run_controller_setup_and_configuration', 'update_connected_controller_option', 'advance_controller_setup_reveal', 'advance_controller_setup_dismissal', 'read_controller_identity', 'commit_setup_options', 'run_city_command_assignment', 'clear_unassigned_officer_commands', 'run_city_command_states', 'run_map_packet_command_states', 'select_next_force_city', 'select_next_force_map_packet', 'sample_city_command_policy', 'clear_current_city_project_orders', 'build_current_city_officer_roster', 'finish_city_command_assignment', 'retain_city_command_stage', 'dispatch_city_assignment_state'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_setup_assignment_fields=sole_setup_assignment_fields)
    sole_game_text_fields = {name: records[name]['effects'] for name in ('_aux_text_call_fields', '_aux_text_clear_glyph_pair_fields', '_aux_text_dispatch_stage_fields', '_aux_text_legacy_glyph_fields', '_aux_text_legacy_glyph_result', '_aux_text_shift_word_fields', '_object_scene_directory_fields', '_object_scene_legacy_fields', '_object_scene_legacy_result', 'begin_auxiliary_command_stage_fields', 'calculate_glyph_row_layout_fields', 'decode_high_plane_rows_fields', 'decode_unmasked_literal_plane_fields', 'dispatch_auxiliary_command_stage_fields', 'dispatch_city_command_stage_fields', 'dispatch_map_packet_command_stage_fields', 'dispatch_repeating_scene_presentation_fields', 'draw_auxiliary_text_panel_border_fields', 'draw_auxiliary_text_panel_markers_fields', 'draw_auxiliary_text_panel_rows_fields', 'expand_glyph_tile_sequence_fields', 'expand_monochrome_glyph_byte_fields', 'initialize_auxiliary_text_panel_fields', 'initialize_object_scene_video_fields', 'run_repeating_scene_presentation_fields', 'select_glyph_bitmap_fields', 'upload_auxiliary_text_panel_glyphs_fields', 'upload_expanded_glyph_rows_fields', 'upload_glyph_tile_sequence_fields')}
    for owner in ('dispatch_city_command_stage', 'dispatch_map_packet_command_stage', 'begin_auxiliary_command_stage', 'dispatch_auxiliary_command_stage', 'upload_glyph_tile_sequence', 'calculate_glyph_row_layout', 'select_glyph_bitmap', 'expand_monochrome_glyph_byte', 'upload_expanded_glyph_rows', 'initialize_auxiliary_text_panel', 'draw_auxiliary_text_panel_border', 'draw_auxiliary_text_panel_rows', 'upload_auxiliary_text_panel_glyphs', 'draw_auxiliary_text_panel_markers', 'decode_unmasked_literal_plane', 'decode_high_plane_rows', 'run_repeating_scene_presentation', 'dispatch_repeating_scene_presentation', 'initialize_object_scene_video', 'expand_glyph_tile_sequence'):
        records[owner]['effects'] = dict(legacy_projection=records[owner]['effects'], sole_current_game_text_fields=sole_game_text_fields)
    return lower_declared(records,BUSINESS_SCENE_SUPPORT_BINDINGS,LOWERERS)

# B38 sole Main formation fields and genuine Dynamic JMP routes; native lowerers unchanged.
for _module,_names in {'business_gameplay': ['advance_setup_dismissal',
                       'advance_setup_reveal',
                       'cycle_setup_option',
                       'initialize_setup_video',
                       'settle_city_projects_and_refresh_map',
                       'update_first_setup_option',
                       'update_fourth_setup_option',
                       'update_second_setup_option',
                       'update_setup_player_choices',
                       'update_third_setup_option',
                       'write_setup_video_address'],
 'business_highbank': ['advance_officer_growth_levels'],
 'contexts_gameplay': ['GameplayCall', 'ProjectValues', 'SetupPlane', 'SetupValues'],
 'contexts_highbank': ['GrowthValues'],
 'contexts_scene_support': ['CityCommandValues',
                            'GlyphTileLayout',
                            'SceneCall',
                            'ScenePresentation',
                            'checked_context'],
 'domain': ['Boundary',
            'Cursor',
            'Long',
            'SceneState',
            'Table',
            'VideoPlaneAddress',
            'Word',
            'checked_cursor',
            'checked_state',
            'data_view',
            'descending_inclusive',
            'divu_retained',
            'low16',
            'low8',
            'negative_byte',
            'negative_word',
            'ram_view',
            'replace_byte',
            'replace_word',
            's16',
            'swap_words',
            'u16',
            'u32',
            'u8',
            'uint'],
 'services': ['BattlePresentationMemory',
              'FirstDeploymentFrame',
              'SceneRefreshBoundary',
              'SceneRefreshMemory',
              'SceneRenderFrame',
              '_first_word',
              '_presentation_call_fields',
              '_scene_refresh_emit',
              '_scene_render_compare',
              'append_map_sprites',
              'call_target',
              'clear_video_sprite_plane',
              'enqueue_sound_command',
              'first_replace',
              'initialize_video_registers_and_planes',
              'sample_random_pair',
              'sample_random_preserving_seed_fields',
              'set_vram_write_address',
              'snapshot_and_clear_scene_palette',
              'upload_portrait_tiles',
              'wait_for_scene_sound_byte']}.items():
    APPROVED.setdefault(_module,set()).update(_names)
DECLARATIONS.pop('_presentation_random',None)
DECLARATIONS.update({'_scene_formation_legacy_fields': {'signature': 'state: SceneState, frame: ScenePresentation, entry: Long, needs_stack: '
                                                 'bool=False',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'checked_context(frame, ScenePresentation, state)\n'
                                            'if type(needs_stack) is not bool:\n'
                                            "    raise ValueError('actual physical-call requirement required')\n"
                                            'actual = first_replace(FirstDeploymentFrame.unobserved(), target_x=frame.command, '
                                            'target_y=frame.foreground, unit=frame.mode, count=frame.rows, distance=frame.tile, '
                                            'offset_x=frame.stride, offset_y=frame.palette, choice=frame.remaining, '
                                            'roster=frame.source, candidates=frame.destination, auxiliary=None if frame.actor is '
                                            'None else frame.actor.cursor(), scratch=None if frame.opponent is None else '
                                            'frame.opponent.cursor())\n'
                                            'if needs_stack:\n'
                                            '    raise SceneRefreshBoundary(entry, actual, None)\n'
                                            'return actual'},
 '_scene_formation_legacy_projection': {'signature': 'frame: ScenePresentation, actual: FirstDeploymentFrame',
                                        'returns': 'ScenePresentation',
                                        'flow': 'return replace(frame, command=actual.target_x, foreground=actual.target_y, '
                                                'mode=actual.unit, rows=actual.count, tile=actual.distance, '
                                                'stride=actual.offset_x, palette=actual.offset_y, remaining=actual.choice, '
                                                'source=actual.roster, destination=actual.candidates)'},
 '_scene_formation_random_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, mask: Word, '
                                                 'continuation: Long',
                                    'returns': 'FirstDeploymentFrame',
                                    'flow': 'if (mask, continuation) not in ((7, 269592), (3, 269616), (1, 269676), (1, 269696), '
                                            '(1, 269730)):\n'
                                            "    raise ValueError('actual Main formation RNG arm required')\n"
                                            'memory.frame(frame)\n'
                                            'if frame.stack_cursor is None:\n'
                                            '    raise SceneRefreshBoundary(243490, frame, continuation)\n'
                                            'def child(actual_memory, entered):\n'
                                            '    return '
                                            'sample_random_preserving_seed_fields(SceneRefreshMemory(actual_memory.state), '
                                            'entered)\n'
                                            'frame = _presentation_call_fields(BattlePresentationMemory(memory.state), frame, '
                                            'continuation, child)\n'
                                            "return memory.sync_status(_first_word(frame, 'target_x', low16(frame.target_x) & "
                                            'mask))'},
 'choose_alternate_first_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                          'returns': 'ScenePresentation',
                                          'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269558, True)\n'
                                                  'actual = '
                                                  'choose_alternate_first_leader_action_fields(SceneRefreshMemory(state), '
                                                  'actual)\n'
                                                  'return _scene_formation_legacy_projection(frame, actual)'},
 'choose_alternate_first_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                                 'returns': 'FirstDeploymentFrame',
                                                 'flow': 'return choose_scene_object_leader_action_fields(memory, frame, 0)'},
 'choose_fifth_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269562, True)\n'
                                        'actual = choose_fifth_leader_action_fields(SceneRefreshMemory(state), actual)\n'
                                        'return _scene_formation_legacy_projection(frame, actual)'},
 'choose_fifth_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'return choose_scene_object_leader_action_fields(memory, frame, 3)'},
 'choose_first_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269546, True)\n'
                                        'actual = choose_first_leader_action_fields(SceneRefreshMemory(state), actual)\n'
                                        'return _scene_formation_legacy_projection(frame, actual)'},
 'choose_first_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'return choose_scene_object_leader_action_fields(memory, frame, 0)'},
 'choose_scene_object_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, kind: Word',
                                              'returns': 'FirstDeploymentFrame',
                                              'flow': 'if kind not in (0, 1, 2, 3):\n'
                                                      "    raise ValueError('actual leader action branch required')\n"
                                                      'memory.frame(frame)\n'
                                                      'if kind == 0:\n'
                                                      '    memory.sync_status(frame)\n'
                                                      '    elapsed = memory.state.read(4294934880, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, elapsed, 6, 16)\n'
                                                      '    if elapsed < 6:\n'
                                                      '        frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 4)\n'
                                                      '        frame = _scene_formation_random_fields(memory, frame, 3, 269616)\n'
                                                      '        if low16(frame.target_x) == 0:\n'
                                                      '            frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 5)\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 5)\n'
                                                      '    morale = memory.state.read(4294934904, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, morale, 40, 16)\n'
                                                      '    if morale > 40:\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    frame = _scene_formation_random_fields(memory, frame, 7, 269592)\n'
                                                      '    if low16(frame.target_x) != 0:\n'
                                                      '        frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 4)\n'
                                                      '    return memory.sync_status(frame)\n'
                                                      'if kind == 1:\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 4)\n'
                                                      '    elapsed = memory.state.read(4294934880, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, elapsed, 6, 16)\n'
                                                      '    if elapsed < 6:\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 1)\n'
                                                      '    elapsed = memory.state.read(4294934880, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, elapsed, 10, 16)\n'
                                                      '    if elapsed >= 10:\n'
                                                      '        frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 5)\n'
                                                      '    morale = memory.state.read(4294934904, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, morale, 40, 16)\n'
                                                      '    if morale > 40:\n'
                                                      '        return memory.sync_status(frame)\n'
                                                      '    frame = _scene_formation_random_fields(memory, frame, 1, 269676)\n'
                                                      '    if low16(frame.target_x) == 0:\n'
                                                      '        frame = _scene_refresh_emit(memory, frame, 4294934832, 2, 4)\n'
                                                      '    return memory.sync_status(frame)\n'
                                                      'continuation = 269696 if kind == 2 else 269730\n'
                                                      'threshold = 5 if kind == 2 else 6\n'
                                                      'frame = _scene_formation_random_fields(memory, frame, 1, continuation)\n'
                                                      'if low16(frame.target_x) != 0:\n'
                                                      '    return _scene_refresh_emit(memory, frame, 4294934832, 2, 4)\n'
                                                      'elapsed = memory.state.read(4294934880, 2)\n'
                                                      'frame = _scene_render_compare(memory, frame, elapsed, threshold, 16)\n'
                                                      'return _scene_refresh_emit(memory, frame, 4294934832, 2, 5 if elapsed >= '
                                                      'threshold else 4)'},
 'choose_second_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                 'returns': 'ScenePresentation',
                                 'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269550, True)\n'
                                         'actual = choose_second_leader_action_fields(SceneRefreshMemory(state), actual)\n'
                                         'return _scene_formation_legacy_projection(frame, actual)'},
 'choose_second_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                        'returns': 'FirstDeploymentFrame',
                                        'flow': 'return choose_scene_object_leader_action_fields(memory, frame, 1)'},
 'choose_third_leader_action': {'signature': 'state: SceneState, frame: ScenePresentation',
                                'returns': 'ScenePresentation',
                                'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269554, True)\n'
                                        'actual = choose_third_leader_action_fields(SceneRefreshMemory(state), actual)\n'
                                        'return _scene_formation_legacy_projection(frame, actual)'},
 'choose_third_leader_action_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                       'returns': 'FirstDeploymentFrame',
                                       'flow': 'return choose_scene_object_leader_action_fields(memory, frame, 2)'},
 'set_first_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269298, False)\n'
                                              'actual = set_first_timed_formation_orders_fields(SceneRefreshMemory(state), '
                                              'actual)\n'
                                              'return _scene_formation_legacy_projection(frame, actual)'},
 'set_first_timed_formation_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'return set_scene_object_formation_orders_fields(memory, frame, 1)'},
 'set_mixed_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269302, False)\n'
                                              'actual = set_mixed_timed_formation_orders_fields(SceneRefreshMemory(state), '
                                              'actual)\n'
                                              'return _scene_formation_legacy_projection(frame, actual)'},
 'set_mixed_timed_formation_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'return set_scene_object_formation_orders_fields(memory, frame, 2)'},
 'set_scene_object_formation_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame, kind: Word',
                                              'returns': 'FirstDeploymentFrame',
                                              'flow': 'if kind not in (0, 1, 2, 3, 4):\n'
                                                      "    raise ValueError('actual formation order branch required')\n"
                                                      'memory.frame(frame)\n'
                                                      'orders = (5, 5, 5)\n'
                                                      'if kind != 0:\n'
                                                      '    threshold, early = ((4, (1, 1, 1)), (5, (1, 1, 4)), (5, (1, 1, 1)), '
                                                      '(6, (4, 4, 4)))[kind - 1]\n'
                                                      '    memory.sync_status(frame)\n'
                                                      '    elapsed = memory.state.read(4294934880, 2)\n'
                                                      '    frame = _scene_render_compare(memory, frame, elapsed, threshold, 16)\n'
                                                      '    if elapsed < threshold:\n'
                                                      '        orders = early\n'
                                                      'for address, order in ((4294934826, orders[0]), (4294934828, orders[1]), '
                                                      '(4294934830, orders[2])):\n'
                                                      '    frame = _scene_refresh_emit(memory, frame, address, 2, order)\n'
                                                      'return memory.sync_status(frame)'},
 'set_third_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                      'returns': 'ScenePresentation',
                                      'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269306, False)\n'
                                              'actual = set_third_timed_formation_orders_fields(SceneRefreshMemory(state), '
                                              'actual)\n'
                                              'return _scene_formation_legacy_projection(frame, actual)'},
 'set_third_timed_formation_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                             'returns': 'FirstDeploymentFrame',
                                             'flow': 'return set_scene_object_formation_orders_fields(memory, frame, 3)'},
 'set_uniform_conservative_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                     'returns': 'ScenePresentation',
                                     'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269294, False)\n'
                                             'actual = set_uniform_conservative_orders_fields(SceneRefreshMemory(state), '
                                             'actual)\n'
                                             'return _scene_formation_legacy_projection(frame, actual)'},
 'set_uniform_conservative_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                            'returns': 'FirstDeploymentFrame',
                                            'flow': 'return set_scene_object_formation_orders_fields(memory, frame, 0)'},
 'set_uniform_timed_formation_orders': {'signature': 'state: SceneState, frame: ScenePresentation',
                                        'returns': 'ScenePresentation',
                                        'flow': 'actual = _scene_formation_legacy_fields(state, frame, 269310, False)\n'
                                                'actual = set_uniform_timed_formation_orders_fields(SceneRefreshMemory(state), '
                                                'actual)\n'
                                                'return _scene_formation_legacy_projection(frame, actual)'},
 'set_uniform_timed_formation_orders_fields': {'signature': 'memory: SceneRefreshMemory, frame: FirstDeploymentFrame',
                                               'returns': 'FirstDeploymentFrame',
                                               'flow': 'return set_scene_object_formation_orders_fields(memory, frame, 4)'}})

DECLARATIONS.update({'_map_packet_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: int, continuation: int', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, uint(continuation, 32))\nentered = first_replace(frame, stack_cursor=stack)\nif target == 199824:\n    result = calculate_map_packet_supply_fields(state, entered)\nelif target == 199874:\n    result = apply_map_packet_supply_losses_fields(state, entered)\nelif target == 200062:\n    result = sample_map_packet_loss_factors_fields(state, entered)\nelif target == 200134:\n    result = compact_map_packet_survivors_fields(state, entered)\nelif target == 200244:\n    result = replace_map_queue_leader_fields(state, entered)\nelif target == 200316:\n    result = remove_map_queue_leader_fields(state, entered)\nelif target == 200424:\n    result = shuffle_force_turn_order_fields(state, entered)\nelif target == 33748:\n    from ..high_level_battle_ai.contexts_policy_memory import BattlePolicyMemory\n    from ..high_level_battle_ai.business_formation import first_deployment_random_fields\n    result = first_deployment_random_fields(BattlePolicyMemory(state), entered)\nelse:\n    result = execute_deployment_menu_fields(state, target, entered)\nresult = _resource_cost_frame(state, result, target)\nactual = result.stack_cursor.long()\nif actual != continuation:\n    raise MovementContinuationBoundary(actual, result, 'actual map-packet child return LONG changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}})

DECLARATIONS.update({'_map_packet_divu_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, divisor: int, instruction: int', 'returns': 'FirstDeploymentFrame', 'flow': "if (carrier, instruction) not in (('count', 199856), ('unit', 200236)):\n    raise ValueError('original map packet DIVU site required')\nuint(divisor, 16)\nif not divisor:\n    raise MovementContinuationBoundary(instruction, frame, 'original map packet DIVU zero trap')\nif frame.carrier(carrier) // divisor > 65535:\n    return frame\nreturn _movement_divu_word(state, frame, carrier, divisor, instruction)"}})

DECLARATIONS.update({'_map_packet_legacy_entry_fields': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'FirstDeploymentFrame', 'flow': 'checked_context(values, CityCommandValues, state)\nreturn first_replace(FirstDeploymentFrame.unobserved(), target_x=values.value, target_y=values.field, unit=values.member, count=values.count, distance=values.readiness_loss, offset_x=values.troop_rate, offset_y=values.force_index, choice=values.selected, roster=values.packet, candidates=values.roster, controller=values.destination, opponent=values.assignments, scratch=values.scratch, status=state.sr & 31)'}})

DECLARATIONS.update({'_map_packet_legacy_result_fields': {'signature': 'state: SceneState, values: CityCommandValues, frame: FirstDeploymentFrame', 'returns': 'CityCommandValues', 'flow': 'return replace(values, value=frame.target_x, field=frame.target_y, member=frame.unit, count=frame.count, readiness_loss=frame.distance, troop_rate=frame.offset_x, force_index=frame.offset_y, selected=frame.choice)'}})

DECLARATIONS.update({'_map_packet_lost_message_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "stack = frame.stack_cursor.advance(-2)\nvalue = state.read(4294964066, 2)\nstack.set_word(0, value)\nframe = _movement_test(state, first_replace(frame, stack_cursor=stack), value, 16)\nstack = frame.stack_cursor.advance(-2)\nvalue = state.read(4294964086, 2)\nstack.set_word(0, value)\nframe = _movement_test(state, first_replace(frame, stack_cursor=stack), value, 16)\nsaved = ('target_x', 'target_y', 'unit', 'count', 'distance', 'offset_x', 'offset_y', 'choice', 'roster', 'candidates', 'controller', 'scan', 'opponent', 'scratch', 'auxiliary')\nframe = _movement_save_longs(state, frame, saved)\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294964086), 0, low16(frame.unit))\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294964176), 0, low16(frame.distance))\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294965056), 0, 202)\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294964066), 0, 0, clear=True)\nframe = _map_packet_call_fields(state, frame, 199284, 200032)\nframe = _movement_restore_longs(state, frame, saved)\nvalue = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294964086), 0, value)\nvalue = frame.stack_cursor.word()\nframe = first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))\nreturn _settlement_store_word_fields(state, frame, state.table_at(4294964066), 0, value)"}})

DECLARATIONS.update({'_map_packet_survivor_store_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': 'frame = _settlement_write_byte_fields(state, frame, frame.scan, value=low8(frame.distance))\nreturn first_replace(frame, scan=frame.scan.advance(1))'}})

DECLARATIONS.update({'apply_map_packet_supply_losses': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = apply_map_packet_supply_losses_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'apply_map_packet_supply_losses_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 199874)\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294954952), 0, 0, clear=True)\nframe = _settlement_write_byte_fields(state, frame, state.table_at(4294954953), value=frame.roster.byte(13))\nframe = _movement_move(state, frame, 'choice', 0, 16)\nframe = first_replace(frame, candidates=state.table_at(4294952960).cursor(), controller=state.table_at(4294947328), scan=state.table_at(4294954930).cursor(), opponent=state.table_at(4294953984))\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _special_action_sub_word(state, frame, 'target_y', 1)\nwhile True:\n    frame = _map_packet_call_fields(state, frame, 200062, 199910)\n    frame = _movement_move(state, frame, 'distance', 0, 16)\n    frame = _movement_move(state, frame, 'distance', frame.roster.byte(low16(frame.target_y), 13), 8)\n    frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'offset_x', 1)\n    frame = _movement_move(state, frame, 'offset_y', frame.controller.word(low16(frame.offset_x)), 16)\n    frame = _special_action_sub_word(state, frame, 'offset_y', low16(frame.unit))\n    if not frame.status & 5:\n        frame = _settlement_store_word_fields(state, frame, frame.controller, low16(frame.offset_x), low16(frame.offset_y))\n        frame = _movement_fixed_shift_word(state, frame, 'offset_x', 1)\n        frame = _movement_move(state, frame, 'offset_y', frame.candidates.word(low16(frame.offset_x), 2), 16)\n        frame = _special_action_sub_word(state, frame, 'offset_y', low16(frame.count))\n        if frame.status & 1:\n            frame = _movement_move(state, frame, 'offset_y', 0, 16)\n        frame = _settlement_store_word_fields(state, frame, frame.candidates, low16(frame.offset_x), low16(frame.offset_y), 2)\n        frame = _movement_add_word(state, frame, 'choice', 1)\n        frame = _map_packet_survivor_store_fields(state, frame)\n    else:\n        frame = _settlement_write_byte_fields(state, frame, frame.opponent, value=255, offset=low16(frame.distance))\n        frame = _movement_move(state, frame, 'unit', frame.roster.byte(4), 8)\n        frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)\n        selected = False\n        for address in (4294964858, 4294964860, 4294964862):\n            frame = _movement_compare(state, frame, low16(frame.unit), state.read(address, 2), 16)\n            if frame.status & 4:\n                selected = True\n                break\n        if selected:\n            frame = _map_packet_lost_message_fields(state, frame)\n    counter = u16(low16(frame.target_y) - 1)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, counter))\n    if counter == 65535:\n        break\nframe = _movement_compare(state, frame, low16(frame.target_x), low16(frame.choice), 16)\nif not frame.status & 4:\n    frame = _map_packet_call_fields(state, frame, 200134, 200058)\nreturn _movement_move(state, frame, 'target_x', low16(frame.choice), 16)"}})

DECLARATIONS.update({'calculate_map_packet_supply': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = calculate_map_packet_supply_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'calculate_map_packet_supply_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 199824)\nframe = first_replace(frame, candidates=state.table_at(4294952960).cursor())\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _special_action_sub_word(state, frame, 'target_y', 1)\nframe = _movement_move_long(state, frame, 'count', 0)\nwhile True:\n    frame = _movement_move(state, frame, 'unit', 0, 16)\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_y), 13), 8)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 2)\n    frame = _movement_arithmetic_long(state, frame, 'count', frame.candidates.long(low16(frame.unit)))\n    frame = _movement_arithmetic_long(state, frame, 'count', 100)\n    counter = u16(low16(frame.target_y) - 1)\n    frame = first_replace(frame, target_y=replace_word(frame.target_y, counter))\n    if counter == 65535:\n        break\nframe = _map_packet_divu_fields(state, frame, 'count', 10, 199856)\nframe = _movement_move(state, frame, 'unit', low16(frame.count), 16)\nframe = _movement_fixed_shift_word(state, frame, 'count', 1)\nframe = _movement_add_word(state, frame, 'count', low16(frame.unit))\nreturn _movement_move_long(state, frame, 'count', frame.count & 65535)"}})

DECLARATIONS.update({'compact_map_packet_survivors': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = compact_map_packet_survivors_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'compact_map_packet_survivors_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200134)\nframe = _movement_move(state, frame, 'offset_y', low16(frame.choice), 16)\nif not frame.status & 4:\n    frame = _special_action_sub_word(state, frame, 'offset_y', 1)\n    frame = first_replace(frame, candidates=state.table_at(4294954930).cursor())\n    while True:\n        value = frame.candidates.byte()\n        frame = first_replace(frame, candidates=frame.candidates.advance(1))\n        frame = _settlement_write_byte_fields(state, frame, frame.roster, value=value, offset=low16(frame.offset_y), displacement=13)\n        counter = u16(low16(frame.offset_y) - 1)\n        frame = first_replace(frame, offset_y=replace_word(frame.offset_y, counter))\n        if counter == 65535:\n            break\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.choice))\n    frame = _map_packet_call_fields(state, frame, 200244, 200160)\n    frame = first_replace(frame, candidates=frame.roster.advance(13 + s16(low16(frame.target_x))), controller=state.table_at(u32(frame.roster.base + 13 + s16(low16(frame.choice)))))\nelse:\n    frame = _map_packet_call_fields(state, frame, 200316, 200176)\n    frame = first_replace(frame, candidates=frame.roster.advance(13 + s16(low16(frame.target_x))), controller=state.table_at(frame.roster.base))\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', frame.candidates.byte(), 8)\n    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)\n    if frame.status & 4:\n        break\n    frame = _movement_add_word(state, frame, 'target_y', 12)\n    while True:\n        value = frame.candidates.byte()\n        frame = first_replace(frame, candidates=frame.candidates.advance(1))\n        frame = _settlement_write_byte_fields(state, frame, frame.controller, value=value)\n        frame = first_replace(frame, controller=state.table_at(u32(frame.controller.base + 1)))\n        counter = u16(low16(frame.target_y) - 1)\n        frame = first_replace(frame, target_y=replace_word(frame.target_y, counter))\n        if counter == 65535:\n            break\nframe = _settlement_write_byte_fields(state, frame, frame.controller, value=0, clear=True)\nframe = _movement_test(state, frame, low16(frame.choice), 16)\nif frame.status & 4:\n    return frame\nframe = first_replace(frame, candidates=state.table_at(4294951936).cursor())\nframe = _movement_move(state, frame, 'offset_y', low16(frame.choice), 16)\nframe = _special_action_sub_word(state, frame, 'offset_y', 1)\nframe = _movement_move_long(state, frame, 'unit', 0)\nframe = _movement_move(state, frame, 'count', 0, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.offset_y), 13), 8)\n    frame, value = _movement_binary_flags(state, frame, low8(frame.unit), frame.candidates.byte(low16(frame.count)), 8)\n    frame = first_replace(frame, unit=replace_byte(frame.unit, value))\n    counter = u16(low16(frame.offset_y) - 1)\n    frame = first_replace(frame, offset_y=replace_word(frame.offset_y, counter))\n    if counter == 65535:\n        break\nframe = _map_packet_divu_fields(state, frame, 'unit', low16(frame.choice), 200236)\nreturn _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=3)"}})

DECLARATIONS.update({'deduct_all_map_packet_supply': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = deduct_all_map_packet_supply_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'deduct_all_map_packet_supply_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 199738)\nframe = first_replace(frame, roster=state.table_at(4294938624).cursor())\nwhile True:\n    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    if frame.status & 4:\n        return frame\n    frame = _map_packet_call_fields(state, frame, 199824, 199756)\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(9), 8)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 8)\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(10), 8)\n    frame = _movement_shift_long(state, frame, 'unit')\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(11), 8)\n    frame = _movement_shift_long(state, frame, 'unit')\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(12), 8)\n    frame = _movement_arithmetic_long(state, frame, 'unit', frame.count, True)\n    if frame.status & 1:\n        frame = _map_packet_call_fields(state, frame, 199874, 199788)\n        frame = _movement_test(state, frame, low16(frame.target_x), 16)\n        if frame.status & 4:\n            continue\n        frame = _movement_move_long(state, frame, 'unit', 0)\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=12)\n    frame = _movement_shift_long(state, frame, 'unit', True)\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=11)\n    frame = _movement_shift_long(state, frame, 'unit', True)\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=10)\n    frame = _movement_fixed_shift_word(state, frame, 'unit', 8, True)\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=9)\n    frame = first_replace(frame, roster=frame.roster.advance(13 + s16(low16(frame.target_x))))"}})

DECLARATIONS.update({'initialize_force_turn_order': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = initialize_force_turn_order_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'initialize_force_turn_order_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200372)\nframe = first_replace(frame, roster=state.table_at(4294965012).cursor(), candidates=state.table_at(200408).cursor())\nframe = _movement_move(state, frame, 'target_x', 15, 16)\nwhile True:\n    value = frame.candidates.byte()\n    frame = first_replace(frame, candidates=frame.candidates.advance(1))\n    frame = _settlement_write_byte_fields(state, frame, frame.roster, value=value)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    counter = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, counter))\n    if counter == 65535:\n        break\nframe = _map_packet_call_fields(state, frame, 200424, 200396)\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294965028), 0, 0, clear=True)\nreturn _settlement_store_word_fields(state, frame, state.table_at(4294964736), 0, 176)"}})

DECLARATIONS.update({'recover_idle_officer_readiness': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = recover_idle_officer_readiness_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'recover_idle_officer_readiness_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200532)\nframe = first_replace(frame, roster=state.table_at(4294953984).cursor(), scan=state.table_at(4294947328).cursor(), opponent=state.table_at(4294946816), scratch=state.table_at(4294961720))\nframe = _movement_move(state, frame, 'target_x', 255, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\n    frame = _movement_compare(state, frame, low8(frame.target_y), 40, 8)\n    if frame.status & 5:\n        frame = _movement_test(state, frame, frame.scratch.byte(low16(frame.target_y)), 8)\n        if frame.status & 4:\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n            frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n            frame = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_y)), 16)\n            frame = _movement_multiply_word(state, frame, 'unit', 15)\n            frame = _movement_divu_word(state, frame, 'unit', 100, 200586)\n            frame = _movement_move(state, frame, 'count', frame.scan.word(low16(frame.target_y)), 16)\n            frame = _movement_add_word(state, frame, 'count', low16(frame.unit))\n            frame = _movement_compare(state, frame, low16(frame.count), frame.opponent.word(low16(frame.target_y)), 16)\n            if not frame.status & 5:\n                frame = _movement_move(state, frame, 'count', frame.opponent.word(low16(frame.target_y)), 16)\n            frame = _settlement_store_word_fields(state, frame, frame.scan, low16(frame.target_y), low16(frame.count))\n    counter = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, counter))\n    if counter == 65535:\n        return frame"}})

DECLARATIONS.update({'remove_map_queue_leader': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = remove_map_queue_leader_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'remove_map_queue_leader_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200316)\nsaved = ('target_x', 'target_y', 'roster', 'candidates')\nframe = _movement_save_longs(state, frame, saved)\nframe = first_replace(frame, roster=state.table_at(16726450).cursor())\nframe = _movement_move(state, frame, 'target_x', state.read(4294954952, 2), 16)\nwhile True:\n    frame = _movement_test(state, frame, frame.roster.byte(), 8)\n    if frame.status & 4:\n        break\n    frame = _movement_compare(state, frame, low8(frame.target_x), frame.roster.byte(1), 8)\n    if frame.status & 4:\n        while True:\n            value = frame.roster.byte(2)\n            frame = _settlement_write_byte_fields(state, frame, frame.roster, value=value)\n            if frame.status & 4:\n                break\n            frame = _settlement_write_byte_fields(state, frame, frame.roster, value=frame.roster.byte(3), offset=1)\n            frame = first_replace(frame, roster=frame.roster.advance(2))\n        break\n    frame = first_replace(frame, roster=frame.roster.advance(2))\nreturn _movement_restore_longs(state, frame, saved)"}})

DECLARATIONS.update({'replace_map_queue_leader': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = replace_map_queue_leader_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'replace_map_queue_leader_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200244)\nsaved = ('target_x', 'target_y', 'roster')\nframe = _movement_save_longs(state, frame, saved)\nframe = _movement_move(state, frame, 'target_x', 0, 16)\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(13), 8)\nframe = _movement_move(state, frame, 'target_y', state.read(4294954952, 2), 16)\nframe = first_replace(frame, roster=state.table_at(16726450).cursor())\nwhile True:\n    frame = _movement_test(state, frame, frame.roster.byte(), 8)\n    if frame.status & 4:\n        break\n    frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(1), 8)\n    if frame.status & 4:\n        frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.target_x), offset=1)\n        frame = first_replace(frame, roster=state.table_at(16723968).cursor())\n        while True:\n            frame = first_replace(frame, roster=frame.roster.advance(1))\n            frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(), 8)\n            if frame.status & 4:\n                break\n            frame = first_replace(frame, roster=frame.roster.advance(1))\n            while True:\n                value = frame.roster.byte()\n                frame = first_replace(frame, roster=frame.roster.advance(1))\n                frame = _movement_test(state, frame, value, 8)\n                if frame.status & 4:\n                    break\n        frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.target_x))\n        break\n    frame = first_replace(frame, roster=frame.roster.advance(2))\nreturn _movement_restore_longs(state, frame, saved)"}})

DECLARATIONS.update({'sample_map_packet_loss_factors': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = sample_map_packet_loss_factors_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'sample_map_packet_loss_factors_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200062)\nframe = _movement_save_longs(state, frame, ('target_x', 'target_y'))\nframe = _map_packet_call_fields(state, frame, 33748, 200072)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y)\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_add_word(state, frame, 'target_x', 5)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\nframe = _map_packet_call_fields(state, frame, 33748, 200098)\nframe = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\nframe = _movement_move_long(state, frame, 'target_y', frame.target_x)\nframe = _movement_shift_long(state, frame, 'target_x')\nframe = _special_action_shift_long(state, frame, 'target_x', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y, True)\nframe = _special_action_shift_long(state, frame, 'target_y', 1)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y, True)\nframe = _special_action_shift_long(state, frame, 'target_y', 2)\nframe = _movement_arithmetic_long(state, frame, 'target_x', frame.target_y, True)\nframe = _special_action_swap(state, frame, 'target_x')\nframe = _movement_add_word(state, frame, 'target_x', 500)\nframe = _movement_move(state, frame, 'count', low16(frame.target_x), 16)\nreturn _movement_restore_longs(state, frame, ('target_x', 'target_y'))"}})

DECLARATIONS.update({'select_next_force_turn': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = select_next_force_turn_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'select_next_force_turn_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200486)\nframe = _movement_move(state, frame, 'target_x', state.read(4294965028, 2), 16)\nframe = first_replace(frame, roster=state.table_at(4294965012).cursor(), candidates=state.table_at(4294960704).cursor())\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\n    value = low8(frame.target_y)\n    frame = _movement_move(state, frame, 'target_y', u16(value - 256 if value & 128 else value), 16)\n    if frame.status & 8:\n        break\n    frame = _movement_add_word(state, frame, 'target_x', 1)\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n    frame = _movement_test(state, frame, frame.candidates.word(low16(frame.target_y)), 16)\n    if frame.status & 8:\n        continue\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\n    break\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294965028), 0, low16(frame.target_x))\nframe = _settlement_store_word_fields(state, frame, state.table_at(4294964086), 0, low16(frame.target_y))\nreturn _settlement_store_word_fields(state, frame, state.table_at(4294964068), 0, 0, clear=True)"}})

DECLARATIONS.update({'shuffle_force_turn_order': {'signature': 'state: SceneState, values: CityCommandValues', 'returns': 'CityCommandValues', 'flow': 'frame = shuffle_force_turn_order_fields(state, _map_packet_legacy_entry_fields(state, values))\nreturn _map_packet_legacy_result_fields(state, values, frame)'}})

DECLARATIONS.update({'shuffle_force_turn_order_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 200424)\nframe = first_replace(frame, roster=state.table_at(4294965012).cursor())\nframe = _movement_move(state, frame, 'choice', 15, 16)\nwhile True:\n    frame = _map_packet_call_fields(state, frame, 33748, 200438)\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964764, 2), 16)\n    frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\n    frame = _movement_move(state, frame, 'target_y', state.read(4294964764, 2), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'target_y', 8, True)\n    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)\n    frame = _movement_move(state, frame, 'unit', frame.roster.byte(low16(frame.target_x)), 8)\n    if not frame.status & 8:\n        frame = _movement_move(state, frame, 'count', frame.roster.byte(low16(frame.target_y)), 8)\n        if not frame.status & 8:\n            frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.count), offset=low16(frame.target_x))\n            frame = _settlement_write_byte_fields(state, frame, frame.roster, value=low8(frame.unit), offset=low16(frame.target_y))\n    counter = u16(low16(frame.choice) - 1)\n    frame = first_replace(frame, choice=replace_word(frame.choice, counter))\n    if counter == 65535:\n        return frame"}})

APPROVED.setdefault('business_movement_support',set()).update(('_movement_move', '_movement_move_long', '_movement_test', '_movement_test_long', '_movement_compare', '_movement_binary_flags', '_movement_arithmetic_long', '_movement_fixed_shift_word', '_movement_shift_long', '_movement_add_word', '_movement_multiply_word', '_movement_divu_word', '_movement_save_longs', '_movement_restore_longs', 'MovementContinuationBoundary'))

APPROVED.setdefault('business_city',set()).update(('_resource_cost_frame', '_settlement_store_word_fields', '_settlement_write_byte_fields', '_special_action_sub_word', '_special_action_shift_long', '_special_action_swap', 'execute_deployment_menu_fields'))

APPROVED.setdefault('contexts_policy_memory',set()).update(('BattlePolicyMemory',))

APPROVED.setdefault('business_formation',set()).update(('first_deployment_random_fields',))

# Explicit cross-family D41 imports and one editable readiness percentage.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(('_resource_cost_frame', '_settlement_store_word_fields', '_settlement_write_byte_fields', '_special_action_sub_word', '_special_action_shift_long', '_special_action_swap', 'execute_deployment_menu_fields'))
APPROVED.setdefault((2, 'high_level_battle_ai.contexts_policy_memory'),set()).update(('BattlePolicyMemory',))
APPROVED.setdefault((2, 'high_level_battle_ai.business_formation'),set()).update(('first_deployment_random_fields',))
DECLARATIONS.update({'recover_idle_officer_readiness_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "recovery_percent = 15\nframe = _resource_cost_frame(state, frame, 200532)\nframe = first_replace(frame, roster=state.table_at(4294953984).cursor(), scan=state.table_at(4294947328).cursor(), opponent=state.table_at(4294946816), scratch=state.table_at(4294961720))\nframe = _movement_move(state, frame, 'target_x', 255, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), 8)\n    frame = _movement_compare(state, frame, low8(frame.target_y), 40, 8)\n    if frame.status & 5:\n        frame = _movement_test(state, frame, frame.scratch.byte(low16(frame.target_y)), 8)\n        if frame.status & 4:\n            frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n            frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n            frame = _movement_move(state, frame, 'unit', frame.opponent.word(low16(frame.target_y)), 16)\n            frame = _movement_multiply_word(state, frame, 'unit', recovery_percent)\n            frame = _movement_divu_word(state, frame, 'unit', 100, 200586)\n            frame = _movement_move(state, frame, 'count', frame.scan.word(low16(frame.target_y)), 16)\n            frame = _movement_add_word(state, frame, 'count', low16(frame.unit))\n            frame = _movement_compare(state, frame, low16(frame.count), frame.opponent.word(low16(frame.target_y)), 16)\n            if not frame.status & 5:\n                frame = _movement_move(state, frame, 'count', frame.opponent.word(low16(frame.target_y)), 16)\n            frame = _settlement_store_word_fields(state, frame, frame.scan, low16(frame.target_y), low16(frame.count))\n    counter = u16(low16(frame.target_x) - 1)\n    frame = first_replace(frame, target_x=replace_word(frame.target_x, counter))\n    if counter == 65535:\n        return frame", 'slots': {15: ('idle_recovery_percent', 0, 65535)}}})

# D49 exact imports and whole-function declarations; ordinary lowerers unchanged.
APPROVED.setdefault('business_gameplay',set()).update(('_map_presentation_arithmetic_fields', '_map_presentation_db_fields'))
DECLARATIONS.update({'_assignment_location_carry_fields': {'flow': 'status = frame.status | 1 if carry else frame.status & 30\n'
                                               'state.sr = state.sr & 65504 | status\n'
                                               'return first_replace(frame, status=status)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame, carry: bool'},
 '_assignment_location_store_fields': {'flow': "frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                               "frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 1), 8)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)\n"
                                               'frame = _settlement_store_word_fields(state, frame, state.table_at(4294964062), 0, '
                                               'low16(frame.target_x))\n'
                                               "frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                               "frame = _movement_move(state, frame, 'target_x', frame.roster.byte(0, 2), 8)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 4)\n"
                                               'frame = _settlement_store_word_fields(state, frame, state.table_at(4294964064), 0, '
                                               'low16(frame.target_x))\n'
                                               'return _assignment_location_carry_fields(state, frame, False)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'locate_selected_force_packet': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                          'returned = locate_selected_force_packet_fields(state, entered)\n'
                                          'result = _map_packet_legacy_result_fields(state, values, returned)\n'
                                          'return replace(result, packet=returned.roster.cursor())',
                                  'returns': 'CityCommandValues',
                                  'signature': 'state: SceneState, values: CityCommandValues'},
 'locate_selected_force_packet_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 199566)\n'
                                                 "frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                                 "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n"
                                                 'frame = first_replace(frame, roster=state.table_at(4294960704).cursor())\n'
                                                 "frame = _movement_move(state, frame, 'target_x', "
                                                 'frame.roster.word(low16(frame.target_x)), 16)\n'
                                                 'frame = first_replace(frame, roster=state.table_at(4294942800).cursor())\n'
                                                 'frame = _movement_test(state, frame, frame.roster.byte(low16(frame.target_x)), 8)\n'
                                                 'selected_header = not bool(frame.status & 4)\n'
                                                 'frame = first_replace(frame, roster=state.table_at(4294938624).cursor())\n'
                                                 'if selected_header:\n'
                                                 "    frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                                 '    while True:\n'
                                                 "        frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\n"
                                                 "        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, "
                                                 '16)\n'
                                                 '        if frame.status & 4:\n'
                                                 '            return _assignment_location_carry_fields(state, frame, True)\n'
                                                 '        frame = _movement_compare(state, frame, low8(frame.target_x), '
                                                 'frame.roster.byte(0, 4), 8)\n'
                                                 '        if frame.status & 4:\n'
                                                 '            return _assignment_location_store_fields(state, frame)\n'
                                                 '        frame = first_replace(frame, roster=frame.roster.advance(13 + '
                                                 's16(low16(frame.target_y))))\n'
                                                 'while True:\n'
                                                 "    frame = _movement_move(state, frame, 'unit', frame.roster.byte(), 8)\n"
                                                 "    frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 15, 16)\n"
                                                 '    if frame.status & 4:\n'
                                                 '        return _assignment_location_carry_fields(state, frame, True)\n'
                                                 '    frame = _movement_compare(state, frame, low8(frame.target_y), frame.roster.byte(0, '
                                                 '4), 8)\n'
                                                 '    if frame.status & 4:\n'
                                                 "        frame = _movement_move(state, frame, 'count', low16(frame.unit), 16)\n"
                                                 "        frame = _map_presentation_arithmetic_fields(state, frame, 'count', 1, True)\n"
                                                 '        while True:\n'
                                                 '            frame = _movement_compare(state, frame, low8(frame.target_x), '
                                                 'frame.roster.byte(low16(frame.count), 13), 8)\n'
                                                 '            if frame.status & 4:\n'
                                                 '                return _assignment_location_store_fields(state, frame)\n'
                                                 "            frame, again = _map_presentation_db_fields(frame, 'count')\n"
                                                 '            if not again:\n'
                                                 '                break\n'
                                                 '    frame = first_replace(frame, roster=frame.roster.advance(13 + '
                                                 's16(low16(frame.unit))))',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'locate_selected_ruler_city': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                        'returned = locate_selected_ruler_city_fields(state, entered)\n'
                                        'result = _map_packet_legacy_result_fields(state, values, returned)\n'
                                        'return replace(result, scratch=state.table_at(returned.roster.base))',
                                'returns': 'CityCommandValues',
                                'signature': 'state: SceneState, values: CityCommandValues'},
 'locate_selected_ruler_city_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 199164)\n'
                                               'frame = first_replace(frame, roster=state.table_at(4294960704).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n"
                                               "frame = _movement_move(state, frame, 'target_x', frame.roster.word(low16(frame.target_x)), "
                                               '16)\n'
                                               'frame = first_replace(frame, roster=state.table_at(4294953984).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x)), "
                                               '8)\n'
                                               "frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 63, 16)\n"
                                               'frame = _movement_compare(state, frame, low16(frame.target_y), 40, 16)\n'
                                               'if frame.status & 5:\n'
                                               "    frame = _movement_fixed_shift_word(state, frame, 'target_y', 2)\n"
                                               '    frame = first_replace(frame, roster=state.table_at(871110).cursor())\n'
                                               '    frame = _settlement_store_word_fields(state, frame, state.table_at(4294964062), 0, '
                                               'frame.roster.word(low16(frame.target_y), 2))\n'
                                               '    frame = _settlement_store_word_fields(state, frame, state.table_at(4294964064), 0, '
                                               'frame.roster.word(low16(frame.target_y)))\n'
                                               '    return _assignment_location_carry_fields(state, frame, False)\n'
                                               'frame = first_replace(frame, roster=state.table_at(4294964264).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_x', 39, 16)\n"
                                               "frame = _movement_move(state, frame, 'target_y', state.read(4294964086, 2), 16)\n"
                                               'while True:\n'
                                               '    frame = _movement_compare(state, frame, low8(frame.target_y), '
                                               'frame.roster.byte(low16(frame.target_x)), 8)\n'
                                               '    if frame.status & 4:\n'
                                               '        frame = first_replace(frame, roster=state.table_at(871114).cursor())\n'
                                               "        frame = _movement_fixed_shift_word(state, frame, 'target_x', 2)\n"
                                               '        frame = _settlement_store_word_fields(state, frame, state.table_at(4294964062), 0, '
                                               'frame.roster.word(low16(frame.target_x), 2))\n'
                                               '        frame = _settlement_store_word_fields(state, frame, state.table_at(4294964064), 0, '
                                               'frame.roster.word(low16(frame.target_x)))\n'
                                               '        return _assignment_location_carry_fields(state, frame, False)\n'
                                               "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                               '    if not again:\n'
                                               '        return _assignment_location_carry_fields(state, frame, True)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D50 precise current source admission/DECL; ordinary lowerers unchanged.
APPROVED.setdefault('business_gameplay',set()).update(('_map_presentation_bit_fields', '_resource_cost_frame', '_setup_asl_word_fields', '_setup_call_fields', '_setup_change_word_fields', '_setup_compare_memory_fields', '_setup_coordinate_high_byte_fields', '_setup_legacy_entry_fields', '_setup_legacy_result_fields', '_setup_write_fields', 'settle_city_projects_and_refresh_map_fields'))
APPROVED.setdefault((2, 'high_level_gameplay_flow.contexts_services'),set()).update(('SceneRefreshMemory',))
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('_glyph_shift_long_fields',))
APPROVED.setdefault('business_highbank',set()).update(('advance_officer_growth_levels_fields',))
APPROVED.setdefault((2, 'high_level_remaining_flows.business_city'),set()).update(('_city_encounter_shift_word_fields',))
DECLARATIONS.pop('_cycle_player_choice',None)
DECLARATIONS.pop('_setup_transfer_control',None)
DECLARATIONS.pop('_run_configuration_choices',None)
DECLARATIONS.update({'_city_assignment_child_fields': {'flow': "children = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields}\nif target == 201486:\n    from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields\n    return wait_command_intro_fields(state, frame)\nif target in children:\n    return children[target](state, frame)\nif target == 33748:\n    return first_deployment_random_fields(BattlePolicyMemory(state), frame)\nif target == 418532:\n    return advance_officer_growth_levels_fields(state, frame)\nif target == 71950:\n    from .business_gameplay import settle_city_projects_and_refresh_map_fields\n    return settle_city_projects_and_refresh_map_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long'},
 '_city_assignment_vector_fields': {'flow': 'if (base, table, continuation) not in ((200716, 200710, 200662), (201464, 201432, 201430)):\n'
                                            "    raise ValueError('actual assignment dynamic table role required')\n"
                                            "frame = _movement_move(state, frame, 'target_x', "
                                            'state.table_at(table).word(low16(frame.target_x)), 16)\n'
                                            'return _setup_call_fields(state, frame, u32(base + s16(low16(frame.target_x))), continuation)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame, base: Long, table: Long, continuation: '
                                                 'Long'},
 '_controller_setup_begin_fields': {'flow': 'if type(main_menu) is not bool:\n'
                                            "    raise ValueError('actual setup phase selector required')\n"
                                            'frame = _controller_setup_interrupt_status_fields(state, frame, 9984)\n'
                                            "frame = _movement_move(state, frame, 'target_x', state.read(4294964742, 2), 16)\n"
                                            "frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 191, 8)\n"
                                            'frame = _setup_write_fields(state, frame, 12582916, low16(frame.target_x))\n'
                                            'frame = _setup_write_fields(state, frame, 4294964754, 0, clear=True)\n'
                                            'for target, token in ((26830, 174826 if main_menu else 198092), (26662, 174832 if main_menu '
                                            'else 198098)):\n'
                                            '    frame = _setup_call_fields(state, frame, target, token)\n'
                                            'frame = _setup_write_fields(state, frame, 16740406, 0 if main_menu else 1, clear=main_menu)\n'
                                            'frame = _setup_call_fields(state, frame, 176478, 174842 if main_menu else 198110)\n'
                                            'counters = (16740386, 16740416, 16740418, 16740414) if main_menu else (16740408, 16740410, '
                                            '16740414)\n'
                                            'for address in counters:\n'
                                            '    frame = _setup_write_fields(state, frame, address, 0, clear=True)\n'
                                            'frame = _setup_call_fields(state, frame, 176056 if main_menu else 198382, 174872 if main_menu '
                                            'else 198132)\n'
                                            'frame = _controller_setup_fill_descriptor_fields(state, frame, 41472 if main_menu else 41152, '
                                            '174758 if main_menu else 174736)\n'
                                            'return _controller_setup_interrupt_status_fields(state, frame, 9472)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame, main_menu: bool'},
 '_controller_setup_byte_shift_fields': {'flow': "if (carrier, right) not in (('target_y', False), ('unit', True)):\n"
                                                 "    raise ValueError('actual controller BYTE shift role required')\n"
                                                 'original = frame.carrier(carrier)\n'
                                                 'value = low8(original)\n'
                                                 'if right:\n'
                                                 '    frame = first_replace(frame, **{carrier: value})\n'
                                                 '    frame = _movement_fixed_shift_word(state, frame, carrier, 1, True)\n'
                                                 '    status = frame.status & 17 | (8 if value >> 1 & 128 else 0) | (4 if value >> 1 == 0 '
                                                 'else 0)\n'
                                                 '    state.sr = state.sr & 65504 | status\n'
                                                 '    return first_replace(frame, status=status, **{carrier: replace_byte(original, value '
                                                 '>> 1)})\n'
                                                 'frame, value = _movement_binary_flags(state, frame, value, value, 8)\n'
                                                 'return first_replace(frame, **{carrier: replace_byte(original, value)})',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, right: bool'},
 '_controller_setup_child_fields': {'flow': 'children = {196744: refresh_setup_option_labels_fields, 197292: '
                                            'render_packed_sprite_position_fields, 197314: render_selected_setup_options_fields, 197764: '
                                            'render_setup_player_position_fields, 197788: cycle_second_player_choice_fields, 197918: '
                                            'cycle_third_player_choice_fields, 198064: run_controller_setup_and_configuration_fields, '
                                            '198294: update_connected_controller_option_fields, 198382: '
                                            'advance_controller_setup_reveal_fields, 198426: advance_controller_setup_dismissal_fields, '
                                            '198466: read_controller_identity_fields, 198510: commit_setup_options_fields}\n'
                                            'if target in children:\n'
                                            '    return children[target](state, frame)\n'
                                            'return _city_assignment_child_fields(state, frame, target)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long'},
 '_controller_setup_cycle_player_fields': {'flow': "if type(third) is not bool:\n    raise ValueError('actual second/third player role required')\nfor address in (16740408, 16740410):\n    frame = _setup_compare_memory_fields(state, frame, address, 16)\n    if frame.status & 1:\n        return frame\nframe = _map_presentation_bit_fields(state, frame, state.read(4294964741, 1), 4)\ndecrease = not bool(frame.status & 4)\nadjust = decrease\nif not decrease:\n    frame = _map_presentation_bit_fields(state, frame, state.read(4294964741, 1), 8)\n    adjust = not bool(frame.status & 4)\nwhile True:\n    if adjust:\n        if decrease:\n            frame = _movement_test(state, frame, low16(frame.offset_x), 16)\n            if frame.status & 4:\n                frame = _movement_move_long(state, frame, 'offset_x', 2)\n                frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n                if not frame.status & 4:\n                    frame = _movement_move_long(state, frame, 'offset_x', 6)\n            else:\n                frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', 1, True)\n        else:\n            frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n            limit = 6 if frame.status & 1 else 2\n            frame = _movement_compare(state, frame, low16(frame.offset_x), limit, 16)\n            frame = _movement_move(state, frame, 'offset_x', 0, 16) if frame.status & 4 else _map_presentation_arithmetic_fields(state, frame, 'offset_x', 1)\n    frame = _movement_compare(state, frame, low16(frame.offset_x), state.read(16740396, 2), 16)\n    if frame.status & 4:\n        adjust = True\n        continue\n    if third:\n        frame = _movement_compare(state, frame, low16(frame.offset_x), state.read(16740398, 2), 16)\n        if frame.status & 4:\n            adjust = True\n            continue\n    return frame",
                                           'returns': 'FirstDeploymentFrame',
                                           'signature': 'state: SceneState, frame: FirstDeploymentFrame, third: bool'},
 '_controller_setup_fill_descriptor_fields': {'flow': 'if (descriptor, handler) not in ((41152, 174736), (41472, 174758), (41408, '
                                                      '174782)):\n'
                                                      "    raise ValueError('actual controller/setup IRQ descriptor required')\n"
                                                      'frame = _setup_write_fields(state, frame, 12582916, 36610)\n'
                                                      'frame = _setup_write_fields(state, frame, 12582916, 1610612738, 4)\n'
                                                      'frame = first_replace(frame, scratch=state.table_at(12582912))\n'
                                                      "frame = _movement_move(state, frame, 'offset_y', 13107, 16)\n"
                                                      "frame = _movement_move(state, frame, 'choice', 3455, 16)\n"
                                                      'while True:\n'
                                                      '    frame = _setup_write_fields(state, frame, frame.scratch.base, '
                                                      'low16(frame.offset_y))\n'
                                                      "    frame, again = _map_presentation_db_fields(frame, 'choice')\n"
                                                      '    if not again:\n'
                                                      '        break\n'
                                                      'for address, value, width in ((16740364, descriptor, 2), (16740366, handler, 4), '
                                                      '(16740372, 3, 2), (16740374, 1, 2)):\n'
                                                      '    frame = _setup_write_fields(state, frame, address, value, width)\n'
                                                      'return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame, descriptor: Word, handler: '
                                                           'Long'},
 '_controller_setup_interrupt_status_fields': {'flow': 'if sr not in (9984, 9472):\n'
                                                       "    raise ValueError('original setup full SR required')\n"
                                                       'state.sr = sr\n'
                                                       'return first_replace(frame, status=sr & 31)',
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame, sr: Word'},
 '_controller_setup_last_button_fields': {'flow': 'if type(previous) is not bool:\n'
                                                  "    raise ValueError('actual setup navigation role required')\n"
                                                  "frame = _movement_move_long(state, frame, 'target_x', 5)\n"
                                                  'if not previous:\n'
                                                  "    frame = _movement_move_long(state, frame, 'target_y', 4)\n"
                                                  'frame = _movement_test(state, frame, state.read(16740404, 2), 16)\n'
                                                  'if frame.status & 4:\n'
                                                  '    return frame\n'
                                                  "frame = _movement_move_long(state, frame, 'target_x', 6)\n"
                                                  'if not previous:\n'
                                                  "    frame = _movement_move_long(state, frame, 'target_y', 5)\n"
                                                  'frame = _setup_compare_memory_fields(state, frame, 16740404, 1)\n'
                                                  'if frame.status & 4:\n'
                                                  '    return frame\n'
                                                  "frame = _movement_move_long(state, frame, 'target_x', 7)\n"
                                                  "return frame if previous else _movement_move_long(state, frame, 'target_y', 6)",
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame, previous: bool=False'},
 '_controller_setup_main_iteration_fields': {'flow': "frame = _setup_call_fields(state, frame, 176056, 174966)\nframe = _setup_call_fields(state, frame, 176102, 174972)\nframe = _movement_test(state, frame, state.read(16740414, 2), 16)\nif not frame.status & 4:\n    frame = _setup_compare_memory_fields(state, frame, 16740418, 16)\n    return (frame, not bool(frame.status & 1))\nfor target, token in ((197314, 174988), (175450, 174994), (175496, 175000), (175544, 175006), (175592, 175012), (175640, 175018), (196744, 175024)):\n    frame = _setup_call_fields(state, frame, target, token)\nframe = _movement_test(state, frame, state.read(16740404, 2), 16)\ncopy_player = False\nif not frame.status & 4:\n    frame = _setup_compare_memory_fields(state, frame, 16740404, 1)\n    if frame.status & 4:\n        frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n        copy_player = bool(frame.status & 4)\n    else:\n        frame = _setup_compare_memory_fields(state, frame, 16740386, 6)\n        copy_player = bool(frame.status & 4)\n        if not copy_player:\n            frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n            copy_player = bool(frame.status & 4)\nif copy_player:\n    frame = _setup_write_fields(state, frame, 4294964739, state.read(4294964741, 1), 1)\nframe = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 32)\ncheck_exit = False\nif not frame.status & 4:\n    frame = _movement_move(state, frame, 'target_x', 172, 8)\n    frame = _setup_call_fields(state, frame, 32906, 175112)\n    frame = _controller_setup_last_button_fields(state, frame)\n    frame = _movement_compare(state, frame, frame.target_x & 65535, state.read(16740386, 2), 16)\n    if frame.status & 4:\n        frame = _setup_write_fields(state, frame, 16740414, 1)\n        check_exit = True\n    else:\n        frame = _movement_compare(state, frame, frame.target_y & 65535, state.read(16740386, 2), 16)\n        if frame.status & 4:\n            frame = _controller_setup_interrupt_status_fields(state, frame, 9984)\n            frame = _controller_setup_fill_descriptor_fields(state, frame, 41408, 174782)\n            frame = _controller_setup_interrupt_status_fields(state, frame, 9472)\n        frame = _setup_change_word_fields(state, frame, 16740386, 1)\nelse:\n    frame = _map_presentation_bit_fields(state, frame, state.read(4294964739, 1), 16)\n    if not frame.status & 4:\n        frame = _controller_setup_last_button_fields(state, frame, True)\n        frame = _movement_compare(state, frame, low16(frame.target_x), state.read(16740386, 2), 16)\n        if frame.status & 4:\n            frame = _setup_write_fields(state, frame, 16740386, 0, clear=True)\n            frame = _controller_setup_interrupt_status_fields(state, frame, 9984)\n            frame = _controller_setup_fill_descriptor_fields(state, frame, 41472, 174758)\n            frame = _controller_setup_interrupt_status_fields(state, frame, 9472)\n        else:\n            frame = _movement_test(state, frame, state.read(16740386, 2), 16)\n            if not frame.status & 4:\n                frame = _setup_change_word_fields(state, frame, 16740386, 1, True)\nif not check_exit:\n    frame = _movement_move(state, frame, 'target_x', state.read(4294964739, 1), 8)\n    frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 128, 8)\n    if not frame.status & 4:\n        frame = _setup_write_fields(state, frame, 16740414, 1)\nframe = _setup_compare_memory_fields(state, frame, 16740418, 16)\nreturn (frame, not bool(frame.status & 1))",
                                             'returns': 'tuple',
                                             'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 '_controller_setup_option_sprite_fields': {'flow': 'roles = ((0, 16740390, 197718, 176406, 197360), (1, 16740388, 197724, 176420, '
                                                    '197408), (2, 16740392, 197730, 176420, 197456), (3, 16740394, 197734, 176420, '
                                                    '197504))\n'
                                                    'if (option, value_address, coordinate_table, sprite, continuation) not in roles:\n'
                                                    "    raise ValueError('closed setup option sprite roles required')\n"
                                                    'frame, visible = _controller_setup_visible_fields(state, frame, option, option == 0)\n'
                                                    'if not visible:\n'
                                                    '    return frame\n'
                                                    "frame = _movement_move(state, frame, 'target_y', state.read(value_address, 2), 16)\n"
                                                    "frame = _setup_asl_word_fields(state, frame, 'target_y', 1)\n"
                                                    'frame = first_replace(frame, roster=state.table_at(coordinate_table).cursor())\n'
                                                    "frame = _movement_move(state, frame, 'target_x', "
                                                    'frame.roster.word(low16(frame.target_y)), 16)\n'
                                                    'frame = first_replace(frame, roster=state.table_at(sprite).cursor())\n'
                                                    'return _setup_call_fields(state, frame, 197292, continuation)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame, option: int, value_address: '
                                                         'Long, coordinate_table: Long, sprite: Long, continuation: Long'},
 '_controller_setup_palette_fields': {'flow': 'if (counter, continuation, dismiss) not in ((16740408, 198418, False), (16740410, 198458, '
                                              'True)):\n'
                                              "    raise ValueError('closed controller palette roles required')\n"
                                              'frame = _setup_compare_memory_fields(state, frame, counter, 16)\n'
                                              'if not frame.status & 1:\n'
                                              '    return frame\n'
                                              'if dismiss:\n'
                                              "    frame = _movement_move(state, frame, 'target_x', state.read(counter, 2), 16)\n"
                                              'else:\n'
                                              "    frame = _movement_move(state, frame, 'target_x', 15, 16)\n"
                                              "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', "
                                              'state.read(counter, 2), True)\n'
                                              "frame = _movement_move(state, frame, 'target_y', 64, 16)\n"
                                              'frame = first_replace(frame, roster=state.table_at(177262).cursor())\n'
                                              'frame = _setup_call_fields(state, frame, 56998, continuation)\n'
                                              'return _setup_change_word_fields(state, frame, counter, 1)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame, counter: Long, continuation: Long, '
                                                   'dismiss: bool'},
 '_controller_setup_visible_fields': {'flow': 'frame = _movement_test(state, frame, state.read(16740386, 2), 16) if first else '
                                              '_setup_compare_memory_fields(state, frame, 16740386, option)\n'
                                              'if not frame.status & 4:\n'
                                              '    return (frame, True)\n'
                                              'frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 8)\n'
                                              'return (frame, bool(frame.status & 4))',
                                      'returns': 'tuple',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame, option: int, first: bool=False'},
 '_controller_setup_wait_irq_fields': {'flow': 'if poll not in (198216, 174956):\n'
                                               "    raise ValueError('actual setup IRQ poll required')\n"
                                               'frame = _setup_write_fields(state, frame, 4294964754, 2048)\n'
                                               'frame = _movement_test(state, frame, state.read(4294964754, 1), 8)\n'
                                               'if not frame.status & 4:\n'
                                               "    raise MovementContinuationBoundary(poll, frame, 'original setup poll requires real "
                                               "asynchronous IRQ RAM progress')\n"
                                               'return frame',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame, poll: Long'},
 'advance_controller_setup_dismissal': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                                'returned = advance_controller_setup_dismissal_fields(state, entered)\n'
                                                'return _setup_legacy_result_fields(state, values, returned)',
                                        'returns': 'SetupValues',
                                        'signature': 'state: SceneState, values: SetupValues'},
 'advance_controller_setup_dismissal_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 198426)\n'
                                                       'return _controller_setup_palette_fields(state, frame, 16740410, 198458, True)',
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'advance_controller_setup_reveal': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                             'returned = advance_controller_setup_reveal_fields(state, entered)\n'
                                             'return _setup_legacy_result_fields(state, values, returned)',
                                     'returns': 'SetupValues',
                                     'signature': 'state: SceneState, values: SetupValues'},
 'advance_controller_setup_reveal_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 198382)\n'
                                                    'return _controller_setup_palette_fields(state, frame, 16740408, 198418, False)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'build_current_city_officer_roster': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                               'returned = build_current_city_officer_roster_fields(state, entered)\n'
                                               'return _map_packet_legacy_result_fields(state, values, returned)',
                                       'returns': 'CityCommandValues',
                                       'signature': 'state: SceneState, values: CityCommandValues'},
 'build_current_city_officer_roster_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 201126)\n'
                                                      'frame = first_replace(frame, roster=state.table_at(4294965034).cursor(), '
                                                      'candidates=state.table_at(4294953984).cursor(), '
                                                      'controller=state.table_at(4294954240))\n'
                                                      "frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\n"
                                                      "frame = _movement_move(state, frame, 'distance', 0, 16)\n"
                                                      "frame = _movement_move(state, frame, 'target_y', 255, 16)\n"
                                                      'while True:\n'
                                                      "    frame = _movement_move(state, frame, 'unit', "
                                                      'frame.candidates.byte(low16(frame.target_y)), 8)\n'
                                                      '    frame = _movement_compare(state, frame, low16(frame.unit), '
                                                      'low16(frame.target_x), 16)\n'
                                                      '    if frame.status & 4:\n'
                                                      "        frame = _movement_move(state, frame, 'count', low16(frame.target_y), 16)\n"
                                                      '        frame = _movement_test(state, frame, '
                                                      'frame.controller.byte(low16(frame.count)), 8)\n'
                                                      '        if not frame.status & 4:\n'
                                                      '            frame = _map_presentation_bit_fields(state, frame, frame.count, 16384)\n'
                                                      '            frame = first_replace(frame, count=frame.count | 16384)\n'
                                                      '        frame = _setup_write_fields(state, frame, frame.roster.base, '
                                                      'low16(frame.count))\n'
                                                      '        frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                                      "        frame = _map_presentation_arithmetic_fields(state, frame, 'distance', 1)\n"
                                                      "    frame, again = _map_presentation_db_fields(frame, 'target_y')\n"
                                                      '    if not again:\n'
                                                      '        break\n'
                                                      'frame = _setup_write_fields(state, frame, frame.roster.base, 65535)\n'
                                                      'return _setup_write_fields(state, frame, 4294965090, low16(frame.distance))',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'clear_current_city_project_orders': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                               'returned = clear_current_city_project_orders_fields(state, entered)\n'
                                               'return _map_packet_legacy_result_fields(state, values, returned)',
                                       'returns': 'CityCommandValues',
                                       'signature': 'state: SceneState, values: CityCommandValues'},
 'clear_current_city_project_orders_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 201084)\n'
                                                      'frame = first_replace(frame, roster=state.table_at(4294961164).cursor())\n'
                                                      "frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\n"
                                                      "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, False)\n"
                                                      "frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', "
                                                      'state.read(4294964068, 2))\n'
                                                      "frame = _movement_fixed_shift_word(state, frame, 'target_x', 2, False)\n"
                                                      'for offset in (0, 4, 8):\n'
                                                      '    frame = _setup_write_fields(state, frame, '
                                                      'frame.roster.address(low16(frame.target_x), offset), 4294967295, 4)\n'
                                                      'return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'clear_unassigned_officer_commands': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                               'returned = clear_unassigned_officer_commands_fields(state, entered)\n'
                                               'return _map_packet_legacy_result_fields(state, values, returned)',
                                       'returns': 'CityCommandValues',
                                       'signature': 'state: SceneState, values: CityCommandValues'},
 'clear_unassigned_officer_commands_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200682)\n'
                                                      'frame = first_replace(frame, roster=state.table_at(4294954240).cursor())\n'
                                                      "frame = _movement_move(state, frame, 'target_x', 255, 16)\n"
                                                      'while True:\n'
                                                      "    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\n"
                                                      '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                                      '    frame = _movement_compare(state, frame, low8(frame.target_y), 2, 8)\n'
                                                      '    if frame.status & 1:\n'
                                                      '        frame = _setup_write_fields(state, frame, u32(frame.roster.base - 1), 0, 1, '
                                                      'True)\n'
                                                      "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                                      '    if not again:\n'
                                                      '        return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'commit_setup_options': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                  'returned = commit_setup_options_fields(state, entered)\n'
                                  'return _setup_legacy_result_fields(state, values, returned)',
                          'returns': 'SetupValues',
                          'signature': 'state: SceneState, values: SetupValues'},
 'commit_setup_options_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 198510)\n'
                                         'frame = _setup_write_fields(state, frame, 4294963154, state.read(16740388, 2))\n'
                                         "frame = _movement_move(state, frame, 'target_x', state.read(16740390, 2), 16)\n"
                                         'frame = _setup_write_fields(state, frame, 4294963156, low16(frame.target_x))\n'
                                         'frame = _setup_write_fields(state, frame, 4294963172, low16(frame.target_x))\n'
                                         'frame = _setup_write_fields(state, frame, 4294964084, '
                                         'state.table_at(198624).byte(low16(frame.target_x)), 1)\n'
                                         'frame = _setup_write_fields(state, frame, 4294964085, 0, 1, True)\n'
                                         'for source, destination in ((16740392, 4294963158), (16740394, 4294963160)):\n'
                                         '    frame = _setup_write_fields(state, frame, destination, state.read(source, 2))\n'
                                         'frame = _setup_write_fields(state, frame, 4294964860, 128)\n'
                                         'frame = _setup_write_fields(state, frame, 4294964862, 128)\n'
                                         "frame = _movement_move(state, frame, 'target_x', state.read(16740404, 2), 16)\n"
                                         'frame = first_replace(frame, roster=state.table_at(16740396).cursor(), '
                                         'candidates=state.table_at(198628).cursor())\n'
                                         "frame = _movement_move(state, frame, 'target_y', state.read(4294963156, 2), 16)\n"
                                         'for step in range(2):\n'
                                         "    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, False)\n"
                                         "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', state.read(4294963156, "
                                         '2))\n'
                                         "frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, False)\n"
                                         'frame = first_replace(frame, candidates=frame.candidates.advance(s16(low16(frame.target_y))), '
                                         'controller=state.table_at(4294964858))\n'
                                         'while True:\n'
                                         "    frame = _movement_move(state, frame, 'target_y', frame.roster.word(), 16)\n"
                                         '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                         "    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, False)\n"
                                         '    frame = _setup_write_fields(state, frame, frame.controller.base, '
                                         'frame.candidates.word(low16(frame.target_y)))\n'
                                         '    frame = first_replace(frame, controller=frame.controller.advance(2))\n'
                                         "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                         '    if not again:\n'
                                         '        return frame',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'cycle_second_player_choice': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                        'returned = cycle_second_player_choice_fields(state, entered)\n'
                                        'return _setup_legacy_result_fields(state, values, returned)',
                                'returns': 'SetupValues',
                                'signature': 'state: SceneState, values: SetupValues'},
 'cycle_second_player_choice_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 197788)\n'
                                               'return _controller_setup_cycle_player_fields(state, frame, False)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'cycle_third_player_choice': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                       'returned = cycle_third_player_choice_fields(state, entered)\n'
                                       'return _setup_legacy_result_fields(state, values, returned)',
                               'returns': 'SetupValues',
                               'signature': 'state: SceneState, values: SetupValues'},
 'cycle_third_player_choice_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 197918)\n'
                                              'return _controller_setup_cycle_player_fields(state, frame, True)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_city_assignment_state': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                            'returned = dispatch_city_assignment_state_fields(state, entered)\n'
                                            'return _map_packet_legacy_result_fields(state, values, returned)',
                                    'returns': 'CityCommandValues',
                                    'signature': 'state: SceneState, values: CityCommandValues'},
 'dispatch_city_assignment_state_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 201416)\n'
                                                   "frame = _movement_move(state, frame, 'target_x', state.read(4294964066, 2), 16)\n"
                                                   "frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, False)\n"
                                                   'return _city_assignment_vector_fields(state, frame, 201464, 201432, 201430)',
                                           'returns': 'FirstDeploymentFrame',
                                           'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'finish_city_command_assignment': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                            'returned = finish_city_command_assignment_fields(state, entered)\n'
                                            'return _map_packet_legacy_result_fields(state, values, returned)',
                                    'returns': 'CityCommandValues',
                                    'signature': 'state: SceneState, values: CityCommandValues'},
 'finish_city_command_assignment_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 201190)\n'
                                                   'frame = _setup_call_fields(state, frame, 59552, 201196)\n'
                                                   'frame = _setup_call_fields(state, frame, 71950, 201202)\n'
                                                   'return _setup_write_fields(state, frame, 4294964076, 1)',
                                           'returns': 'FirstDeploymentFrame',
                                           'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'read_controller_identity': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                      'returned = read_controller_identity_fields(state, entered)\n'
                                      'return _setup_legacy_result_fields(state, values, returned)',
                              'returns': 'SetupValues',
                              'signature': 'state: SceneState, values: SetupValues'},
 'read_controller_identity_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 198466)\n'
                                             'frame = _setup_write_fields(state, frame, frame.roster.base, 64, 1)\n'
                                             "frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\n"
                                             "frame = _movement_move(state, frame, 'target_y', low8(frame.target_x), 8)\n"
                                             "frame = _controller_setup_byte_shift_fields(state, frame, 'target_y', False)\n"
                                             "frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) | "
                                             'low8(frame.target_y), 8)\n'
                                             "frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 10, 8)\n"
                                             'frame = _setup_write_fields(state, frame, frame.roster.base, 0, 1)\n'
                                             "frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\n"
                                             "frame = _movement_move(state, frame, 'unit', low8(frame.target_y), 8)\n"
                                             "frame = _controller_setup_byte_shift_fields(state, frame, 'unit', True)\n"
                                             "frame = _movement_move(state, frame, 'target_y', low8(frame.target_y) | low8(frame.unit), "
                                             '8)\n'
                                             "frame = _movement_move(state, frame, 'target_y', low8(frame.target_y) & 5, 8)\n"
                                             "return _movement_move(state, frame, 'target_x', low8(frame.target_x) | low8(frame.target_y), "
                                             '8)',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'refresh_setup_option_labels': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                         'returned = refresh_setup_option_labels_fields(state, entered)\n'
                                         'return _setup_legacy_result_fields(state, values, returned)',
                                 'returns': 'SetupValues',
                                 'signature': 'state: SceneState, values: SetupValues'},
 'refresh_setup_option_labels_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 196744)\n'
                                                "frame = _movement_move(state, frame, 'target_x', state.read(16740402, 2), 16)\n"
                                                "frame = _movement_move(state, frame, 'target_y', state.read(16740390, 2), 16)\n"
                                                'frame = _movement_compare(state, frame, low16(frame.target_y), low16(frame.target_x), '
                                                '16)\n'
                                                'if frame.status & 4:\n'
                                                '    return frame\n'
                                                'frame = first_replace(frame, roster=state.table_at(196830).cursor())\n'
                                                "frame = _setup_asl_word_fields(state, frame, 'target_y', 2)\n"
                                                'frame = first_replace(frame, '
                                                'roster=state.table_at(frame.roster.long(low16(frame.target_y))).cursor())\n'
                                                'while True:\n'
                                                "    frame = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)\n"
                                                '    frame = _movement_compare(state, frame, low16(frame.target_x), 65535, 16)\n'
                                                '    if frame.status & 4:\n'
                                                '        break\n'
                                                '    frame = _setup_call_fields(state, frame, 177222, 196788)\n'
                                                "    frame = _movement_move_long(state, frame, 'target_x', 0)\n"
                                                "    frame = _movement_move(state, frame, 'offset_x', frame.roster.word(), 16)\n"
                                                '    frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                                "    frame = _movement_move_long(state, frame, 'offset_x', 0)\n"
                                                '    while True:\n'
                                                "        frame = _movement_move(state, frame, 'target_x', frame.roster.word(), 16)\n"
                                                '        frame = first_replace(frame, roster=frame.roster.advance(2))\n'
                                                '        frame = _movement_compare(state, frame, low16(frame.target_x), 65535, 16)\n'
                                                '        if frame.status & 4:\n'
                                                '            break\n'
                                                "        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, "
                                                '16)\n'
                                                "        frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) | 33536, "
                                                '16)\n'
                                                '        frame = _setup_write_fields(state, frame, 12582912, low16(frame.target_x))\n'
                                                'return _setup_write_fields(state, frame, 16740402, state.read(16740390, 2))',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_packed_sprite_position': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                           'returned = render_packed_sprite_position_fields(state, entered)\n'
                                           'return _setup_legacy_result_fields(state, values, returned)',
                                   'returns': 'SetupValues',
                                   'signature': 'state: SceneState, values: SetupValues'},
 'render_packed_sprite_position_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 197292)\n'
                                                  "frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n"
                                                  'frame = _setup_coordinate_high_byte_fields(state, frame)\n'
                                                  "frame = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 255, 16)\n"
                                                  "frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 255, 16)\n"
                                                  "frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                  'return _setup_call_fields(state, frame, 44040, 197312)',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_selected_setup_options': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                           'returned = render_selected_setup_options_fields(state, entered)\n'
                                           'return _setup_legacy_result_fields(state, values, returned)',
                                   'returns': 'SetupValues',
                                   'signature': 'state: SceneState, values: SetupValues'},
 'render_selected_setup_options_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 197314)\n'
                                                  'for roles in ((0, 16740390, 197718, 176406, 197360), (1, 16740388, 197724, 176420, '
                                                  '197408), (2, 16740392, 197730, 176420, 197456), (3, 16740394, 197734, 176420, '
                                                  '197504)):\n'
                                                  '    frame = _controller_setup_option_sprite_fields(state, frame, *roles)\n'
                                                  'frame, visible = _controller_setup_visible_fields(state, frame, 4)\n'
                                                  'if visible:\n'
                                                  '    frame = _setup_compare_memory_fields(state, frame, 16740390, 2)\n'
                                                  '    if frame.status & 4:\n'
                                                  '        frame = _setup_compare_memory_fields(state, frame, 16740396, 3)\n'
                                                  '        if not frame.status & 1:\n'
                                                  '            frame = _setup_write_fields(state, frame, 16740396, 0, clear=True)\n'
                                                  "    frame = _movement_move(state, frame, 'target_x', state.read(16740396, 2), 16)\n"
                                                  "    frame = _setup_asl_word_fields(state, frame, 'target_x', 1)\n"
                                                  '    frame = first_replace(frame, roster=state.table_at(197740).cursor())\n'
                                                  "    frame = _movement_move(state, frame, 'target_y', "
                                                  'frame.roster.word(low16(frame.target_x)), 16)\n'
                                                  "    frame = _movement_move(state, frame, 'target_x', 176, 16)\n"
                                                  '    frame = first_replace(frame, roster=state.table_at(176434).cursor())\n'
                                                  "    frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                  '    frame = _setup_call_fields(state, frame, 44040, 197572)\n'
                                                  'frame = _movement_test(state, frame, state.read(16740404, 2), 16)\n'
                                                  'if frame.status & 4:\n'
                                                  '    return frame\n'
                                                  'frame = _setup_compare_memory_fields(state, frame, 16740386, 5)\n'
                                                  'if frame.status & 1:\n'
                                                  '    return frame\n'
                                                  'if frame.status & 4:\n'
                                                  '    frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 8)\n'
                                                  '    visible = bool(frame.status & 4)\n'
                                                  'else:\n'
                                                  '    visible = True\n'
                                                  'if visible:\n'
                                                  '    frame = first_replace(frame, roster=state.table_at(176442).cursor())\n'
                                                  "    frame = _movement_move(state, frame, 'target_x', state.read(16740398, 2), 16)\n"
                                                  "    frame = _movement_save_longs(state, frame, ('target_x',))\n"
                                                  '    frame = _setup_call_fields(state, frame, 197764, 197626)\n'
                                                  "    frame = _movement_restore_longs(state, frame, ('target_x',))\n"
                                                  'frame = _setup_compare_memory_fields(state, frame, 16740404, 2)\n'
                                                  'if not frame.status & 4:\n'
                                                  '    return frame\n'
                                                  'frame = _setup_compare_memory_fields(state, frame, 16740386, 6)\n'
                                                  'if frame.status & 1:\n'
                                                  '    return frame\n'
                                                  'if frame.status & 4:\n'
                                                  '    frame = _map_presentation_bit_fields(state, frame, state.read(4294964001, 1), 8)\n'
                                                  '    visible = bool(frame.status & 4)\n'
                                                  'else:\n'
                                                  '    visible = True\n'
                                                  'if not visible:\n'
                                                  '    return frame\n'
                                                  'frame = first_replace(frame, roster=state.table_at(176450).cursor())\n'
                                                  "frame = _movement_move(state, frame, 'target_x', state.read(16740400, 2), 16)\n"
                                                  "frame = _movement_save_longs(state, frame, ('target_x',))\n"
                                                  'frame = _setup_call_fields(state, frame, 197764, 197688)\n'
                                                  "return _movement_restore_longs(state, frame, ('target_x',))",
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'render_setup_player_position': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                          'returned = render_setup_player_position_fields(state, entered)\n'
                                          'return _setup_legacy_result_fields(state, values, returned)',
                                  'returns': 'SetupValues',
                                  'signature': 'state: SceneState, values: SetupValues'},
 'render_setup_player_position_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 197764)\n'
                                                 "frame = _setup_asl_word_fields(state, frame, 'target_x', 1)\n"
                                                 'frame = first_replace(frame, scan=state.table_at(197740).cursor())\n'
                                                 "frame = _movement_move(state, frame, 'target_y', frame.scan.word(low16(frame.target_x)), "
                                                 '16)\n'
                                                 "frame = _movement_move(state, frame, 'target_x', 176, 16)\n"
                                                 "frame = _movement_move_long(state, frame, 'unit', 0)\n"
                                                 'return _setup_call_fields(state, frame, 44040, 197786)',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'retain_city_command_stage': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                       'returned = retain_city_command_stage_fields(state, entered)\n'
                                       'return _map_packet_legacy_result_fields(state, values, returned)',
                               'returns': 'CityCommandValues',
                               'signature': 'state: SceneState, values: CityCommandValues'},
 'retain_city_command_stage_fields': {'flow': 'return _resource_cost_frame(state, frame, 201210)',
                                      'returns': 'FirstDeploymentFrame',
                                      'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'run_city_command_assignment': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                         'returned = run_city_command_assignment_fields(state, entered)\n'
                                         'return _map_packet_legacy_result_fields(state, values, returned)',
                                 'returns': 'CityCommandValues',
                                 'signature': 'state: SceneState, values: CityCommandValues'},
 'run_city_command_assignment_fields': {'flow': "frame = _resource_cost_frame(state, frame, 200618)\nframe = _setup_call_fields(state, frame, 200976, 200622)\nwhile True:\n    frame = _setup_call_fields(state, frame, 200820, 200626)\n    frame = _movement_test(state, frame, state.read(4294964068, 2), 16)\n    if frame.status & 8:\n        break\n    frame = _setup_call_fields(state, frame, 201084, 200638)\n    frame = _setup_call_fields(state, frame, 201126, 200642)\n    frame = _setup_write_fields(state, frame, 4294965032, 1)\n    frame = _movement_move(state, frame, 'target_x', state.read(4294965030, 2), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1, False)\n    frame = _city_assignment_vector_fields(state, frame, 200716, 200710, 200662)\nframe = _setup_call_fields(state, frame, 59438, 200670)\nframe = _setup_call_fields(state, frame, 200682, 200674)\nreturn _setup_call_fields(state, frame, 418532, 200680)",
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'run_city_command_states': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                     'returned = run_city_command_states_fields(state, entered)\n'
                                     'return _map_packet_legacy_result_fields(state, values, returned)',
                             'returns': 'CityCommandValues',
                             'signature': 'state: SceneState, values: CityCommandValues'},
 'run_city_command_states_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200740)\n'
                                            'while True:\n'
                                            '    frame = _setup_call_fields(state, frame, 200820, 200744)\n'
                                            '    frame = _movement_test(state, frame, state.read(4294964068, 2), 16)\n'
                                            '    if frame.status & 8:\n'
                                            '        return frame\n'
                                            '    frame = _setup_call_fields(state, frame, 201126, 200756)\n'
                                            '    frame = _setup_write_fields(state, frame, 4294965032, 1)\n'
                                            '    frame = _setup_call_fields(state, frame, 211138, 200768)',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'run_controller_setup_and_configuration': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                                    'returned = run_controller_setup_and_configuration_fields(state, entered)\n'
                                                    'return _setup_legacy_result_fields(state, values, returned)',
                                            'returns': 'SetupValues',
                                            'signature': 'state: SceneState, values: SetupValues'},
 'run_controller_setup_and_configuration_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 198064)\n'
                                                           'frame = _controller_setup_begin_fields(state, frame, False)\n'
                                                           'while True:\n'
                                                           '    frame = _controller_setup_wait_irq_fields(state, frame, 198216)\n'
                                                           '    frame = _setup_compare_memory_fields(state, frame, 16740410, 16)\n'
                                                           '    if not frame.status & 1:\n'
                                                           '        break\n'
                                                           '    frame = _setup_call_fields(state, frame, 198382, 198238)\n'
                                                           '    frame = _setup_call_fields(state, frame, 198294, 198244)\n'
                                                           "    frame = _movement_move(state, frame, 'target_x', state.read(4294964739, "
                                                           '1), 8)\n'
                                                           "    frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & "
                                                           '32, 8)\n'
                                                           '    if not frame.status & 4:\n'
                                                           '        frame = _setup_write_fields(state, frame, 16740414, 1)\n'
                                                           "        frame = _movement_move(state, frame, 'target_x', 172, 8)\n"
                                                           '        frame = _setup_call_fields(state, frame, 32906, 198276)\n'
                                                           '    frame = _movement_test(state, frame, state.read(16740414, 2), 16)\n'
                                                           '    if not frame.status & 4:\n'
                                                           '        frame = _setup_call_fields(state, frame, 198426, 198290)\n'
                                                           'frame = _controller_setup_begin_fields(state, frame, True)\n'
                                                           'while True:\n'
                                                           '    frame = _controller_setup_wait_irq_fields(state, frame, 174956)\n'
                                                           '    frame, finished = _controller_setup_main_iteration_fields(state, frame)\n'
                                                           '    if finished:\n'
                                                           '        return frame',
                                                   'returns': 'FirstDeploymentFrame',
                                                   'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'run_map_packet_command_states': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                           'returned = run_map_packet_command_states_fields(state, entered)\n'
                                           'return _map_packet_legacy_result_fields(state, values, returned)',
                                   'returns': 'CityCommandValues',
                                   'signature': 'state: SceneState, values: CityCommandValues'},
 'run_map_packet_command_states_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200772)\n'
                                                  'while True:\n'
                                                  '    frame = _setup_call_fields(state, frame, 200878, 200776)\n'
                                                  '    frame = _movement_test(state, frame, state.read(4294965082, 2), 16)\n'
                                                  '    if frame.status & 8:\n'
                                                  '        return frame\n'
                                                  '    frame = _setup_write_fields(state, frame, 4294965032, 1)\n'
                                                  '    frame = _setup_call_fields(state, frame, 213240, 200796)\n'
                                                  '    frame = first_replace(frame, roster=state.table_at(4294938624).cursor())\n'
                                                  '    frame = first_replace(frame, roster=frame.roster.advance(s16(state.read(4294965082, '
                                                  '2))))\n'
                                                  "    frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                                  "    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\n"
                                                  "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 13)\n"
                                                  '    frame = _setup_change_word_fields(state, frame, 4294965082, low16(frame.target_x))',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'sample_city_command_policy': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                        'returned = sample_city_command_policy_fields(state, entered)\n'
                                        'return _map_packet_legacy_result_fields(state, values, returned)',
                                'returns': 'CityCommandValues',
                                'signature': 'state: SceneState, values: CityCommandValues'},
 'sample_city_command_policy_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200976)\n'
                                               'frame = _setup_call_fields(state, frame, 33748, 200982)\n'
                                               'frame = first_replace(frame, roster=state.table_at(201212).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294963154, 2), 16)\n"
                                               'from ..high_level_remaining_flows.business_city import _city_encounter_shift_word_fields\n'
                                               "frame = _city_encounter_shift_word_fields(state, frame, 'target_x', 6, False)\n"
                                               'frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))))\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 2, False)\n"
                                               "frame = _movement_move_long(state, frame, 'target_y', 0)\n"
                                               "frame = _movement_move(state, frame, 'target_y', state.read(4294964764, 2), 16)\n"
                                               "frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'target_y', 4)\n"
                                               'from ..high_level_remaining_flows.business_city import _special_action_swap\n'
                                               "frame = _special_action_swap(state, frame, 'target_y')\n"
                                               "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                               'frame = _movement_compare(state, frame, low16(frame.target_y), '
                                               'frame.roster.word(low16(frame.target_x)), 16)\n'
                                               'if not frame.status & 1:\n'
                                               "    frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 4)\n"
                                               '    frame = _movement_compare(state, frame, low16(frame.target_y), '
                                               'frame.roster.word(low16(frame.target_x), 2), 16)\n'
                                               '    if not frame.status & 1:\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 4)\n"
                                               'frame = _setup_call_fields(state, frame, 33748, 201040)\n'
                                               'frame = first_replace(frame, controller=state.table_at(201404))\n'
                                               "frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\n"
                                               "frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'target_x', 3)\n"
                                               "frame = _special_action_swap(state, frame, 'target_x')\n"
                                               "frame = _movement_move(state, frame, 'target_y', 0, 16)\n"
                                               'frame = _movement_compare(state, frame, low16(frame.target_x), '
                                               'frame.controller.word(low16(frame.unit)), 16)\n'
                                               'if not frame.status & 1:\n'
                                               "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 1)\n"
                                               '    frame = _movement_compare(state, frame, low16(frame.target_x), '
                                               'frame.controller.word(low16(frame.unit), 2), 16)\n'
                                               '    if not frame.status & 1:\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 1)\n"
                                               'return _setup_write_fields(state, frame, 4294965030, low16(frame.target_y))',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'select_next_force_city': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                    'returned = select_next_force_city_fields(state, entered)\n'
                                    'return _map_packet_legacy_result_fields(state, values, returned)',
                            'returns': 'CityCommandValues',
                            'signature': 'state: SceneState, values: CityCommandValues'},
 'select_next_force_city_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200820)\n'
                                           'frame = first_replace(frame, roster=state.table_at(4294964263).cursor(), '
                                           'candidates=state.table_at(4294961719).cursor())\n'
                                           "frame = _movement_move(state, frame, 'target_x', state.read(4294964068, 2), 16)\n"
                                           "frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1)\n"
                                           "frame = _movement_move(state, frame, 'unit', state.read(4294964086, 2), 16)\n"
                                           'while True:\n'
                                           '    frame = _movement_compare(state, frame, low16(frame.target_x), 40, 16)\n'
                                           '    if not frame.status & 5:\n'
                                           "        frame = _movement_move(state, frame, 'target_x', 65535, 16)\n"
                                           '        break\n'
                                           '    frame = _movement_test(state, frame, frame.candidates.byte(low16(frame.target_x)), 8)\n'
                                           '    if frame.status & 4:\n'
                                           "        frame = _movement_move(state, frame, 'target_y', "
                                           'frame.roster.byte(low16(frame.target_x)), 8)\n'
                                           '        frame = _movement_compare(state, frame, low8(frame.target_y), low8(frame.unit), 8)\n'
                                           '        if frame.status & 4:\n'
                                           '            break\n'
                                           "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1)\n"
                                           'return _setup_write_fields(state, frame, 4294964068, low16(frame.target_x))',
                                   'returns': 'FirstDeploymentFrame',
                                   'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'select_next_force_map_packet': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                          'returned = select_next_force_map_packet_fields(state, entered)\n'
                                          'return _map_packet_legacy_result_fields(state, values, returned)',
                                  'returns': 'CityCommandValues',
                                  'signature': 'state: SceneState, values: CityCommandValues'},
 'select_next_force_map_packet_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200878)\n'
                                                 'frame = first_replace(frame, roster=state.table_at(4294938624).cursor())\n'
                                                 'frame = first_replace(frame, roster=frame.roster.advance(s16(state.read(4294965082, '
                                                 '2))))\n'
                                                 "frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                                 'while True:\n'
                                                 "    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(), 8)\n"
                                                 '    frame = _map_presentation_bit_fields(state, frame, frame.target_y, 32)\n'
                                                 '    if frame.status & 4:\n'
                                                 "        frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, "
                                                 '16)\n'
                                                 '        if frame.status & 4:\n'
                                                 '            return _setup_write_fields(state, frame, 4294965082, 65535)\n'
                                                 '        frame = _movement_compare(state, frame, low8(frame.target_x), '
                                                 'frame.roster.byte(4), 8)\n'
                                                 '        if frame.status & 4:\n'
                                                 '            break\n'
                                                 "    frame = _movement_move(state, frame, 'target_y', low16(frame.target_y) & 15, 16)\n"
                                                 '    if frame.status & 4:\n'
                                                 '        return _setup_write_fields(state, frame, 4294965082, 65535)\n'
                                                 '    frame = first_replace(frame, roster=frame.roster.advance(13 + '
                                                 's16(low16(frame.target_y))))\n'
                                                 "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 13)\n"
                                                 '    frame = _setup_change_word_fields(state, frame, 4294965082, low16(frame.target_y))\n'
                                                 "frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                                 'for offset, destination in ((1, 4294965084), (2, 4294965086), (3, 4294965088)):\n'
                                                 "    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(offset), 8)\n"
                                                 '    frame = _setup_write_fields(state, frame, destination, low16(frame.target_x))\n'
                                                 'return frame',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'update_connected_controller_option': {'flow': 'entered = _setup_legacy_entry_fields(state, values)\n'
                                                'returned = update_connected_controller_option_fields(state, entered)\n'
                                                'return _setup_legacy_result_fields(state, values, returned)',
                                        'returns': 'SetupValues',
                                        'signature': 'state: SceneState, values: SetupValues'},
 'update_connected_controller_option_fields': {'flow': "frame = _resource_cost_frame(state, frame, 198294)\nframe = _movement_test(state, frame, state.read(16740414, 2), 16)\nif frame.status & 4:\n    frame = first_replace(frame, roster=state.table_at(10551301).cursor())\n    frame = _setup_call_fields(state, frame, 198466, 198314)\n    frame = _movement_compare(state, frame, low8(frame.target_x), 11, 8)\n    if frame.status & 4:\n        frame = _movement_move(state, frame, 'offset_x', state.read(16740404, 2), 16)\n        frame = _movement_move(state, frame, 'offset_y', 2, 16)\n        frame = _setup_call_fields(state, frame, 176154, 198342)\n        frame = _setup_write_fields(state, frame, 16740404, low16(frame.offset_x))\n    else:\n        frame = _setup_write_fields(state, frame, 16740404, 0, clear=True)\nframe = _movement_move(state, frame, 'target_y', state.read(16740404, 2), 16)\nframe = _setup_asl_word_fields(state, frame, 'target_y', 1)\nframe = first_replace(frame, scan=state.table_at(197756).cursor())\nframe = _movement_move(state, frame, 'target_x', frame.scan.word(low16(frame.target_y)), 16)\nframe = first_replace(frame, roster=state.table_at(176458).cursor())\nframe = _movement_move(state, frame, 'target_y', 112, 16)\nframe = _movement_move_long(state, frame, 'unit', 0)\nreturn _setup_call_fields(state, frame, 44040, 198380)",
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D50 first-window exact caller contract repair, sole core unchanged.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'),set()).update(('_position_order_shift',))
DECLARATIONS.update({'sample_city_command_policy_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 200976)\n'
                                               'frame = _setup_call_fields(state, frame, 33748, 200982)\n'
                                               'frame = first_replace(frame, roster=state.table_at(201212).cursor())\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294963154, 2), 16)\n"
                                               'from ..high_level_remaining_flows.business_highbank import _position_order_shift\n'
                                               "frame = _position_order_shift(frame, 'target_x', 6, False)\n"
                                               'state.sr = state.sr & 65504 | frame.status\n'
                                               'frame = first_replace(frame, roster=frame.roster.advance(s16(low16(frame.target_x))))\n'
                                               "frame = _movement_move(state, frame, 'target_x', state.read(4294964086, 2), 16)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_x', 2, False)\n"
                                               "frame = _movement_move_long(state, frame, 'target_y', 0)\n"
                                               "frame = _movement_move(state, frame, 'target_y', state.read(4294964764, 2), 16)\n"
                                               "frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'target_y', 4)\n"
                                               'from ..high_level_remaining_flows.business_city import _special_action_swap\n'
                                               "frame = _special_action_swap(state, frame, 'target_y')\n"
                                               "frame = _movement_move(state, frame, 'unit', 0, 16)\n"
                                               'frame = _movement_compare(state, frame, low16(frame.target_y), '
                                               'frame.roster.word(low16(frame.target_x)), 16)\n'
                                               'if not frame.status & 1:\n'
                                               "    frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 4)\n"
                                               '    frame = _movement_compare(state, frame, low16(frame.target_y), '
                                               'frame.roster.word(low16(frame.target_x), 2), 16)\n'
                                               '    if not frame.status & 1:\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 4)\n"
                                               'frame = _setup_call_fields(state, frame, 33748, 201040)\n'
                                               'frame = first_replace(frame, controller=state.table_at(201404))\n'
                                               "frame = _movement_move_long(state, frame, 'target_x', frame.target_x & 65535)\n"
                                               "frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'target_x', 3)\n"
                                               "frame = _special_action_swap(state, frame, 'target_x')\n"
                                               "frame = _movement_move(state, frame, 'target_y', 0, 16)\n"
                                               'frame = _movement_compare(state, frame, low16(frame.target_x), '
                                               'frame.controller.word(low16(frame.unit)), 16)\n'
                                               'if not frame.status & 1:\n'
                                               "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 1)\n"
                                               '    frame = _movement_compare(state, frame, low16(frame.target_x), '
                                               'frame.controller.word(low16(frame.unit), 2), 16)\n'
                                               '    if not frame.status & 1:\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 1)\n"
                                               'return _setup_write_fields(state, frame, 4294965030, low16(frame.target_y))',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D51 exact source imports/DECL; ordinary mnemonic lowerers unchanged.
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'),set()).update(('copy_scene_palette_variant_fields', 'read_vdp_plane_rle_rows_fields', 'snapshot_and_clear_scene_palette_fields', 'write_vdp_swapped_byte_rle_stream_fields'))
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'),set()).update(('clear_video_sprite_plane_fields', 'enqueue_sound_command_fields'))
DECLARATIONS.update({'_aux_text_call_fields': {'flow': 'frame = _resource_cost_frame(state, frame, target)\n'
                                   'stack = frame.stack_cursor.advance(-4)\n'
                                   'stack.set_long(0, continuation)\n'
                                   'entered = first_replace(frame, stack_cursor=stack)\n'
                                   'children = {216932: dispatch_auxiliary_command_stage_fields, 218130: '
                                   'expand_glyph_tile_sequence_fields, 218232: calculate_glyph_row_layout_fields, 218256: '
                                   'select_glyph_bitmap_fields, 218290: expand_monochrome_glyph_byte_fields, 218314: '
                                   'upload_expanded_glyph_rows_fields, 218692: draw_auxiliary_text_panel_border_fields, 218778: '
                                   'draw_auxiliary_text_panel_rows_fields, 218866: upload_auxiliary_text_panel_glyphs_fields, 218944: '
                                   'draw_auxiliary_text_panel_markers_fields, 240310: decode_unmasked_literal_plane_fields, 240322: '
                                   'decode_high_plane_rows_fields, 243604: dispatch_repeating_scene_presentation_fields, 252652: '
                                   'initialize_object_scene_video_fields}\n'
                                   'if target in children:\n'
                                   '    result = children[target](state, entered)\n'
                                   'elif target == 240334:\n'
                                   '    result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\n'
                                   'elif target == 240466:\n'
                                   '    result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\n'
                                   'elif target == 240532:\n'
                                   '    result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\n'
                                   'elif target == 240266:\n'
                                   '    result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\n'
                                   'elif target == 26830:\n'
                                   '    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n'
                                   '    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\n'
                                   'elif target == 32906:\n'
                                   '    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n'
                                   '    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\n'
                                   'else:\n'
                                   "    raise MovementContinuationBoundary(target, entered, 'auxiliary text child lacks a complete "
                                   "admitted frame')\n"
                                   'result = _resource_cost_frame(state, result, target)\n'
                                   'token = result.stack_cursor.long()\n'
                                   'if token != continuation:\n'
                                   "    raise MovementContinuationBoundary(token, result, 'auxiliary text RTS slot changed')\n"
                                   'state.sr = state.sr & 65504 | result.status\n'
                                   'return first_replace(result, stack_cursor=result.stack_cursor.advance(4))',
                           'returns': 'FirstDeploymentFrame',
                           'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long'},
 '_aux_text_clear_glyph_pair_fields': {'flow': "frame = _movement_move_long(state, frame, 'choice', 0)\n"
                                               'offsets = (0, 4) if double else (0,)\n'
                                               'for offset in offsets:\n'
                                               '    frame = _setup_write_fields(state, frame, u32(frame.controller.base + offset), 0, 4)\n'
                                               'for offset in offsets:\n'
                                               '    frame = _setup_write_fields(state, frame, u32(frame.controller.base + '
                                               's16(low16(frame.target_y)) + offset), 0, 4)\n'
                                               'return first_replace(frame, controller=frame.controller.advance(8 if double else 4))',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame, double: bool=False'},
 '_aux_text_dispatch_stage_fields': {'flow': 'while True:\n'
                                             "    frame = _movement_move(state, frame, 'target_x', state.read(4294965032, 2), 16)\n"
                                             '    if frame.status & 8:\n'
                                             '        return frame\n'
                                             "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1, True)\n"
                                             "    frame = _movement_fixed_shift_word(state, frame, 'target_x', 1)\n"
                                             "    frame = _movement_move(state, frame, 'target_x', "
                                             'state.table_at(table).word(low16(frame.target_x)), 16)\n'
                                             '    frame = _aux_text_call_fields(state, frame, u32(base + s16(low16(frame.target_x))), '
                                             'token)',
                                     'returns': 'FirstDeploymentFrame',
                                     'signature': 'state: SceneState, frame: FirstDeploymentFrame, table: Long, base: Long, token: Long'},
 '_aux_text_legacy_glyph_fields': {'flow': 'checked_context(layout, GlyphTileLayout, state)\n'
                                           'return first_replace(FirstDeploymentFrame.unobserved(), target_x=layout.value, '
                                           'target_y=layout.row_stride, unit=layout.remaining, count=layout.glyph, distance=layout.rows, '
                                           'offset_x=layout.shift_count, offset_y=layout.packed_bits, choice=layout.pixels, '
                                           'roster=layout.counts, candidates=layout.identifiers, controller=layout.destination, '
                                           'scan=layout.bitmap)',
                                   'returns': 'FirstDeploymentFrame',
                                   'signature': 'state: SceneState, layout: GlyphTileLayout'},
 '_aux_text_legacy_glyph_result': {'flow': 'return replace(layout, value=frame.target_x, row_stride=frame.target_y, remaining=frame.unit, '
                                           'glyph=frame.count, rows=frame.distance, shift_count=frame.offset_x, '
                                           'packed_bits=frame.offset_y, pixels=frame.choice, counts=frame.roster, '
                                           'identifiers=frame.candidates, bitmap=frame.scan, destination=None if frame.controller is None '
                                           'else frame.controller.cursor()).validate(state)',
                                   'returns': 'GlyphTileLayout',
                                   'signature': 'state: SceneState, layout: GlyphTileLayout, frame: FirstDeploymentFrame'},
 '_aux_text_shift_word_fields': {'flow': 'frame = _position_order_shift(frame, carrier, amount, False)\n'
                                         'state.sr = state.sr & 65504 | frame.status\n'
                                         'return frame',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'state: SceneState, frame: FirstDeploymentFrame, carrier: str, amount: int'},
 '_object_scene_directory_fields': {'flow': "frame = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), 16)\n"
                                            "frame = _setup_asl_word_fields(state, frame, 'target_x', 2)\n"
                                            'frame = first_replace(frame, roster=state.table_at(directory).cursor())\n'
                                            'pointer = frame.roster.long(low16(frame.target_x))\n'
                                            'return first_replace(frame, roster=state.table_at(pointer).cursor())',
                                    'returns': 'FirstDeploymentFrame',
                                    'signature': 'state: SceneState, frame: FirstDeploymentFrame, directory: Long'},
 '_object_scene_legacy_fields': {'flow': 'checked_context(observed, ScenePresentation, state)\n'
                                         'destination = observed.destination\n'
                                         'if observed.video_address is not None:\n'
                                         '    destination = state.table_at(observed.video_address.carrier).cursor()\n'
                                         'return first_replace(FirstDeploymentFrame.unobserved(), target_x=observed.command, '
                                         'target_y=observed.foreground, unit=observed.mode, count=observed.rows, distance=observed.tile, '
                                         'offset_x=observed.stride, offset_y=observed.palette, choice=observed.remaining, '
                                         'roster=observed.source, candidates=destination, controller=observed.actor, '
                                         'scan=observed.opponent)',
                                 'returns': 'FirstDeploymentFrame',
                                 'signature': 'state: SceneState, observed: ScenePresentation'},
 '_object_scene_legacy_result': {'flow': 'destination = None if frame.candidates is None else frame.candidates.cursor()\n'
                                         'address = observed.video_address\n'
                                         'if address is not None and destination is not None:\n'
                                         '    address = VideoPlaneAddress(destination.base)\n'
                                         '    destination = None\n'
                                         'return replace(observed, command=frame.target_x, foreground=frame.target_y, mode=frame.unit, '
                                         'rows=frame.count, tile=frame.distance, stride=frame.offset_x, palette=frame.offset_y, '
                                         'remaining=frame.choice, source=frame.roster, destination=destination, actor=frame.controller, '
                                         'opponent=frame.scan, video_address=address).validate(state)',
                                 'returns': 'ScenePresentation',
                                 'signature': 'state: SceneState, observed: ScenePresentation, frame: FirstDeploymentFrame'},
 'begin_auxiliary_command_stage': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                           'returned = begin_auxiliary_command_stage_fields(state, entered)\n'
                                           'return _map_packet_legacy_result_fields(state, values, returned)',
                                   'returns': 'CityCommandValues',
                                   'signature': 'state: SceneState, values: CityCommandValues'},
 'begin_auxiliary_command_stage_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 216870)\n'
                                                  'frame = _aux_text_call_fields(state, frame, 216886, 216874)\n'
                                                  'frame = _setup_write_fields(state, frame, 4294965032, 1)\n'
                                                  'return _aux_text_call_fields(state, frame, 216932, 216884)',
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'calculate_glyph_row_layout': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                        'returned = calculate_glyph_row_layout_fields(state, entered)\n'
                                        'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                'returns': 'GlyphTileLayout',
                                'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'calculate_glyph_row_layout_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218232)\n'
                                               "frame = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\n"
                                               "frame = _movement_fixed_shift_word(state, frame, 'unit', 3)\n"
                                               "frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 32)\n"
                                               "frame = _movement_move(state, frame, 'unit', low16(frame.unit) & 65504, 16)\n"
                                               "frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n"
                                               "frame = _aux_text_shift_word_fields(state, frame, 'target_y', 6)\n"
                                               "frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', low16(frame.unit))\n"
                                               "frame = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\n"
                                               "return _movement_fixed_shift_word(state, frame, 'unit', 2, True)",
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'decode_high_plane_rows': {'flow': 'entered = _object_scene_legacy_fields(state, frame)\n'
                                    'returned = decode_high_plane_rows_fields(state, entered)\n'
                                    'return _object_scene_legacy_result(state, frame, returned)',
                            'returns': 'ScenePresentation',
                            'signature': 'state: SceneState, frame: ScenePresentation'},
 'decode_high_plane_rows_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 240322)\n'
                                           'frame = _setup_write_fields(state, frame, 4294934528, 32768)\n'
                                           "frame = _movement_move(state, frame, 'offset_y', 32, 16)\n"
                                           "raise MovementContinuationBoundary(240342, frame, 'high-plane decoder shared tail has no "
                                           "admitted entry facade')",
                                   'returns': 'FirstDeploymentFrame',
                                   'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'decode_unmasked_literal_plane': {'flow': 'entered = _object_scene_legacy_fields(state, frame)\n'
                                           'returned = decode_unmasked_literal_plane_fields(state, entered)\n'
                                           'return _object_scene_legacy_result(state, frame, returned)',
                                   'returns': 'ScenePresentation',
                                   'signature': 'state: SceneState, frame: ScenePresentation'},
 'decode_unmasked_literal_plane_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 240310)\n'
                                                  'frame = _setup_write_fields(state, frame, 4294934528, 0, clear=True)\n'
                                                  'frame = _setup_write_fields(state, frame, 4294934530, 1)\n'
                                                  "raise MovementContinuationBoundary(240346, frame, 'literal decoder shared tail has no "
                                                  "admitted entry facade')",
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_auxiliary_command_stage': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                              'returned = dispatch_auxiliary_command_stage_fields(state, entered)\n'
                                              'return _map_packet_legacy_result_fields(state, values, returned)',
                                      'returns': 'CityCommandValues',
                                      'signature': 'state: SceneState, values: CityCommandValues'},
 'dispatch_auxiliary_command_stage_fields': {'flow': 'return _aux_text_dispatch_stage_fields(state, _resource_cost_frame(state, frame, '
                                                     '216932), 216956, 216980, 216952)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_city_command_stage': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                         'returned = dispatch_city_command_stage_fields(state, entered)\n'
                                         'return _map_packet_legacy_result_fields(state, values, returned)',
                                 'returns': 'CityCommandValues',
                                 'signature': 'state: SceneState, values: CityCommandValues'},
 'dispatch_city_command_stage_fields': {'flow': 'return _aux_text_dispatch_stage_fields(state, _resource_cost_frame(state, frame, 211138), '
                                                '211162, 211180, 211158)',
                                        'returns': 'FirstDeploymentFrame',
                                        'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_map_packet_command_stage': {'flow': 'entered = _map_packet_legacy_entry_fields(state, values)\n'
                                               'returned = dispatch_map_packet_command_stage_fields(state, entered)\n'
                                               'return _map_packet_legacy_result_fields(state, values, returned)',
                                       'returns': 'CityCommandValues',
                                       'signature': 'state: SceneState, values: CityCommandValues'},
 'dispatch_map_packet_command_stage_fields': {'flow': 'return _aux_text_dispatch_stage_fields(state, _resource_cost_frame(state, frame, '
                                                      '213240), 213264, 213312, 213260)',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'dispatch_repeating_scene_presentation': {'flow': 'entered = _object_scene_legacy_fields(state, frame)\n'
                                                   'returned = dispatch_repeating_scene_presentation_fields(state, entered)\n'
                                                   'return _object_scene_legacy_result(state, frame, returned)',
                                           'returns': 'ScenePresentation',
                                           'signature': 'state: SceneState, frame: ScenePresentation'},
 'dispatch_repeating_scene_presentation_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 243604)\n'
                                                          "frame = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), "
                                                          '16)\n'
                                                          "frame = _setup_asl_word_fields(state, frame, 'target_x', 2)\n"
                                                          'target = u32(243614 + s16(low16(frame.target_x)))\n'
                                                          "raise MovementContinuationBoundary(target, frame, 'computed presentation JMP "
                                                          "entry requires its genuine owner facade')",
                                                  'returns': 'FirstDeploymentFrame',
                                                  'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'draw_auxiliary_text_panel_border': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                              'returned = draw_auxiliary_text_panel_border_fields(state, entered)\n'
                                              'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                      'returns': 'GlyphTileLayout',
                                      'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'draw_auxiliary_text_panel_border_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218692)\n'
                                                     "frame = _movement_move(state, frame, 'target_x', 10, 16)\n"
                                                     "frame = _movement_move(state, frame, 'unit', 5, 16)\n"
                                                     'while True:\n'
                                                     "    frame = _movement_move(state, frame, 'distance', low16(frame.target_x), 16)\n"
                                                     '    frame = _setup_write_fields(state, frame, frame.auxiliary.base, frame.target_y, '
                                                     '4)\n'
                                                     "    frame = _movement_move(state, frame, 'count', 7, 16)\n"
                                                     '    while True:\n'
                                                     '        frame = _setup_write_fields(state, frame, frame.scratch.base, '
                                                     'low16(frame.distance))\n'
                                                     "        frame = _map_presentation_arithmetic_fields(state, frame, 'distance', 6)\n"
                                                     "        frame, again = _map_presentation_db_fields(frame, 'count')\n"
                                                     '        if not again:\n'
                                                     '            break\n'
                                                     '    frame = _movement_compare(state, frame, low16(frame.unit), 3, 16)\n'
                                                     '    middle = bool(frame.status & 4)\n'
                                                     '    if middle:\n'
                                                     "        frame = _movement_move(state, frame, 'offset_x', 8463, 16)\n"
                                                     '    else:\n'
                                                     '        frame = _movement_compare(state, frame, low16(frame.unit), 2, 16)\n'
                                                     '        middle = bool(frame.status & 4)\n'
                                                     '        if middle:\n'
                                                     "            frame = _movement_move(state, frame, 'offset_x', 8449, 16)\n"
                                                     '    if middle:\n'
                                                     '        frame = _setup_write_fields(state, frame, frame.scratch.base, 0)\n'
                                                     '        frame = _setup_write_fields(state, frame, frame.scratch.base, 0)\n'
                                                     "        frame = _movement_move(state, frame, 'count', 13, 16)\n"
                                                     '        while True:\n'
                                                     '            frame = _setup_write_fields(state, frame, frame.scratch.base, '
                                                     'low16(frame.offset_x))\n'
                                                     "            frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', "
                                                     '1)\n'
                                                     "            frame, again = _map_presentation_db_fields(frame, 'count')\n"
                                                     '            if not again:\n'
                                                     '                break\n'
                                                     "    frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1, True)\n"
                                                     "    frame = _movement_arithmetic_long(state, frame, 'target_y', 131072, True)\n"
                                                     "    frame, again = _map_presentation_db_fields(frame, 'unit')\n"
                                                     '    if not again:\n'
                                                     '        return frame',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'draw_auxiliary_text_panel_markers': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                               'returned = draw_auxiliary_text_panel_markers_fields(state, entered)\n'
                                               'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                       'returns': 'GlyphTileLayout',
                                       'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'draw_auxiliary_text_panel_markers_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218944)\n'
                                                      "for carrier, value in (('auxiliary', 1128398851), ('scratch', 3473462), ('scratch', "
                                                      "3604536), ('auxiliary', 1145307139), ('scratch', 3997758)):\n"
                                                      "    address = frame.auxiliary.base if carrier == 'auxiliary' else "
                                                      'frame.scratch.base\n'
                                                      '    frame = _setup_write_fields(state, frame, address, value, 4)\n'
                                                      'return frame',
                                              'returns': 'FirstDeploymentFrame',
                                              'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'draw_auxiliary_text_panel_rows': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                            'returned = draw_auxiliary_text_panel_rows_fields(state, entered)\n'
                                            'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                    'returns': 'GlyphTileLayout',
                                    'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'draw_auxiliary_text_panel_rows_fields': {'flow': "frame = _resource_cost_frame(state, frame, 218778)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964040, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 2)\nframe = first_replace(frame, roster=state.table_at(state.table_at(218896).long(low16(frame.target_x))).cursor())\nframe = _movement_move(state, frame, 'count', 8, 16)\nframe = first_replace(frame, roster=frame.roster.advance(1))\nwhile True:\n    frame = _movement_move(state, frame, 'distance', frame.roster.byte(), 8)\n    frame = first_replace(frame, roster=frame.roster.advance(1))\n    frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 255, 16)\n    frame = _movement_move(state, frame, 'offset_x', low16(frame.distance), 16)\n    frame = _movement_fixed_shift_word(state, frame, 'offset_x', 1)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', 5)\n    frame = _movement_fixed_shift_word(state, frame, 'offset_x', 3, True)\n    frame = _movement_fixed_shift_word(state, frame, 'distance', 1)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'distance', low16(frame.offset_x))\n    frame = _movement_move(state, frame, 'offset_x', low16(frame.unit), 16)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', low16(frame.distance))\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.distance), 16)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'offset_y', 1, True)\n    frame = _setup_write_fields(state, frame, frame.auxiliary.base, frame.target_y, 4)\n    while True:\n        frame = _setup_write_fields(state, frame, frame.scratch.base, low16(frame.offset_x))\n        frame = _map_presentation_arithmetic_fields(state, frame, 'offset_x', 1)\n        frame, again = _map_presentation_db_fields(frame, 'offset_y')\n        if not again:\n            break\n    frame = _movement_arithmetic_long(state, frame, 'target_y', 131072, True)\n    frame = _setup_write_fields(state, frame, frame.auxiliary.base, frame.target_y, 4)\n    frame = _movement_move(state, frame, 'offset_y', low16(frame.distance), 16)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'offset_y', 1, True)\n    while True:\n        frame = _setup_write_fields(state, frame, frame.scratch.base, low16(frame.unit))\n        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 1)\n        frame, again = _map_presentation_db_fields(frame, 'offset_y')\n        if not again:\n            break\n    frame = _movement_arithmetic_long(state, frame, 'target_y', 262144, True)\n    frame = _map_presentation_arithmetic_fields(state, frame, 'unit', low16(frame.distance))\n    frame, again = _map_presentation_db_fields(frame, 'count')\n    if not again:\n        return frame",
                                           'returns': 'FirstDeploymentFrame',
                                           'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'expand_glyph_tile_sequence': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                        'returned = expand_glyph_tile_sequence_fields(state, entered)\n'
                                        'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                'returns': 'GlyphTileLayout',
                                'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'expand_glyph_tile_sequence_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218130)\n'
                                               'while True:\n'
                                               '    frame = first_replace(frame, controller=state.table_at(4294955776).cursor())\n'
                                               "    frame = _movement_move(state, frame, 'target_x', 0, 16)\n"
                                               "    frame = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\n"
                                               '    frame = first_replace(frame, roster=frame.roster.advance(1))\n'
                                               '    if frame.status & 8:\n'
                                               '        return frame\n'
                                               '    if frame.status & 4:\n'
                                               '        continue\n'
                                               '    frame = _aux_text_call_fields(state, frame, 218232, 218146)\n'
                                               '    while True:\n'
                                               "        frame = _movement_move(state, frame, 'count', frame.candidates.word(), 16)\n"
                                               '        frame = first_replace(frame, candidates=frame.candidates.advance(2))\n'
                                               '        frame = _aux_text_call_fields(state, frame, 218256, 218152)\n'
                                               "        frame = _movement_move(state, frame, 'distance', 15, 16)\n"
                                               '        while True:\n'
                                               '            frame = _aux_text_call_fields(state, frame, 218290, 218160)\n'
                                               '            frame = _setup_write_fields(state, frame, frame.controller.base, frame.choice, '
                                               '4)\n'
                                               '            frame = _aux_text_call_fields(state, frame, 218290, 218166)\n'
                                               '            frame = _setup_write_fields(state, frame, u32(frame.controller.base + '
                                               's16(low16(frame.target_y))), frame.choice, 4)\n'
                                               '            frame = first_replace(frame, controller=frame.controller.advance(4))\n'
                                               "            frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 1, True)\n"
                                               "            frame, again = _map_presentation_db_fields(frame, 'distance')\n"
                                               '            if not again:\n'
                                               '                break\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1, True)\n"
                                               '        if frame.status & 4:\n'
                                               '            break\n'
                                               '        frame = _aux_text_clear_glyph_pair_fields(state, frame, True)\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 2, True)\n"
                                               '    frame = _movement_test(state, frame, low16(frame.unit), 16)\n'
                                               '    if not frame.status & 4:\n'
                                               "        frame = _map_presentation_arithmetic_fields(state, frame, 'unit', 1, True)\n"
                                               '        while True:\n'
                                               '            frame = _aux_text_clear_glyph_pair_fields(state, frame)\n'
                                               "            frame, again = _map_presentation_db_fields(frame, 'unit')\n"
                                               '            if not again:\n'
                                               '                break\n'
                                               '    frame = _aux_text_call_fields(state, frame, 218314, 218228)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'expand_monochrome_glyph_byte': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                          'returned = expand_monochrome_glyph_byte_fields(state, entered)\n'
                                          'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                  'returns': 'GlyphTileLayout',
                                  'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'expand_monochrome_glyph_byte_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218290)\n'
                                                 "frame = _movement_move(state, frame, 'offset_y', frame.scan.byte(), 8)\n"
                                                 'frame = first_replace(frame, scan=frame.scan.advance(1))\n'
                                                 "frame = _movement_move_long(state, frame, 'choice', 0)\n"
                                                 "frame = _movement_move(state, frame, 'offset_x', 7, 16)\n"
                                                 'while True:\n'
                                                 "    frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'choice', 4)\n"
                                                 '    old = low8(frame.offset_y)\n'
                                                 '    carry = bool(old & 128)\n'
                                                 '    bits = u8(old << 1 | bool(frame.status & 16))\n'
                                                 '    status = (17 if carry else 0) | (8 if bits & 128 else 0) | (4 if bits == 0 else 0)\n'
                                                 '    state.sr = state.sr & 65504 | status\n'
                                                 '    frame = first_replace(frame, offset_y=replace_byte(frame.offset_y, bits), '
                                                 'status=status)\n'
                                                 '    if carry:\n'
                                                 "        frame = _movement_move(state, frame, 'choice', low8(frame.choice) | 1, 8)\n"
                                                 "    frame, again = _map_presentation_db_fields(frame, 'offset_x')\n"
                                                 '    if not again:\n'
                                                 '        return frame',
                                         'returns': 'FirstDeploymentFrame',
                                         'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'initialize_auxiliary_text_panel': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                             'returned = initialize_auxiliary_text_panel_fields(state, entered)\n'
                                             'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                     'returns': 'GlyphTileLayout',
                                     'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'initialize_auxiliary_text_panel_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218586)\n'
                                                    "frame = _movement_move(state, frame, 'target_x', state.read(4294964040, 2), 16)\n"
                                                    "frame = _movement_move(state, frame, 'target_x', "
                                                    'state.table_at(218686).byte(low16(frame.target_x)), 8)\n'
                                                    'frame = _setup_write_fields(state, frame, 4294964042, low16(frame.target_x))\n'
                                                    "frame = _movement_move(state, frame, 'target_y', 5, 16)\n"
                                                    'frame = _aux_text_call_fields(state, frame, 418260, 218608)\n'
                                                    'frame = first_replace(frame, roster=state.table_at(4294966016).cursor(), '
                                                    'candidates=state.table_at(4294966144).cursor())\n'
                                                    "frame = _movement_move(state, frame, 'target_x', 7, 16)\n"
                                                    'while True:\n'
                                                    '    value = frame.roster.long()\n'
                                                    '    frame = first_replace(frame, roster=frame.roster.advance(4))\n'
                                                    '    frame = _setup_write_fields(state, frame, frame.candidates.base, value, 4)\n'
                                                    '    frame = first_replace(frame, candidates=frame.candidates.advance(4))\n'
                                                    "    frame, again = _map_presentation_db_fields(frame, 'target_x')\n"
                                                    '    if not again:\n'
                                                    '        break\n'
                                                    'frame = _setup_write_fields(state, frame, frame.candidates.base, 3822, 4)\n'
                                                    'frame = first_replace(frame, auxiliary=state.table_at(12582916).cursor(), '
                                                    'scratch=state.table_at(12582912).cursor())\n'
                                                    "frame = _movement_move_long(state, frame, 'target_y', 1103757315)\n"
                                                    'frame = _setup_write_fields(state, frame, frame.auxiliary.base, 36736)\n'
                                                    'frame = _aux_text_call_fields(state, frame, 218692, 218658)\n'
                                                    "frame = _movement_arithmetic_long(state, frame, 'target_y', 8650752, True)\n"
                                                    "frame = _movement_move(state, frame, 'unit', 8477, 16)\n"
                                                    'frame = _aux_text_call_fields(state, frame, 218778, 218672)\n'
                                                    'frame = _setup_write_fields(state, frame, frame.auxiliary.base, 36610)\n'
                                                    'frame = _aux_text_call_fields(state, frame, 218866, 218680)\n'
                                                    'return _aux_text_call_fields(state, frame, 218944, 218684)',
                                            'returns': 'FirstDeploymentFrame',
                                            'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'initialize_object_scene_video': {'flow': 'entered = _object_scene_legacy_fields(state, frame)\n'
                                           'returned = initialize_object_scene_video_fields(state, entered)\n'
                                           'return _object_scene_legacy_result(state, frame, returned)',
                                   'returns': 'ScenePresentation',
                                   'signature': 'state: SceneState, frame: ScenePresentation'},
 'initialize_object_scene_video_fields': {'flow': "frame = _resource_cost_frame(state, frame, 252652)\nfor value in (36610, 33328, 33584, 33799, 34152, 34560, 35584, 35969, 36149, 36610, 36881, 37268, 37376):\n    frame = _setup_write_fields(state, frame, 12582916, value)\nfor address, value in ((4294934560, 48), (4294934564, 0), (4294934566, 48), (4294934562, 32), (4294934568, 0), (4294934570, 32)):\n    frame = _setup_write_fields(state, frame, address, value)\nfor directory, video, token in ((253012, 0, 252816), (253032, 8192, 252840), (253052, 16384, 252864)):\n    frame = _object_scene_directory_fields(state, frame, directory)\n    frame = _movement_move(state, frame, 'target_x', video, 16)\n    frame = _aux_text_call_fields(state, frame, 240466, token)\nfor source, video, token in ((319632, 32768, 252878), (326628, 40960, 252892)):\n    frame = first_replace(frame, roster=state.table_at(source).cursor())\n    frame = _movement_move(state, frame, 'target_x', video, 16)\n    frame = _aux_text_call_fields(state, frame, 240466, token)\nfor directory, address, token in ((253072, 57344, 252924), (253092, 61440, 252956)):\n    frame = _object_scene_directory_fields(state, frame, directory)\n    frame = first_replace(frame, candidates=state.table_at(address).cursor())\n    frame = _movement_move_long(state, frame, 'offset_x', 128)\n    frame = _aux_text_call_fields(state, frame, 240334, token)\nfor source, address, target, token in ((283667, 49152, 240322, 252978), (284396, 49216, 240322, 253000)):\n    frame = first_replace(frame, roster=state.table_at(source).cursor(), candidates=state.table_at(address).cursor())\n    frame = _movement_move_long(state, frame, 'offset_x', 128)\n    frame = _aux_text_call_fields(state, frame, target, token)\nframe = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), 16)\nframe = _map_presentation_arithmetic_fields(state, frame, 'target_x', 4)\nreturn _aux_text_call_fields(state, frame, 240532, 253010)",
                                          'returns': 'FirstDeploymentFrame',
                                          'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'run_repeating_scene_presentation': {'flow': 'entered = _object_scene_legacy_fields(state, frame)\n'
                                              'returned = run_repeating_scene_presentation_fields(state, entered)\n'
                                              'return _object_scene_legacy_result(state, frame, returned)',
                                      'returns': 'ScenePresentation',
                                      'signature': 'state: SceneState, frame: ScenePresentation'},
 'run_repeating_scene_presentation_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 243506)\n'
                                                     'frame = _controller_setup_interrupt_status_fields(state, frame, 9984)\n'
                                                     "frame = _movement_move(state, frame, 'target_x', state.read(4294964742, 2), 16)\n"
                                                     "frame = _movement_move(state, frame, 'target_x', low8(frame.target_x) & 191, 8)\n"
                                                     'frame = _setup_write_fields(state, frame, 12582916, low16(frame.target_x))\n'
                                                     'frame = _aux_text_call_fields(state, frame, 26830, 243530)\n'
                                                     'frame = _aux_text_call_fields(state, frame, 252652, 243534)\n'
                                                     'frame = _aux_text_call_fields(state, frame, 240266, 243538)\n'
                                                     "frame = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), 16)\n"
                                                     "frame = _setup_asl_word_fields(state, frame, 'target_x', 1)\n"
                                                     "frame = _movement_move(state, frame, 'target_x', "
                                                     'state.table_at(243592).word(low16(frame.target_x)), 16)\n'
                                                     'frame = _aux_text_call_fields(state, frame, 32906, 243554)\n'
                                                     'frame = _controller_setup_interrupt_status_fields(state, frame, 9472)\n'
                                                     'while True:\n'
                                                     '    frame = _setup_write_fields(state, frame, 4294964754, 1280)\n'
                                                     '    for target, token in ((33736, 243570), (242312, 243574), (239992, 243578), '
                                                     '(243604, 243582), (242236, 243588)):\n'
                                                     '        frame = _aux_text_call_fields(state, frame, target, token)',
                                             'returns': 'FirstDeploymentFrame',
                                             'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'select_glyph_bitmap': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                 'returned = select_glyph_bitmap_fields(state, entered)\n'
                                 'return _aux_text_legacy_glyph_result(state, layout, returned)',
                         'returns': 'GlyphTileLayout',
                         'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'select_glyph_bitmap_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218256)\n'
                                        'stack = frame.stack_cursor.advance(-2)\n'
                                        'stack.set_word(0, low16(frame.count))\n'
                                        'frame = first_replace(frame, stack_cursor=stack)\n'
                                        'frame = _movement_test(state, frame, low16(frame.count), 16)\n'
                                        "frame = _movement_move(state, frame, 'distance', low16(frame.count), 16)\n"
                                        "frame = _movement_move_long(state, frame, 'count', frame.count & 65280)\n"
                                        "frame = _glyph_shift_long_fields(SceneRefreshMemory(state), frame, 'count', 3)\n"
                                        "frame = _movement_move(state, frame, 'distance', low16(frame.distance) & 255, 16)\n"
                                        "frame = _aux_text_shift_word_fields(state, frame, 'distance', 5)\n"
                                        "frame = _map_presentation_arithmetic_fields(state, frame, 'count', low16(frame.distance))\n"
                                        'frame = first_replace(frame, scan=state.table_at(u32(529820 + '
                                        's16(low16(frame.count)))).cursor())\n'
                                        "frame = _movement_move(state, frame, 'count', frame.stack_cursor.word(), 16)\n"
                                        'return first_replace(frame, stack_cursor=frame.stack_cursor.advance(2))',
                                'returns': 'FirstDeploymentFrame',
                                'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_auxiliary_text_panel_glyphs': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                                'returned = upload_auxiliary_text_panel_glyphs_fields(state, entered)\n'
                                                'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                        'returns': 'GlyphTileLayout',
                                        'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'upload_auxiliary_text_panel_glyphs_fields': {'flow': "frame = _resource_cost_frame(state, frame, 218866)\nframe = _setup_write_fields(state, frame, 12582916, 1612709888, 4)\nframe = _movement_move(state, frame, 'target_x', state.read(4294964040, 2), 16)\nframe = _movement_fixed_shift_word(state, frame, 'target_x', 2)\nframe = first_replace(frame, roster=state.table_at(state.table_at(218896).long(low16(frame.target_x))).cursor(), candidates=state.table_at(state.table_at(218920).long(low16(frame.target_x))).cursor())\nreturn _aux_text_call_fields(state, frame, 218130, 218894)",
                                               'returns': 'FirstDeploymentFrame',
                                               'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_expanded_glyph_rows': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                        'returned = upload_expanded_glyph_rows_fields(state, entered)\n'
                                        'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                'returns': 'GlyphTileLayout',
                                'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'upload_expanded_glyph_rows_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218314)\n'
                                               'frame = first_replace(frame, controller=state.table_at(4294955776).cursor())\n'
                                               "frame = _movement_fixed_shift_word(state, frame, 'target_y', 1, True)\n"
                                               "frame = _map_presentation_arithmetic_fields(state, frame, 'target_y', 1, True)\n"
                                               'while True:\n'
                                               '    value = frame.controller.long()\n'
                                               '    frame = first_replace(frame, controller=frame.controller.advance(4))\n'
                                               '    frame = _setup_write_fields(state, frame, 12582912, value, 4)\n'
                                               "    frame, again = _map_presentation_db_fields(frame, 'target_y')\n"
                                               '    if not again:\n'
                                               '        return frame',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'},
 'upload_glyph_tile_sequence': {'flow': 'entered = _aux_text_legacy_glyph_fields(state, layout)\n'
                                        'returned = upload_glyph_tile_sequence_fields(state, entered)\n'
                                        'return _aux_text_legacy_glyph_result(state, layout, returned)',
                                'returns': 'GlyphTileLayout',
                                'signature': 'state: SceneState, layout: GlyphTileLayout'},
 'upload_glyph_tile_sequence_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 218108)\n'
                                               'frame = _setup_write_fields(state, frame, 12582916, 1075838976, 4)\n'
                                               'frame = first_replace(frame, roster=state.table_at(563484).cursor(), '
                                               'candidates=state.table_at(563506).cursor())\n'
                                               'return expand_glyph_tile_sequence_fields(state, frame)',
                                       'returns': 'FirstDeploymentFrame',
                                       'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})

# D51 actual 3547C/06420014 immediate is decimal20; reconstruction repair only.
DECLARATIONS.update({'calculate_glyph_row_layout_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 218232)\nframe = _movement_move(state, frame, 'unit', low16(frame.target_x), 16)\nframe = _movement_fixed_shift_word(state, frame, 'unit', 3)\nframe = _map_presentation_arithmetic_fields(state, frame, 'unit', 20)\nframe = _movement_move(state, frame, 'unit', low16(frame.unit) & 65504, 16)\nframe = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\nframe = _aux_text_shift_word_fields(state, frame, 'target_y', 6)\nframe = _map_presentation_arithmetic_fields(state, frame, 'target_y', low16(frame.unit))\nframe = _movement_move(state, frame, 'unit', low16(frame.target_y), 16)\nreturn _movement_fixed_shift_word(state, frame, 'unit', 2, True)"}})

APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(('wait_command_intro_fields',))


# Source136: real existing full children; each old caller retains its own return LONG.
DECLARATIONS.update({'_aux_text_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nchildren = {216932: dispatch_auxiliary_command_stage_fields, 218130: expand_glyph_tile_sequence_fields, 218232: calculate_glyph_row_layout_fields, 218256: select_glyph_bitmap_fields, 218290: expand_monochrome_glyph_byte_fields, 218314: upload_expanded_glyph_rows_fields, 218692: draw_auxiliary_text_panel_border_fields, 218778: draw_auxiliary_text_panel_rows_fields, 218866: upload_auxiliary_text_panel_glyphs_fields, 218944: draw_auxiliary_text_panel_markers_fields, 240310: decode_unmasked_literal_plane_fields, 240322: decode_high_plane_rows_fields, 243604: dispatch_repeating_scene_presentation_fields, 252652: initialize_object_scene_video_fields}\nif target in children:\n    result = children[target](state, entered)\nelif target == 240334:\n    result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\nelif target == 240466:\n    result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\nelif target == 240532:\n    result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\nelif target == 240266:\n    result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\nelif target == 26830:\n    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\nelif target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\nelif target == 418260:\n    from ..high_level_dynamic_flows.business_actions import upload_portrait_tiles_frame_fields\n    result = upload_portrait_tiles_frame_fields(state, entered)\nelif target == 33736:\n    from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields\n    result = wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), entered)\nelif target == 242312:\n    from ..high_level_scene_flows.business_objects import append_scene_center_marker_fields\n    result = append_scene_center_marker_fields(SceneRefreshMemory(state), entered)\nelif target == 239992:\n    from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n    result = advance_scene_palette_fade_fields(SceneRefreshMemory(state), entered)\nelif target == 242236:\n    from ..high_level_scene_flows.business_scene import finish_actor_sprite_chains_fields\n    result = finish_actor_sprite_chains_fields(SceneRefreshMemory(state), entered)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'auxiliary text child lacks a complete admitted frame')\nresult = _resource_cost_frame(state, result, target)\ntoken = result.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, result, 'auxiliary text RTS slot changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}})
APPROVED.setdefault((2, 'high_level_dynamic_flows.business_actions'), set()).update(('upload_portrait_tiles_frame_fields',))
APPROVED.setdefault((2, 'high_level_gameplay_flow.business_services'), set()).update(('wait_for_scene_sound_byte_fields',))
APPROVED.setdefault((2, 'high_level_scene_flows.business_objects'), set()).update(('append_scene_center_marker_fields',))
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('advance_scene_palette_fade_fields', 'finish_actor_sprite_chains_fields'))


# Source140: one literal-plane internal entry, original physical owners unchanged.
DECLARATIONS.update({'decode_unmasked_literal_plane_fields': {'flow': 'frame = _resource_cost_frame(state, frame, 240310)\nframe = _setup_write_fields(state, frame, 4294934528, 0, clear=True)\nframe = _setup_write_fields(state, frame, 4294934530, 1)\nfrom ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_literal_fields\nreturn read_vdp_plane_rle_rows_from_literal_fields(SceneRefreshMemory(state), frame)', 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('read_vdp_plane_rle_rows_from_literal_fields',))

DECLARATIONS.update({'_city_assignment_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "children = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields, 59438: recover_unacted_officer_b200_fields}\nif target == 201486:\n    from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields\n    return wait_command_intro_fields(state, frame)\nif target in children:\n    return children[target](state, frame)\nif target == 33748:\n    return first_deployment_random_fields(BattlePolicyMemory(state), frame)\nif target == 418532:\n    return advance_officer_growth_levels_fields(state, frame)\nif target == 71950:\n    from .business_gameplay import settle_city_projects_and_refresh_map_fields\n    return settle_city_projects_and_refresh_map_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')"}, 'recover_unacted_officer_b200_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 59438)\nframe = first_replace(frame, roster=state.table_at(4294953984).cursor(), candidates=state.table_at(4294964263).cursor(), controller=state.table_at(4294954240).cursor(), scan=state.table_at(4294947328).cursor(), opponent=state.table_at(4294946816), scratch=state.table_at(4294961720))\nframe = _movement_move(state, frame, 'target_x', 255, 16)\nframe = _movement_move(state, frame, 'choice', state.read(4294964086, 2), 16)\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(s16(low16(frame.target_x))), 8)\n    frame = _movement_compare(state, frame, low8(frame.target_y), 40, 8)\n    if frame.status & 5:\n        city = s16(low16(frame.target_y))\n        frame = _movement_test(state, frame, frame.scratch.byte(city), 8)\n        if frame.status & 4:\n            frame = _movement_compare(state, frame, low8(frame.choice), frame.candidates.byte(city), 8)\n            if frame.status & 4:\n                frame = _movement_test(state, frame, frame.controller.byte(s16(low16(frame.target_x))), 8)\n                if frame.status & 4:\n                    frame = _movement_move(state, frame, 'target_y', low16(frame.target_x), 16)\n                    frame = _movement_fixed_shift_word(state, frame, 'target_y', 1)\n                    offset = s16(low16(frame.target_y))\n                    frame = _movement_move(state, frame, 'unit', frame.opponent.word(offset), 16)\n                    frame = _movement_multiply_word(state, frame, 'unit', 15)\n                    frame = _movement_divu_word(state, frame, 'unit', 100, 59520)\n                    frame = _movement_move(state, frame, 'count', frame.scan.word(offset), 16)\n                    frame = _movement_add_word(state, frame, 'count', low16(frame.unit))\n                    frame = _movement_compare(state, frame, low16(frame.count), frame.opponent.word(offset), 16)\n                    if not frame.status & 5:\n                        frame = _movement_move(state, frame, 'count', frame.opponent.word(offset), 16)\n                    frame = _settlement_store_word_fields(state, frame, frame.scan, offset, low16(frame.count))\n    frame, more = _map_presentation_db_fields(frame, 'target_x')\n    if not more:\n        return frame"}})


# Source140: genuine complete roster/save routes; caller-owned real return LONGs.
DECLARATIONS.update({'_aux_text_call_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long, continuation: Long', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, target)\nstack = frame.stack_cursor.advance(-4)\nstack.set_long(0, continuation)\nentered = first_replace(frame, stack_cursor=stack)\nchildren = {216932: dispatch_auxiliary_command_stage_fields, 218130: expand_glyph_tile_sequence_fields, 218232: calculate_glyph_row_layout_fields, 218256: select_glyph_bitmap_fields, 218290: expand_monochrome_glyph_byte_fields, 218314: upload_expanded_glyph_rows_fields, 218692: draw_auxiliary_text_panel_border_fields, 218778: draw_auxiliary_text_panel_rows_fields, 218866: upload_auxiliary_text_panel_glyphs_fields, 218944: draw_auxiliary_text_panel_markers_fields, 240310: decode_unmasked_literal_plane_fields, 240322: decode_high_plane_rows_fields, 243604: dispatch_repeating_scene_presentation_fields, 252652: initialize_object_scene_video_fields, 216886: load_active_packet_roster_fields}\nif target in children:\n    result = children[target](state, entered)\nelif target == 240334:\n    result = read_vdp_plane_rle_rows_fields(SceneRefreshMemory(state), entered)\nelif target == 240466:\n    result = write_vdp_swapped_byte_rle_stream_fields(SceneRefreshMemory(state), entered)\nelif target == 240532:\n    result = copy_scene_palette_variant_fields(SceneRefreshMemory(state), entered)\nelif target == 240266:\n    result = snapshot_and_clear_scene_palette_fields(SceneRefreshMemory(state), entered)\nelif target == 26830:\n    from ..high_level_gameplay_flow.business_services import clear_video_sprite_plane_fields\n    result = clear_video_sprite_plane_fields(SceneRefreshMemory(state), entered)\nelif target == 32906:\n    from ..high_level_gameplay_flow.business_services import enqueue_sound_command_fields\n    result = enqueue_sound_command_fields(SceneRefreshMemory(state), entered)\nelif target == 418260:\n    from ..high_level_dynamic_flows.business_actions import upload_portrait_tiles_frame_fields\n    result = upload_portrait_tiles_frame_fields(state, entered)\nelif target == 33736:\n    from ..high_level_gameplay_flow.business_services import wait_for_scene_sound_byte_fields\n    result = wait_for_scene_sound_byte_fields(SceneRefreshMemory(state), entered)\nelif target == 242312:\n    from ..high_level_scene_flows.business_objects import append_scene_center_marker_fields\n    result = append_scene_center_marker_fields(SceneRefreshMemory(state), entered)\nelif target == 239992:\n    from ..high_level_scene_flows.business_scene import advance_scene_palette_fade_fields\n    result = advance_scene_palette_fade_fields(SceneRefreshMemory(state), entered)\nelif target == 242236:\n    from ..high_level_scene_flows.business_scene import finish_actor_sprite_chains_fields\n    result = finish_actor_sprite_chains_fields(SceneRefreshMemory(state), entered)\nelif target in (211180, 211262, 211336, 211404, 211444, 211472, 211640, 212394, 213232) and continuation == 211158:\n    from ..high_level_ai_policy_v2.business_scene_routes import execute_march_policy_fields\n    result = execute_march_policy_fields(state, entered, target)\nelif target in (213312, 213424, 213694, 213878, 214078, 214120, 214330, 214520, 214600, 214634, 214704, 214810, 215166, 215342, 215538, 215596, 216016, 216074, 216402, 216482, 216526, 216834, 216842) and continuation == 213260:\n    from ..high_level_ai_policy_v2.business_scene_packet_policy import execute_packet_policy_fields\n    result = execute_packet_policy_fields(state, entered, target)\nelif target in (216980, 217188, 217320, 217394, 217428, 217506, 217616, 217734, 217922, 218044, 218092, 218100) and continuation == 216952:\n    from ..high_level_ai_policy_v2.business_scene_active_packets import execute_active_packet_fields\n    result = execute_active_packet_fields(state, entered, target)\nelse:\n    raise MovementContinuationBoundary(target, entered, 'auxiliary text child lacks a complete admitted frame')\nresult = _resource_cost_frame(state, result, target)\ntoken = result.stack_cursor.long()\nif token != continuation:\n    raise MovementContinuationBoundary(token, result, 'auxiliary text RTS slot changed')\nstate.sr = state.sr & 65504 | result.status\nreturn first_replace(result, stack_cursor=result.stack_cursor.advance(4))"}, 'load_active_packet_roster_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 216886)\nframe = first_replace(frame, roster=state.table_at(state.read(16726060, 4)).cursor(), candidates=state.table_at(4294965034).cursor())\nframe = _movement_move(state, frame, 'target_y', 0, 16)\nframe = _movement_move(state, frame, 'target_y', frame.roster.byte(0, 4), 8)\nframe = _setup_write_fields(state, frame, 4294964086, low16(frame.target_y))\nframe = _movement_move(state, frame, 'target_x', frame.roster.byte(), 8)\nframe = _movement_move(state, frame, 'target_x', low16(frame.target_x) & 15, 16)\nframe = _map_presentation_arithmetic_fields(state, frame, 'target_x', 1, True)\nwhile True:\n    frame = _movement_move(state, frame, 'target_y', 0, 16)\n    frame = _movement_move(state, frame, 'target_y', frame.roster.byte(low16(frame.target_x), 13), 8)\n    frame = _setup_write_fields(state, frame, frame.candidates.base, low16(frame.target_y))\n    frame = first_replace(frame, candidates=frame.candidates.advance(2))\n    frame, again = _map_presentation_db_fields(frame, 'target_x')\n    if not again:\n        break\nreturn _setup_write_fields(state, frame, frame.candidates.base, 65535)"}})

DECLARATIONS.update({'_city_assignment_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "children = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields, 59438: recover_unacted_officer_b200_fields, 59552: clear_unowned_debt_records_fields}\nif target == 201486:\n    from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields\n    return wait_command_intro_fields(state, frame)\nif target in children:\n    return children[target](state, frame)\nif target == 33748:\n    return first_deployment_random_fields(BattlePolicyMemory(state), frame)\nif target == 418532:\n    return advance_officer_growth_levels_fields(state, frame)\nif target == 71950:\n    from .business_gameplay import settle_city_projects_and_refresh_map_fields\n    return settle_city_projects_and_refresh_map_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')"}, '_clear_invalid_debt_record_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _setup_write_fields(state, frame, frame.roster.base, 0, 4, True)\nframe = _movement_move(state, frame, 'count', state.read(4294960896, 2), 16)\nrecord_mask = 1 << (low16(frame.target_x) & 31)\nframe = _map_presentation_bit_fields(state, frame, frame.count, record_mask)\nframe = first_replace(frame, count=frame.count & ~record_mask)\nreturn _setup_write_fields(state, frame, 4294960896, low16(frame.count))"}, 'clear_unowned_debt_records_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame', 'returns': 'FirstDeploymentFrame', 'flow': "frame = _resource_cost_frame(state, frame, 59552)\nframe = first_replace(frame, roster=state.table_at(4294961716).cursor(), candidates=state.table_at(4294964263).cursor())\nframe = _movement_move(state, frame, 'target_x', 15, 16)\nwhile True:\n    frame = _movement_move(state, frame, 'count', 0, 16)\n    frame = _movement_move(state, frame, 'count', frame.roster.byte(), 8)\n    if not frame.status & 4:\n        frame = _movement_test(state, frame, frame.candidates.byte(s16(low16(frame.count))), 8)\n        if frame.status & 8:\n            frame = _clear_invalid_debt_record_fields(state, frame)\n        else:\n            frame = _movement_move(state, frame, 'count', frame.roster.byte(0, 1), 8)\n            frame = _movement_test(state, frame, frame.candidates.byte(s16(low16(frame.count))), 8)\n            if frame.status & 8:\n                frame = _clear_invalid_debt_record_fields(state, frame)\n    frame = first_replace(frame, roster=frame.roster.advance(-4))\n    frame, more = _map_presentation_db_fields(frame, 'target_x')\n    if not more:\n        return frame"}})


# Source143: genuine high-plane BRA and five story JMP entries; physical owners unchanged.
DECLARATIONS.update({'decode_high_plane_rows_fields': {'flow': "frame = _resource_cost_frame(state, frame, 240322)\nframe = _setup_write_fields(state, frame, 4294934528, 32768)\nframe = _movement_move(state, frame, 'offset_y', 32, 16)\nfrom ..high_level_scene_flows.business_scene import read_vdp_plane_rle_rows_from_control_fields\nreturn read_vdp_plane_rle_rows_from_control_fields(SceneRefreshMemory(state), frame)", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame'}, 'dispatch_repeating_scene_presentation_fields': {'flow': "frame = _resource_cost_frame(state, frame, 243604)\nframe = _movement_move(state, frame, 'target_x', state.read(4294934746, 2), 16)\nframe = _setup_asl_word_fields(state, frame, 'target_x', 2)\ntarget = u32(243614 + s16(low16(frame.target_x)))\nif target in (243614, 243618, 243622, 243626, 243630):\n    from ..high_level_scene_flows.business_scene import _story_known_fields\n    return _story_known_fields(SceneRefreshMemory(state), frame, target)\nraise MovementContinuationBoundary(target, frame, 'computed presentation JMP entry requires its genuine owner facade')", 'returns': 'FirstDeploymentFrame', 'signature': 'state: SceneState, frame: FirstDeploymentFrame'}})
APPROVED.setdefault((2, 'high_level_scene_flows.business_scene'), set()).update(('read_vdp_plane_rle_rows_from_control_fields', '_story_known_fields'))

# B107 exact full-owner generator conversion; native lowerers remain original.
_setup_legacy_declaration176 = dict(DECLARATIONS['run_controller_setup_and_configuration_fields'])
APPROVED.setdefault('controller_setup_steps', set()).update(('run_controller_setup_blocking_fields',))
DECLARATIONS.update({'run_controller_setup_and_configuration_fields': {'flow': 'from .controller_setup_steps import '
                                                           'run_controller_setup_blocking_fields\n'
                                                           'return '
                                                           'run_controller_setup_blocking_fields(state, '
                                                           'frame)',
                                                   'returns': 'FirstDeploymentFrame',
                                                   'signature': 'state: SceneState, frame: '
                                                                'FirstDeploymentFrame'}})
_compile_source_before_setup_steps176 = compile_source


def compile_source(source):
    from pathlib import Path
    from .compiler_controller_setup_steps import admit_controller_setup_program
    current = Path(__file__).with_name('controller_setup_steps.py').read_text(encoding='utf-8')
    admit_controller_setup_program(current, _setup_legacy_declaration176)
    return _compile_source_before_setup_steps176(source)

# B109 finite312D8 table: real312D6 LONG is already owned by setup caller.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(['advance_command_notice_phase_fields', 'show_command_intro_fields', 'reset_command_intro_fields', 'confirm_command_map_origin_fields', 'open_command_selection_fields', 'show_command_selected_member_fields', 'initialize_command_choice_menu_fields', 'process_command_choice_menu_fields', 'show_command_policy_notice_fields', 'initialize_command_policy_menu_fields', 'process_command_policy_menu_fields', 'show_command_completion_fields', 'initialize_command_exit_menu_fields', 'process_command_exit_menu_fields', 'refresh_command_map_on_input_fields'])
DECLARATIONS.update({'_city_assignment_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 201464:\n    from ..high_level_remaining_flows.business_highbank import advance_command_notice_phase_fields\n    return advance_command_notice_phase_fields(state, frame)\nif target == 201512:\n    from ..high_level_remaining_flows.business_highbank import show_command_intro_fields\n    return show_command_intro_fields(state, frame)\nif target == 201528:\n    from ..high_level_remaining_flows.business_highbank import reset_command_intro_fields\n    return reset_command_intro_fields(state, frame)\nif target == 201536:\n    from ..high_level_remaining_flows.business_highbank import confirm_command_map_origin_fields\n    return confirm_command_map_origin_fields(state, frame)\nif target == 201596:\n    from ..high_level_remaining_flows.business_highbank import open_command_selection_fields\n    return open_command_selection_fields(state, frame)\nif target == 201638:\n    from ..high_level_remaining_flows.business_highbank import show_command_selected_member_fields\n    return show_command_selected_member_fields(state, frame)\nif target == 201660:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_choice_menu_fields\n    return initialize_command_choice_menu_fields(state, frame)\nif target == 201776:\n    from ..high_level_remaining_flows.business_highbank import process_command_choice_menu_fields\n    return process_command_choice_menu_fields(state, frame)\nif target == 202466:\n    from ..high_level_remaining_flows.business_highbank import show_command_policy_notice_fields\n    return show_command_policy_notice_fields(state, frame)\nif target == 202482:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_policy_menu_fields\n    return initialize_command_policy_menu_fields(state, frame)\nif target == 202602:\n    from ..high_level_remaining_flows.business_highbank import process_command_policy_menu_fields\n    return process_command_policy_menu_fields(state, frame)\nif target == 203092:\n    from ..high_level_remaining_flows.business_highbank import show_command_completion_fields\n    return show_command_completion_fields(state, frame)\nif target == 203108:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_exit_menu_fields\n    return initialize_command_exit_menu_fields(state, frame)\nif target == 203148:\n    from ..high_level_remaining_flows.business_highbank import process_command_exit_menu_fields\n    return process_command_exit_menu_fields(state, frame)\nif target == 203220:\n    from ..high_level_remaining_flows.business_highbank import refresh_command_map_on_input_fields\n    return refresh_command_map_on_input_fields(state, frame)\nchildren = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields, 59438: recover_unacted_officer_b200_fields, 59552: clear_unowned_debt_records_fields}\nif target == 201486:\n    from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields\n    return wait_command_intro_fields(state, frame)\nif target in children:\n    return children[target](state, frame)\nif target == 33748:\n    return first_deployment_random_fields(BattlePolicyMemory(state), frame)\nif target == 418532:\n    return advance_officer_growth_levels_fields(state, frame)\nif target == 71950:\n    from .business_gameplay import settle_city_projects_and_refresh_map_fields\n    return settle_city_projects_and_refresh_map_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')"}})

# B109 finite31006 table: real30FD6 LONG is already owned by setup caller.
APPROVED.setdefault((2, 'high_level_remaining_flows.business_highbank'), set()).update(['open_command_phase_dispatch_fields', 'open_assignment_menu_dispatch_fields', 'open_city_action_menu_dispatch_fields'])
DECLARATIONS.update({'_city_assignment_child_fields': {'signature': 'state: SceneState, frame: FirstDeploymentFrame, target: Long', 'returns': 'FirstDeploymentFrame', 'flow': "if target == 200716:\n    from ..high_level_remaining_flows.business_highbank import open_command_phase_dispatch_fields\n    return open_command_phase_dispatch_fields(state, frame)\nif target == 200724:\n    from ..high_level_remaining_flows.business_highbank import open_assignment_menu_dispatch_fields\n    return open_assignment_menu_dispatch_fields(state, frame)\nif target == 200732:\n    from ..high_level_remaining_flows.business_highbank import open_city_action_menu_dispatch_fields\n    return open_city_action_menu_dispatch_fields(state, frame)\nif target == 201464:\n    from ..high_level_remaining_flows.business_highbank import advance_command_notice_phase_fields\n    return advance_command_notice_phase_fields(state, frame)\nif target == 201512:\n    from ..high_level_remaining_flows.business_highbank import show_command_intro_fields\n    return show_command_intro_fields(state, frame)\nif target == 201528:\n    from ..high_level_remaining_flows.business_highbank import reset_command_intro_fields\n    return reset_command_intro_fields(state, frame)\nif target == 201536:\n    from ..high_level_remaining_flows.business_highbank import confirm_command_map_origin_fields\n    return confirm_command_map_origin_fields(state, frame)\nif target == 201596:\n    from ..high_level_remaining_flows.business_highbank import open_command_selection_fields\n    return open_command_selection_fields(state, frame)\nif target == 201638:\n    from ..high_level_remaining_flows.business_highbank import show_command_selected_member_fields\n    return show_command_selected_member_fields(state, frame)\nif target == 201660:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_choice_menu_fields\n    return initialize_command_choice_menu_fields(state, frame)\nif target == 201776:\n    from ..high_level_remaining_flows.business_highbank import process_command_choice_menu_fields\n    return process_command_choice_menu_fields(state, frame)\nif target == 202466:\n    from ..high_level_remaining_flows.business_highbank import show_command_policy_notice_fields\n    return show_command_policy_notice_fields(state, frame)\nif target == 202482:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_policy_menu_fields\n    return initialize_command_policy_menu_fields(state, frame)\nif target == 202602:\n    from ..high_level_remaining_flows.business_highbank import process_command_policy_menu_fields\n    return process_command_policy_menu_fields(state, frame)\nif target == 203092:\n    from ..high_level_remaining_flows.business_highbank import show_command_completion_fields\n    return show_command_completion_fields(state, frame)\nif target == 203108:\n    from ..high_level_remaining_flows.business_highbank import initialize_command_exit_menu_fields\n    return initialize_command_exit_menu_fields(state, frame)\nif target == 203148:\n    from ..high_level_remaining_flows.business_highbank import process_command_exit_menu_fields\n    return process_command_exit_menu_fields(state, frame)\nif target == 203220:\n    from ..high_level_remaining_flows.business_highbank import refresh_command_map_on_input_fields\n    return refresh_command_map_on_input_fields(state, frame)\nif target == 211138:\n    return dispatch_city_command_stage_fields(state, frame)\nif target == 213240:\n    return dispatch_map_packet_command_stage_fields(state, frame)\nchildren = {200618: run_city_command_assignment_fields, 200682: clear_unassigned_officer_commands_fields, 200740: run_city_command_states_fields, 200772: run_map_packet_command_states_fields, 200820: select_next_force_city_fields, 200878: select_next_force_map_packet_fields, 200976: sample_city_command_policy_fields, 201084: clear_current_city_project_orders_fields, 201126: build_current_city_officer_roster_fields, 201190: finish_city_command_assignment_fields, 201210: retain_city_command_stage_fields, 201416: dispatch_city_assignment_state_fields, 59438: recover_unacted_officer_b200_fields, 59552: clear_unowned_debt_records_fields}\nif target == 201486:\n    from ..high_level_remaining_flows.business_highbank import wait_command_intro_fields\n    return wait_command_intro_fields(state, frame)\nif target in children:\n    return children[target](state, frame)\nif target == 33748:\n    return first_deployment_random_fields(BattlePolicyMemory(state), frame)\nif target == 418532:\n    return advance_officer_growth_levels_fields(state, frame)\nif target == 71950:\n    from .business_gameplay import settle_city_projects_and_refresh_map_fields\n    return settle_city_projects_and_refresh_map_fields(state, frame)\nraise MovementContinuationBoundary(target, frame, 'original assignment child has no complete current field interface')"}})

# Exact first strategic directory; other two directories remain unsupported.
APPROVED.setdefault((2, 'high_level_ai_policy_v2.business_scene_routes'), set()).update({'execute_march_policy_fields'})


# Exact complete packet-policy closure; no native lowerer/role widening.
APPROVED.setdefault((2, 'high_level_ai_policy_v2.business_scene_packet_policy'),set()).update({'execute_packet_policy_fields'})

# Exact third active-packet directory; real34F78 LONG stays with its caller.
APPROVED.setdefault((2, 'high_level_ai_policy_v2.business_scene_active_packets'), set()).update({'execute_active_packet_fields'})
