import unittest

import pi_time

from pi_time.models import rpc


class RpcTestCase(unittest.TestCase):

    def test_rpc_request_sets_attributes(self):
        # Arrange
        apiVersion = pi_time.API_VERSION
        method = 'bogusMethod'
        context = 'bogusContext'
        params = ('bogusParamName', 'bogusParamValue')
        # Act
        request = rpc.RpcRequest(method, context, params)
        # Assert
        self.assertEqual(apiVersion, request.apiVersion)
        self.assertEqual(method, request.method)
        self.assertEqual(context, request.context)
        self.assertEqual(params, request.params)

    def test_api_response_sets_attributes(self):
        # Arrange
        apiVersion = pi_time.API_VERSION
        method = 'bogusMethod'
        context = 'bogusContext'
        data = ('bogusDataName', 'bogusDataValue')
        error = ('bogusErrorName', 'bogusErrorValue')
        # Act
        response = rpc.RpcResponse(method, context, data, error)
        # Assert
        self.assertEqual(apiVersion, response.apiVersion)
        self.assertEqual(method, response.method)
        self.assertEqual(context, response.context)
        self.assertEqual(data, response.data)
        self.assertEqual(error, response.error)


if __name__ == '__main__':
    unittest.main()