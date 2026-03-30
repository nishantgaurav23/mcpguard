import typer

app = typer.Typer()


@app.command()
def main() -> None:
    print("MCPGuard CLI")


if __name__ == "__main__":
    app()
