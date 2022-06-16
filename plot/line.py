import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.layouts import row, Column
from bokeh.models import Slider, Select
from bokeh.transform import dodge
from bokeh.models import Select, DatePicker, Panel

def line_plot(df):

    # Make Column Data Source
    def make_column_data_source(df):
        return ColumnDataSource(data={
            'tanggal' : df[df['PROVINSI']== 'ACEH']['tanggal'],
            'KASUS' : df[df['PROVINSI']== 'ACEH']['KASUS'],
            'SEMBUH' : df[df['PROVINSI']== 'ACEH']['SEMBUH'],
        })

    # Make Line pLOT
    def make_line_plot(source, hover_tool, start, end):
        # Cretae Figure
        fig = figure(title='Line Chart Example',
                    tools=[hover_tool],
                    x_axis_label='Date',
                    y_axis_label='Kasus vs Sembuh',
                    width=1000,
                    height=400,
                    x_axis_type = 'datetime',)

        # Create line plot
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

        # Edit label and title style
        fig.title.text_font_size = '13pt'
        fig.xaxis.axis_label_text_font_size = "12pt"
        fig.yaxis.axis_label_text_font_size = "12pt"
        
        return fig

    # Update Line Plot Callback Function
    def update_line_plot(attr, old, new):
        province = select.value

        # Update title
        plot.title.text = f"Kasus Baru vs Sembuh Provinsi {select.value} Pada {start_date.value} Sampai Dengan {end_date.value}"

        # Generate New Data for Current Data Source
        new_data = {
            'tanggal' : df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['tanggal'],
            'KASUS' :  df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['KASUS'],
            'SEMBUH' :  df[(df['PROVINSI']== province) & (df['tanggal'] >= start_date.value) & (df['tanggal'] <= end_date.value)]['SEMBUH'],
        }

        # Change Current Data Source to New Data
        source.data = new_data

    # Get All Provinces Name
    def get_provinces_name(data_covid):
        provinces = list(data_covid['PROVINSI'].unique())
        provinces.sort()

        return provinces
    
    data_covid = df.copy()

    start = "2022-01-01"
    end = "2022-01-31"

    df = data_covid.copy()

    # Change tanggal column data type to datetime
    df['tanggal'] = pd.to_datetime(df['tanggal'] )

    source = make_column_data_source(df.loc[(data_covid['tanggal'] >= start) & (data_covid['tanggal'] <= end)])

    # Create Hover Tool
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

    # Make Plot
    plot = make_line_plot(source, hover_tool, start, end)

    # Generate Provinces Name
    provinces = get_provinces_name(data_covid)

    # Select Interactive
    select = Select(title="Provinsi:", value="ACEH", options=provinces)
    select.on_change("value", update_line_plot)

    # DatePicker for start date
    start_date = DatePicker(title='Start Date', value=start, min_date="2020-03-01", max_date="2022-05-19")
    start_date.on_change("value", update_line_plot)

    # DatePicker for end date
    end_date = DatePicker(title='Ene Date', value=end, min_date="2020-03-01", max_date="2022-05-19")
    end_date.on_change("value", update_line_plot)

    layout = row(Column(select, start_date, end_date), plot)

    return Panel(child=layout, title='Line Plot')