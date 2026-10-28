import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.function
def above_cutoff(frame, limit):
    return frame.filter(pl.col("amount") > limit)


@app.cell
def _(mo, kept_orders):
    mo.md(f"Orders above cutoff: {kept_orders.height}")


@app.cell
def _(mo):
    cutoff = mo.ui.slider(0, 100, value=25)
    cutoff
    return (cutoff,)


@app.cell
def _(above_cutoff, cutoff, orders):
    kept_orders = above_cutoff(orders, cutoff.value)
    return (kept_orders,)


@app.cell
def _():
    orders = pl.DataFrame({"amount": [5, 40, 90]})
    return (orders,)


if __name__ == "__main__":
    app.run()
