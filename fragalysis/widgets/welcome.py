
import mrich
import ipywidgets
import subprocess

TEMPLATE_SOURCE = "/home/code/templates" # production location
# TEMPLATE_SOURCE = "/home/jovyan/templates" # dev location

FRAGALYSIS_SOURCE = "/home/code/fragalysis" # production location
# FRAGALYSIS_SOURCE = "/home/jovyan/fragalysis" # dev location

def templates():
    """Homepage UI with buttons for managing template notebooks"""

    mrich.h3("Get template notebooks")

    ui_1 = ipywidgets.VBox()
    ui_main = ipywidgets.VBox([ui_1])
    output = ipywidgets.Output()

    TEMPLATE_BUTTONS = [
        ("download", "Download a fragalysis target", "download"),
        ("ligand_cif", "Create ligand CIF", "file"),
    ]

    widgets = []
    for name, description, icon in TEMPLATE_BUTTONS:
        w = ipywidgets.Button(
            description=description,
            icon=icon,
            layout={'width': 'max-content'}
        )

        def button_func(button, template_name=name):
            with output:
                _copy_template(template_name)
    
        w.on_click(button_func)
        
        widgets.append(w)

    ui_1.children = widgets
    
    ui_main.children = [ui_1, output]

    display(ui_main)

def _copy_template(name, destination="/home/jovyan/"):

    args = [
        "cp",
        "-v",
        f"{TEMPLATE_SOURCE}/{name}.ipynb",
        destination,
    ]

    subprocess.run(args)

def manage():
    """Homepage UI with buttons for managing git repos"""

    mrich.h3("Update repositories")

    ui_1 = ipywidgets.VBox()
    ui_main = ipywidgets.VBox([ui_1])
    output = ipywidgets.Output()

    TEMPLATE_BUTTONS = [
        (TEMPLATE_SOURCE, "Template notebooks"),
        (FRAGALYSIS_SOURCE, "Fragalysis Python package"),
    ]

    widgets = []
    for path, description in TEMPLATE_BUTTONS:
        w = ipywidgets.Button(
            description=description,
            # icon=icon,
            layout={'width': 'max-content'}
        )

        def button_func(button, repo_path=path):
            with output:
                _update_repo(repo_path)
    
        w.on_click(button_func)
        
        widgets.append(w)

    ui_1.children = widgets
    
    ui_main.children = [ui_1, output]

    display(ui_main)

def _update_repo(path):
    cmd = f"cd {path} && git pull"
    subprocess.run(cmd, shell=True)