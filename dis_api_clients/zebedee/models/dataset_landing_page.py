from pydantic import BaseModel, Field

from .common import Alert, Description, Link, Section


class DatasetLandingPage(BaseModel):
    type: str = ""
    uri: str = ""
    description: Description = Field(default_factory=Description)
    section: Section = Field(default_factory=Section)
    datasets: list[Link] = Field(default_factory=list)
    related_links: list[Link] = Field(default_factory=list, validation_alias="links")
    related_filterable_datasets: list[Link] = Field(
        default_factory=list,
        validation_alias="relatedFilterableDatasets",
    )
    related_datasets: list[Link] = Field(default_factory=list, validation_alias="relatedDatasets")
    related_documents: list[Link] = Field(default_factory=list, validation_alias="relatedDocuments")
    related_methodology: list[Link] = Field(default_factory=list, validation_alias="relatedMethodology")
    related_methodology_article: list[Link] = Field(
        default_factory=list,
        validation_alias="relatedMethodologyArticle",
    )
    alerts: list[Alert] = Field(default_factory=list)
    timeseries: bool = False


class PageTitle(BaseModel):
    title: str = ""
    edition: str = ""
    uri: str = ""
