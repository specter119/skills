import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    orders = pl.DataFrame(
        {"status": ["open", "closed", "open"], "amount": [10, 20, 30]}
    )
    return (orders,)


@app.cell
def _(mo):
    status_filter = mo.ui.dropdown(["open", "closed"], value="open")
    return (status_filter,)


@app.cell
def _(mo, pl, orders, status_filter):
    status_orders = orders.filter(pl.col("status") == status_filter.value)
    mo.hstack([status_filter, status_orders])
    return (status_orders,)


if __name__ == "__main__":
    app.run()
