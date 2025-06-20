from genovisio_report.src import report
import annotation
from genovisio_report.src import reports
from genovisio_report.main import genovisio_report


def test_expected_csv():
    flat = report.FlatReportData.load_from_csv("tests/expected_output_loss.csv")

    assert flat.report_id == ""
    assert flat.genes_morbid_list == ["TDRD7"]

def test_get_annotations():
    annot = annotation.Annotation.load_from_json("tests/annotation_test_loss.json.gz")
    print('Hello ')
    genes = annot.get_annotated_genes()
    print(genes)
    print(genes["morbid_genes_urls"])

    genes_report = reports.GenesReport.build(annot)
    print(genes_report)


def test_genovisio_report():
    genovisio_report(annotation_input='tests/annotation_test_gain.json.gz',
                     isv_input='tests/isv_gain.json',
                     marcnv_input='tests/marcnv.json',
                     hybrid_input='tests/hybrid.json',
                     output_html='tests/test_output_gain.html',
                     output_csv='tests/test_output_gain.csv',
                     report_id=None, version='0.3.0',
                     workflow_version='0.1.2')
    
    genovisio_report(annotation_input='tests/annotation_test_loss.json.gz',
                     isv_input='tests/isv_loss.json',
                     marcnv_input='tests/marcnv.json',
                     hybrid_input='tests/hybrid.json',
                     output_html='tests/test_output_loss.html',
                     output_csv='tests/test_output_loss.csv',
                     report_id=None, version='0.3.0',
                     workflow_version='0.1.2')
