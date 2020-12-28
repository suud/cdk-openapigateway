"""
Constructs that facilitate the creation of Amazon API Gateway
HttpApi Resources from OpenAPI 3 Documents.
"""

import json
from aws_cdk import core, aws_apigatewayv2 as apigateway


class OpenApiGateway(core.Construct):
    """
    AWS CDK Construct that creates an Amazon API Gateway HttpApi
    based on a parameterized OpenAPI 3 JSON Document.
    """

    @property
    def http_api(self) -> apigateway.HttpApi:
        """The HttpApi created by this construct.

        Returns
        -------
        aws_cdk.aws_apigatewayv2.HttpApi
            HttpApi resource that has been created by this construct.
        """
        return self._http_api

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        openapi_json_path: str,
        param_value_dict: dict = {},
        fail_on_warnings: bool = False,
        **kwargs,
    ):
        """Create HttpApi from parameterized OpenAPI 3 JSON Document.

        Parameters
        ----------
        scope : aws_cdk.core.Construct
            The construct within which this construct is defined.
        id : str
            An identifier that must be uniqie within this scope.
        openapi_json_path : str
            Path to the OpenAPI 3 JSON Document that serves as
            specification to create the API Gateway HttpApi.
        param_value_dict : dict, optional
            Dictionary used to replace some parameters in the OpenAPI 3
            JSON Document during build time. This is necessary to
            reference AWS resources that don't yet exist when the OpenAPI
            Document is written.
            `${<key>}` in the `openapi_json` gets replaced by `<value>`
            from this dictionary.
            For example: {"API_LAMBDA_ARN": api_lambda.function_arn} would
            replace `${API_LAMBDA_ARN}` in the OpenAPI Document by the ARN
            of an `api_lambda` lambda function.
        fail_on_warnings : bool, optional
            Wheter to rollback the API creation when a warning is
            encountered, default is False.

        Examples
        --------
        # inside an AWS CDK Construct that has
        # an api_lambda lambda function defined
        >>> OpenApiGateway(
                self,
                "OpenAPI Gateway",
                "openapi.json",
                {"API_LAMBDA_ARN", api_lambda.function_arn},
                fail_on_warnings=True
            )
        """
        super().__init__(scope, id, **kwargs)

        # read openapi document
        with open(openapi_json_path, "r") as json_file:
            content = json_file.read()
        # replace parameters
        for parameter, value in param_value_dict.items():
            content = content.replace("${" + f"{parameter}" + "}", value)
        openapi = json.loads(content)

        self._http_api = apigateway.HttpApi(self, id)
        # escape hatches to work around missing cdk construct features
        http_api_cfn: apigateway.CfnApi = self._http_api.node.default_child
        http_api_cfn.add_property_override("FailOnWarnings", fail_on_warnings)
        http_api_cfn.add_property_override("Body", openapi)
        http_api_cfn.add_property_deletion_override("Name")
        http_api_cfn.add_property_deletion_override("ProtocolType")

        # output http api url
        core.CfnOutput(self, "HTTP API URL", value=self._http_api.url)
