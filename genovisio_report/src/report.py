import ast
import csv
from dataclasses import asdict, dataclass

from genovisio_report.src import enums, reports


@dataclass
class FlatReportData:
    """
    Flat representation of the report data. Quite cumbersome, but the schema must be explicit and clear.
    """

    report_id: str | None
    cnv_type: str
    cnv_position: str
    marcnv_section1_reason: str
    marcnv_section1_option: str
    marcnv_section1_score: float
    marcnv_section2_reason: str
    marcnv_section2_option: str
    marcnv_section2_score: float
    marcnv_section3_reason: str
    marcnv_section3_option: str
    marcnv_section3_score: float
    marcnv_section4_reason: str
    marcnv_section4_option: str
    marcnv_section4_score: float
    marcnv_section5_reason: str
    marcnv_section5_option: str
    marcnv_section5_score: float
    score_marcnv: float
    score_isv: float
    score_hybrid: float
    classification_marcnv: enums.Severity
    classification_isv: enums.Severity
    classification_hybrid: enums.Severity
    genes_protein_coding_count: int
    genes_morbid_count: int
    genes_disease_associated_count: int
    genes_hi_count: int
    genes_ts_count: int
    genes_morbid_list: list[str]
    genes_disease_associated_list: list[str]
    genes_hi_list: list[str]
    genes_ts_list: list[str]
    isv_gencode_genes: int
    isv_protein_coding: int
    isv_pseudogenes: int
    isv_mirna: int
    isv_lncrna: int
    isv_rrna: int
    isv_snrna: int
    isv_morbid_genes: int
    isv_disease_associated_genes: int
    isv_hi_genes: int
    isv_regions_HI: int
    isv_regions_TS: int
    isv_regulatory: int
    isv_regulatory_enhancer: int
    isv_regulatory_silencer: int
    isv_regulatory_transcriptional_cis_regulatory_region: int
    isv_regulatory_promoter: int
    isv_regulatory_DNase_I_hypersensitive_site: int
    isv_regulatory_enhancer_blocking_element: int
    isv_regulatory_TATA_box: int
    isv_shap_gencode_genes: float
    isv_shap_protein_coding: float
    isv_shap_pseudogenes: float
    isv_shap_mirna: float
    isv_shap_lncrna: float
    isv_shap_rrna: float
    isv_shap_snrna: float
    isv_shap_morbid_genes: float
    isv_shap_disease_associated_genes: float
    isv_shap_hi_genes: float
    isv_shap_regions_HI: float
    isv_shap_regions_TS: float
    isv_shap_regulatory: float
    isv_shap_regulatory_enhancer: float
    isv_shap_regulatory_silencer: float
    isv_shap_regulatory_transcriptional_cis_regulatory_region: float
    isv_shap_regulatory_promoter: float
    isv_shap_regulatory_DNase_I_hypersensitive_site: float
    isv_shap_regulatory_enhancer_blocking_element: float
    isv_shap_regulatory_TATA_box: float
    workflow_version: str | None
    report_version: str

    def store_as_csv(self, csv_file: str) -> None:
        with open(csv_file, "w", newline="") as f:
            flat_dict = asdict(self)
            fieldnames = flat_dict.keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerow(flat_dict)

    @classmethod
    def load_from_csv(cls, csv_file: str) -> "FlatReportData":
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f, quoting=csv.QUOTE_ALL)
            row = next(reader)
        return cls(
            report_id=row["report_id"],
            cnv_type=row["cnv_type"],
            cnv_position=row["cnv_position"],
            marcnv_section1_reason=row["marcnv_section1_reason"],
            marcnv_section1_option=row["marcnv_section1_option"],
            marcnv_section1_score=float(row["marcnv_section1_score"]),
            marcnv_section2_reason=row["marcnv_section2_reason"],
            marcnv_section2_option=row["marcnv_section2_option"],
            marcnv_section2_score=float(row["marcnv_section2_score"]),
            marcnv_section3_reason=row["marcnv_section3_reason"],
            marcnv_section3_option=row["marcnv_section3_option"],
            marcnv_section3_score=float(row["marcnv_section3_score"]),
            marcnv_section4_reason=row["marcnv_section4_reason"],
            marcnv_section4_option=row["marcnv_section4_reason"],
            marcnv_section4_score=float(row["marcnv_section4_score"]),
            marcnv_section5_reason=row["marcnv_section5_reason"],
            marcnv_section5_option=row["marcnv_section5_reason"],
            marcnv_section5_score=float(row["marcnv_section5_score"]),
            score_marcnv=float(row["score_marcnv"]),
            score_isv=float(row["score_isv"]),
            score_hybrid=float(row["score_hybrid"]),
            classification_marcnv=enums.Severity(row["classification_marcnv"]),
            classification_isv=enums.Severity(row["classification_isv"]),
            classification_hybrid=enums.Severity(row["classification_hybrid"]),
            genes_protein_coding_count=int(row["genes_protein_coding_count"]),
            genes_morbid_count=int(row["genes_morbid_count"]),
            genes_disease_associated_count=int(row["genes_disease_associated_count"]),
            genes_hi_count=int(row["genes_hi_count"]),
            genes_ts_count=int(row["genes_ts_count"]),
            genes_morbid_list=ast.literal_eval(row["genes_morbid_list"]),
            genes_disease_associated_list=ast.literal_eval(row["genes_disease_associated_list"]),
            genes_hi_list=ast.literal_eval(row["genes_hi_list"]),
            genes_ts_list=ast.literal_eval(row["genes_ts_list"]),
            isv_gencode_genes=int(row["isv_gencode_genes"]),
            isv_protein_coding=int(row["isv_protein_coding"]),
            isv_pseudogenes=int(row["isv_pseudogenes"]),
            isv_mirna=int(row["isv_mirna"]),
            isv_lncrna=int(row["isv_lncrna"]),
            isv_rrna=int(row["isv_rrna"]),
            isv_snrna=int(row["isv_snrna"]),
            isv_morbid_genes=int(row["isv_morbid_genes"]),
            isv_disease_associated_genes=int(row["isv_disease_associated_genes"]),
            isv_hi_genes=int(row["isv_hi_genes"]),
            isv_regions_HI=int(row["isv_regions_HI"]),
            isv_regions_TS=int(row["isv_regions_TS"]),
            isv_regulatory=int(row["isv_regulatory"]),
            isv_regulatory_enhancer=int(row["isv_regulatory_enhancer"]),
            isv_regulatory_silencer=int(row["isv_regulatory_silencer"]),
            isv_regulatory_transcriptional_cis_regulatory_region=int(
                row["isv_regulatory_transcriptional_cis_regulatory_region"]
            ),
            isv_regulatory_promoter=int(row["isv_regulatory_promoter"]),
            isv_regulatory_DNase_I_hypersensitive_site=int(row["isv_regulatory_DNase_I_hypersensitive_site"]),
            isv_regulatory_enhancer_blocking_element=int(row["isv_regulatory_enhancer_blocking_element"]),
            isv_regulatory_TATA_box=int(row["isv_regulatory_TATA_box"]),
            isv_shap_gencode_genes=float(row["isv_shap_gencode_genes"]),
            isv_shap_protein_coding=float(row["isv_shap_protein_coding"]),
            isv_shap_pseudogenes=float(row["isv_shap_pseudogenes"]),
            isv_shap_mirna=float(row["isv_shap_mirna"]),
            isv_shap_lncrna=float(row["isv_shap_lncrna"]),
            isv_shap_rrna=float(row["isv_shap_rrna"]),
            isv_shap_snrna=float(row["isv_shap_snrna"]),
            isv_shap_morbid_genes=float(row["isv_shap_morbid_genes"]),
            isv_shap_disease_associated_genes=float(row["isv_shap_disease_associated_genes"]),
            isv_shap_hi_genes=float(row["isv_shap_hi_genes"]),
            isv_shap_regions_HI=float(row["isv_shap_regions_HI"]),
            isv_shap_regions_TS=float(row["isv_shap_regions_TS"]),
            isv_shap_regulatory=float(row["isv_shap_regulatory"]),
            isv_shap_regulatory_enhancer=float(row["isv_shap_regulatory_enhancer"]),
            isv_shap_regulatory_silencer=float(row["isv_shap_regulatory_silencer"]),
            isv_shap_regulatory_transcriptional_cis_regulatory_region=float(
                row["isv_shap_regulatory_transcriptional_cis_regulatory_region"]
            ),
            isv_shap_regulatory_promoter=float(row["isv_shap_regulatory_promoter"]),
            isv_shap_regulatory_DNase_I_hypersensitive_site=float(
                row["isv_shap_regulatory_DNase_I_hypersensitive_site"]
            ),
            isv_shap_regulatory_enhancer_blocking_element=float(row["isv_shap_regulatory_enhancer_blocking_element"]),
            isv_shap_regulatory_TATA_box=float(row["isv_shap_regulatory_TATA_box"]),
            workflow_version=row["workflow_version"],
            report_version=row["report_version"],
        )


@dataclass
class ReportData:
    report_id: str | None
    cnv_info: reports.CNVInfo
    marcnv: reports.MarcNVReport
    scores: reports.ScoreReport
    genes: reports.GenesReport
    classification_marcnv: enums.Severity
    classification_isv: enums.Severity
    classification_hybrid: enums.Severity
    isv_shaps: reports.ShapData
    workflow_version: str | None
    report_version: str

    @property
    def version_string(self) -> str:
        if self.workflow_version:
            return f"Generated from workflow v{self.workflow_version}"
        return f"Generated by reporting v{self.report_version}"

    @property
    def flatten(self) -> FlatReportData:
        return FlatReportData(
            report_id=self.report_id,
            cnv_type=self.cnv_info.type,
            cnv_position=self.cnv_info.pos,
            marcnv_section1_reason=self.marcnv.Section_1.reason,
            marcnv_section1_option=self.marcnv.Section_1.option,
            marcnv_section1_score=self.marcnv.Section_1.score,
            marcnv_section2_reason=self.marcnv.Section_2.reason,
            marcnv_section2_option=self.marcnv.Section_2.option,
            marcnv_section2_score=self.marcnv.Section_2.score,
            marcnv_section3_reason=self.marcnv.Section_3.reason,
            marcnv_section3_option=self.marcnv.Section_3.option,
            marcnv_section3_score=self.marcnv.Section_3.score,
            marcnv_section4_reason=self.marcnv.Section_4.reason,
            marcnv_section4_option=self.marcnv.Section_4.option,
            marcnv_section4_score=self.marcnv.Section_4.score,
            marcnv_section5_reason=self.marcnv.Section_5.reason,
            marcnv_section5_option=self.marcnv.Section_5.option,
            marcnv_section5_score=self.marcnv.Section_5.score,
            score_marcnv=self.scores.marcnv,
            score_isv=self.scores.isv,
            score_hybrid=self.scores.hybrid,
            classification_marcnv=self.classification_marcnv,
            classification_isv=self.classification_isv,
            classification_hybrid=self.classification_hybrid,
            genes_protein_coding_count=self.genes.protein_coding,
            genes_morbid_count=self.genes.morbid.count,
            genes_disease_associated_count=self.genes.disease.count,
            genes_hi_count=self.genes.hi.count,
            genes_ts_count=self.genes.ts.count,
            genes_morbid_list=self.genes.morbid.genes,
            genes_disease_associated_list=self.genes.disease.genes,
            genes_hi_list=self.genes.hi.genes,
            genes_ts_list=self.genes.ts.genes,
            isv_gencode_genes=self.isv_shaps.gencode_genes.value,
            isv_protein_coding=self.isv_shaps.protein_coding.value,
            isv_pseudogenes=self.isv_shaps.pseudogenes.value,
            isv_mirna=self.isv_shaps.mirna.value,
            isv_lncrna=self.isv_shaps.lncrna.value,
            isv_rrna=self.isv_shaps.rrna.value,
            isv_snrna=self.isv_shaps.snrna.value,
            isv_morbid_genes=self.isv_shaps.morbid.value,
            isv_disease_associated_genes=self.isv_shaps.disease_associated.value,
            isv_hi_genes=self.isv_shaps.hi_genes.value,
            isv_regions_HI=self.isv_shaps.regions_HI.value,
            isv_regions_TS=self.isv_shaps.regions_TS.value,
            isv_regulatory=self.isv_shaps.regulatory.value,
            isv_regulatory_enhancer=self.isv_shaps.regulatory_enhancer.value,
            isv_regulatory_silencer=self.isv_shaps.regulatory_silencer.value,
            isv_regulatory_transcriptional_cis_regulatory_region=self.isv_shaps.regulatory_transcriptional_cis_regulatory_region.value,
            isv_regulatory_promoter=self.isv_shaps.regulatory_promoter.value,
            isv_regulatory_DNase_I_hypersensitive_site=self.isv_shaps.regulatory_DNase_I_hypersensitive_site.value,
            isv_regulatory_enhancer_blocking_element=self.isv_shaps.regulatory_enhancer_blocking_element.value,
            isv_regulatory_TATA_box=self.isv_shaps.regulatory_TATA_box.value,
            isv_shap_gencode_genes=self.isv_shaps.gencode_genes.shap,
            isv_shap_protein_coding=self.isv_shaps.protein_coding.shap,
            isv_shap_pseudogenes=self.isv_shaps.pseudogenes.shap,
            isv_shap_mirna=self.isv_shaps.mirna.shap,
            isv_shap_lncrna=self.isv_shaps.lncrna.shap,
            isv_shap_rrna=self.isv_shaps.rrna.shap,
            isv_shap_snrna=self.isv_shaps.snrna.shap,
            isv_shap_morbid_genes=self.isv_shaps.morbid.shap,
            isv_shap_disease_associated_genes=self.isv_shaps.disease_associated.shap,
            isv_shap_hi_genes=self.isv_shaps.hi_genes.shap,
            isv_shap_regions_HI=self.isv_shaps.regions_HI.shap,
            isv_shap_regions_TS=self.isv_shaps.regions_TS.shap,
            isv_shap_regulatory=self.isv_shaps.regulatory.shap,
            isv_shap_regulatory_enhancer=self.isv_shaps.regulatory_enhancer.shap,
            isv_shap_regulatory_silencer=self.isv_shaps.regulatory_silencer.shap,
            isv_shap_regulatory_transcriptional_cis_regulatory_region=self.isv_shaps.regulatory_transcriptional_cis_regulatory_region.shap,
            isv_shap_regulatory_promoter=self.isv_shaps.regulatory_promoter.shap,
            isv_shap_regulatory_DNase_I_hypersensitive_site=self.isv_shaps.regulatory_DNase_I_hypersensitive_site.shap,
            isv_shap_regulatory_enhancer_blocking_element=self.isv_shaps.regulatory_enhancer_blocking_element.shap,
            isv_shap_regulatory_TATA_box=self.isv_shaps.regulatory_TATA_box.shap,
            workflow_version=self.workflow_version,
            report_version=self.report_version,
        )
