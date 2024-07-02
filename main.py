import os
import tkinter as tk


def get_directory_structure_(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(rootdir):
        folder = os.path.relpath(dirpath, rootdir)
        sub_dir = dir_structure
        if folder != ".":
            for part in folder.split(os.sep):
                sub_dir = sub_dir.setdefault(part, {})
        for dirname in dirnames:
            sub_dir[dirname] = {}
    return dir_structure


def get_directory_structure(root, max_depth=None):

    if max_depth is not None and max_depth < 1:
        return {}

    dir_structure = {}

    next_max_depth = None if max_depth is None else max_depth - 1
    try:
        for entry in os.scandir(root):
            if entry.is_dir():
                dir_structure[entry.path] = get_directory_structure(entry.path, next_max_depth)
    except PermissionError:
        # Handle the case where the program does not have permissions to access a directory
        print("DENIED:", root)
        return {}

    return dir_structure


def draw_directory_structure(canvas, dir_structure, x, y, depth=0, max_depth=None):
    """
    Draws the directory structure on the canvas up to a specified maximum depth
    """
    if max_depth is not None and depth > max_depth:
        return y

    for key, value in dir_structure.items():
        canvas.create_text(x + depth * 20, y, anchor=tk.NW, text=key, font=("Arial", 10))
        y += 20
        y = draw_directory_structure(canvas, value, x, y, depth + 1, max_depth)
    return y





def visualize_directory(rootdir, max_depth=None):
    """
    Visualizes the directory structure on a Tkinter canvas up to a specified maximum depth
    """
    global canvas, image_id

    dir_structure = get_directory_structure(rootdir, max_depth=max_depth)

    root = tk.Tk()
    root.title("Directory Structure Visualization")

    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)

    image_id = draw_directory_structure(canvas, dir_structure, 10, 10, max_depth=max_depth)

    canvas.bind('<Button-1>', start_drag)
    canvas.bind('<B1-Motion>', drag_image)

    root.mainloop()


def create_graphviz_representation(dir_structure, graph, parent=None):
    for key, value in dir_structure.items():
        node = f"{key}_{id(key)}"
        graph.node(node, key)
        if parent:
            graph.edge(parent, node)
        create_graphviz_representation(value, graph, node)

def visualize_directory_with_graphviz(rootdir, max_depth=None):
    dir_structure = get_directory_structure(rootdir, max_depth)

    dot = graphviz.Digraph(comment='Directory Structure')
    create_graphviz_representation(dir_structure, dot)

    dot.render('directory_structure', view=True, format='png')


def print_directory(rootdir, max_depth=None):
    dir_structure = get_directory_structure(rootdir, max_depth=max_depth)
    print_directory_structure(dir_structure)


# Set max_depth to the desired maximum depth
#

#print_directory('D:\\', max_depth=4)
visualize_directory_with_graphviz('D:/', max_depth=2)
#visualize_directory('D:\\', max_depth=2)


