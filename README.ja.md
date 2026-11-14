# 三国志列伝 乱世の英雄たち · メガドライブのリバースエンジニアリング

[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **日本語** · [English](README.en.md)

**Sangokushi Retsuden: Ransei no Eiyuutachi** · 繁体字中国語版カートリッジ `G-5510-00`

アセンブリ言語と高水準言語で再構築したコードを公開しています。この版を対象に、アセンブリと Python の両方でビルド可能なソースコードを公開する初のプロジェクトです。

## ソースコード

- [アセンブリ](assembly/README.md)：68000 のメインプログラム、Z80 のサウンドドライバー、カートリッジのアドレス配置。[編集ガイド](assembly/EDITING.md)も参照してください。
- [Python](high_level/README.md)：内政、武将、行軍、戦闘、AI、サウンドなどのゲームルールとコンパイラ。[編集ガイド](high_level/EDITING.md)と[元のアドレスの索引](high_level/PENDING_SOURCE_INDEX.md)を用意しています。

## 解析ツール

[解析ツール](reverse_tools/README.md)は、BIN と SMD の相互変換、カートリッジヘッダーの確認、68000 と Z80 の逆アセンブル、MAME の実行トレースに対応しています。グラフィック、音声、シナリオ、SRAM セーブデータも解析できます。

## ビルド

どちらのソースからもメガドライブ用の `SANGO.bin` と `SANGO.smd` をビルドできます。ビルドには Windows と WSL、Python 3.12 以降、Pillow、M68K 対応の Capstone 5、68000 と Z80 用の GNU クロスツールを使います。

`--resource-root` には、`assets/` と `resources/` が直下にある互換[素材パック](high_level/ASSETS.md)のディレクトリを指定します。コマンドは[アセンブリ版](assembly/README.md)と [Python 版](high_level/README.md)を参照してください。
