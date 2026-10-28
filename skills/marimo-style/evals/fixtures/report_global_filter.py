import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    sales = pl.DataFrame(
        {"region": ["north", "south", "north"], "amount": [10, 20, 30]}
    )
    return (sales,)


@app.cell
def _(mo):
    region = mo.ui.dropdown(["north", "south"], value="north")
    region
    return (region,)


@app.cell
def _(mo):
    mo.md("## Filtered view")


@app.cell
def _(pl, region, sales):
    region_sales = sales.filter(pl.col("region") == region.value)
    region_sales
    return (region_sales,)


@app.cell
def _(mo):
    mo.md("### Details")


@app.cell
def _(mo, region_sales):
    mo.md(f"Rows in scope: {region_sales.height}")


if __name__ == "__main__":
    app.run()
