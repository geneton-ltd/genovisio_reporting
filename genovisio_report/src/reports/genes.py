from dataclasses import dataclass, field


import annotation

@dataclass
class GeneReport:
    genes: list[str]
    count: int = field(init=False)

    def __post_init__(self):
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

    @classmethod
    def build(cls, annot: annotation.Annotation) -> "GenesReport":
        sv_counts = annot.get_annotated_genes( )
        return cls(
            protein_coding=annot.count_gene_types()["protein_coding"],
            morbid=GeneReport(sv_counts["morbid_genes"]),
            disease=GeneReport(sv_counts["associated_with_disease"]),
            hi=GeneReport(annot.get_haploinsufficient_gene_names(annotation.enums.Overlap.ANY, [3])),
            ts=GeneReport(annot.get_triplosensitivity_gene_names(annotation.enums.Overlap.ANY, [3])),
        )
