from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="openapigateway",
    version="0.1.4",
    description=(
        "AWS CDK Construct that creates an Amazon API Gateway HttpApi "
        "based on a parameterized OpenAPI 3 Document."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suud/cdk-openapigateway",
    author="Timo Sutterer",
    author_email="hi@timo-sutterer.de",
    packages=["openapigateway"],
    install_requires=[
        "PyYAML",
        "aws-cdk.core>=1.79.0",
        "aws-cdk.aws-apigatewayv2>=1.79.0",
    ],
    extras_require={
        "dev": [
            "wheel==0.36.2",
            "twine==3.3.0",
            "bump2version==1.0.1",
        ],
    },
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 1",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
)
