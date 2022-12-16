import numpy as np
import xarray as xr
import os
import matplotlib
import glob
import cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
from matplotlib import ticker, cm
from matplotlib.colors import LogNorm, BoundaryNorm
from datetime import datetime as dt
import matplotlib as mpl

class quick_view:
    def __init__(self,path):
        self.path = path
        self.data = xr.open_dataset(self.path)
        self.time = self.data['time']
        self.level = self.data['level']
        self.lat = self.data['lat']
        self.lon = self.data['lon']
        self.variables =  [i for i in self.data.data_vars]
        self.save_path = input("Entrer un path pour save les figures: ")

    def Resume(self):
        print("Dimension time: ")
        print(self.time)
        print('--------------------------')
        print("Dimension level: ")
        print(self.level)
        print('--------------------------')
        print("Dimension lat: ")
        print(self.lat)
        print('--------------------------')
        print("Dimension lon: ")
        print(self.lon)
        print('--------------------------')
        print("Variables names: ")
        print(self.variables)

    def lonflip(self,da):
        lon_name = 'lon'
        da['_longitude_adjusted'] = xr.where(
            da[lon_name] > 180,
            da[ lon_name] - 360,
            da[lon_name])
        da = (
            da
            .swap_dims({lon_name: '_longitude_adjusted'})
            .sel(**{'_longitude_adjusted': sorted(da._longitude_adjusted)})
            .drop(lon_name))
        da = da.rename({'_longitude_adjusted': lon_name})
        return da
    
    def First_plot_contour(self,variable,tps,niveau,ax,proj):
        resol = '10m'  # use data at this scale
        cmap = mpl.cm.plasma

            # Add coastlines
        ax.set_extent([self.ds["lon"][0],self.ds["lon"][-1],self.ds["lat"][-1],self.ds["lat"][0]])
        ax.set_title(str(variable)+" "+str(niveau)+" "+str(tps))
        cs=ax.contourf(self.ds['lon'], self.ds['lat'], self.ds,
                    transform = proj, cmap=cmap)

        ax.coastlines(resolution=resol, color='black', linewidth=0.5)
        bodr = cartopy.feature.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land', scale=resol, facecolor='none')
        ax.add_feature(bodr, linestyle='-', alpha=1, linewidth=0.5)
        gl=ax.gridlines(crs=proj, linewidth=0.5, color='black', linestyle='--', draw_labels=True)
        gl.top_labels=False
        gl.right_labels=False
        gl.xlocator= mpl.ticker.FixedLocator(np.arange(self.ds["lon"][0],self.ds["lon"][-1]),10)
        gl.ylocator= mpl.ticker.FixedLocator(np.arange(self.ds["lat"][-1],self.ds["lat"][0]),10)
        return cs

    def first_plot(self,variable,tps,niveau):
        self.ds = self.lonflip(self.data[variable].sel(level=niveau).sel(time=tps))
        fig = plt.figure(figsize=(11,8.5), frameon=False)
        middle_lon = self.ds["lon"][len(self.ds["lon"])//2]
        middle_lat = self.ds["lat"][len(self.ds["lat"])//2]
        print("Select your projection: 1-PlateCarree, 2-AlbersEqualArea, 3-AzimuthalEquidistant, 4-LambertConformal, 5-LambertCylindrical, 6-Mercator, 7-Miller, 8-Mollweide, 9-Orthographic, 10-Orthographic, 11-Robinson, 12-Sinusoidal, 13-Stereographic, 14-TransverseMercator, 15-UTM, 16-InterruptedGoodeHomolosine, 17-RotatedPole, 18-OSGB, 19-EuroPP, 20-Geostationary, 21-NearsidePerspective, 22-Gnomonic, 23-LambertAzimuthalEqualArea, 24-NorthPolarStereo, 25-OSNI, 26-SouthPolarStereo.")
        choice_projection = input()
        if choice_projection =="1":
            proj = ccrs.PlateCarree()
        """if choice_projection =="6":
            proj = ccrs.Stereographic()"""
        ax = plt.axes(projection=proj)
        cs = self.First_plot_contour(variable,tps,niveau,ax,proj)    
        cbar = plt.colorbar(cs, location='right',fraction=0.025, pad=0.04)

