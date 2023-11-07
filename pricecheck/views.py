from django.shortcuts import render
import requests
import requests
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_data(url, params):
    response = requests.get(url, params=params)
    return response.json()

def index(request):

    url_amzn = 'http://localhost:8000/search_amazon/'
    url_flipkart = 'http://localhost:8000/search_flipkart/'
    url_jiomart = 'http://localhost:8000/search_jiomart/'

    if request.method == "POST":
        key = request.POST['key']

        params = {
            'key' : key,
        }

        # print(key)

        start_time = time.time()

        # Sequential Processing

        # data_amzn = requests.get(url_amzn,params).json()
        # data_flipkart = requests.get(url_flipkart,params).json()
        # data_jiomart = requests.get(url_jiomart,params).json()

        # Parallel Processing

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_amzn = executor.submit(fetch_data, url_amzn, params)
            future_flipkart = executor.submit(fetch_data, url_flipkart, params)
            future_jiomart = executor.submit(fetch_data, url_jiomart, params)

        # Get the results of the parallel requests
        data_amzn = future_amzn.result()
        data_flipkart = future_flipkart.result()
        data_jiomart = future_jiomart.result()

        end_time = time.time()

        tim = round(end_time - start_time,2)

        length = min([len(data_amzn),len(data_flipkart),len(data_jiomart)])

        return render(request,'pages/index.html',{'amazon' : data_amzn[:length], 'flipkart' : data_flipkart[:length], 'jiomart' : data_jiomart[:length],'key' : key, 'time' : tim})

    return render(request,'pages/index.html')

