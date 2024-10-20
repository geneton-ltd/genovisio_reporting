import pydantic

from genovisio_report.src import enums, input_utils


class ISVFeatures(pydantic.BaseModel):
    gencode_genes: int
    protein_coding: int
    pseudogenes: int
    mirna: int
    lncrna: int
    rrna: int
    snrna: int
    morbid_genes: int
    disease_associated_genes: int
    hi_genes: int
    regions_HI: int
    regions_TS: int
    regulatory: int
    regulatory_enhancer: int
    regulatory_silencer: int
    regulatory_transcriptional_cis_regulatory_region: int
    regulatory_promoter: int
    regulatory_DNase_I_hypersensitive_site: int
    regulatory_enhancer_blocking_element: int
    regulatory_TATA_box: int

    def as_dict(self) -> dict[str, int]:
        return self.model_dump()


class SHAPs(pydantic.BaseModel):
    gencode_genes: float
    protein_coding: float
    pseudogenes: float
    mirna: float
    lncrna: float
    rrna: float
    snrna: float
    morbid_genes: float
    disease_associated_genes: float
    hi_genes: float
    regions_HI: float
    regions_TS: float
    regulatory: float
    regulatory_enhancer: float
    regulatory_silencer: float
    regulatory_transcriptional_cis_regulatory_region: float
    regulatory_promoter: float
    regulatory_DNase_I_hypersensitive_site: float
    regulatory_enhancer_blocking_element: float
    regulatory_TATA_box: float

    def as_dict(self) -> dict[str, float]:
        return self.model_dump()


class ISVResult(pydantic.BaseModel):
    prediction: float = pydantic.Field(alias="isv_prediction")
    score: float = pydantic.Field(alias="isv_score")
    classification: enums.Severity = pydantic.Field(alias="isv_classification")
    isv_shap_values: SHAPs = pydantic.Field(alias="isv_shap_values")
    isv_shap_scores: SHAPs = pydantic.Field(alias="isv_shap_scores")
    isv_features: ISVFeatures = pydantic.Field(alias="isv_features")

    @pydantic.field_validator("classification", mode="before")
    def classification_uppercase(cls, v: str) -> enums.Severity:
        if v.upper() == "VOUS":
            return enums.Severity.VARIANT_OF_UNCERTAIN_SIGNIFICANCE
        return enums.Severity(v.upper())

    @classmethod
    def construct_from_json_file(cls, path: str) -> "ISVResult":
        return cls(**input_utils.load_json_from_path(path))
