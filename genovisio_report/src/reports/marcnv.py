from dataclasses import dataclass

from genovisio_report.src import input_schemas


@dataclass
class MarcNVReportSection:
    option: str
    reason: str
    score: float

    @classmethod
    def create_from_criterion(cls, criterion: input_schemas.MarcnvCriterion) -> "MarcNVReportSection":
        return cls(option=criterion.option, reason=criterion.reason, score=criterion.score)

    @property
    def format_reason(self) -> str:
        if self.option != "Other":
            return f"<b>{self.option}.</b> {self.reason}"
        else:
            return self.reason


@dataclass
class MarcNVReport:
    Section_1: MarcNVReportSection
    Section_2: MarcNVReportSection
    Section_3: MarcNVReportSection
    Section_4: MarcNVReportSection
    Section_5: MarcNVReportSection

    @classmethod
    def build(cls, marcnv_data: input_schemas.MarcNV) -> "MarcNVReport":
        sections = {
            f"Section_{criterion.section}": MarcNVReportSection.create_from_criterion(criterion)
            for criterion in marcnv_data.criteria
        }
        return cls(**sections)
