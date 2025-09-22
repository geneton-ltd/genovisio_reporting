from dataclasses import dataclass, fields

import plotly.graph_objects as go

from genovisio_report.src import input_schemas


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
        labels = self.label.split(" ", 1)
        if len(labels) == 2:
            return f'<span style="color: black"><b>{labels[0]}</b></span> {labels[1]}'
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
        # return f"<b><i>{self.name}</i></b><br><b>value:</b> {self.value}<br><b>SHAP value:</b> {core.float_format(self.shap)}"
        return f"<b><i>{self.name}</i></b><br><b>count:</b> {self.value}"


@dataclass
class ShapData:
    gencode_genes: ShapDatum | None = None
    disease_associated: ShapDatum | None = None
    hi_genes: ShapDatum | None = None
    lncrna: ShapDatum | None = None
    mirna: ShapDatum | None = None
    morbid: ShapDatum | None = None
    protein_coding: ShapDatum | None = None
    pseudogenes: ShapDatum | None = None
    regions_HI: ShapDatum | None = None
    regions_TS: ShapDatum | None = None
    regulatory: ShapDatum | None = None
    regulatory_DNase_I_hypersensitive_site: ShapDatum | None = None
    regulatory_TATA_box: ShapDatum | None = None
    regulatory_enhancer: ShapDatum | None = None
    regulatory_enhancer_blocking_element: ShapDatum | None = None
    regulatory_promoter: ShapDatum | None = None
    regulatory_silencer: ShapDatum | None = None
    regulatory_transcriptional_cis_regulatory_region: ShapDatum | None = None
    rrna: ShapDatum | None = None
    snrna: ShapDatum | None = None
    regulatory_open_chromatin_region: ShapDatum | None = None
    regulatory_flanking_region: ShapDatum | None = None
    regulatory_CTCF_binding_site: ShapDatum | None = None
    regulatory_TF_binding_site: ShapDatum | None = None
    regulatory_curated: ShapDatum | None = None

    @property
    def as_list_without_nulls(self) -> list[ShapDatum]:
        non_null_values = [value for field in fields(self) if (value := getattr(self, field.name)) is not None]
        sorted_lst = sorted(non_null_values, key=lambda x: x.name, reverse=True)
        return sorted_lst

    @classmethod
    def build_from_isv_result(cls, isv: input_schemas.ISVResult) -> "ShapData":
        if isinstance(isv.isv_shap_values, input_schemas.SHAPsGain):
            return cls(
                gencode_genes=ShapDatum(
                    "Gencode Elements", isv.isv_shap_values.gencode_genes, isv.isv_features.gencode_genes
                ),
                protein_coding=ShapDatum(
                    "Protein Coding Genes", isv.isv_shap_values.protein_coding, isv.isv_features.protein_coding
                ),
                disease_associated=ShapDatum(
                    "Disease associated Genes",
                    isv.isv_shap_values.disease_associated_genes,
                    isv.isv_features.disease_associated_genes,
                ),
                mirna=ShapDatum("Micro RNA", isv.isv_shap_values.mirna, isv.isv_features.mirna),
                morbid=ShapDatum("Morbid Genes", isv.isv_shap_values.morbid_genes, isv.isv_features.morbid_genes),
                pseudogenes=ShapDatum("Pseudogenes", isv.isv_shap_values.pseudogenes, isv.isv_features.pseudogenes),
                regions_TS=ShapDatum(
                    "Triplosensitive Regions", isv.isv_shap_values.regions_TS, isv.isv_features.regions_TS
                ),
                regulatory=ShapDatum(
                    "Regulatory Elements", isv.isv_shap_values.regulatory, isv.isv_features.regulatory
                ),
                regulatory_enhancer=ShapDatum(
                    "Enhancers", isv.isv_shap_values.regulatory_enhancer, isv.isv_features.regulatory_enhancer
                ),
                snrna=ShapDatum("Small nuclear RNA", isv.isv_shap_values.snrna, isv.isv_features.snrna),
                lncrna=ShapDatum("Long non-coding RNA", isv.isv_shap_values.lncrna, isv.isv_features.lncrna),
                rrna=ShapDatum("Ribosomal RNA", isv.isv_shap_values.rrna, isv.isv_features.rrna),
                regulatory_promoter=ShapDatum(
                    "Promoters", isv.isv_shap_values.regulatory_promoter, isv.isv_features.regulatory_promoter
                ),
                regulatory_open_chromatin_region=ShapDatum(
                    "Open Chromatin Regions",
                    isv.isv_shap_values.regulatory_open_chromatin_region,
                    isv.isv_features.regulatory_open_chromatin_region,
                ),
                regulatory_flanking_region=ShapDatum(
                    "Flanking Regions",
                    isv.isv_shap_values.regulatory_flanking_region,
                    isv.isv_features.regulatory_flanking_region,
                ),
                regulatory_CTCF_binding_site=ShapDatum(
                    "CTCF Binding Sites",
                    isv.isv_shap_values.regulatory_CTCF_binding_site,
                    isv.isv_features.regulatory_CTCF_binding_site,
                ),
                regulatory_TF_binding_site=ShapDatum(
                    "Transcription Factor Binding Sites",
                    isv.isv_shap_values.regulatory_TF_binding_site,
                    isv.isv_features.regulatory_TF_binding_site,
                ),
                regulatory_curated=ShapDatum(
                    "Curated Regulatory Elements",
                    isv.isv_shap_values.regulatory_curated,
                    isv.isv_features.regulatory_curated,
                ),
            )
        else:
            return cls(
                gencode_genes=ShapDatum(
                    "Gencode Elements", isv.isv_shap_values.gencode_genes, isv.isv_features.gencode_genes
                ),
                disease_associated=ShapDatum(
                    "Disease associated Genes",
                    isv.isv_shap_values.disease_associated_genes,
                    isv.isv_features.disease_associated_genes,
                ),
                hi_genes=ShapDatum("Haploinsufficient Genes", isv.isv_shap_values.hi_genes, isv.isv_features.hi_genes),
                lncrna=ShapDatum("Long non-coding RNA", isv.isv_shap_values.lncrna, isv.isv_features.lncrna),
                mirna=ShapDatum("Micro RNA", isv.isv_shap_values.mirna, isv.isv_features.mirna),
                rrna=ShapDatum("Ribosomal RNA", isv.isv_shap_values.rrna, isv.isv_features.rrna),
                snrna=ShapDatum("Small nuclear RNA", isv.isv_shap_values.snrna, isv.isv_features.snrna),
                morbid=ShapDatum("Morbid Genes", isv.isv_shap_values.morbid_genes, isv.isv_features.morbid_genes),
                protein_coding=ShapDatum(
                    "Protein Coding Genes", isv.isv_shap_values.protein_coding, isv.isv_features.protein_coding
                ),
                pseudogenes=ShapDatum("Pseudogenes", isv.isv_shap_values.pseudogenes, isv.isv_features.pseudogenes),
                regions_HI=ShapDatum(
                    "Haploinsufficient Regions", isv.isv_shap_values.regions_HI, isv.isv_features.regions_HI
                ),
                regulatory=ShapDatum(
                    "Regulatory Elements", isv.isv_shap_values.regulatory, isv.isv_features.regulatory
                ),
                regulatory_open_chromatin_region=ShapDatum(
                    "Open Chromatin Regions",
                    isv.isv_shap_values.regulatory_open_chromatin_region,
                    isv.isv_features.regulatory_open_chromatin_region,
                ),
                regulatory_enhancer=ShapDatum(
                    "Enhancers", isv.isv_shap_values.regulatory_enhancer, isv.isv_features.regulatory_enhancer
                ),
                regulatory_promoter=ShapDatum(
                    "Promoters", isv.isv_shap_values.regulatory_promoter, isv.isv_features.regulatory_promoter
                ),
                regulatory_flanking_region=ShapDatum(
                    "Flanking Regions",
                    isv.isv_shap_values.regulatory_flanking_region,
                    isv.isv_features.regulatory_flanking_region,
                ),
                regulatory_CTCF_binding_site=ShapDatum(
                    "CTCF Binding Sites",
                    isv.isv_shap_values.regulatory_CTCF_binding_site,
                    isv.isv_features.regulatory_CTCF_binding_site,
                ),
                regulatory_TF_binding_site=ShapDatum(
                    "Transcription Factor Binding Sites",
                    isv.isv_shap_values.regulatory_TF_binding_site,
                    isv.isv_features.regulatory_TF_binding_site,
                ),
                regulatory_curated=ShapDatum(
                    "Curated Regulatory Elements",
                    isv.isv_shap_values.regulatory_curated,
                    isv.isv_features.regulatory_curated,
                ),
            )

    def generate_plot_as_json(self) -> str:
        data = self.as_list_without_nulls
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
            # text=[core.float_format(shap) for shap in shaps],
            textposition="outside",
            textfont=dict(size=9),
            hovertext=hovertexts,
            hoverinfo="text",
        )

        # dynamic range for x axis
        shap_min_value = min(min(shaps) - 0.1, -1)
        shap_max_value = max(max(shaps) + 0.1, 1)

        fig.add_vline(x=0, line_color="black", line_width=1)
        fig.update_xaxes(
            range=[shap_min_value, shap_max_value], showline=False, zeroline=True, ticks="", showticklabels=False
        )
        fig.update_yaxes(tickfont=dict(size=9), tickmode="array", tickvals=labels, ticktext=color_labels)
        fig.update_layout(template="plotly_white", height=450, width=400, margin=dict(l=20, r=20, t=20, b=20))
        return fig.to_json()
