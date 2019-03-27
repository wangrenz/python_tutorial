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

4. `Rbf` 用于n维散乱数据的径向基函数逼近/插值

少量数据可以，大量自动站插值会出错（求解矩阵）。
```python
func = Rbf(lon, lat, zvalue,function='linear')
zvalue_new = func(olon, olat)
```
5. `griddata` 插值D维无结构数据(散点)

大量自动站数据插值会出错。
```python
zvalue_new = interpolate.griddata((lon,lat),zvalue,(olon,olat),method='linear')
```



### 4.2 格点到站点

1. `interpn` 双线性内插

```python
lon = np.linspace(startlon, endlon, xsize, dtype='f8')
lat = np.linspace(startlat, endlat, ysize, dtype='f8')
itrp_pre = interpolate.interpn((lat, lon), grid_data, obs_data[['Lat','Lon']].values.astype('f8'), method='linear') 
```


