#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import io
import glob
import hashlib
import platform
import datetime


def main():

    parser = argparse.ArgumentParser(description='直下のファイルをいい感じにリネームするやーつ')
    parser.add_argument('parent_dir_path', help='リネームするファイルが格納されているディレクトリのパス')
    parser.add_argument('--join_by', help='ファイル名の各要素を接続する文字。デフォルトは「_」')
    parser.add_argument('--genre', help='ファイル名に付与するジャンル名。デフォルトは付与なし')
    parser.add_argument('--cname', help='[current DO NOT WORK]ファイル名に付与するキャラクター名。デフォルトは付与なし')
    parser.add_argument('--no_ext_normalize', help='拡張子を変換しません。デフォルトは拡張子を小文字に、jpegやtiffは3文字に変換されます。', action='store_true')
    parser.add_argument('--force', help='確認せずに実行。あんまりおすすめしません。', action='store_true')
    parser.add_argument('--show_all', help='変換した場合のテスト結果を表示します。リネームは行われません。', action='store_true')

    parsed_args = parser.parse_args()

    parent_dir_path = parsed_args.parent_dir_path

    if not os.path.exists(parent_dir_path):
        print("[ERROR] parent_dir_path is not exist.")
        return

    elif not os.path.isdir(parent_dir_path):
        print("[ERROR] parent_dir_path is exist, but not dir.")
        return

    # 対象ディレクトリ、ファイル数、
    print("=== welcome file_rename! ===")
    print('parent_dir_path : ' + parent_dir_path)
    include_files = glob.glob(os.path.join(parent_dir_path, "*"))
    print("file count      : " + str(len(include_files)))
    print("rename sample   :")
    if parsed_args.show_all:
        for idx, in_file in enumerate(include_files):
            print("\t" + "(" + str(idx+1) + "/" + str(len(include_files)) + ") " + os.path.basename(in_file) + " -> " + create_new_filename(in_file, parsed_args.join_by, parsed_args.genre, parsed_args.no_ext_normalize))
        return
    else:
        for in_file in include_files[:5]:
            print("\t" + os.path.basename(in_file) + " -> " + create_new_filename(in_file, parsed_args.join_by, parsed_args.genre, parsed_args.no_ext_normalize))
    
    # 実行可能かチェック
    if parsed_args.force:
        exec = True
    else:
        exec = question_to_execute()

    if exec:
        # print("RENAME!RENAME!RENAME!")

        for idx, in_file in enumerate(include_files):
            dirname  = os.path.dirname(in_file)
            basename = os.path.basename(in_file)
            newname  = create_new_filename(in_file, parsed_args.join_by, parsed_args.genre, parsed_args.no_ext_normalize)
            print("\t" + "(" + str(idx+1) + "/" + str(len(include_files)) + ") " + basename + " -> " + newname)
            rename_path_modify = os.path.join(dirname, newname)
            if os.path.exists(rename_path_modify):
                print("[duplicate file] plz check duplicate")
                cnt = 0
                while True:
                    cnt += 1
                    rename_path_modify = os.path.join(dirname, add_suffix_duplicate_file(newname, cnt))
                    print(cnt)
                    if not os.path.exists (rename_path_modify):
                        os.rename(os.path.join(dirname, basename), rename_path_modify)
                        break
            else:
                os.rename(os.path.join(dirname, basename), rename_path_modify)
                print("[rename] " + os.path.join(dirname, basename) + " -> " + rename_path_modify)
        return
    else:
        print("process abort.")
        return

def question_to_execute():
    while True:
        flg = input("ARE YOU SURE TO RENAME FILES INSIDE THIS DIRECTORY? [y/N]: ").lower()
        if flg in ['y', 'yes']:
            return True
        elif flg in ['n', 'no']:
            return False


def create_new_filename(target_file, join_str, genre, no_ext_normalize):
    filename_array = []

    file_ctime = ctime_2_yyyymmddhhmmss(target_file)
    file_md5   = calc_MD5(target_file)
    file_ext   = os.path.splitext(target_file)[1]


    if not genre is None:
        filename_array.append(genre)
    filename_array.append(file_ctime)
    filename_array.append(file_md5)

    if no_ext_normalize:
        ext = file_ext
    else:
        ext = ext_normalize(file_ext)

    if not join_str is None:
        return join_str.join(filename_array) + ext
    else:
        return "_".join(filename_array) + ext
    

def ctime_2_yyyymmddhhmmss(target_file):
    if platform.system() == 'Windows':
        ct = datetime.datetime.fromtimestamp(os.path.getctime(target_file))
        return ct.strftime('%Y%m%d%H%M%S')
    else:
        return "DO_NOT_SUPPORT_THIS_OPARATING_SYSTEM"

def calc_MD5(target_file):
    with open(target_file, 'rb') as f:
        fData = f.read()
        return hashlib.md5(fData).hexdigest()

def ext_normalize(ext):

    ext_lower = ext.lower()

    trans_dict = {
        ".jpeg": ".jpg",
        ".tiff": ".tif",
    }

    if ext_lower in trans_dict:
        return trans_dict[ext_lower]
    else:
        return ext_lower

def add_suffix_duplicate_file(filename, count):
    ext_dot_idx = filename.rfind(".")
    fn_1 = filename[:ext_dot_idx]
    fn_2 = filename[ext_dot_idx + 1 :]
    return fn_1 + "_duplicate_" + str(count) + "." + fn_2

if __name__ == "__main__":
    main()