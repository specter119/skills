import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    orders = pl.DataFrame(
        {"region": ["north", "south"], "amount": [10, 20]}
    )
    return (orders,)


@app.cell
def _(orders, pl):
    result = orders["amount"].sum()
    chart = orders.group_by("region").agg(pl.col("amount").sum())
    chart
    return (result, chart)


if __name__ == "__main__":
    app.run()
