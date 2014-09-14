import unittest

import pi_time

from pi_time import settings
from pi_time.models.api import ApiRequest, ApiResponse


class ApiTestCase(unittest.TestCase):

    def test_api_request_sets_attributes(self):
        # Arrange
        apiVersion = pi_time.API_VERSION
        method = 'bogusSensor'
        context = 'bogusContext'
        params = ('bogusParamName', 'bogusParamValue')
        # Act
        request = ApiRequest(method, context, params)
        # Assert
        self.assertEqual(apiVersion, request.apiVersion)
        self.assertEqual(method, request.method)
        self.assertEqual(context, request.context)
        self.assertEqual(params, request.params)

    def test_api_response_sets_attributes(self):
        # Arrange
        apiVersion = pi_time.API_VERSION
        method = 'bogusSensor'
        context = 'bogusContext'
        data = ('bogusDataName', 'bogusDataValue')
        error = ('bogusErrorName', 'bogusErrorValue')
        # Act
        response = ApiResponse(method, context, data, error)
        # Assert
        self.assertEqual(apiVersion, response.apiVersion)
        self.assertEqual(method, response.method)
        self.assertEqual(context, response.context)
        self.assertEqual(data, response.data)
        self.assertEqual(error, response.error)


if __name__ == '__main__':
    unittest.main()