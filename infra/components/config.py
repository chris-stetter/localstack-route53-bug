import pulumi_aws as aws

localstack_host = "http://localstack:4566"
endpoints = {attr: localstack_host for attr in dir(
    aws.ProviderEndpointArgs) if not "_" in attr}
endpoints["lambda"] = localstack_host

localstack_config = {
    "skip_credentials_validation": True,
    "skip_requesting_account_id": True,
    "s3_use_path_style": True,
    "access_key": "test",
    "secret_key": "test",
    "endpoints": [endpoints],
}