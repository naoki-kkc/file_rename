import tkinter as tk
import tkinterdnd2 as tkdnd2

# labelにドロップされた時に呼ばれる関数
def after_drop(event):
    # print(event.data)
    label_text.set(event.data)

# root = tk.Tk()
root = tkdnd2.Tk() # ドラッグ&ドロップを実現するため、tkinterdnd2でメインウインドウを作成

root.title('file_rename') # タイトル
root.geometry('300x300')  # 画面サイズ

# ドラッグドロップ用ラベルを作成
root.drop_target_register(tkdnd2.DND_FILES) # ドロップ対象はファイル
label_text = tk.StringVar(root)
label_text.set('ファイルをドロップするとファイルパスを表示します')
label = tk.Label(root, textvariable=label_text)
label.drop_target_register(tkdnd2.DND_FILES)
label.dnd_bind('<<Drop>>', after_drop)
label.grid(row=0, column=0, padx=10)

# 画面表示
root.mainloop()