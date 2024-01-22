import os

from tree_utils.struct_tree_out import print_tree

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的目录
current_dir = os.path.dirname(current_file_path)
path0 = r'D:\aprojectPython\pythonProject\bili_douyin_xhs_uploader'

print_tree(path0, exclude_dirs={'test', '__init__.py'})
