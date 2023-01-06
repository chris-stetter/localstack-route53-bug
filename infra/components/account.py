import pulumi_aws as aws
from pulumi import ComponentResource, Output, ResourceOptions


class Account(ComponentResource):

    def __init__(
        self,
        name: str,
        provider_config: dict,
        account_email: str = None,
        opts: ResourceOptions = None
    ):
        """Creates an AWS account and an explicit provider for it.
        Args:
            name (str): The account name.
            provider_config (dict): The config used for the provider.
            account_email (str): The email used for the account.
            opts (ResourceOptions, optional): Additional options. Defaults to None.
        """

        super().__init__('custom:resource:Account', name, {}, opts)

        child_opts = ResourceOptions(parent=self)
        role_name = f"{name}-account-role"

        self.account = aws.organizations.Account(
            f"{name}-account",
            email=account_email,
            role_name=role_name,
            opts=ResourceOptions.merge(
                    opts, ResourceOptions(parent=self)
                )
        )

        self.id = self.account.id

        # Define explicit provider to work with created account
        assume_role = aws.ProviderAssumeRoleArgs(role_arn=Output.concat("arn:aws:iam::", self.account.id, ":role/", role_name))
        self.provider = aws.Provider(
            f"{name}-account-provider",
            assume_role=assume_role,
            opts=child_opts,
            **provider_config
        )

        self.us_provider = aws.Provider(
            f"{name}-account-us-provider",
            assume_role=assume_role,
            opts=child_opts,
            **provider_config
        )

        self.register_outputs({})
