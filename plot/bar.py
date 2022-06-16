import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.layouts import Column
from bokeh.transform import dodge
from bokeh.models import DateRangeSlider, Panel

def bar_plot(df):

        data_covid = df.copy()

        # Change tanggal column data type to datetime
        data_covid['tanggal'] = pd.to_datetime(data_covid['tanggal']).dt.date

        # Generate case data per province
        Jawabarat = data_covid[data_covid['PROVINSI'] == 'JAWA BARAT'][['KASUS','SEMBUH','MENINGGAL']]
        Jawatengah = data_covid[data_covid['PROVINSI'] == 'JAWA TENGAH'][['KASUS','SEMBUH','MENINGGAL']]
        Jawatimur = data_covid[data_covid['PROVINSI'] == 'JAWA TIMUR'][['KASUS','SEMBUH','MENINGGAL']]
        Jakarta = data_covid[data_covid['PROVINSI'] == 'DKI JAKARTA'][['KASUS','SEMBUH','MENINGGAL']]
        Banten = data_covid[data_covid['PROVINSI'] == 'BANTEN'][['KASUS','SEMBUH','MENINGGAL']]
        Yogyakarta = data_covid[data_covid['PROVINSI'] == 'DAERAH ISTIMEWA YOGYAKARTA'][['KASUS','SEMBUH','MENINGGAL']]

        province = ['Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'DKI Jakarta', 'Banten', 'DI Yogyakarta']

        # Generate total case, heal, death per province
        case = [int(Jawabarat['KASUS'].sum()),
                int(Jawatengah['KASUS'].sum()),
                int(Jawatimur['KASUS'].sum()), 
                int(Jakarta['KASUS'].sum()), 
                int(Banten['KASUS'].sum()), 
                int(Yogyakarta['KASUS'].sum())]
        heal = [int(Jawabarat['SEMBUH'].sum()), 
                int(Jawatengah['SEMBUH'].sum()), 
                int(Jawatimur['SEMBUH'].sum()), 
                int(Jakarta['SEMBUH'].sum()), 
                int(Banten['SEMBUH'].sum()), 
                int(Yogyakarta['SEMBUH'].sum())]
        death = [int(Jawabarat['MENINGGAL'].sum()), 
                int(Jawatengah['MENINGGAL'].sum()), 
                int(Jawatimur['MENINGGAL'].sum()), 
                int(Jakarta['MENINGGAL'].sum()), 
                int(Banten['MENINGGAL'].sum()), 
                int(Yogyakarta['MENINGGAL'].sum())]

        # Generate data source
        source = ColumnDataSource(data=dict(province=province, case=case, heal=heal, death=death, color=Spectral6))

        def date_range(df, start, end):
                df = df.loc[(df['tanggal'] >= start) & (df['tanggal'] <= end)]
                return df

        # Update Bar Plot Callback Function
        def update_plot_bar(attr, old, new):
                # Change range of data
                start = date_range_slider.value_as_date[0]
                end = date_range_slider.value_as_date[1]
                df = date_range(data_covid, start, end)
                
                # Generate case data per province
                Jawabarat = df[df['PROVINSI'] == 'JAWA BARAT'][['KASUS','SEMBUH','MENINGGAL']]
                Jawatengah = df[df['PROVINSI'] == 'JAWA TENGAH'][['KASUS','SEMBUH','MENINGGAL']]
                Jawatimur = df[df['PROVINSI'] == 'JAWA TIMUR'][['KASUS','SEMBUH','MENINGGAL']]
                Jakarta = df[df['PROVINSI'] == 'DKI JAKARTA'][['KASUS','SEMBUH','MENINGGAL']]
                Banten = df[df['PROVINSI'] == 'BANTEN'][['KASUS','SEMBUH','MENINGGAL']]
                Yogyakarta = df[df['PROVINSI'] == 'DAERAH ISTIMEWA YOGYAKARTA'][['KASUS','SEMBUH','MENINGGAL']]

                # Generate new total case, heal, death per province
                new_case = [int(Jawabarat['KASUS'].sum()),
                                int(Jawatengah['KASUS'].sum()),
                                int(Jawatimur['KASUS'].sum()), 
                                int(Jakarta['KASUS'].sum()), 
                                int(Banten['KASUS'].sum()), 
                                int(Yogyakarta['KASUS'].sum())]
                new_heal = [int(Jawabarat['SEMBUH'].sum()), 
                                int(Jawatengah['SEMBUH'].sum()), 
                                int(Jawatimur['SEMBUH'].sum()), 
                                int(Jakarta['SEMBUH'].sum()), 
                                int(Banten['SEMBUH'].sum()), 
                                int(Yogyakarta['SEMBUH'].sum())]
                new_death = [int(Jawabarat['MENINGGAL'].sum()), 
                                int(Jawatengah['MENINGGAL'].sum()), 
                                int(Jawatimur['MENINGGAL'].sum()), 
                                int(Jakarta['MENINGGAL'].sum()), 
                                int(Banten['MENINGGAL'].sum()), 
                                int(Yogyakarta['MENINGGAL'].sum())]

                # Generate new data for data source
                new_data = dict(province=province, case=new_case, heal=new_heal, death=new_death, color=Spectral6)

                # Change Current Data Source to New Data
                source.data = new_data

        def make_bar_plot_1(source, tooltips):
                # Cretae Figure
                fig = figure(x_range=province, 
                                height=500, 
                                width=1000, 
                                title="Kasus Covid-19 di 6 Provinsi Besar di Pulau Jawa", 
                                tooltips=tooltips)

                # Create bar plot
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
                # Cretae Figure
                fig = figure(x_range=province, 
                                height=500, 
                                width=1000, 
                                title="Perbandingan Kasus Sembuh dan Meninggal",
                                tooltips=tooltips)
                
                # Create bar plot
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

        layout = Column(date_range_slider, bar1, bar2)

        return Panel(child=layout, title='Bar Plot')