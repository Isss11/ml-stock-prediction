from django.shortcuts import render
from django.http import HttpResponse
from . import ARIMAForecaster, StockDetail
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
import json

# Constructs a ARIMA model to forecast stock returns, using ML
@api_view(['POST'])
def arimaForecast(request):
    requestValues = JSONParser().parse(request)
    forecaster = ARIMAForecaster.ARIMAForecaster(requestValues["ticker"])
    
    # Obtains the actual approximated percentage returns from the training data forecasted returns
    forecaster.createModel()
    allReturns = forecaster.getCombinedReturns(requestValues["forecastLength"])
    print(allReturns.to_json())
    
    # Allowing non-dictionary values to serialized by setting safe equal to false
    return JsonResponse(allReturns.to_json(), status=status.HTTP_200_OK, safe=False)

# Returns general stock information used in the UI
@api_view(['POST'])
def stockDetail(request, stockTicker):
    stockInfo = StockDetail.StockDetail(str(stockTicker))
    
    return JsonResponse(stockInfo.getGeneralInfo())