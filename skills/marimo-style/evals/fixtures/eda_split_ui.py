import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo


@app.cell
def _(mo):
    min_amount = mo.ui.slider(0, 100)
    return (min_amount,)


@app.cell
def _(mo):
    region = mo.ui.dropdown(["north", "south"])
    return (region,)


@app.cell
def _(mo):
    show_outliers = mo.ui.checkbox()
    return (show_outliers,)


if __name__ == "__main__":
    app.run()
