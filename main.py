import os

from tree_utils.struct_tree_out import print_tree

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的目录
current_dir = os.path.dirname(current_file_path)
print_tree(current_dir)
