# cdk-openapigatewayv2
> AWS CDK Construct that creates an API Gateway v2 based on a parameterized OpenApi JSON Document.

## Installation

```sh
pip install openapigatewayv2
```

## Usage

### Example 1: API backed by Lambda Function

*openapi.json:*
```json
... "${API_LAMBDA_ARN}"
```

```python
from aws_cdk import aws_iam as iam, aws_lambda as _lambda
from openapigatewayv2 import OpenApiGateway

api_lambda = ...

# ${<key>} in openapi_json_path will be replaced by <value>
params_to_replace = {"API_LAMBDA_ARN": api_lambda.function_arn}
openapi = OpenApiGateway(
    self,
    "OpenAPI Gateway",
    openapi_json_path="openapi.json",
    param_value_dict=params_to_replace,
    fail_on_warnings=True,
)

# get createad httpApi resource
http_api = openapi.http_api

http_api_arn = (
    f"arn:{scope.partition}:execute-api:"
    f"{http_api.env.region}:{http_api.env.account}:"
    f"{http_api.http_api_id}/*/*/*"
)

# grant api gateway permission to invoke lambda function
api_lambda.add_permission(
        f"Invoke By {http_api.id} Permission",
        principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
        action="lambda:InvokeFunction",
        source_arn=http_api_arn,
)
```

## Development setup

To install this package, along with the tools you need to develop and publish
it, run the following:

```sh
pip install -e .[dev]
```

## Contributing

1. [Fork this repository](https://github.com/suud/openapigatewayv2/fork)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

MIT
