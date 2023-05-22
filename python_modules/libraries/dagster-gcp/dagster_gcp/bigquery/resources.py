from contextlib import contextmanager
from typing import Any, Iterator, Optional

from dagster import (
    ConfigurableResource,
    IAttachDifferentObjectToOpContext,
    ResourceDependency,
    resource,
)
from dagster._core.definitions.resource_definition import dagster_maintained_resource

from google.cloud import bigquery
from pydantic import Field

from ..auth.resources import GoogleAuthResource


class BigQueryResource(ConfigurableResource, IAttachDifferentObjectToOpContext):
    """Resource for interacting with Google BigQuery.

    Examples:
        .. code-block:: python

            from dagster import Definitions, asset
            from dagster_gcp import BigQueryResource

            @asset
            def my_table(bigquery: BigQueryResource):
                with bigquery.get_client() as client:
                    client.query("SELECT * FROM my_dataset.my_table")

            defs = Definitions(
                assets=[my_table],
                resources={
                    "bigquery": BigQueryResource(project="my-project")
                }
            )
    """

    project: Optional[str] = Field(
        default=None,
        description=(
            "Project ID for the project which the client acts on behalf of. Will be passed when"
            " creating a dataset / job. If not passed, falls back to the default inferred from the"
            " environment."
        ),
    )

    location: Optional[str] = Field(
        default=None,
        description="Default location for jobs / datasets / tables.",
    )

    google_auth_resource: ResourceDependency[Optional[GoogleAuthResource]]

    gcp_credentials: Optional[str] = Field(
        default=None,
        description=(
            "GCP authentication credentials. If provided, a temporary file will be created"
            " with the credentials and ``GOOGLE_APPLICATION_CREDENTIALS`` will be set to the"
            " temporary file. To avoid issues with newlines in the keys, you must base64"
            " encode the key. You can retrieve the base64 encoded key with this shell"
            " command: ``cat $GOOGLE_AUTH_CREDENTIALS | base64``"
        ),
    )

    @classmethod
    def _is_dagster_maintained(cls) -> bool:
        return True

    @contextmanager
    def get_client(self) -> Iterator[bigquery.Client]:
        """Context manager to create a BigQuery Client.

        Examples:
            .. code-block:: python

                from dagster import asset
                from dagster_gcp import BigQueryResource

                @asset
                def my_table(bigquery: BigQueryResource):
                    with bigquery.get_client() as client:
                        client.query("SELECT * FROM my_dataset.my_table")
        """
        if self.google_auth_resource is None:
            if self.gcp_credentials is not None:
                auth_resource = GoogleAuthResource(service_account_info=self.gcp_credentials)
            else:
                auth_resource = GoogleAuthResource()
        else:
            auth_resource = self.google_auth_resource

        yield bigquery.Client(
            project=self.project,
            location=self.location,
            credentials=auth_resource.get_credentials(),
        )

    def get_object_to_set_on_execution_context(self) -> Any:
        with self.get_client() as client:
            yield client


@dagster_maintained_resource
@resource(
    config_schema=BigQueryResource.to_config_schema(),
    description="Dagster resource for connecting to BigQuery",
)
def bigquery_resource(context):
    bq_resource = BigQueryResource.from_resource_context(context)
    with bq_resource.get_client() as client:
        yield client
