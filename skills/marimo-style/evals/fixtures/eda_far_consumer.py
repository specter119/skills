import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    orders = pl.DataFrame({"amount": [5, 40, 90]})
    return (orders,)


@app.cell
def _(mo):
    cutoff = mo.ui.slider(0, 100, value=30)
    return (cutoff,)


@app.cell
def _(mo):
    mo.md("## Section A")


@app.cell
def _(mo):
    mo.md("## Section B")


@app.cell
def _(mo):
    mo.md("## Section C")


@app.cell
def _(cutoff, mo, orders, pl):
    kept_orders = orders.filter(pl.col("amount") > cutoff.value)
    mo.md(f"{kept_orders.height} rows kept")
    return (kept_orders,)


if __name__ == "__main__":
    app.run()
