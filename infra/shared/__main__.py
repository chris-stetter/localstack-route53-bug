import pulumi
import pulumi_aws as aws
from infra.components.config import localstack_config

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

config = pulumi.Config()
domain_name = config.require('rootDomain')

hosted_zone = aws.route53.Zone("primary", name=domain_name,
                           opts=org_default_resource_options)

pulumi.export("hosted_zone", hosted_zone)