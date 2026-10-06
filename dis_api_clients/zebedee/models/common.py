from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str = ""
    email: str = ""
    telephone: str = ""


class Description(BaseModel):
    title: str = ""
    edition: str = ""
    summary: str = ""
    keywords: list[str] = Field(default_factory=list)
    meta_description: str = Field(default="", validation_alias="metaDescription")
    migration_link: str = Field(default="", validation_alias="migrationLink")
    national_statistic: bool = Field(default=False, validation_alias="nationalStatistic")
    welsh_statistic: bool = Field(default=False, validation_alias="welshStatistic")
    survey: str = ""
    latest_release: bool = Field(default=False, validation_alias="latestRelease")
    contact: Contact = Field(default_factory=Contact)
    release_date: str = Field(default="", validation_alias="releaseDate")
    next_release: str = Field(default="", validation_alias="nextRelease")
    dataset_id: str = Field(default="", validation_alias="datasetId")
    unit: str = ""
    pre_unit: str = Field(default="", validation_alias="preUnit")
    source: str = ""
    version_label: str = Field(default="", validation_alias="versionLabel")
    canonical_topic: str = Field(default="", validation_alias="canonicalTopic")
    topics: list[str] = Field(default_factory=list, validation_alias="secondaryTopics")
    finalised: bool = False
    cancelled: bool = False
    cancellation_notice: list[str] = Field(default_factory=list, validation_alias="cancellationNotice")
    published: bool = False
    provisional_date: str = Field(default="", validation_alias="provisionalDate")
    abstract: str = Field(default="", validation_alias="_abstract")


class Link(BaseModel):
    title: str = ""
    summary: str = ""
    uri: str = ""


class Alert(BaseModel):
    date: str = ""
    markdown: str = ""
    type: str = ""


class Section(BaseModel):
    title: str = ""
    markdown: str = ""
