from datetime import datetime, timedelta

import xarray as xr

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.io import metar
from metpy.plots.declarative import (BarbPlot, ContourPlot, FilledContourPlot, MapPanel,
                                     PanelContainer, PlotObs)
from metpy.units import units

# Open the netCDF file as a xarray Dataset and parse the full dataset
data = xr.open_dataset(get_test_data('GFS_test.nc', False)).metpy.parse_cf()

# View a summary of the Dataset
print(data)

# set time
plot_time = datetime(2010, 10, 26, 12)


ds = data.metpy.sel(lat=slice(70, 10), lon=slice(360 - 150, 360 - 55))

ds['wind_speed'] = mpcalc.wind_speed(ds['u-component_of_wind_isobaric'],
                                     ds['v-component_of_wind_isobaric'])

# Set attributes for contours of Geopotential Heights at 300 hPa
cntr2 = ContourPlot()
cntr2.data = ds
cntr2.field = 'Geopotential_height_isobaric'
cntr2.level = 300 * units.hPa
cntr2.time = plot_time
cntr2.contours = list(range(0, 10000, 120))
cntr2.linecolor = 'black'
cntr2.linestyle = 'solid'
cntr2.clabels = True

# Set attributes for plotting color-filled contours of wind speed at 300 hPa
cfill = FilledContourPlot()
cfill.data = ds
cfill.field = 'wind_speed'
cfill.level = 300 * units.hPa
cfill.time = plot_time
cfill.contours = list(range(10, 201, 20))
cfill.colormap = 'BuPu'
cfill.colorbar = 'horizontal'
cfill.plot_units = 'knot'

# Set the attributes for the map and add our data to the map
panel = MapPanel()
panel.area = [-125, -74, 20, 55]
panel.projection = 'lcc'
panel.layers = ['states', 'coastline', 'borders']
panel.title = f'{cfill.level.m}-hPa Heights and Wind Speed at {plot_time}'
panel.plots = [cfill, cntr2]

# Set the attributes for the panel and put the panel in the figure
pc = PanelContainer()
pc.size = (15, 15)
pc.panels = [panel]

# Show the image
pc.show()