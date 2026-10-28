import marimo

__generated_with = "0.17.0"
app = marimo.App()

with app.setup:
    import marimo as mo


@app.cell
def _():
    city_options = {"US": ["NYC", "SF"], "CA": ["Toronto", "Banff"]}
    return (city_options,)


@app.cell
def _(mo):
    country = mo.ui.dropdown(["US", "CA"], value="US")
    return (country,)


@app.cell
def _(city_options, country, mo):
    city = mo.ui.dropdown(city_options[country.value])
    return (city,)


if __name__ == "__main__":
    app.run()
