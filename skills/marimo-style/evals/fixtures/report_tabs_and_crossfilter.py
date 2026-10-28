import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import altair as alt
    import polars as pl


@app.cell
def _():
    orders = pl.DataFrame({"amount": [5, 40, 90], "kind": ["a", "b", "a"]})
    return (orders,)


@app.cell
def _(mo):
    mo.md("## Cross-filter demo")


@app.cell
def _(alt, mo, orders):
    overview_chart = mo.ui.altair_chart(
        alt.Chart(orders.to_pandas()).mark_bar().encode(x="kind", y="amount")
    )
    overview_chart
    return (overview_chart,)


@app.cell
def _(mo, overview_chart):
    mo.md(f"Rows in current selection: {len(overview_chart.value)}")


@app.cell
def _(mo, orders):
    tabs = mo.ui.tabs({"Guide": mo.md("Pick bars above."), "Raw data": orders})
    tabs
    return (tabs,)


if __name__ == "__main__":
    app.run()
