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
class ShapData:
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


def generate_plot_as_json(isv: input_schemas.ISVResult) -> str:
    data = [
        ShapData(
            "Disease associated Genes",
            isv.isv_shap_values.disease_associated_genes,
            isv.isv_features.disease_associated_genes,
        ),
        ShapData("Overlapped Gencode Elements", isv.isv_shap_values.gencode_genes, isv.isv_features.gencode_genes),
        ShapData("Haploinsufficient Genes", isv.isv_shap_values.hi_genes, isv.isv_features.hi_genes),
        ShapData("Long non-coding RNA", isv.isv_shap_values.lncrna, isv.isv_features.lncrna),
        ShapData("Micro RNA", isv.isv_shap_values.mirna, isv.isv_features.mirna),
        ShapData("Morbid Genes", isv.isv_shap_values.morbid_genes, isv.isv_features.morbid_genes),
        ShapData("Protein Coding Genes", isv.isv_shap_values.protein_coding, isv.isv_features.protein_coding),
        ShapData("Pseudogenes", isv.isv_shap_values.pseudogenes, isv.isv_features.pseudogenes),
        ShapData("Haploinsufficient Regions", isv.isv_shap_values.regions_HI, isv.isv_features.regions_HI),
        ShapData("Triplosensitive Regions", isv.isv_shap_values.regions_TS, isv.isv_features.regions_TS),
        ShapData("Regulatory Elements", isv.isv_shap_values.regulatory, isv.isv_features.regulatory),
        ShapData(
            "DNase I hypersensitive sites",
            isv.isv_shap_values.regulatory_DNase_I_hypersensitive_site,
            isv.isv_features.regulatory_DNase_I_hypersensitive_site,
        ),
        ShapData("TATA box", isv.isv_shap_values.regulatory_TATA_box, isv.isv_features.regulatory_TATA_box),
        ShapData("Enhancers", isv.isv_shap_values.regulatory_enhancer, isv.isv_features.regulatory_enhancer),
        ShapData(
            "Enhancer-blocking Elements",
            isv.isv_shap_values.regulatory_enhancer_blocking_element,
            isv.isv_features.regulatory_enhancer_blocking_element,
        ),
        ShapData("Promoters", isv.isv_shap_values.regulatory_promoter, isv.isv_features.regulatory_promoter),
        ShapData("Silencers", isv.isv_shap_values.regulatory_silencer, isv.isv_features.regulatory_silencer),
        ShapData(
            "Transcriptional cis-regulatory Regions",
            isv.isv_shap_values.regulatory_transcriptional_cis_regulatory_region,
            isv.isv_features.regulatory_transcriptional_cis_regulatory_region,
        ),
        ShapData("Ribosomal RNA", isv.isv_shap_values.rrna, isv.isv_features.rrna),
        ShapData("Small nuclear RNA", isv.isv_shap_values.snrna, isv.isv_features.snrna),
    ]

    # sort data by name in reverse order
    data = sorted(data, key=lambda x: x.name, reverse=True)

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
