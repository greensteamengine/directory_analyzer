import os
from typing import Self
from bisect import insort_left


class FileSystemNode(object):

    @staticmethod
    def build_directory_tree(root_path, max_depth=None, use_filter=False):

        def should_include(tested_path):
            return not use_filter or not os.path.basename(tested_path).startswith('.')

        if max_depth is not None and max_depth < 1:
            return None

        root_node = FileSystemNode(root_path, None)

        next_max_depth = None if max_depth is None else max_depth - 1
        if next_max_depth > 0:
            try:
                for entry in os.scandir(root_path):
                    if should_include(entry.path):
                        new_child_node = FileSystemNode(entry.path, root_node)
                        root_node.add_child(new_child_node)
                        if entry.is_dir():
                            new_child_node.build_directory_tree(entry.path, next_max_depth, use_filter)

            except PermissionError:
                # Handle the case where the program does not have permissions to access a directory
                print(f"Permission denied: {root_path}")

        return root_node

    def __init__(self, path, parent):
        self.__path = path
        self.__children = []
        self.__parent = parent

        self.size = None
        self.__type = None

        if os.path.isdir(path):
            self.__type = 'dir'
        elif os.path.isfile(path):
            self.__type = 'file'
            self.size = os.path.getsize(path)

    def __lt__(self, other):
        return self.name < other.name

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children

    def add_child(self, child_node: Self):
        insort_left(self.__children, child_node)

    @property
    def name(self):
        return os.path.basename(self.__path)

    @property
    def dir(self):
        return os.path.dirname(self.__path)

    def subtree_iterator(self, include_depth=False):
        stack = [(self, 0)]
        while stack:
            current_node, node_depth = stack.pop()
            if include_depth:
                yield current_node, node_depth
            else:
                yield current_node
            child_data = [(node, node_depth+1) for node in current_node.children]
            stack.extend(reversed(child_data))

    def calculate_tree_node_sizes(self):
        if self.__type == 'dir':
            total_size = 0
            for child_node in self.__children:
                total_size += child_node.calculate_size()
            self.size += total_size
        return self.size
