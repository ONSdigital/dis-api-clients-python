from pydantic import AliasChoices, BaseModel, Field

from .common import Description


class Version(BaseModel):
    uri: str = ""
    release_date: str = Field(default="", validation_alias="updateDate")
    notice: str = Field(default="", validation_alias="correctionNotice")
    label: str = ""


class Download(BaseModel):
    file: str = ""
    uri: str = ""
    version: str = ""
    size: str = Field(default="", validation_alias=AliasChoices("Size", "size"))


class SupplementaryFile(BaseModel):
    title: str = ""
    file: str = ""
    uri: str = ""
    version: str = ""
    size: str = Field(default="", validation_alias=AliasChoices("Size", "size"))


class Dataset(BaseModel):
    type: str = ""
    uri: str = ""
    description: Description = Field(default_factory=Description)
    downloads: list[Download] = Field(default_factory=list)
    supplementary_files: list[SupplementaryFile] = Field(
        default_factory=list,
        validation_alias="supplementaryFiles",
    )
    versions: list[Version] = Field(default_factory=list)


class FileSize(BaseModel):
    size: int = Field(default=0, validation_alias="fileSize")
