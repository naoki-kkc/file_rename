import tkinter as tk
import tkinterdnd2 as tkdnd2
import os

# labelにドロップされた時に呼ばれる関数
def after_drop(event):
    # print(event.data)
    path_str = event.data
    
    # パスの種類で実行ボタンの有効/無効を制御
    if os.path.isdir(path_str):
        label_text.set(path_str)
        exec_button['state'] = tk.NORMAL
    else:
        label_text.set('ドロップされたパスはディレクトリではありません')
        exec_button['state'] = tk.DISABLED

# root = tk.Tk()
root = tkdnd2.Tk() # ドラッグ&ドロップを実現するため、tkinterdnd2でメインウインドウを作成

root.title('file_rename') # タイトル
root.geometry('600x150')  # 画面サイズ

# ドラッグドロップ用ラベルを作成
root.drop_target_register(tkdnd2.DND_FILES) # ドロップ対象はファイル
root.dnd_bind('<<Drop>>', after_drop)       # ドロップされたイベントを検知

# ラベル部分　
label_text = tk.StringVar(root)
label_text.set('ウインドウ内にファイルをドロップするとファイルパスを表示します')
label = tk.Label(root, textvariable=label_text)

# 実行ボタン/終了ボタン
exec_button  = tk.Button(root, text='実行', width=30, state=tk.DISABLED)
close_button = tk.Button(root, text='終了', width=30, state=tk.NORMAL)

# レイアウト
label.grid(row=0, column=0, padx=10)
exec_button.grid(row=1, column=0, padx=20)
close_button.grid(row=1, column=1, padx=10)

# 画面表示
root.mainloop()