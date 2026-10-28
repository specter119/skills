import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    sales = pl.DataFrame(
        {"region": ["north", "south", "east"], "amount": [10, 20, 30]}
    )
    return (sales,)


@app.cell
def _(mo, sales):
    total_amount = sales["amount"].sum()
    mo.md(f"## Sales overview — total amount: {total_amount}")


@app.cell
def _(mo):
    region_filter = mo.ui.dropdown(["north", "south", "east"], value="north")
    region_filter
    return (region_filter,)


@app.cell
def _(mo, pl, region_filter, sales):
    region_sales = sales.filter(pl.col("region") == region_filter.value)
    mo.md(f"Rows in selected region: {region_sales.height}")
    return (region_sales,)


@app.cell
def _(mo):
    mo.md("### Notes\n\nStatic narrative that does not depend on any cell.")


@app.cell
def _(mo, sales):
    region_counts = sales["region"].value_counts()
    region_counts
    return (region_counts,)


if __name__ == "__main__":
    app.run()
