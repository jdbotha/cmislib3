# -*- coding: utf-8 -*-
#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#
"""
Module that takes care of network communications for cmislib. It does
not know anything about CMIS or do anything special with regard to the
response it receives.
"""
import logging
from urllib.parse import urlencode

import requests
from requests.auth import HTTPBasicAuth


class RESTService(object):

    """
    Generic service for interacting with an HTTP end point. Sets headers
    such as the USER_AGENT and builds the basic auth handler.
    """

    def __init__(self):
        self.user_agent = 'cmislib/%s +http://chemistry.apache.org/'
        self.logger = logging.getLogger('cmislib.net.RESTService')

    def get(self,
            url,
            username=None,
            password=None,
            **kwargs):

        """ Makes a get request to the URL specified."""

        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if type(url) == bytes:
                url = url.decode("utf8")
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)

        self.logger.debug('About to do a GET on:' + str(url))

        headers['User-Agent'] = self.user_agent
        return requests.get(url, verify=False, headers=headers, auth=HTTPBasicAuth(username, password))

    def delete(self, url, username=None, password=None, **kwargs):

        """ Makes a delete request to the URL specified. """

        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)

        self.logger.debug('About to do a DELETE on:' + url)

        headers['User-Agent'] = self.user_agent
        return requests.delete(url, verify=False, headers=headers, auth=HTTPBasicAuth(username, password))

    def put(self,
            url,
            payload,
            contentType,
            username=None,
            password=None,
            **kwargs):

        """
        Makes a PUT request to the URL specified and includes the payload
        that gets passed in. The content type header gets set to the
        specified content type.
        """
        if type(url) == bytes:
            url = url.decode("utf8")
        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)

        self.logger.debug('About to do a PUT on:' + url)

        headers['User-Agent'] = self.user_agent
        if contentType is not None:
            headers['Content-Type'] = contentType
        return requests.put(url, verify=False, headers=headers, auth=HTTPBasicAuth(username, password),
                                 data=payload)

    def post(self,
             url,
             payload,
             contentType,
             username=None,
             password=None,
             **kwargs):

        """
        Makes a POST request to the URL specified and posts the payload
        that gets passed in. The content type header gets set to the
        specified content type.
        """

        headers = {}
        if kwargs:
            if 'headers' in kwargs:
                headers = kwargs['headers']
                del kwargs['headers']
                self.logger.debug('Headers passed in: %s', headers)
            if url.find('?') >= 0:
                url = url + '&' + urlencode(kwargs)
            else:
                url = url + '?' + urlencode(kwargs)

        self.logger.debug('About to do a POST on:' + url)

        # h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        # h.add_credentials(username, password)
        headers['User-Agent'] = self.user_agent
        if contentType is not None:
            headers['Content-Type'] = contentType

        # return h.requst(url, body=payload, method='POST', headers=headers)
        return requests.post(url, verify=False, headers=headers, auth=HTTPBasicAuth(username, password),data=payload)