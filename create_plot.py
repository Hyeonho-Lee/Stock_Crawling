import os
import re
import time
import datetime
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import parse

pd.options.display.float_format = '{:.0f}'.format

def create_plot(code, csv, png):
    
    result = pd.read_csv(csv)
    result_data = pd.DataFrame({'Date' : result['날짜'].apply(lambda x: pd.to_datetime(str(x), format = '%Y.%m.%d')), 'Closing_Price' : result['종가'], 'Market_Price' : result['시가'], 'High_Price' : result['고가'], 'Low_Price' : result['저가']})
    
    result_data.set_index(result_data['Date'], inplace = True)
    
    for col in result_data.columns:
        if col == 'Date':
            del result_data[col]
    
    save = result_data.plot(kind = 'line', title = '{code} Data'.format(code = code), figsize = (12, 5), legend = True, fontsize = 12, linestyle = '-', linewidth = 1)
    
    plt.show()
    plt.savefig(png)
    
    return result_data

#code = 263750
#csv = './code/{code}/{code}.csv'.format(code = code)
#png = './code/{code}/{code}.png'.format(code = code)
#get_path = './code/{code}'.format(code = code)
#create_plot(code, csv, png)