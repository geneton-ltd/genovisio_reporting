import re
from dataclasses import dataclass

import plotly.graph_objects as go

from genovisio_report.src import core, input_schemas


def _split_string(s: str) -> str:
    words = s.split("_")
    result: list[str] = []
    current = words[0]
    for word in words[1:]:
        if len(current) + len(word) < 35:
            current += f"_{word}"
        else:
            result.append(current)
            current = word
    if current not in result:
        result.append(current)

    return "<br>".join(result)


@dataclass
class ShapDatum:
    name: str
    shap: float
    value: int

    @property
    def label(self) -> str:
        return f"[{self.value}] {self.name}"

    @property
    def color_label(self) -> str | None:
        m = re.search(r"(\[.+\] )(.+)", _split_string(self.label))
        if m:
            return f'<span style="color: gray"><b>{m.group(1)}</b></span>{m.group(2)}'
        return None

    @property
    def color(self) -> str:
        if self.shap > 0:
            return "rgb(225, 29, 29)"
        elif self.shap < 0:
            return "rgb(0, 128, 0)"
        else:
            return "gray"

    @property
    def hovertext(self) -> str:
        return f"<b><i>{self.name}</i></b><br><b>value:</b> {self.value}<br><b>SHAP value:</b> {core.float_format(self.shap)}"


@dataclass
class ShapData:
    gencode_genes: ShapDatum
    disease_associated: ShapDatum
    hi_genes: ShapDatum
    lncrna: ShapDatum
    mirna: ShapDatum
    morbid: ShapDatum
    protein_coding: ShapDatum
    pseudogenes: ShapDatum
    regions_HI: ShapDatum
    regions_TS: ShapDatum
    regulatory: ShapDatum
    regulatory_DNase_I_hypersensitive_site: ShapDatum
    regulatory_TATA_box: ShapDatum
    regulatory_enhancer: ShapDatum
    regulatory_enhancer_blocking_element: ShapDatum
    regulatory_promoter: ShapDatum
    regulatory_silencer: ShapDatum
    regulatory_transcriptional_cis_regulatory_region: ShapDatum
    rrna: ShapDatum
    snrna: ShapDatum

    @property
    def as_list(self) -> list[ShapDatum]:
        lst = [
            self.disease_associated,
            self.gencode_genes,
            self.hi_genes,
            self.lncrna,
            self.mirna,
            self.morbid,
            self.protein_coding,
            self.pseudogenes,
            self.regions_HI,
            self.regions_TS,
            self.regulatory,
            self.regulatory_DNase_I_hypersensitive_site,
            self.regulatory_TATA_box,
            self.regulatory_enhancer,
            self.regulatory_enhancer_blocking_element,
            self.regulatory_promoter,
            self.regulatory_silencer,
            self.regulatory_transcriptional_cis_regulatory_region,
            self.rrna,
            self.snrna,
        ]
        sorted_lst = sorted(lst, key=lambda x: x.name, reverse=True)
        return sorted_lst

    @classmethod
    def build_from_isv_result(cls, isv: input_schemas.ISVResult) -> "ShapData":
        return cls(
            gencode_genes=ShapDatum(
                "Overlapped Gencode Elements", isv.isv_shap_values.gencode_genes, isv.isv_features.gencode_genes
            ),
            disease_associated=ShapDatum(
                "Disease associated Genes",
                isv.isv_shap_values.disease_associated_genes,
                isv.isv_features.disease_associated_genes,
            ),
            hi_genes=ShapDatum("Haploinsufficient Genes", isv.isv_shap_values.hi_genes, isv.isv_features.hi_genes),
            lncrna=ShapDatum("Long non-coding RNA", isv.isv_shap_values.lncrna, isv.isv_features.lncrna),
            mirna=ShapDatum("Micro RNA", isv.isv_shap_values.mirna, isv.isv_features.mirna),
            morbid=ShapDatum("Morbid Genes", isv.isv_shap_values.morbid_genes, isv.isv_features.morbid_genes),
            protein_coding=ShapDatum(
                "Protein Coding Genes", isv.isv_shap_values.protein_coding, isv.isv_features.protein_coding
            ),
            pseudogenes=ShapDatum("Pseudogenes", isv.isv_shap_values.pseudogenes, isv.isv_features.pseudogenes),
            regions_HI=ShapDatum(
                "Haploinsufficient Regions", isv.isv_shap_values.regions_HI, isv.isv_features.regions_HI
            ),
            regions_TS=ShapDatum(
                "Triplosensitive Regions", isv.isv_shap_values.regions_TS, isv.isv_features.regions_TS
            ),
            regulatory=ShapDatum("Regulatory Elements", isv.isv_shap_values.regulatory, isv.isv_features.regulatory),
            regulatory_DNase_I_hypersensitive_site=ShapDatum(
                "DNase I hypersensitive sites",
                isv.isv_shap_values.regulatory_DNase_I_hypersensitive_site,
                isv.isv_features.regulatory_DNase_I_hypersensitive_site,
            ),
            regulatory_TATA_box=ShapDatum(
                "TATA box", isv.isv_shap_values.regulatory_TATA_box, isv.isv_features.regulatory_TATA_box
            ),
            regulatory_enhancer=ShapDatum(
                "Enhancers", isv.isv_shap_values.regulatory_enhancer, isv.isv_features.regulatory_enhancer
            ),
            regulatory_enhancer_blocking_element=ShapDatum(
                "Enhancer-blocking Elements",
                isv.isv_shap_values.regulatory_enhancer_blocking_element,
                isv.isv_features.regulatory_enhancer_blocking_element,
            ),
            regulatory_promoter=ShapDatum(
                "Promoters", isv.isv_shap_values.regulatory_promoter, isv.isv_features.regulatory_promoter
            ),
            regulatory_silencer=ShapDatum(
                "Silencers", isv.isv_shap_values.regulatory_silencer, isv.isv_features.regulatory_silencer
            ),
            regulatory_transcriptional_cis_regulatory_region=ShapDatum(
                "Transcriptional cis-regulatory Regions",
                isv.isv_shap_values.regulatory_transcriptional_cis_regulatory_region,
                isv.isv_features.regulatory_transcriptional_cis_regulatory_region,
            ),
            rrna=ShapDatum("Ribosomal RNA", isv.isv_shap_values.rrna, isv.isv_features.rrna),
            snrna=ShapDatum("Small nuclear RNA", isv.isv_shap_values.snrna, isv.isv_features.snrna),
        )

    def generate_plot_as_json(self) -> str:
        data = self.as_list
        # Extract the data into separate lists
        labels = [dp.label for dp in data]
        colors = [dp.color for dp in data]
        hovertexts = [dp.hovertext for dp in data]
        shaps = [dp.shap for dp in data]
        color_labels = [dp.color_label for dp in data]

        fig = go.Figure()
        fig.add_bar(
            x=shaps,
            y=labels,
            orientation="h",
            marker=dict(color=colors),
            text=[core.float_format(shap) for shap in shaps],
            textposition="outside",
            textfont=dict(size=9),
            hovertext=hovertexts,
            hoverinfo="text",
        )

        fig.add_vline(x=0, line_color="black", line_width=1)
        fig.update_xaxes(tickfont=dict(size=9), range=[-1, 1])
        fig.update_yaxes(tickfont=dict(size=9), tickmode="array", tickvals=labels, ticktext=color_labels)
        fig.update_layout(template="plotly_white", height=450, width=400, margin=dict(l=20, r=20, t=20, b=20))
        return fig.to_json()
