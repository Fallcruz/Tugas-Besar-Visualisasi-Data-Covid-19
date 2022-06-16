import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show, reset_output
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot, Column
from bokeh.models import Slider, Select
from bokeh.transform import dodge
from bokeh.io import show
from bokeh.models import Slider, Select, DateRangeSlider
from datetime import datetime

data_covid = pd.read_csv('./data/covid_data.csv')
data_covid = data_covid.drop("Unnamed: 0", axis=1)
data_covid['tanggal'] = pd.to_datetime(data_covid['tanggal']).dt.date

# Data Kasus Per Provinsi
Jawabarat = data_covid[data_covid['PROVINSI'] == 'JAWA BARAT'][['KASUS','SEMBUH','MENINGGAL']]
Jawatengah = data_covid[data_covid['PROVINSI'] == 'JAWA TENGAH'][['KASUS','SEMBUH','MENINGGAL']]
Jawatimur = data_covid[data_covid['PROVINSI'] == 'JAWA TIMUR'][['KASUS','SEMBUH','MENINGGAL']]
Jakarta = data_covid[data_covid['PROVINSI'] == 'DKI JAKARTA'][['KASUS','SEMBUH','MENINGGAL']]
Banten = data_covid[data_covid['PROVINSI'] == 'BANTEN'][['KASUS','SEMBUH','MENINGGAL']]
Bali = data_covid[data_covid['PROVINSI'] == 'BALI'][['KASUS','SEMBUH','MENINGGAL']]

province = ['Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'DKI Jakarta', 'Banten', 'Bali']
case = [int(Jawabarat['KASUS'].sum()),
        int(Jawatengah['KASUS'].sum()),
        int(Jawatimur['KASUS'].sum()), 
        int(Jakarta['KASUS'].sum()), 
        int(Banten['KASUS'].sum()), 
        int(Bali['KASUS'].sum())]
heal = [int(Jawabarat['SEMBUH'].sum()), 
        int(Jawatengah['SEMBUH'].sum()), 
        int(Jawatimur['SEMBUH'].sum()), 
        int(Jakarta['SEMBUH'].sum()), 
        int(Banten['SEMBUH'].sum()), 
        int(Bali['SEMBUH'].sum())]
death = [int(Jawabarat['MENINGGAL'].sum()), 
        int(Jawatengah['MENINGGAL'].sum()), 
        int(Jawatimur['MENINGGAL'].sum()), 
        int(Jakarta['MENINGGAL'].sum()), 
        int(Banten['MENINGGAL'].sum()), 
        int(Bali['MENINGGAL'].sum())]

source = ColumnDataSource(data=dict(province=province, case=case, heal=heal, death=death, color=Spectral6))

def date_range(df, start, end):
    df = df.loc[(df['tanggal'] >= start) & (df['tanggal'] <= end)]
    return df

def update_plot_bar(attr, old, new):
    # Change range of data
    start = date_range_slider.value_as_date[0]
    end = date_range_slider.value_as_date[1]
    df = date_range(data_covid, start, end)
    
    # Data Kasus Per Provinsi
    Jawabarat = df[df['PROVINSI'] == 'JAWA BARAT'][['KASUS','SEMBUH','MENINGGAL']]
    Jawatengah = df[df['PROVINSI'] == 'JAWA TENGAH'][['KASUS','SEMBUH','MENINGGAL']]
    Jawatimur = df[df['PROVINSI'] == 'JAWA TIMUR'][['KASUS','SEMBUH','MENINGGAL']]
    Jakarta = df[df['PROVINSI'] == 'DKI JAKARTA'][['KASUS','SEMBUH','MENINGGAL']]
    Banten = df[df['PROVINSI'] == 'BANTEN'][['KASUS','SEMBUH','MENINGGAL']]
    Bali = df[df['PROVINSI'] == 'BALI'][['KASUS','SEMBUH','MENINGGAL']]

    new_case = [int(Jawabarat['KASUS'].sum()),
                int(Jawatengah['KASUS'].sum()),
                int(Jawatimur['KASUS'].sum()), 
                int(Jakarta['KASUS'].sum()), 
                int(Banten['KASUS'].sum()), 
                int(Bali['KASUS'].sum())]
    new_heal = [int(Jawabarat['SEMBUH'].sum()), 
                int(Jawatengah['SEMBUH'].sum()), 
                int(Jawatimur['SEMBUH'].sum()), 
                int(Jakarta['SEMBUH'].sum()), 
                int(Banten['SEMBUH'].sum()), 
                int(Bali['SEMBUH'].sum())]
    new_death = [int(Jawabarat['MENINGGAL'].sum()), 
                int(Jawatengah['MENINGGAL'].sum()), 
                int(Jawatimur['MENINGGAL'].sum()), 
                int(Jakarta['MENINGGAL'].sum()), 
                int(Banten['MENINGGAL'].sum()), 
                int(Bali['MENINGGAL'].sum())]

    new_data = dict(province=province, case=new_case, heal=new_heal, death=new_death, color=Spectral6)
    source.data = new_data

def make_bar_plot_1(source, tooltips):
    fig = figure(x_range=province, 
                height=500, 
                width=1000, 
                title="Kasus Covid-19 Di Provinsi Besar Pulau Jawa", 
                tooltips=tooltips)

    fig.vbar(x = 'province',
            top = 'case',
            width = .9,
            color = 'color',
            legend_field = 'province',
            source = source,
            fill_alpha = .7,
            line_alpha = .5,
            line_color='green',
            line_dash='dashed')

    fig.xaxis.axis_label="Provinsi"
    fig.yaxis.axis_label="Kasus"
    fig.legend.orientation = "vertical"
    fig.legend.location = "top_right"

    return fig

def make_bar_plot_2(source, tooltips):
    fig = figure(x_range=province, 
                height=500, 
                width=1000, 
                title="Perbandingan Kasus Sembuh dan Meninggal",
                tooltips=tooltips)

    fig.vbar(x=dodge('province', -0.23, range=fig.x_range), 
            top='heal', 
            width=0.4, 
            source=source,
            color="#94eb52", 
            legend_label="Sembuh",
            fill_alpha = .7,
            line_alpha = .5,
            line_color='green',
            line_dash='dashed')

    fig.vbar(x=dodge('province', 0.23, range=fig.x_range), 
            top='death', 
            width=0.4, 
            source=source,
            color="#e84d60", 
            legend_label="Meninggal",
            fill_alpha = .7,
            line_alpha = .5,
            line_color='green',
            line_dash='dashed')

    fig.xaxis.axis_label="Provinsi"
    fig.yaxis.axis_label="Total"
    fig.legend.orientation = "vertical"
    fig.legend.location = "top_right"

    return fig

# tooltips
tooltips_bar1 = [
            ("Provinsi", '@province'),
            ("Jumlah Kasus", '@case')]
tooltips_bar2 = [
            ("Provinsi", '@province'),
            ("Jumlah Kasus", '@case'),
            ("Total Sembuh", '@heal'),
            ("Total Meninggal", '@death')]

# Create Bar Plot
bar1 = make_bar_plot_1(source, tooltips_bar1)
bar2 = make_bar_plot_2(source, tooltips_bar2)

tanggal = data_covid['tanggal'].unique()
tanggal = pd.to_datetime(tanggal)
tanggal = tanggal.sort_values()

date_range_slider = DateRangeSlider(
    title="Date Range", start=min(tanggal), end=max(tanggal),
    value=(min(tanggal), max(tanggal)), step=1, width=1000)

date_range_slider.on_change("value", update_plot_bar)

# layout = row(bar1)
curdoc().add_root(Column(row(date_range_slider), bar1, bar2))