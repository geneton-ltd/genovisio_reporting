import argparse
import csv
import importlib.metadata
import os
import sys
from dataclasses import asdict

import annotation
import jinja2

from genovisio_report.src import core, input_schemas, report, reports


def build_data(
    annot_path: str,
    marcnv_path: str,
    isv_path: str,
    hybrid_path: str,
    report_id: str | None,
    version: str,
    workflow_version: str | None,
) -> report.ReportData:
    marcnv_data = input_schemas.MarcNV.construct_from_json_file(marcnv_path)
    hybrid_data = input_schemas.HybridData.construct_from_json_file(hybrid_path)
    annot = annotation.Annotation.load_from_json(annot_path)
    isv_data = input_schemas.ISVResult.construct_from_json_file(isv_path)

    marcnv_report = reports.MarcNVReport.build(marcnv_data)
    score_report = reports.ScoreReport.build(marcnv_data, isv_data, hybrid_data)
    genes_report = reports.GenesReport.build(annot)
    cnv_info = reports.CNVInfo.build(annot.cnv)
    shaps = reports.ShapData.build_from_isv_result(isv_data)

    return report.ReportData(
        report_id=report_id,
        cnv_info=cnv_info,
        marcnv=marcnv_report,
        scores=score_report,
        genes=genes_report,
        classification_marcnv=marcnv_data.severity,
        classification_isv=isv_data.classification,
        classification_hybrid=hybrid_data.classification,
        isv_shaps=shaps,
        workflow_version=workflow_version,
        report_version=version,
    )


def render_template_html(data: report.ReportData) -> str:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(core.TEMPLATES_DIR))
    template = env.get_template(core.TEMPLATE_FILENAME)

    with open(core.CSS_FILE, "r") as f:
        css = f.read()

    content = template.render(
        css=css,
        id=data.report_id,
        cnv_info=data.cnv_info,
        scores=data.scores,
        acmg=data.marcnv,
        isv_shap=data.isv_shaps.generate_plot_as_json(),
        genes=data.genes,
        marcnv_plot=reports.create_prediction_plot(data.classification_marcnv),
        isv_plot=reports.create_prediction_plot(data.classification_isv),
        hybrid_plot=reports.create_prediction_plot(data.classification_isv),
        float_format_string=core.FLOAT_FORMAT_STRING,
        version_string=data.version_string,
    )

    return content


def genovisio_report(
    annotation_input: str,
    isv_input: str,
    marcnv_input: str,
    hybrid_input: str,
    output_html: str,
    output_csv: str | None,
    report_id: str | None,
    version: str,
    workflow_version: str | None,
) -> None:
    data = build_data(
        annot_path=annotation_input,
        marcnv_path=marcnv_input,
        isv_path=isv_input,
        hybrid_path=hybrid_input,
        report_id=report_id,
        version=version,
        workflow_version=workflow_version,
    )

    content = render_template_html(data)

    output_path_html = os.path.abspath(output_html)
    if not os.path.exists(os.path.dirname(output_path_html)):
        os.makedirs(os.path.dirname(output_path_html))
    with open(output_path_html, "w") as f:
        f.write(content)
    print(f"Report generated successfully at {output_path_html}", file=sys.stderr)

    if not output_csv:
        return

    output_path_csv = os.path.abspath(output_csv)
    if not os.path.exists(os.path.dirname(output_path_csv)):
        os.makedirs(os.path.dirname(output_path_csv))
    with open(output_path_csv, "w", newline="") as f:
        flat_dict = asdict(data.flatten)
        fieldnames = flat_dict.keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerow(flat_dict)

    print(f"Report data stored at {output_path_csv}", file=sys.stderr)


def main() -> None:
    try:
        version = importlib.metadata.version("genovisio_report")
    except importlib.metadata.PackageNotFoundError:
        version = "dev-0.0.0"
        print(f"Not installed as package. Using placeholder {version=}", file=sys.stderr)

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="Report ID")
    parser.add_argument("--annot", type=str, help="Path to the annotation file", required=True)
    parser.add_argument("--isv", type=str, help="Path to the ISV results", required=True)
    parser.add_argument("--marcnv", type=str, help="Path to the MarCNV results", required=True)
    parser.add_argument("--hybrid", type=str, help="Path to the hybrid results", required=True)
    parser.add_argument("--out_html", type=str, help="Path to the output HTML", required=True)
    parser.add_argument("--out_csv", type=str, help="Path to the output CSV", required=False, default=None)
    parser.add_argument("--workflow_version", type=str, help="Workflow version", default=None)
    parser.add_argument("--version", action="version", version=version)
    args = parser.parse_args()

    genovisio_report(
        annotation_input=args.annot,
        isv_input=args.isv,
        marcnv_input=args.marcnv,
        output_html=args.out_html,
        output_csv=args.out_csv,
        hybrid_input=args.hybrid,
        report_id=args.id,
        version=version,
        workflow_version=args.workflow_version,
    )


if __name__ == "__main__":
    main()
