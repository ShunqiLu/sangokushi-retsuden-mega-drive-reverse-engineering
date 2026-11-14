"""Explicit CLI entry; --help/import does not construct the game or a UI."""
import argparse
import json
import sys
from pathlib import Path


def _close_resources(app, capture, outcome, *, debug, active_error):
    """Finish both owners in order; cleanup cannot hide a pending exception."""
    errors = []
    if app is not None:
        try:
            app.close(outcome='application_closed', evidence={'source': 'command_line_finally'})
        except BaseException as error:
            errors.append(('关闭运行资源失败', error))
    if capture is not None:
        capture_outcome = 'application_close_failed' if errors else outcome
        try:
            receipt = capture.close(outcome=capture_outcome)
            print('入口输入捕获收据：' + str(receipt) + '；仅收集输入，不代表通过验收。', file=sys.stderr)
        except BaseException as error:
            errors.append(('关闭入口捕获失败', error))
        try:
            print('入口输入捕获摘要：' + json.dumps(capture.summary(), ensure_ascii=False,
                allow_nan=False), file=sys.stderr)
        except BaseException as error:
            errors.append(('读取入口捕获摘要失败', error))
    for label, error in errors:
        print(f'{label}：{type(error).__name__}：{error}', file=sys.stderr)
        if active_error is not None:
            active_error.add_note(label + '：' + type(error).__name__ + '：' + str(error))
        if debug:
            import traceback
            traceback.print_exception(type(error), error, error.__traceback__)
    if active_error is None:
        for _, error in errors:
            if not isinstance(error, Exception):
                for label, other in errors:
                    if other is not error:
                        error.add_note(label + '：' + type(other).__name__ + '：' + str(other))
                raise error
    return bool(errors)


def main(argv=None):
    parser = argparse.ArgumentParser(description='运行重建游戏的统一入口（完整运行仍待验收）。')
    parser.add_argument('--config', type=Path, required=True, help='显式资源、存档权限和有限事件配置 JSON')
    parser.add_argument('--session-output', type=Path,
        help='可选：工程 build 内尚不存在且父目录已存在的新会话目录；只派生运行/诊断/WAV输出，不改输入或预算')
    parser.add_argument('--frontend', choices=('window', 'console'), default='window',
        help='正常前端：window（默认窗口）或 console（同一应用的有限 JSON 行交互）')
    event_output = parser.add_mutually_exclusive_group()
    event_output.add_argument('--capture-entries', type=Path,
        help='可选明确的有限入口输入捕获配置；默认关闭，不补状态／设备／游戏预算')
    event_output.add_argument('--page-scene-events', action='store_true',
        help='将当前场景的有序记录存到本次会话的新文件，降低长时间运行的内存占用')
    restarts = parser.add_mutually_exclusive_group()
    restarts.add_argument('--intro-restarts', type=Path, help='可选外置有限片头复位计划；不指定则不启用，不能扩充其它运行预算')
    restarts.add_argument('--narrative-restarts', type=Path, help='可选外置有限剧情退出复位计划；与片头IRQ复位计划择一')
    restarts.add_argument('--restarts', type=Path, help='可选外置有序片头/剧情联合复位计划；每项kind和有限供应均须明确')
    parser.add_argument('--debug', action='store_true', help='错误时显示完整技术堆栈')
    args = parser.parse_args(argv)
    app = None
    capture = None
    exit_code = 0
    capture_outcome = 'configuration_failed'
    try:
        from .config import load_runtime_config
        config = load_runtime_config(args.config, session_output=args.session_output)
        if args.frontend == 'console' and config.frontend.frame_plan is None:
            raise ValueError('控制台要求配置中已有完整 frontend.frame_plan；不自动转换 events 或补设备预算。')
        if args.capture_entries is not None:
            from .entry_capture_config import load_configured_entry_capture
            capture_outcome = 'capture_initialization_failed'
            capture = load_configured_entry_capture(args.capture_entries, project_root=config.project_root)
            capture.start()
        from .application import GameApplication
        capture_outcome = 'application_open_failed'
        journal_path = None
        if args.page_scene_events:
            journal_path = config.output.with_name(config.output.name + '-scene-events.bin')
        app = GameApplication.open(config, scene_journal_path=journal_path)
        capture_outcome = 'application_interrupted'
        if capture is not None:
            capture.attach_source_context(app.rig.source, app.rig.scene)
        if args.intro_restarts is not None:
            from .intro_restart_config import enable_configured_intro_restarts
            enable_configured_intro_restarts(app, args.intro_restarts)
        if args.narrative_restarts is not None:
            from .narrative_restart_config import enable_configured_narrative_restarts
            enable_configured_narrative_restarts(app, args.narrative_restarts)
        if args.restarts is not None:
            from .ordered_restart_config import enable_configured_ordered_restarts
            enable_configured_ordered_restarts(app, args.restarts)
        if args.frontend == 'console':
            from .console import run_console
            result = run_console(app, config.frontend)
        else:
            from .frontend import run_frontend
            result = run_frontend(app, config.frontend)
        exit_code = result.exit_code
        capture_outcome = 'application_completed' if exit_code == 0 else 'application_reported_failure'
    except Exception as error:
        print(f'未能完成启动或运行：{type(error).__name__}：{error}', file=sys.stderr)
        print('未自动补充资源、设备事件或存档；请检查配置及诊断记录。此结果不代表游戏通过验收。', file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        exit_code = 1
        capture_outcome = 'application_failed'
    finally:
        active_error = sys.exc_info()[1]
        if active_error is not None:
            capture_outcome = 'application_interrupted'
        if _close_resources(app, capture, capture_outcome, debug=args.debug, active_error=active_error):
            exit_code = 1
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
