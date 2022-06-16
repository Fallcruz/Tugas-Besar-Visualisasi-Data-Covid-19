import pandas as pd
from bokeh.io import curdoc
from plot.line import line_plot
from plot.bar import bar_plot
from bokeh.layouts import Column
from bokeh.models import Tabs

df = pd.read_csv('./data/covid_data.csv')
df = df.drop("Unnamed: 0", axis=1)

line_plot = line_plot(df)
bar_plot = bar_plot(df)

curdoc().add_root(Tabs(tabs=[line_plot, bar_plot]))