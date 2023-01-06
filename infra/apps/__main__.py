import pulumi
import pulumi_aws as aws
from infra.components.account import Account
from infra.components.config import localstack_config

shared_stack = pulumi.StackReference("dev-shared")
root_hosted_zone = shared_stack.get_output("hosted_zone")

org_provider = aws.Provider("provider", **localstack_config)
org_default_resource_options = pulumi.ResourceOptions(provider=org_provider)

# When using Localstack there is by default no organization to work with, otherwise: AWSOrganizationsNotInUseException
org = aws.organizations.Organization(
    "org",
    aws_service_access_principals=[
        "cloudtrail.amazonaws.com",
        "config.amazonaws.com",
    ],
    feature_set="ALL",
    opts=org_default_resource_options
)

# The account needs an organization to be deployed
org_default_resource_options = pulumi.ResourceOptions.merge(
    org_default_resource_options, pulumi.ResourceOptions(depends_on=org)
)

stack = pulumi.get_stack()

account = Account(
    name=stack,
    account_email="info@example.com",
    provider_config=localstack_config,
    opts=org_default_resource_options
)

config = pulumi.Config()
domain_name = f"{stack}.{config.require('domainName')}"

example_certificate = aws.acm.Certificate(
    "exampleCertificate",
    domain_name=domain_name,
    validation_method="DNS",
    opts=pulumi.ResourceOptions(provider=account.us_provider)
)

cert_validation = aws.route53.Record(
    "certValidation",
    name=example_certificate.domain_validation_options[0].resource_record_name,
    records=[example_certificate.domain_validation_options[0].resource_record_value],
    ttl=60,
    type=example_certificate.domain_validation_options[0].resource_record_type,
    zone_id=root_hosted_zone["zone_id"],
    opts=org_default_resource_options
)

cert_certificate_validation = aws.acm.CertificateValidation(
    "cert",
    certificate_arn=example_certificate.arn,
    validation_record_fqdns=[cert_validation.fqdn],
    opts=pulumi.ResourceOptions(provider=account.us_provider)
)

pulumi.export("certificate_arn", cert_certificate_validation.certificate_arn)
