#!/usr/bin/env python3

'''

exchangeratesapi.__init__.py


exchangeratesapi.io API wrapper


'''


from datetime import date
from functools import lru_cache
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode


class BaseCurrencyDescriptor:
    '''
    Custom descriptor for the ExchangeRatesIO.base_currency attribute
    '''

    def __init__(self, base):
        self.base = base

    def __set__(self, obj, value):
        '''
        Custom __set__ method for the BaseCurrencyDescriptor type

        Ensures the base currency for the ExchangeRatesIO class
        is a 3-letter string
        '''
        if type(value) != str:
            raise TypeError('base type must be a string')
        if len(value) != 3:
            raise ValueError('base value must be 3 letters long')
        obj.__dict__[self.base] = value.upper()


class ExchangeRatesIO:

    def __init__(self, base_currency):
        self.base_currency = base_currency

    base_currency = BaseCurrencyDescriptor('base_currency')

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__qualname__,
                                 self.base_currency)

    @lru_cache(maxsize=8)
    def _request(self, url, data=None, **kwargs):
        '''
        A custom request method for the exchangeratesapi.io wrapper.

        args:
            url (str) -> the url to send the http request

        kwargs:
            data (dict) -> the data to pass in the http request

        returns:
            http.client.HTTPResponse object

        raises:
            http.client.HTTPException if the response code is ___?
        '''
        response = urlopen(url, data=data)
        if response.status in (200, 201,):
            return response
        raise HTTPException(
                'status code received {}'.format(response.status))

    def _build_url(self, base_url, **kwargs):
        '''
        Build an exchangeratesapi.io URL with parameters that are
        passed in as keywords

        args:
            base (str) -> the base exchangesapi URL
                          ex. https://api.exchangeratesapi.io/latest

        kwargs:
            the parameters which to pass in the URL

        returns:
            str -> a URL in the form
                   'https://api.exchangeratesapi.io/[API_point]?param=val'
        '''
        url = base_url + '?'
        params = '&'.join(('{}={}'.format(key, val) for key, val in
                          kwargs.items()))
        url += params
        return url

    @lru_cache(maxsize=8)
    def latest(self, base=None, *, symbols=None, parse_json=False):
        '''
        Get the latest exchange rates relative the instance's base currency.

        args:
            None

        kwargs:
            base (str) -> a 3 letter currency string
            symbols (tuple) -> a list of currency symbols to retrieve
                               a symbol shall be 3 characters long
            parse_json (bool) -> overrides the return
                                 Parses the HTTPResponse and returns the
                                 JSON dictionary instead

        returns:
            http.client.HTTPResponse object

        raises:
            http.client.HTTPException (see ExchangeRatesIO._request)
            TypeError -> if symbols provided is an unhashable type
        '''
        url = 'https://api.exchangeratesapi.io/latest'
        data = {} # start our data dictionary
        if not base:
            # if the base is not provided, use the instance's base currency
            base = self.base_currency
        data['base'] = base

        # check for any symbols provided
        if symbols:
            data['symbols'] = ','.join(symbols)

        url = self._build_url(url, **data)
        response = self._request(url)
        if parse_json:
            response = loads(response.read())
        return response

    @lru_cache(maxsize=8)
    def historical(self, dt, base=None, *, end=None, symbols=None,
                   parse_json=False):
        '''
        Get historical exchange rates for any date in history since 1999.

        args:
            dt (datetime) -> a Python datetime object with a year, month,
                             and day.  The proper syntax for the
                             actual request URL is 'YYYY-MM-DD'.

        kwargs:
            base (str) -> a 3 letter currency string
            end (datetime) -> a Python datetime object with a year, month,
                              and day.  The proper syntax for the
                              actual request URL is 'YYYY-MM-DD'. This is
                              the end date in a range of dates to search.
            symbols (tuple) -> a list of currency symbols to retrieve
                               a symbol shall be 3 characters long
            parse_json (bool) -> overrides the return
                                 Parses the HTTPResponse and returns the
                                 JSON dictionary instead

        returns:
            http.client.HTTPResponse object

        raise:
            AttributeError -> when dt is not a datetime.date object
            TypeError -> if symbols provided is an unhashable type
        '''
        url = 'https://api.exchangeratesapi.io/'
        data = {} # start our data dictionary
        if not base:
            # if the base is not provided, use the instance's base currency
            base = self.base_currency
        data['base'] = base

        # check for any symbols provided
        if symbols:
            data['symbols'] = ','.join(symbols)

        # Check whether or not an end date is provided.
        # This is done because the URL for a range of dates
        # and the URL for a single date are different.
        # range: /history?start_at=[start]&end_at=[end]
        # single date: /[date]
        if end:
            # if the user specifies an end date, they are searching
            # for a range of dates
            data['start_at'] = dt.strftime('%Y-%m-%d')
            data['end_at'] = end.strftime('%Y-%m-%d')
            url += 'history'
        else:
            # if the user does not specify an end date, we will
            # simply use the date provided (dt) as the point to reach
            url += dt.strftime('%Y-%m-%d')

        url = self._build_url(url, **data)
        response = self._request(url)
        if parse_json:
            response = loads(response.read())
        return response
