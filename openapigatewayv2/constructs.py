import json
from aws_cdk import core, aws_apigatewayv2 as apigateway


class OpenApiGateway(core.Construct):
    """AWS CDK Construct that creates an API Gateway v2 based on a
    parameterized OpenApi JSON Document.
    """

    @property
    def http_api(self) -> apigateway.HttpApi:
        """The HttpApi created by this construct"""
        return self._http_api

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        openapi_json_path: str,
        param_value_dict: dict,
        fail_on_warnings: bool = False,
        **kwargs,
    ):
        """"""
        super().__init__(scope, id, **kwargs)

        # read openapi document
        with open(openapi_json_path, "r") as json_file:
            content = json_file.read()
        # replace parameters
        for parameter, value in param_value_dict.items():
            content = content.replace("${" + f"{parameter}" + "}", value)
        openapi = json.loads(content)

        # create api gateway based on openapi document
        self._http_api = apigateway.HttpApi(self, id)
        # escape hatches to work around missing cdk construct feature
        http_api_cfn: apigateway.CfnApi = self._http_api.node.default_child
        http_api_cfn.add_property_override("FailOnWarnings", fail_on_warnings)
        http_api_cfn.add_property_override("Body", openapi)
        http_api_cfn.add_property_deletion_override("Name")
        http_api_cfn.add_property_deletion_override("ProtocolType")

        # output api gateway v2 url
        core.CfnOutput(self, "HTTP API URL", value=self._http_api.url)
