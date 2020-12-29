"""
Constructs that facilitate the creation of Amazon API Gateway
HttpApi Resources from OpenAPI 3 Documents.
"""

import json
import yaml
from aws_cdk import core, aws_apigatewayv2 as apigateway


class OpenApiGateway(core.Construct):
    """
    AWS CDK Construct that creates an Amazon API Gateway HttpApi
    based on a parameterized OpenAPI 3 Document.
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

    @property
    def http_api_arn(self) -> str:
        """The ARN of the HttpApi created by this construct.

        Returns
        -------
        str
            ARN of the HttpApi resource that has been created by this
            construct.
        """
        return self._http_api_arn

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        openapi_path: str,
        param_value_dict: dict = {},
        fail_on_warnings: bool = False,
        **kwargs,
    ):
        """Create HttpApi from parameterized OpenAPI 3 Document.

        Parameters
        ----------
        scope : aws_cdk.core.Construct
            The construct within which this construct is defined.
        id : str
            An identifier that must be uniqie within this scope.
        openapi_path : str
            Path to the OpenAPI 3 Document that serves as
            specification to create the API Gateway HttpApi.
            JSON and YAML files are supported.
        param_value_dict : dict, optional
            Dictionary used to replace some parameters in the OpenAPI 3
            Document during build time. This is necessary to reference
            AWS resources that don't yet exist when the OpenAPI Document
            is written. `${<key>}` in the OpenAPI Document gets replaced
            by `<value>` from this dictionary.
            For example: {"API_LAMBDA_ARN": api_lambda.function_arn} would
            replace `${API_LAMBDA_ARN}` in the OpenAPI Document by the ARN
            of an `api_lambda` lambda function.
        fail_on_warnings : bool, optional
            Wheter to rollback the API creation when a warning is
            encountered, default is False.

        Examples
        --------
        >>> # inside an AWS CDK Construct
        >>> api_lambda = _lambda()
        >>> OpenApiGateway(
        >>>     self,
        >>>     "OpenAPI Gateway",
        >>>     "openapi.json",
        >>>     {"API_LAMBDA_ARN": api_lambda.function_arn},
        >>>     fail_on_warnings=True
        >>> )
        """

        super().__init__(scope, id, **kwargs)

        # read openapi document
        with open(openapi_path, "r") as openapi_file:
            openapi_str = openapi_file.read()
        # replace parameters
        for parameter, value in param_value_dict.items():
            openapi_str = openapi_str.replace("${" + f"{parameter}" + "}", value)

        # deserialize string
        openapi = json_or_yaml_to_dict(openapi_str)

        # create httpApi
        self._http_api = apigateway.HttpApi(self, id)
        # escape hatches to work around missing cdk construct features
        http_api_cfn: apigateway.CfnApi = self._http_api.node.default_child
        http_api_cfn.add_property_override("FailOnWarnings", fail_on_warnings)
        http_api_cfn.add_property_override("Body", openapi)
        http_api_cfn.add_property_deletion_override("Name")
        http_api_cfn.add_property_deletion_override("ProtocolType")

        # construct arn of httpApi
        self._http_api_arn = (
            f"arn:{scope.partition}:execute-api:"
            f"{self._http_api.env.region}:{self._http_api.env.account}:"
            f"{self._http_api.http_api_id}/*/*/*"
        )

        # output http api url
        core.CfnOutput(self, "HttpApiUrl", value=self._http_api.url)


def json_or_yaml_to_dict(string: str) -> dict:
    """Parse JSON/YAML string to dict.

    Parameters
    ----------
    string : str
        String containing a valid JSON or YAML document.

    Returns
    -------
    dict
        Dictionary of the parsed string.

    Raises
    ------
    ValueError
        If the string can neither be parsed as JSON nor YAML.
    """
    try:
        return json.loads(string)
    except Exception:
        pass

    try:
        return yaml.safe_load(string)
    except Exception:
        pass

    raise ValueError("Failed parsing string as JSON or YAML")
