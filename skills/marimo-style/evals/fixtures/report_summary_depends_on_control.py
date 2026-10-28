import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _(mo, above_threshold):
    mo.md(f"## Summary — rows above threshold: {above_threshold.height}")


@app.cell
def _():
    orders = pl.DataFrame({"amount": [5, 40, 90]})
    return (orders,)


@app.cell
def _(mo):
    min_amount = mo.ui.slider(0, 100, value=20)
    min_amount
    return (min_amount,)


@app.cell
def _(min_amount, orders, pl):
    above_threshold = orders.filter(pl.col("amount") > min_amount.value)
    return (above_threshold,)


if __name__ == "__main__":
    app.run()
