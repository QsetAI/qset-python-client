# Qset Python API

## Client installation
To install the client, run this command in your terminal:


```python
$ pip install qset-python-client
```

## Basic Usage


```python
from qset import Client
cli = Client(api_key='<your-api-key>')
```


```python
cli.get_available_datasets()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>universe</th>
      <th>featureset</th>
      <th>desc</th>
      <th>type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>binance_timebars_5</td>
      <td>binance</td>
      <td>timebars</td>
      <td>{'period': '5'}</td>
      <td>asset</td>
    </tr>
    <tr>
      <th>1</th>
      <td>binance_timebars_600</td>
      <td>binance</td>
      <td>timebars</td>
      <td>{'period': '600'}</td>
      <td>asset</td>
    </tr>
    <tr>
      <th>2</th>
      <td>binance_f_timebars_5</td>
      <td>binance_f</td>
      <td>timebars</td>
      <td>{'period': '5'}</td>
      <td>asset</td>
    </tr>
    <tr>
      <th>3</th>
      <td>binance_f_timebars_600</td>
      <td>binance_f</td>
      <td>timebars</td>
      <td>{'period': '600'}</td>
      <td>asset</td>
    </tr>
    <tr>
      <th>4</th>
      <td>binance_f_timebars_1800</td>
      <td>binance_f</td>
      <td>timebars</td>
      <td>{'period': '1800'}</td>
      <td>asset</td>
    </tr>
  </tbody>
</table>
</div>




```python
cli.get_dataset(dataset='binance_timebars_5', query={'start': '2020.06.01 10:00:00',
                                                     'end': '2020.06.02 12:00:00',
                                                     'columns': ['startRange', 'pVWAP'],
                                                     'ticker': 'BTC-USDT'})
```




    





<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>startRange</th>
      <th>pVWAP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2020-06-01 10:00:00</td>
      <td>9541.746843</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020-06-01 10:00:05</td>
      <td>9541.439337</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2020-06-01 10:00:10</td>
      <td>9541.426286</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020-06-01 10:00:15</td>
      <td>9539.757527</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2020-06-01 10:00:20</td>
      <td>9539.608216</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>18714</th>
      <td>2020-06-02 11:59:35</td>
      <td>10117.849291</td>
    </tr>
    <tr>
      <th>18715</th>
      <td>2020-06-02 11:59:40</td>
      <td>10119.051351</td>
    </tr>
    <tr>
      <th>18716</th>
      <td>2020-06-02 11:59:45</td>
      <td>10117.896965</td>
    </tr>
    <tr>
      <th>18717</th>
      <td>2020-06-02 11:59:50</td>
      <td>10115.770162</td>
    </tr>
    <tr>
      <th>18718</th>
      <td>2020-06-02 11:59:55</td>
      <td>10116.022257</td>
    </tr>
  </tbody>
</table>
<p>18719 rows × 2 columns</p>
</div>



For more examples, see the [quickstart jupyter notebook](https://github.com/QsetAI/qset-python-client/blob/main/examples/QuickStart.ipynb). 

## Resources
- Interactive docs: http://api.qset.ai/docs
