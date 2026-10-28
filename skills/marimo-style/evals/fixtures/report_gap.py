import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo
    import polars as pl


@app.cell
def _():
    orders = pl.DataFrame(
        {"channel": ["web", "store", "web"], "amount": [10, 20, 30]}
    )
    return (orders,)


@app.cell
def _(mo):
    channel = mo.ui.dropdown(["web", "store"], value="web")
    channel
    return (channel,)


@app.cell
def _(mo, orders):
    overall_total = orders["amount"].sum()
    mo.md(f"Unrelated overall total: {overall_total}")


@app.cell
def _(mo, pl, channel, orders):
    channel_orders = orders.filter(pl.col("channel") == channel.value)
    mo.md(f"Orders in selected channel: {channel_orders.height}")
    return (channel_orders,)


if __name__ == "__main__":
    app.run()
