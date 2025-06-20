import mrich
import ipywidgets
from ..requests.urls import STACKS
from ..requests.download import target_list, download_target
import re


def download():
    """UI for downloading targets from fragalysis"""
    _download_ui_1()


def _download_ui_1():
    """Create widgets to request target list"""

    mrich.h3("download target")

    ui_1 = ipywidgets.VBox()
    ui_main = ipywidgets.VBox([ui_1])

    output = ipywidgets.Output()

    w_stack = ipywidgets.Dropdown(
        options=STACKS.keys(),
        value="production",
        description="Stack",
    )

    w_token = ipywidgets.Password(description="Token")

    b_get_targets = ipywidgets.Button(
        description="Get target list",
    )

    def button_func(button):
        with output:
            _download_ui_2(ui_main=ui_main, token=w_token.value, stack=w_stack.value)

    b_get_targets.on_click(button_func)

    ui_1.children = [w_stack, w_token, b_get_targets, output]

    display(ui_main)


def _download_ui_2(ui_main, stack: str, token: str | None = None):
    """widgets to request target download"""

    output = ipywidgets.Output()

    ui_2 = ipywidgets.VBox()

    with mrich.loading("Getting targets..."):
        targets = target_list(token=token, stack=stack)

    options = sorted((f"{d[1]} ({d[2]})" for d in targets))

    w_target = ipywidgets.Dropdown(
        options=options,
        description="Target",
    )

    w_destination = ipywidgets.Text(description="Destination", value="..")

    b_download = ipywidgets.Button(
        description="Download",
    )

    def button_func(button):
        with output:
            match = re.search(r"^(.*) \((lb[0-9]*-[0-9]*)\)$", w_target.value)

            name, tas = match.groups()

            download_target(
                name=name,
                tas=tas,
                stack=stack,
                token=token,
                destination=w_destination.value,
            )

    b_download.on_click(button_func)

    ui_2.children = [w_target, w_destination, b_download, output]
    ui_main.children = [ui_main.children[0], ui_2]
