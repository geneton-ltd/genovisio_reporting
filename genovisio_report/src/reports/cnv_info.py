from dataclasses import dataclass

import annotation


@dataclass
class CNVInfo:
    chr: str
    start: int
    end: int
    cnv_type: str
    cyto_position: str

    @classmethod
    def build(cls, cnv_data: annotation.CNVRegionAnnotation) -> "CNVInfo":
        return cls(
            chr=cnv_data.chr,
            start=cnv_data.start,
            end=cnv_data.end,
            cnv_type=cnv_data.cnv_type,
            cyto_position=cnv_data.cytogenetic_position,
        )

    @property
    def copy_number(self) -> int:
        return 1 if self.type == "LOSS" else 3

    @property
    def type(self) -> str:
        return self.cnv_type.upper()

    @property
    def pos(self) -> str:
        return f"{self.cyto_position}({self.chr}:{self.start}-{self.end})x{self.copy_number}"
