"""汇编版构建命令。"""


def main(argv=None):
    from .build import main as build_main
    return build_main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
