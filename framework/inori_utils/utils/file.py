# -*- coding: utf-8 -*-
# @Time        : 2024/4/26
# @Author      : liuboyuan
import os
import zipfile
import tarfile


def user_file_builder(root_folder, user_id, file_name):
    return os.path.join(root_folder, user_id, file_name)


def compress_directory(dir_path, output_zip_path):
    """
    将指定的目录及其所有内容压缩到指定的ZIP文件中。
    :param dir_path: 要压缩的目录路径
    :param output_zip_path: 输出ZIP文件的路径
    """
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                # 获取文件绝对路径
                abs_file_path = os.path.join(root, file)

                # 计算相对路径（相对于要压缩的根目录）
                arc_rel_path = os.path.relpath(abs_file_path, start=dir_path)

                # 添加文件到压缩包内，保持其目录结构
                zipf.write(abs_file_path, arcname=arc_rel_path)


def list_files(directory):
    """
    列出指定目录下的所有文件。

    :param directory: 要列出文件的目录路径
    """
    res = []
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    res.append(entry.name)
                    # print(entry.name)
    except FileNotFoundError:
        print(f"目录 '{directory}' 未找到。")
    finally:
        return res


def unzip_file(zip_file_path, output_folder):
    """
    解压zip文件到指定的文件夹。

    :param zip_file_path: zip文件的路径
    :param output_folder: 解压后文件存放的文件夹路径
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    print(f"文件已解压到: {output_folder}")
    os.remove(zip_file_path)



def untar_file(tar_file_path, output_folder):
    """
    解压tar文件到指定的文件夹。

    :param tar_file_path: tar文件的路径
    :param output_folder: 解压后文件存放的文件夹路径
    """
    with tarfile.open(tar_file_path, 'r:') as tar_ref:
        tar_ref.extractall(output_folder)
    print(f"文件已解压到: {output_folder}")
    os.remove(tar_file_path)