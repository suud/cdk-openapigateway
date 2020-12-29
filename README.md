# openapigateway
> Create an Amazon API Gateway from an OpenAPI 3 Document.

![PyPI](https://img.shields.io/pypi/v/openapigateway)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapigateway)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - License](https://img.shields.io/pypi/l/openapigateway)

AWS CDK Construct that creates an Amazon API Gateway HttpApi based on a
parameterized OpenAPI 3 Document.

## Installation

```sh
pip install openapigateway
```

## Usage

### Example 1: API backed by Lambda Function

*openapi.yaml:*
```yaml
[...]
paths:
  /pets:
    get:
      summary: List all pets
      responses:
        [...]
      x-amazon-apigateway-integration:
        uri: "${API_LAMBDA_ARN}"
        type: "AWS_PROXY"
        httpMethod: "POST"
        connectionType: "INTERNET"
        payloadFormatVersion: "2.0"
      x-amazon-apigateway-request-validator:
        validateRequestBody: true
        validateRequestParameters: true
[...]
```

*open_api_stack.py:*
```python
from aws_cdk import core, aws_iam as iam, aws_lambda as _lambda
from openapigateway import OpenApiGateway


class OpenApiStack(core.Stack):
    def __init__(
        self, scope: core.Construct, construct_id: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # function that handles api request(s)
        api_lambda = _lambda.Function([...])

        # create api from openapi document and replace params
        openapi = OpenApiGateway(
            self,
            "OpenAPI Gateway",
            openapi_path="openapi.yaml",
            param_value_dict={"API_LAMBDA_ARN": api_lambda.function_arn},
            fail_on_warnings=True,
        )

        # get arn of createad HttpApi resource
        http_api = openapi.http_api
        http_api_arn = (
            f"arn:{self.partition}:execute-api:"
            f"{http_api.env.region}:{http_api.env.account}:"
            f"{http_api.http_api_id}/*/*/*"
        )

        # grant HttpApi permission to invoke api lambda function
        api_lambda.add_permission(
            f"Invoke By {http_api.node.id} Permission",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=http_api_arn,
        )
```

## [Documentation](https://suud.github.io/cdk-openapigateway)

## Development setup

### optional: use virtualenv

```sh
# create virtualenv on MacOS and Linux
python3 -m venv .venv
# activate virtualenv
source .venv/bin/activate
```

### install dependencies

To install this package, along with the tools you need to develop and publish
it, run the following:

```sh
pip install -e ".[dev]"
```

## Contributing

1. [Fork this repository](https://github.com/suud/cdk-openapigateway/fork)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

MIT
