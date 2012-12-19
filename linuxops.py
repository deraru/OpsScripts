#!/usr/bin/env python
# coding: utf-8
import shlex, subprocess

class Server:
    # 引数
    # command: コマンド
    # std_in: 内部利用の標準入力（オプション）
    # 戻り値
    # コマンド実行結果
    @classmethod
    def exec_pipe_command(self, command, std_in=None):
        # コマンドをトークン化する
        if not isinstance(command, list):
            args = shlex.split(command)
        else:
            args = command

        # パイプがある場合
        if '|' in args:
            # 最初のパイプの位置を取得
            i = args.index('|')
            # 標準入力が無い場合
            if std_in is None:
                # 最初のパイプまでを実行
                p = subprocess.Popen(args[:i], stdout=subprocess.PIPE)
            # 標準入力がある場合
            else:
                # 最初のパイプまでを実行
                p = subprocess.Popen(args[:i], stdin=std_in, stdout=subprocess.PIPE)
            # 最初のパイプ以降の部分で再帰呼び出し
            output = self.exec_pipe_command(args[i + 1:], p.stdout)

        # パイプが無い場合
        else:
            # 標準入力が無い場合
            if std_in is None:
                # そのまま実行
                p = subprocess.Popen(args, stdout=subprocess.PIPE)
            # 標準入力がある場合
            else:
                # そのまま実行
                p = subprocess.Popen(args, stdin=std_in, stdout=subprocess.PIPE)
            # 出力を取り出す
            output = p.communicate()[0]

        # 出力をリターン
        return output
