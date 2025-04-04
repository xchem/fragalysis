import mrich
import ipywidgets

# import hippo


def knitwork():
    """UI for running fragment knitwork"""
    _knitwork_ui_1()


def _knitwork_ui_1():

    mrich.h3("fragment knitwork")

    output = ipywidgets.Output()

    ui_1 = ipywidgets.VBox()
    ui_main = ipywidgets.VBox([ui_1])

    w_db = ipywidgets.Text(
        description="HIPPO DB", value="", placeholder="target.sqlite"
    )

    w_get_animal = ipywidgets.Button(description="Get HIPPO animal")

    def button_func(button):
        with output:
            _knitwork_ui_2(
                ui_main=ui_main,
                db=w_db.value,
            )

    w_get_animal.on_click(button_func)

    ui_1.children = [w_db, w_get_animal, output]

    display(ui_1)


def _knitwork_ui_2(ui_main, db):

    if not db:
        mrich.error("No database specified")
        return

    with mrich.loading("Loading hippo..."):
        import hippo

    animal = hippo.HIPPO("Knitwork", db)

    # output = ipywidgets.Output()

    # ui_2 = ipywidgets.VBox()

    # ui_2.children = [w_target, w_destination, b_download, output]
    # ui_main.children = [ui_main.children[0], ui_2]
