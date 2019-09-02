#!/opt/software/miniconda3/bin/python
# -*- coding: UTF-8 -*-
import os,sys
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import xarray as xr
import cartopy as cart
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import natural_earth, Reader
from cartopy.mpl.patch import geos_to_path
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import fiona
import shapely.vectorized
from shapely.geometry import shape
import matplotlib
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def time_stand(time):
	time = datetime.strptime(time,"%Y-%m-%d %H:%M:%S").strftime('%Y%m%d%H')
	return time
#------------------------

def add_yc_name(ax):
	cnfont = {'fontname':'simhei'}
	fsize = 12
	ax.text(120.4, 34.8,'海州湾渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(121.7, 33.0,'吕泗渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(123.8, 33.0,'大沙渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(126.5, 32.4,'沙外渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(123.5, 31.5,'长江口渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(126.5, 31.5,'江外渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(123.3, 30.3,'舟山渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)
	ax.text(126.5, 30.3,'舟外渔场',verticalalignment='center',horizontalalignment='center',transform=ccrs.PlateCarree(),color='k', fontsize=fsize, **cnfont)

	return
#-------------------------------
if __name__ == '__main__':

	subfname = r'/data/JSAI/code/ncl_code/include/cnmap/yuchang.shp'
	
	fullname = sys.argv[1]
	savepath = sys.argv[2]

	ds = xr.open_dataset(fullname)
	
	starttime = ds.attrs['startTime']
	foctime   = ds.attrs['forecastime']
	timeOfValidity = ds.attrs['timeOfValidity']
	
	lon0 = 119
	lon1 = 128.5
	lat0 = 29
	lat1 = 36
	colors = np.array( [ [255,255,255],[166,242,143], [61,186,61], [97,184,255], [0,0,225], \
		[250,0,250], [128,0,64]] ,dtype='f4')
	cmap = matplotlib.colors.ListedColormap(colors/255., name='rain_cmap')
	levels =np.array([0.1,10,25,50,100,250],dtype='f4')
	cnfont = {'fontname':'simhei'}
	
	plt.figure(figsize=(11,11),dpi=100)
	ax = plt.axes(projection=ccrs.PlateCarree())

	ax.add_geometries(Reader(subfname).geometries(),ccrs.PlateCarree(),facecolor='none',edgecolor='black',linewidth=1,alpha=0.6)
	ax.coastlines('10m',linewidth=1.9)
	land = cfeature.NaturalEarthFeature('physical', 'land', '10m',edgecolor='face',facecolor=cfeature.COLORS['land'])
	ax.add_feature(land,facecolor='0.85')

	im = ds.r24h.plot.contourf(ax=ax,xlim=(lon0,lon1), ylim=(lat0,lat1),extend='both',levels=levels, cmap=cmap,cbar_kwargs={'cax':inset_axes(ax, width="2.7%", height="55%", loc=3),'label': '','ticks': levels , 'extendfrac': 'auto'}, transform=ccrs.PlateCarree())
	
	ax.set_xticks( np.arange(119,129,1), crs=ccrs.PlateCarree())
	ax.set_yticks( np.arange(29, 37, 1), crs=ccrs.PlateCarree())
	lon_formatter = LongitudeFormatter(zero_direction_label=True)
	lat_formatter = LatitudeFormatter()
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)
	ax.set_xlabel('')
	ax.set_ylabel('')
	
	ax.text(0.003, 0.57,r'Unit:mm',verticalalignment='bottom',horizontalalignment='left',transform=ax.transAxes,color='k', fontsize=10,)
	ax.text(0.0, 1.01,'江苏省渔场24小时降水预报',verticalalignment='bottom',horizontalalignment='left',transform=ax.transAxes,color='k', fontsize=14, **cnfont)

	ax.text(1.0, 1.005, time_stand(starttime) + ' +' + str(timeOfValidity) + ' -> ' + time_stand(foctime), verticalalignment='bottom',horizontalalignment='right',transform=ax.transAxes,color='k', fontsize=14,)
	ax.set_title('')
	
	add_yc_name(ax)
	
	plt.savefig( savepath +'/'+ fullname.split('/')[-1][:-3]+'.png',bbox_inches='tight')
	
