from genovisio_report.src import report


def test_expected_csv():
    flat = report.FlatReportData.load_from_csv("tests/expected_output_loss.csv")

    assert flat.report_id == ""
    assert flat.genes_morbid_list == ["TDRD7"]
