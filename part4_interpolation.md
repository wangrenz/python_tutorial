## 4 Python中插值方法

这里主要介绍`scipy.interpolate`中的插值方法在气象空间数据中的应用。

官方文档：https://docs.scipy.org/doc/scipy/reference/interpolate.html

### 4.1 站点到格点
1. `LinearNDInterpolator` N维分段双线性插值
```python
olon = np.linspace(_minLon,_maxLon, int( (_maxLon - _minLon)/ _res + 0.1) +1 )
olat = np.linspace(_minLat,_maxLat, int( (_maxLat - _minLat)/ _res + 0.1) +1 )
cartcoord = list(zip(lon, lat))
interp = interpolate.LinearNDInterpolator(cartcoord, zvalue, )
zvalue_new = interp(olon, olat)
```
效果

<div align=center><img src="https://github.com/wangrenz/python_tutorial/blob/master/figures/LinearNDInterpolator.png" width="70%" /></div>

2. `CloughTocher2DInterpolator`2D数据中的分段三次样条插值，C1平滑，曲率最小化插值
```python
cartcoord = list(zip(lon, lat))
interp = interpolate.LinearNDInterpolator(cartcoord, zvalue, )
zvalue_new = interp(olon, olat)
```
效果

<div align=center><img src="https://github.com/wangrenz/python_tutorial/blob/master/figures/CloughTocher2DInterpolator.png" width="70%" /></div>

3. `SmoothBivariateSpline` 平滑的二元样条近似
```python
interp = interpolate.SmoothBivariateSpline(lon, lat, zvalue, kx=2, ky=2, s=0)
zvalue_new = interp.ev(olon, olat)
```
效果

<div align=center><img src="https://github.com/wangrenz/python_tutorial/blob/master/figures/SmoothBivariateSplinekx2ky2.png" width="70%" /></div>

### 4.2 格点到站点

1. `interpn` 双线性内插

```python
lon = np.linspace(startlon, endlon, xsize, dtype='f8')
lat = np.linspace(startlat, endlat, ysize, dtype='f8')
itrp_pre = interpolate.interpn((lat, lon), grid_data, obs_data[['Lat','Lon']].values.astype('f8'), method='linear') 
```


