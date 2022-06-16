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
from bokeh.models import CustomJS, Select, DatePicker

def make_column_data_source(df):
    return ColumnDataSource(data={
        'tanggal' : df[df['PROVINSI']== 'ACEH']['tanggal'],
        'KASUS' : df[df['PROVINSI']== 'ACEH']['KASUS'],
        'SEMBUH' : df[df['PROVINSI']== 'ACEH']['SEMBUH'],
    })

def make_line_plot(source, hover_tool, start, end):
    # Generate canvas
    fig = figure(title='Line Chart Example',
                tools=[hover_tool],
                x_axis_label='Date',
                y_axis_label='Kasus vs Sembuh',
                width=1000,
                height=400,
                x_axis_type = 'datetime',)

    # Draw the line
    fig.line('tanggal', 'KASUS', 
            line_alpha=0.8,
            color='#CE1141',
            legend_label='Kasus Baru', 
            source=source,
            line_width=2)

    fig.line('tanggal', 'SEMBUH', 
            color='#006BB6',
            line_alpha=0.8,
            legend_label='Sembuh', 
            source=source,
            line_width=2)
    
    
    fig.title.text = f"Kasus Baru vs Sembuh Provinsi ACEH Pada {start} Sampai Dengan {end}"
    fig.legend.location = 'top_left'
    
    return fig


def update_line_plot(attr, old, new):
    province = select.value
    plot.title.text = f"Kasus Baru vs Sembuh Provinsi {select.value} Pada {start_date.value} Sampai Dengan {end_date.value}"
    new_data = {
        'tanggal' : df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['tanggal'],
        'KASUS' :  df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['KASUS'],
        'SEMBUH' :  df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['SEMBUH'],
    }
    source.data = new_data

def get_provinces_name(data_covid):
    provinces = list(data_covid['PROVINSI'].unique())
    provinces.sort()

    return provinces

data_covid = pd.read_csv('./data/covid_data.csv')
data_covid = data_covid.drop("Unnamed: 0", axis=1)

start = "2022-01-01"
end = "2022-01-31"

df = data_covid.copy()

df['tanggal'] = pd.to_datetime(df['tanggal'] )

source = make_column_data_source(df.loc[(data_covid['tanggal'] >= start) & (data_covid['tanggal'] <= end)])

hover_tool = HoverTool(
    tooltips=[
        ("Jumlah Kasus Baru", '@KASUS'),
        ("Jumlah Sembuh", '@SEMBUH'),
        ("Tanggal", '@tanggal{%F}')
    ],
    formatters={
        '@tanggal' : 'datetime',
    },
)

plot = make_line_plot(source, hover_tool, start, end)

provinces = get_provinces_name(data_covid)

select = Select(title="Provinsi:", value="ACEH", options=provinces)
select.on_change("value", update_line_plot)

start_date = DatePicker(title='Start Date', value=start, min_date="2020-03-01", max_date="2022-05-19")
start_date.on_change("value", update_line_plot)

end_date = DatePicker(title='Ene Date', value=end, min_date="2020-03-01", max_date="2022-05-19")
end_date.on_change("value", update_line_plot)

layout = row(plot)
curdoc().add_root(row(Column(select, start_date, end_date), plot))