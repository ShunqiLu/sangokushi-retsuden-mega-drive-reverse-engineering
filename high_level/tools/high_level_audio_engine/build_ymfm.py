"""用本地 YMFM 源码和 GNU 兼容 C++ 编译器构建桌面音频桥。"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


SOURCES = ('ymfm_opn.cpp', 'ymfm_adpcm.cpp', 'ymfm_ssg.cpp')
HEADERS = ('ymfm.h', 'ymfm_adpcm.h', 'ymfm_fm.h', 'ymfm_fm.ipp',
           'ymfm_opn.h', 'ymfm_ssg.h')
NOTICE = """# YMFM

此桌面音频桥使用 Aaron Giles 的 YMFM 芯片模型。
上游源码：https://github.com/aaronsgiles/ymfm

此目录中的 YMFM_LICENSE.txt 来自用于本次构建的上游源码，保留完整许可证。
"""


def build_library(compiler: Path, output: Path, *, ymfm_source: Path) -> Path:
    """构建 FM 音频桥，并把原样许可证和上游链接写入输出目录。"""
    compiler = compiler.resolve(strict=True)
    if not compiler.is_file():
        raise ValueError('choose an existing GNU-compatible C++ compiler executable')
    upstream = ymfm_source.resolve(strict=True)
    license_source = upstream / 'LICENSE'
    members = [upstream / 'src' / name for name in (*SOURCES, *HEADERS)]
    for member in (license_source, *members):
        if not member.is_file():
            raise ValueError(f'YMFM source root requires {member.relative_to(upstream)}')
    output = output.resolve()
    if output.is_relative_to(upstream) or output.exists():
        raise ValueError('choose a new output directory outside the YMFM source root')

    project = Path(__file__).resolve().parents[2]
    bridge = project / 'src/host_audio/ymfm_bridge.cpp'
    if not bridge.is_file():
        raise ValueError('this edition requires src/host_audio/ymfm_bridge.cpp')
    output.mkdir(parents=True, exist_ok=False)
    library = output / ('g5510_ymfm.dll' if sys.platform == 'win32' else 'libg5510_ymfm.so')
    # 固定的 ASCII 相对文件名兼容 MinGW，也允许上游源码位于其他磁盘。
    with TemporaryDirectory(prefix='ymfm-build-', dir=output) as temporary:
        work = Path(temporary)
        sources = work / 'ymfm'
        sources.mkdir()
        for member in members:
            shutil.copyfile(member, sources / member.name)
        shutil.copyfile(bridge, work / bridge.name)
        shutil.copyfile(license_source, work / 'LICENSE')
        command = [str(compiler), '-std=c++14', '-O2', '-shared']
        command += ['-static'] if sys.platform == 'win32' else ['-fPIC']
        command += ['-I', 'ymfm', bridge.name, *('ymfm/' + name for name in SOURCES),
                    '-o', library.name]
        subprocess.run(command, cwd=work, check=True)
        (work / library.name).rename(library)
        (work / 'LICENSE').rename(output / 'YMFM_LICENSE.txt')
    (output / 'YMFM_PROVENANCE.md').write_text(NOTICE, encoding='utf-8', newline='\n')
    return library


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', type=Path, required=True,
                        help='GNU 兼容 C++ 编译器的路径')
    parser.add_argument('--ymfm-source', type=Path, required=True,
                        help='含 LICENSE 和 src/ 的本地 YMFM 源码目录')
    parser.add_argument('--output', type=Path, required=True,
                        help='新的音频桥输出目录')
    args = parser.parse_args(argv)
    try:
        library = build_library(args.compiler, args.output, ymfm_source=args.ymfm_source)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'音频桥构建：{error}\n')
    print(library)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
