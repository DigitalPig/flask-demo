#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.charts import Line
from bokeh.embed import components
import requests

app = Flask(__name__)

## This is the place we use to store the information
app.vars = {}


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods = ['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    app.vars['stock'] = request.form['ticker']
    app.vars['columns'] = request.form.getlist('price')
    return redirect('/graph')

@app.route('/graph')
def graph():
  ## This function is to plot the tick price based on the selected ticker
  url = "https://www.quandl.com/api/v3/datasets/WIKI/"
  full_url = url + app.vars['stock'] + '/' + 'data.json'
 
  stock_obj = requests.get(full_url).json()
  stock_data = pd.DataFrame.from_dict(stock_obj['dataset_data']['data'])
  stock_data.columns = stock_obj['dataset_data']['column_names']
  stock_data['Date'] = pd.to_datetime(stock_data['Date'])
  ## Now we have the data
  ## Let's construct Bokeh figure!
  #plot = figure(title = 'Stock Data', x_axis_label = 'Date', x_axis_type = 'datetime')
  plot=Line(stock_data, x='Date', y=app.vars['columns'], legend = "top_right",
            ylabel="Stock Price")
  #plot=Line(stock_data, x='Date', y='Adj. Close')
  script, div = components(plot)
  return render_template('graph.html', stock_name = app.vars['stock'], script = script,
                         div = div)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507)
