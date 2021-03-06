#### Python文件读写

##### NETCDF数据
1. `scipy`库
```python
from scipy.io import netcdf
f = netcdf.netcdf_file('uv_force.nc', 'w')
```
2. `xarray`库
```python
import xarray as xr
ds = xr.open_dataset('uv.nc')
```


##### grib数据
调用`cfgrib`包来解`grib`，读取到`xarray`。目前`cfgrib`不支持读取多种层次，详见：https://github.com/ecmwf/cfgrib/issues/2

```python
>>> import xarray as xr
# ERA5再分析数据
>>> ds = xr.open_dataset('10muv.grib', engine='cfgrib')
>>> ds
<xarray.Dataset>
Dimensions:     (latitude: 721, longitude: 1440, time: 8760)
Coordinates:
    number      int64 ...
  * time        (time) datetime64[ns] 2018-01-01 ... 2018-12-31T23:00:00
    step        timedelta64[ns] ...
    surface     int64 ...
  * latitude    (latitude) float64 90.0 89.75 89.5 89.25 ... -89.5 -89.75 -90.0
  * longitude   (longitude) float64 0.0 0.25 0.5 0.75 ... 359.2 359.5 359.8
    valid_time  (time) datetime64[ns] ...
Data variables:
    u10         (time, latitude, longitude) float32 ...
    v10         (time, latitude, longitude) float32 ...
Attributes:
    GRIB_edition:            1
    GRIB_centre:             ecmf
    GRIB_centreDescription:  European Centre for Medium-Range Weather Forecasts
    GRIB_subCentre:          0
    Conventions:             CF-1.7
    institution:             European Centre for Medium-Range Weather Forecasts
    history:                 2019-06-14T15:03:35 GRIB to CDM+CF via cfgrib-0....
    
# GFS预报数据
>>> ds = xr.open_dataset('gfs.t00z.pgrb2.0p50.f000', engine='cfgrib', backend_kwargs={'filter_by_keys':{'typeOfLevel':'surface'}})
>>> ds
<xarray.Dataset>
Dimensions:     (latitude: 361, longitude: 720)
Coordinates:
    time        datetime64[ns] ...
    step        timedelta64[ns] ...
    surface     int64 ...
  * latitude    (latitude) float64 90.0 89.5 89.0 88.5 ... -89.0 -89.5 -90.0
  * longitude   (longitude) float64 0.0 0.5 1.0 1.5 ... 358.0 358.5 359.0 359.5
    valid_time  datetime64[ns] ...
Data variables:
    vis         (latitude, longitude) float32 ...
    gust        (latitude, longitude) float32 ...
    hindex      (latitude, longitude) float32 ...
    sp          (latitude, longitude) float32 ...
    orog        (latitude, longitude) float32 ...
    t           (latitude, longitude) float32 ...
    sdwe        (latitude, longitude) float32 ...
    sde         (latitude, longitude) float32 ...
    cpofp       (latitude, longitude) float32 ...
    wilt        (latitude, longitude) float32 ...
    fldcp       (latitude, longitude) float32 ...
    SUNSD       (latitude, longitude) float32 ...
    lftx        (latitude, longitude) float32 ...
    cape        (latitude, longitude) float32 ...
    cin         (latitude, longitude) float32 ...
    4lftx       (latitude, longitude) float32 ...
    hpbl        (latitude, longitude) float32 ...
    lsm         (latitude, longitude) float32 ...
    siconc      (latitude, longitude) float32 ...
    landn       (latitude, longitude) float32 ...
Attributes:
    GRIB_edition:            2
    GRIB_centre:             kwbc
    GRIB_centreDescription:  US National Weather Service - NCEP
    GRIB_subCentre:          0
    Conventions:             CF-1.7
    institution:             US National Weather Service - NCEP
    history:                 2019-06-14T15:33:24 GRIB to CDM+CF via cfgrib-0....
```
批量读取
```python
>>> ds = xr.open_mfdataset(files, concat_dim='valid_time', engine="cfgrib",backend_kwargs={'filter_by_keys':{'typeOfLevel':'heightAboveGround','level':10},'indexpath':''})
>>>
>>> ds = ds.drop(["time","heightAboveGround","step"])
>>> ds.rename({'valid_time':'time'})
<xarray.Dataset>
Dimensions:    (latitude: 361, longitude: 720, time: 17)
Coordinates:
  * latitude   (latitude) float64 90.0 89.5 89.0 88.5 ... -89.0 -89.5 -90.0
  * longitude  (longitude) float64 0.0 0.5 1.0 1.5 ... 358.0 358.5 359.0 359.5
  * time       (time) datetime64[ns] 2019-07-29T18:00:00 ... 2019-08-02T18:00:00
Data variables:
    u10        (time, latitude, longitude) float32 dask.array<shape=(17, 361, 720), chunksize=(1, 361, 720)>
    v10        (time, latitude, longitude) float32 dask.array<shape=(17, 361, 720), chunksize=(1, 361, 720)>
Attributes:
    GRIB_edition:            2
    GRIB_centre:             kwbc
    GRIB_centreDescription:  US National Weather Service - NCEP
    GRIB_subCentre:          0
    Conventions:             CF-1.7
    institution:             US National Weather Service - NCEP
    history:                 2019-07-31T11:22:23 GRIB to CDM+CF via cfgrib-0....
```
