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
    chrom: str
    start: int
    end: int
    cnv_type: str
    cytogenetic_location: str
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
    genes_morbid_url: list[str]
    genes_disease_associated_url: list[str]
    genes_hi_url: list[str]
    genes_ts_url: list[str]
    isv_gencode_genes: int | None
    isv_protein_coding: int | None
    isv_pseudogenes: int | None
    isv_mirna: int | None
    isv_lncrna: int | None
    isv_rrna: int | None
    isv_snrna: int | None
    isv_morbid_genes: int | None
    isv_disease_associated_genes: int | None
    isv_hi_genes: int | None
    isv_regions_HI: int | None
    isv_regions_TS: int | None
    isv_regulatory: int | None
    isv_regulatory_enhancer: int | None
    isv_regulatory_silencer: int | None
    isv_regulatory_transcriptional_cis_regulatory_region: int | None
    isv_regulatory_promoter: int | None
    isv_regulatory_DNase_I_hypersensitive_site: int | None
    isv_regulatory_enhancer_blocking_element: int | None
    isv_regulatory_TATA_box: int | None
    isv_shap_gencode_genes: float | None
    isv_shap_protein_coding: float | None
    isv_shap_pseudogenes: float | None
    isv_shap_mirna: float | None
    isv_shap_lncrna: float | None
    isv_shap_rrna: float | None
    isv_shap_snrna: float | None
    isv_shap_morbid_genes: float | None
    isv_shap_disease_associated_genes: float | None
    isv_shap_hi_genes: float | None
    isv_shap_regions_HI: float | None
    isv_shap_regions_TS: float | None
    isv_shap_regulatory: float | None
    isv_shap_regulatory_enhancer: float | None
    isv_shap_regulatory_silencer: float | None
    isv_shap_regulatory_transcriptional_cis_regulatory_region: float | None
    isv_shap_regulatory_promoter: float | None
    isv_shap_regulatory_DNase_I_hypersensitive_site: float | None
    isv_shap_regulatory_enhancer_blocking_element: float | None
    isv_shap_regulatory_TATA_box: float | None
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
            chrom=row["chrom"],
            start=int(row["start"]),
            end=int(row["end"]),
            cnv_type=row["cnv_type"],
            cytogenetic_location=row["cytogenetic_location"],
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
            genes_morbid_url=ast.literal_eval(row['genes_morbid_url']),
            genes_disease_associated_url=ast.literal_eval(row['genes_disease_associated_url']),
            genes_hi_url=ast.literal_eval(row['genes_hi_url']),
            genes_ts_url=ast.literal_eval(row['genes_ts_url']),
            isv_gencode_genes=int(row["isv_gencode_genes"]) if row["isv_gencode_genes"] else None,
            isv_protein_coding=int(row["isv_protein_coding"]) if row["isv_protein_coding"] else None,
            isv_pseudogenes=int(row["isv_pseudogenes"]) if row["isv_pseudogenes"] else None,
            isv_mirna=int(row["isv_mirna"]) if row["isv_mirna"] else None,
            isv_lncrna=int(row["isv_lncrna"]) if row["isv_lncrna"] else None,
            isv_rrna=int(row["isv_rrna"]) if row["isv_rrna"] else None,
            isv_snrna=int(row["isv_snrna"]) if row["isv_snrna"] else None,
            isv_morbid_genes=int(row["isv_morbid_genes"]) if row["isv_morbid_genes"] else None,
            isv_disease_associated_genes=int(row["isv_disease_associated_genes"])
            if row["isv_disease_associated_genes"]
            else None,
            isv_hi_genes=int(row["isv_hi_genes"]) if row["isv_hi_genes"] else None,
            isv_regions_HI=int(row["isv_regions_HI"]) if row["isv_regions_HI"] else None,
            isv_regions_TS=int(row["isv_regions_TS"]) if row["isv_regions_TS"] else None,
            isv_regulatory=int(row["isv_regulatory"]) if row["isv_regulatory"] else None,
            isv_regulatory_enhancer=int(row["isv_regulatory_enhancer"]) if row["isv_regulatory_enhancer"] else None,
            isv_regulatory_silencer=int(row["isv_regulatory_silencer"]) if row["isv_regulatory_silencer"] else None,
            isv_regulatory_transcriptional_cis_regulatory_region=int(
                row["isv_regulatory_transcriptional_cis_regulatory_region"]
            )
            if row["isv_regulatory_transcriptional_cis_regulatory_region"]
            else None,
            isv_regulatory_promoter=int(row["isv_regulatory_promoter"]) if row["isv_regulatory_promoter"] else None,
            isv_regulatory_DNase_I_hypersensitive_site=int(row["isv_regulatory_DNase_I_hypersensitive_site"])
            if row["isv_regulatory_DNase_I_hypersensitive_site"]
            else None,
            isv_regulatory_enhancer_blocking_element=int(row["isv_regulatory_enhancer_blocking_element"])
            if row["isv_regulatory_enhancer_blocking_element"]
            else None,
            isv_regulatory_TATA_box=int(row["isv_regulatory_TATA_box"]) if row["isv_regulatory_TATA_box"] else None,
            isv_shap_gencode_genes=float(row["isv_shap_gencode_genes"]) if row["isv_shap_gencode_genes"] else None,
            isv_shap_protein_coding=float(row["isv_shap_protein_coding"]) if row["isv_shap_protein_coding"] else None,
            isv_shap_pseudogenes=float(row["isv_shap_pseudogenes"]) if row["isv_shap_pseudogenes"] else None,
            isv_shap_mirna=float(row["isv_shap_mirna"]) if row["isv_shap_mirna"] else None,
            isv_shap_lncrna=float(row["isv_shap_lncrna"]) if row["isv_shap_lncrna"] else None,
            isv_shap_rrna=float(row["isv_shap_rrna"]) if row["isv_shap_rrna"] else None,
            isv_shap_snrna=float(row["isv_shap_snrna"]) if row["isv_shap_snrna"] else None,
            isv_shap_morbid_genes=float(row["isv_shap_morbid_genes"]) if row["isv_shap_morbid_genes"] else None,
            isv_shap_disease_associated_genes=float(row["isv_shap_disease_associated_genes"])
            if row["isv_shap_disease_associated_genes"]
            else None,
            isv_shap_hi_genes=float(row["isv_shap_hi_genes"]) if row["isv_shap_hi_genes"] else None,
            isv_shap_regions_HI=float(row["isv_shap_regions_HI"]) if row["isv_shap_regions_HI"] else None,
            isv_shap_regions_TS=float(row["isv_shap_regions_TS"]) if row["isv_shap_regions_TS"] else None,
            isv_shap_regulatory=float(row["isv_shap_regulatory"]) if row["isv_shap_regulatory"] else None,
            isv_shap_regulatory_enhancer=float(row["isv_shap_regulatory_enhancer"])
            if row["isv_shap_regulatory_enhancer"]
            else None,
            isv_shap_regulatory_silencer=float(row["isv_shap_regulatory_silencer"])
            if row["isv_shap_regulatory_silencer"]
            else None,
            isv_shap_regulatory_transcriptional_cis_regulatory_region=float(
                row["isv_shap_regulatory_transcriptional_cis_regulatory_region"]
            )
            if row["isv_shap_regulatory_transcriptional_cis_regulatory_region"]
            else None,
            isv_shap_regulatory_promoter=float(row["isv_shap_regulatory_promoter"])
            if row["isv_shap_regulatory_promoter"]
            else None,
            isv_shap_regulatory_DNase_I_hypersensitive_site=float(
                row["isv_shap_regulatory_DNase_I_hypersensitive_site"]
            )
            if row["isv_shap_regulatory_DNase_I_hypersensitive_site"]
            else None,
            isv_shap_regulatory_enhancer_blocking_element=float(row["isv_shap_regulatory_enhancer_blocking_element"])
            if row["isv_shap_regulatory_enhancer_blocking_element"]
            else None,
            isv_shap_regulatory_TATA_box=float(row["isv_shap_regulatory_TATA_box"])
            if row["isv_shap_regulatory_TATA_box"]
            else None,
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
            chrom=self.cnv_info.chr,
            start=self.cnv_info.start,
            end=self.cnv_info.end,
            cytogenetic_location=self.cnv_info.cyto_position,
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
            genes_morbid_url=self.genes.omim_URL_morbid_genes,
            genes_disease_associated_url=self.genes.omim_URL_disease_asscoiated_genes,
            genes_hi_url=self.genes.omim_URL_hi_genes,
            genes_ts_url=self.genes.omim_URL_ts_genes,
            isv_gencode_genes=self.isv_shaps.gencode_genes.value if self.isv_shaps.gencode_genes else None,
            isv_protein_coding=self.isv_shaps.protein_coding.value if self.isv_shaps.protein_coding else None,
            isv_pseudogenes=self.isv_shaps.pseudogenes.value if self.isv_shaps.pseudogenes else None,
            isv_mirna=self.isv_shaps.mirna.value if self.isv_shaps.mirna else None,
            isv_lncrna=self.isv_shaps.lncrna.value if self.isv_shaps.lncrna else None,
            isv_rrna=self.isv_shaps.rrna.value if self.isv_shaps.rrna else None,
            isv_snrna=self.isv_shaps.snrna.value if self.isv_shaps.snrna else None,
            isv_morbid_genes=self.isv_shaps.morbid.value if self.isv_shaps.morbid else None,
            isv_disease_associated_genes=self.isv_shaps.disease_associated.value
            if self.isv_shaps.disease_associated
            else None,
            isv_hi_genes=self.isv_shaps.hi_genes.value if self.isv_shaps.hi_genes else None,
            isv_regions_HI=self.isv_shaps.regions_HI.value if self.isv_shaps.regions_HI else None,
            isv_regions_TS=self.isv_shaps.regions_TS.value if self.isv_shaps.regions_TS else None,
            isv_regulatory=self.isv_shaps.regulatory.value if self.isv_shaps.regulatory else None,
            isv_regulatory_enhancer=self.isv_shaps.regulatory_enhancer.value
            if self.isv_shaps.regulatory_enhancer
            else None,
            isv_regulatory_silencer=self.isv_shaps.regulatory_silencer.value
            if self.isv_shaps.regulatory_silencer
            else None,
            isv_regulatory_transcriptional_cis_regulatory_region=self.isv_shaps.regulatory_transcriptional_cis_regulatory_region.value
            if self.isv_shaps.regulatory_transcriptional_cis_regulatory_region
            else None,
            isv_regulatory_promoter=self.isv_shaps.regulatory_promoter.value
            if self.isv_shaps.regulatory_promoter
            else None,
            isv_regulatory_DNase_I_hypersensitive_site=self.isv_shaps.regulatory_DNase_I_hypersensitive_site.value
            if self.isv_shaps.regulatory_DNase_I_hypersensitive_site
            else None,
            isv_regulatory_enhancer_blocking_element=self.isv_shaps.regulatory_enhancer_blocking_element.value
            if self.isv_shaps.regulatory_enhancer_blocking_element
            else None,
            isv_regulatory_TATA_box=self.isv_shaps.regulatory_TATA_box.value
            if self.isv_shaps.regulatory_TATA_box
            else None,
            isv_shap_gencode_genes=self.isv_shaps.gencode_genes.shap if self.isv_shaps.gencode_genes else None,
            isv_shap_protein_coding=self.isv_shaps.protein_coding.shap if self.isv_shaps.protein_coding else None,
            isv_shap_pseudogenes=self.isv_shaps.pseudogenes.shap if self.isv_shaps.pseudogenes else None,
            isv_shap_mirna=self.isv_shaps.mirna.shap if self.isv_shaps.mirna else None,
            isv_shap_lncrna=self.isv_shaps.lncrna.shap if self.isv_shaps.lncrna else None,
            isv_shap_rrna=self.isv_shaps.rrna.shap if self.isv_shaps.rrna else None,
            isv_shap_snrna=self.isv_shaps.snrna.shap if self.isv_shaps.snrna else None,
            isv_shap_morbid_genes=self.isv_shaps.morbid.shap if self.isv_shaps.morbid else None,
            isv_shap_disease_associated_genes=self.isv_shaps.disease_associated.shap
            if self.isv_shaps.disease_associated
            else None,
            isv_shap_hi_genes=self.isv_shaps.hi_genes.shap if self.isv_shaps.hi_genes else None,
            isv_shap_regions_HI=self.isv_shaps.regions_HI.shap if self.isv_shaps.regions_HI else None,
            isv_shap_regions_TS=self.isv_shaps.regions_TS.shap if self.isv_shaps.regions_TS else None,
            isv_shap_regulatory=self.isv_shaps.regulatory.shap if self.isv_shaps.regulatory else None,
            isv_shap_regulatory_enhancer=self.isv_shaps.regulatory_enhancer.shap
            if self.isv_shaps.regulatory_enhancer
            else None,
            isv_shap_regulatory_silencer=self.isv_shaps.regulatory_silencer.shap
            if self.isv_shaps.regulatory_silencer
            else None,
            isv_shap_regulatory_transcriptional_cis_regulatory_region=self.isv_shaps.regulatory_transcriptional_cis_regulatory_region.shap
            if self.isv_shaps.regulatory_transcriptional_cis_regulatory_region
            else None,
            isv_shap_regulatory_promoter=self.isv_shaps.regulatory_promoter.shap
            if self.isv_shaps.regulatory_promoter
            else None,
            isv_shap_regulatory_DNase_I_hypersensitive_site=self.isv_shaps.regulatory_DNase_I_hypersensitive_site.shap
            if self.isv_shaps.regulatory_DNase_I_hypersensitive_site
            else None,
            isv_shap_regulatory_enhancer_blocking_element=self.isv_shaps.regulatory_enhancer_blocking_element.shap
            if self.isv_shaps.regulatory_enhancer_blocking_element
            else None,
            isv_shap_regulatory_TATA_box=self.isv_shaps.regulatory_TATA_box.shap
            if self.isv_shaps.regulatory_TATA_box
            else None,
            workflow_version=self.workflow_version,
            report_version=self.report_version,
        )
