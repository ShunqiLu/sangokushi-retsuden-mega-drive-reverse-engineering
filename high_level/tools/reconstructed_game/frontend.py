"""Small Tk frontend over actual recovered video and explicit finite events.

Importing this module creates no window and executes no game. The engine owns
all software/device state; this file owns only widgets, keyboard levels and the
cursor in a caller-declared event list. No implicit console clock is modeled.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import traceback
from uuid import uuid4

from .config import FrontendConfig, EventSpec
from .frame_plan import FiniteFramePlan
from ..high_level_input.hardware_controller import PadButtons
from ..high_level_video.frame_interrupts import VideoBusState, InterruptRequest
from ..high_level_video.integrated_scene_driver import PhysicalPadSnapshot
from ..high_level_video.render import RenderedFrame
from ..high_level_audio_engine.driver_startup import Im1ClockGrant


_BUTTON_NAMES = {
    'up': '上', 'down': '下', 'left': '左', 'right': '右',
    'a': 'A', 'b': 'B', 'c': 'C', 'start': '开始',
}
_EVENT_NAMES = {
    'irq': '外供中断', 'device': '设备事件',
    'audio_advance': '音频程序继续', 'audio_im1': '外供音频中断',
    'fm_clocks': 'FM 时钟', 'psg_clocks': 'PSG 时钟',
}


@dataclass(frozen=True)
class FrontendResult:
    status: str
    consumed_events: int
    total_events: int
    diagnostic_path: str | None
    error: str | None
    unit: str = 'events'

    @property
    def exit_code(self):
        # Exhaustion/normal close is not a claim of whole-game acceptance.
        return 1 if self.status == 'boundary' else 0


def _pad_changes(event, keymap, held_keys):
    """Replace only explicitly keyboard-owned ports in this IRQ declaration."""
    changes = {row.port: PhysicalPadSnapshot(row.port,
        PadButtons(**{name: True for name in row.buttons})) for row in event.pad_changes}
    for port in event.live_pad_ports:
        pressed = {binding.button for binding in keymap
            if binding.port == port and binding.key.casefold() in held_keys}
        changes[port] = PhysicalPadSnapshot(port,
            PadButtons(**{name: True for name in pressed}))
    return tuple(changes[port] for port in sorted(changes))


def _dispatch(app, event, keymap, held_keys):
    """Closed six-event adapter; the application remains the sole engine API."""
    if type(event) is not EventSpec:
        raise ValueError('one validated finite EventSpec required')
    if event.kind == 'irq':
        if event.video is None:
            raise ValueError('IRQ event requires its complete explicit video observation')
        return app.step_irq(InterruptRequest(event.level),
            bus_state=VideoBusState(event.video.status_without_dma,
                event.video.hv, event.video.open_bus),
            pad_changes=_pad_changes(event, keymap, held_keys))
    if event.kind == 'device':
        return app.step_device(event.event)
    if event.kind == 'audio_advance':
        return app.advance_audio()
    if event.kind == 'audio_im1':
        return app.deliver_im1(Im1ClockGrant(event.timestamp, event.clock_hz))
    if event.kind == 'fm_clocks':
        return app.advance_chips(fm_ticks=event.clocks, psg_input_clocks=0)
    if event.kind == 'psg_clocks':
        return app.advance_chips(fm_ticks=0, psg_input_clocks=event.clocks)
    raise ValueError('unsupported explicit frontend event: ' + str(event.kind))


def _diagnostic(directory, *, error, index, event, total, held_keys, stage):
    """Preserve one small new failure record; never overwrite prior evidence."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    name = 'frontend-boundary-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    path = directory / (name + '-' + uuid4().hex[:8] + '.json')
    # Continuation boundaries already retain the exact rejected destination.
    # Preserve that scalar without entering their Frame or reading Scene RAM;
    # a shared generic error message must not erase the actual call target.
    target = vars(error).get('target')
    if type(target) is not int or not 0 <= target <= 0xFFFFFFFF:
        target = None
    details = dict(format='g5510-reconstructed-frontend-boundary-v1', stage=stage,
        event_index=index, total_declared_events=total,
        attempted_event=None if event is None else asdict(event),
        keyboard_levels=sorted(held_keys), exception_type=type(error).__name__,
        boundary=str(error), traceback=''.join(traceback.format_exception(error)),
        boundary_target=target,
        boundary_target_hex=None if target is None else format(target, '08X'),
        boundary_target_source='actual_exception_retained_target_not_inferred',
        Scene_RAM_or_material_dump=False, host_ready_or_phase_writes=False,
        prefix_reentry=False, automatic_clock_relation=False)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(details, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return str(path)


class _GameWindow:
    """All callbacks stay on the owning game/Session/Tk thread."""
    def __init__(self, tk, root, app, config):
        self.tk, self.root, self.app, self.config = tk, root, app, config
        self.index, self.status = 0, 'paused'
        self._frame_plan = None if config.frame_plan is None else FiniteFramePlan(app, config.frame_plan)
        self.total = len(config.events) if config.frame_plan is None else config.frame_plan.max_frames
        self.unit = 'events' if config.frame_plan is None else 'frames'
        self.error = self.diagnostic_path = None
        self.closed = self.running = False
        self._after_id = self._photo = None
        self._keys = set()
        self._save_exports = []
        self._mapped_keys = {row.key.casefold() for row in config.keymap}
        root.title('复原游戏 · 实际显存画面')
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.bind('<KeyPress>', self._key_down)
        root.bind('<KeyRelease>', self._key_up)
        root.bind('<FocusOut>', self._focus_out)
        root.report_callback_exception = self._callback_failure
        self.canvas = tk.Canvas(root, width=1, height=1, highlightthickness=0, background='#202020')
        self.canvas.pack(padx=10, pady=(10, 4))
        self._image_item = self.canvas.create_image(0, 0, anchor='nw')
        self._status_text = tk.StringVar(master=root)
        tk.Label(root, textvariable=self._status_text, justify='left', wraplength=820).pack(
            fill='x', padx=10, pady=4)
        controls = tk.Frame(root)
        controls.pack(fill='x', padx=10, pady=4)
        self._start_button = tk.Button(controls, text='继续计划', command=self.start)
        self._start_button.pack(side='left')
        self._pause_button = tk.Button(controls, text='暂停', command=self.pause)
        self._pause_button.pack(side='left', padx=5)
        self._step_button = tk.Button(controls, text='单次推进', command=self.single_step)
        self._step_button.pack(side='left')
        self._extend_button = tk.Button(controls, text='延长帧计划', command=self.extend_frame_limit)
        self._extend_button.pack(side='left', padx=5)
        self._save_button = tk.Button(controls, text='导出存档', command=self.export_save)
        self._save_button.pack(side='left')
        tk.Button(controls, text='关闭', command=self.close).pack(side='right')
        keys = '；'.join('端口' + str(row.port + 1) + ' ' + row.key + '→'
            + _BUTTON_NAMES[row.button] for row in config.keymap)
        tk.Label(root, text='按键映射（配置文件可编辑）：' + keys, justify='left', wraplength=820).pack(
            fill='x', padx=10, pady=(4, 2))
        tk.Label(root, text='显示实际显存渲染。界面间隔不是游戏帧率；每次只消费一个声明事件或一个有限整帧。',
            justify='left', wraplength=820).pack(fill='x', padx=10, pady=(2, 10))
        self._update_status('已暂停；按“继续计划”或“单个事件”推进。')

    def _key_down(self, event):
        key = event.keysym.casefold()
        if key in self._mapped_keys:
            self._keys.add(key)

    def _key_up(self, event):
        self._keys.discard(event.keysym.casefold())

    def _focus_out(self, event):
        # A host focus observation changes keyboard levels only. No physical
        # snapshot is sent until a later declared live-pad IRQ consumes them.
        self.root.after_idle(self._clear_unfocused_keys)

    def _clear_unfocused_keys(self):
        if not self.closed and self.root.focus_get() is None:
            self._keys.clear()

    def _update_status(self, message):
        self._status_text.set(('帧 ' if self.unit == 'frames' else '事件 ') + str(self.index) + '/' + str(self.total)
            + '　' + message)
        disabled = 'disabled' if self.status in ('boundary', 'exhausted') else 'normal'
        self._start_button.configure(state=disabled)
        self._step_button.configure(state=disabled)
        self._extend_button.configure(state=('normal' if self._frame_plan is not None
            and self.status == 'exhausted' and not self.closed else 'disabled'))
        self._save_button.configure(state=('disabled' if self.closed
            or self.status == 'boundary' else 'normal'))

    def _cancel_tick(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def _display(self):
        frame = self.app.render()
        if type(frame) is not RenderedFrame:
            raise ValueError('application.render must return its exact actual RenderedFrame')
        rgb = bytearray(frame.width * frame.height * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = frame.rgba[0::4], frame.rgba[1::4], frame.rgba[2::4]
        ppm = ('P6\n' + str(frame.width) + ' ' + str(frame.height) + '\n255\n').encode('ascii') + bytes(rgb)
        photo = self.tk.PhotoImage(master=self.root, data=ppm, format='PPM')
        if self.config.scale != 1:
            photo = photo.zoom(self.config.scale, self.config.scale)
        self._photo = photo
        self.canvas.configure(width=frame.width * self.config.scale, height=frame.height * self.config.scale)
        self.canvas.itemconfigure(self._image_item, image=photo)

    def show_initial(self):
        try:
            self._display()
        except Exception as error:
            self._fail(error, 'initial_actual_render')

    def start(self):
        if self.closed or self.running or self.status in ('boundary', 'exhausted'):
            return
        self.running, self.status = True, 'running'
        self._update_status('执行已声明计划；不额外生成硬件事件。')
        self._after_id = self.root.after(self.config.timer_interval_ms, self._tick)

    def pause(self):
        self.running = False
        self._cancel_tick()
        if self.status not in ('boundary', 'exhausted'):
            self.status = 'paused'
            self._update_status('已暂停；原程序与设备状态保留。')

    def _tick(self):
        self._after_id = None
        if self.closed or not self.running:
            return
        self._advance_one()
        if self.running and not self.closed:
            self._after_id = self.root.after(self.config.timer_interval_ms, self._tick)

    def single_step(self):
        if self.closed or self.status in ('boundary', 'exhausted'):
            return
        self.pause()
        self._advance_one()

    def extend_frame_limit(self):
        """Ask for an explicit new total; never restart or refill the game."""
        if self.closed or self.running or self.status != 'exhausted' or self._frame_plan is None:
            return
        from tkinter import messagebox, simpledialog
        text = simpledialog.askstring('延长帧计划',
            '输入新的总帧上限，须大于 ' + str(self.total)
            + '。\n保留当前游戏；不增加声音文件、DMA或其它设备额度。', parent=self.root)
        if text is None:
            return
        value = text.strip()
        if not value or any(character not in '0123456789' for character in value) or len(value) > 18:
            messagebox.showerror('未修改计划', '请输入不超过18位的正整数总帧上限。', parent=self.root)
            return
        new_limit = int(value)
        if new_limit <= self.total:
            messagebox.showerror('未修改计划', '新的总帧上限必须大于当前上限。', parent=self.root)
            return
        try:
            self._frame_plan.extend_max_frames(new_limit)
            self.total = self._frame_plan.spec.max_frames
            self.status = 'paused'
            self._update_status('帧上限已明确延长，当前游戏状态保留；按“继续计划”后推进。')
        except Exception as error:
            self._fail(error, 'explicit_frame_limit_extension')

    def export_save(self):
        """Explicitly export the actual SRAM; never overwrite or resume a game."""
        if self.closed or self.status == 'boundary':
            return
        self.pause()
        from tkinter import filedialog, messagebox
        destination = filedialog.asksaveasfilename(parent=self.root,
            title='导出当前实际存档到新文件（不覆盖旧文件）',
            initialdir=str(self.app.config.project_root / 'build'),
            defaultextension='.srm', confirmoverwrite=False,
            filetypes=(('原始8192字节存档', '*.srm'), ('所有文件', '*')))
        if not destination:
            return
        try:
            path = self.app.export_save(destination)
        except (OSError, ValueError) as error:
            # Invalid destinations or an existing file are host I/O failures,
            # not failed game instructions. Keep the same paused live game.
            messagebox.showerror('未能导出存档', str(error)
                + '\n只允许工程 build 内的新文件；游戏未重启，旧文件未覆盖。', parent=self.root)
            return
        self._save_exports.append(str(path))
        self._update_status('已导出当前实际8192字节：' + str(path)
            + '。未覆盖输入存档；导出不表示原游戏已完成保存或存档有效。')

    def _advance_one(self):
        if self.index >= self.total:
            self._exhausted()
            return
        event = self.config.events[self.index] if self._frame_plan is None else self._frame_plan.spec
        try:
            if self._frame_plan is None:
                _dispatch(self.app, event, self.config.keymap, frozenset(self._keys))
                message = _EVENT_NAMES[event.kind] + '已消费。'
            else:
                self._frame_plan.step(pad_changes=_pad_changes(event, self.config.keymap, frozenset(self._keys)))
                message = '一个显式有限整帧已消费；没有推导硬件时序。'
            self.index += 1
            self._display()
            self._update_status(message)
            if self.index == self.total:
                self._exhausted()
        except Exception as error:
            self._fail(error, 'event_or_actual_render', event=event)

    def _exhausted(self):
        self.running, self.status = False, 'exhausted'
        self._cancel_tick()
        self._update_status('有限事件计划已用完，已停止。未自动补帧／时钟；这不表示整游戏已完成。')

    def _fail(self, error, stage, event=None):
        self.running, self.status, self.error = False, 'boundary', str(error)
        self._cancel_tick()
        try:
            self.diagnostic_path = _diagnostic(self.config.diagnostics_directory,
                error=error, index=self.index, event=event, total=self.total,
                held_keys=self._keys, stage=stage)
            saved = '\n详情已保存：' + self.diagnostic_path
        except Exception as save_error:
            saved = '\n保存详情失败：' + str(save_error)
            self.error += saved
        self._update_status('遇到边界，推进已停止；不重入或补状态。\n'
            + type(error).__name__ + '：' + str(error) + saved)

    def _callback_failure(self, kind, error, trace):
        # Tk otherwise prints callback failures and keeps advancing. Preserve
        # the actual exception, stop the queue, and keep the last real picture.
        self._fail(error.with_traceback(trace), 'Tk_callback')

    def close(self):
        if self.closed:
            return
        self.running = False
        self._cancel_tick()
        if self.status not in ('boundary', 'exhausted'):
            self.status = 'user_closed'
        try:
            self.app.close(outcome='frontend_' + self.status, evidence=dict(
                source='Tk_close', consumed_events=self.index, declared_events=self.total, unit=self.unit,
                diagnostic=self.diagnostic_path, boundary=self.error,
                explicit_save_exports=list(self._save_exports),
                explicit_frame_limit_extensions=[] if self._frame_plan is None
                    else list(self._frame_plan.limit_extensions)))
        except Exception as error:
            self._fail(error, 'application_close')
        finally:
            self.closed = True
            self.root.destroy()

    def result(self):
        return FrontendResult(self.status, self.index, self.total, self.diagnostic_path, self.error, self.unit)


def run_frontend(app, config: FrontendConfig) -> FrontendResult:
    """Create the one window explicitly; close the application on all exits.

    Failure cannot be resumed. Successful frame-limit exhaustion may be
    explicitly extended in place without changing any device supply or
    initialization. Changing hardware supplies still requires a new explicit
    application configuration, never reconstruction of a live prefix.
    """
    if type(config) is not FrontendConfig:
        # No unvalidated fallback diagnostics path is authorized. The CLI's
        # outer application finally owns this rejected call's cleanup.
        raise ValueError('one validated explicit FrontendConfig required')
    root = window = None
    try:
        import tkinter as tk
        root = tk.Tk()
        window = _GameWindow(tk, root, app, config)
        window.show_initial()
        root.mainloop()
        return window.result()
    except BaseException as error:
        if window is not None and not window.closed:
            window._fail(error, 'frontend_mainloop')
        elif window is None:
            details = None
            try:
                details = _diagnostic(config.diagnostics_directory, error=error,
                    index=0, event=None, total=(len(config.events) if config.frame_plan is None else config.frame_plan.max_frames), held_keys=(), stage='frontend_creation')
            finally:
                app.close(outcome='frontend_creation_failed', evidence=dict(
                    exception_type=type(error).__name__, boundary=str(error), diagnostic=details))
        raise
    finally:
        if window is not None and not window.closed:
            window.close()
        elif window is None and root is not None:
            root.destroy()
