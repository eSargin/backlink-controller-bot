import os
import sys

import jwt
from flask import Flask, request

import auth
import cache
import redisoperation
import service
import utils

app = Flask(__name__)

@app.route('/removeCache', methods=['POST'])
def RemoveCache(website_url=None):
    if website_url is None:
        '''
        curl -X 'POST' 'http://localhost:5000/removeCache'   -H 'Content-Type: application/json'   -d '{"userId": 1,"type":1}'
        '''
        # get header jwt token
        token = request.headers.get('Authorization')
        decodedToken = None
        if auth.CheckIsAuthenticated(token):
            decodedToken = auth.EncodeToken(token)
        else:
            return '', 204

        if decodedToken is None:
            return '', 204
        else:
            json_data = decodedToken
            # website_url = json_data['website_url']
            if utils.CheckIsEmpty(json_data['userId']) or utils.CheckIsEmpty(json_data['type']):
                print("Auth Is Ok for but Empty Data")
                return '', 204
            userId = json_data['userId']
            jsonType = json_data['type'] # Type 1 -> All websites, Type 2 -> Specific websites
            if jsonType == 1:
                redisoperation.RemoveCacheAll(userId)
            elif jsonType == 2:
                redisoperation.RemoveCacheAllById(userId, json_data['websiteId'])
            else:
                print("Type is not valid")
                return '', 204

@app.route('/service', methods=['POST'])
def StartService(website_url=None):
    if website_url is None:  # POST request
        '''
        curl -X 'POST' 'http://localhost:5000/run'   -H 'Content-Type: application/json'   -d '{"userId": 1,"type":1}'
        '''
        # get header jwt token
        token = request.headers.get('Authorization')
        decodedToken = None
        if auth.CheckIsAuthenticated(token):
            decodedToken = auth.EncodeToken(token)
        else:
            return '', 204

        if decodedToken is None:
            return '', 204
        else:
            json_data = decodedToken
            # website_url = json_data['website_url']
            if utils.CheckIsEmpty(json_data['userId']) or utils.CheckIsEmpty(json_data['type']):
                print("Auth Is Ok for but Empty Data")
                return '', 204
            userId = json_data['userId']
            jsonType = json_data['type']  # Type 1 -> All websites, Type 2 -> Specific websites
            if jsonType == 1:
                # Get all websites
                serviceResponse = service.startService(userId)
                print("Api Response: ", serviceResponse)
                if serviceResponse:
                    print("Service Completed")
                    apiResponse = {
                        "success": True,
                        "message": "Tüm Siteler Başarıyla Sorgulandı."
                    }
                    return apiResponse
                else:
                    print("Service Completed")
                    apiResponse = {
                        "success": False,
                        "message": "Service Stared False"
                    }
                    return apiResponse
            else:
                print("Type 2", json_data)
                if utils.CheckIsEmpty(json_data['websiteId']):
                    print("Auth Is Ok for but Empty Data")
                    return '', 204
                websiteId = json_data['websiteId']
                serviceResponse = service.startServiceSingle(userId, websiteId)
                if serviceResponse:
                    print("Service Completed")
                    apiResponse = {
                        "success": True,
                        "message": "Sorgulama Tamamlandı."
                    }
                    return apiResponse
                else:
                    print("Service Completed")
                    apiResponse = {
                        "success": False,
                        "message": "Service Stared False"
                    }
                    return apiResponse

