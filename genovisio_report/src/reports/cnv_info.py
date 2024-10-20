from dataclasses import dataclass

import annotation

@dataclass
class CNVInfo:
    type: str
    pos: str

    @classmethod
    def build(cls, cnv_data: annotation.CNVRegionAnnotation) -> "CNVInfo":
        copy_number = 1 if cnv_data.cnv_type == annotation.enums.CNVType.LOSS else 3
        return cls(
            type=cnv_data.cnv_type.upper(),
            pos=f"{cnv_data.cytogenetic_position}({cnv_data.chr}:{cnv_data.start}-{cnv_data.end})x{copy_number}",
        )
