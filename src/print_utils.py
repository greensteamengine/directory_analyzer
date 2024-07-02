def print_dir(root_node):
    for node, depth in root_node.subtree_iterator(include_depth=True):
        print_sequence = "   " * depth + f"{node.name}"
        if node.size is not None:
            print_sequence += f" [{node.size}B]"
        print(print_sequence)