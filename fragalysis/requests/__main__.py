import mrich
from typer import Typer

app = Typer()


@app.command()
def target_uploads(
    stack: str = "production",
    token: str | None = None,
    statistics_only: bool = False,
    output: str | None = None,
) -> None:
    """
    Get information for targets uploaded to Fragalysis

    :param stack: Only v2 stacks supported
    :param token: Optional authentication token
    :param statistics_only: Return statistics only
    :param output: Optional path to write pickle data to, if None will print to console
    """

    from .download import target_uploads

    mrich.h1("target_uploads")
    mrich.var("stack", stack)
    mrich.var("token", token)
    mrich.var("statistics_only", statistics_only)
    mrich.var("output", output)
    data = target_uploads(stack=stack, token=token, statistics_only=statistics_only)

    if not output:
        mrich.print(data)
    else:
        import pickle

        mrich.writing(output)
        pickle.dump(data, open(output, "wb"))


@app.command()
def download_target_uploads(
    name: str,
    tas: str,
    index: int | None = None,
    stack: str = "production",
    token: str | None = None,
    # statistics_only: bool = False,
    destination: str | None = None,
):

    from .download import download_target_uploads

    mrich.h1("download_target_uploads")
    mrich.var("name", name)
    mrich.var("tas", tas)
    mrich.var("index", index)
    mrich.var("stack", stack)
    mrich.var("token", token)
    mrich.var("destination", destination)

    download_target_uploads(name=name, tas=tas, index=index, stack=stack, token=token)


if __name__ == "__main__":
    app()
