from dataclasses import dataclass, field

import annotation


@dataclass
class GeneReport:
    genes: list[str]
    count: int = field(init=False)

    def __post_init__(self) -> None:
        self.count = len(self.genes)

    @property
    def list(self) -> str:
        result: list[str] = []
        for gene in self.genes:
            result.append(
                f'<a href="https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}" target=_blank>{gene}</a>'
            )
            # TODO fix html being in python script, should be processed in template
        return ", ".join(result)


@dataclass
class GenesReport:
    protein_coding: int
    morbid: GeneReport
    disease: GeneReport
    hi: GeneReport
    ts: GeneReport
    omim_URL_morbid_genes: list[str]
    omim_URL_disease_asscoiated_genes: list[str]
    omim_URL_hi_genes: list[str]
    omim_URL_ts_genes: list[str]

    @classmethod
    def build(cls, annot: annotation.Annotation) -> "GenesReport":
        sv_counts = annot.get_annotated_genes()
        hi_genes = annot.get_haploinsufficient_gene_names(annotation.enums.Overlap.ANY, [3])
        ts_genes = annot.get_triplosensitivity_gene_names(annotation.enums.Overlap.ANY, [3])
        return cls(
            protein_coding=annot.count_gene_types()["protein_coding"],
            morbid=GeneReport(sv_counts["morbid_genes"]),
            disease=GeneReport(sv_counts["associated_with_disease"]),
            hi=GeneReport(hi_genes),
            ts=GeneReport(ts_genes),
            omim_URL_morbid_genes=sv_counts["morbid_genes_urls"],
            omim_URL_disease_asscoiated_genes=sv_counts["associated_with_disease_urls"],
            omim_URL_hi_genes=annot.get_hi_or_ts_genes_url(hi_genes),
            omim_URL_ts_genes=annot.get_hi_or_ts_genes_url(ts_genes),
        )
