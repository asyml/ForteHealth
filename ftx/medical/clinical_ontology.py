# ***automatically_generated***
# ***source json:../forte-medical/forte_medical/ontology_specs/clinical_ontology.json***
# flake8: noqa
# mypy: ignore-errors
# pylint: skip-file
"""
Automatically generated ontology clinical_ontology. Do not change manually.
"""

from dataclasses import dataclass
from forte.data.data_pack import DataPack
from forte.data.ontology.core import FList
from forte.data.ontology.top import Annotation
from forte.data.ontology.top import Generics
from ft.onto.base_ontology import EntityMention
from typing import Dict
from typing import List
from typing import Optional

__all__ = [
    "ClinicalEntityMention",
    "Description",
    "Body",
    "FrequencyAnnotation",
    "DurationAnnotation",
    "RouteAnnotation",
    "SuffixStrengthAnnotation",
    "FractionStrengthAnnotation",
    "RangeStrengthAnnotation",
    "DecimalStrengthAnnotation",
    "DrugChangeStatusAnnotation",
    "DosagesAnnotation",
    "StrengthAnnotation",
    "StrengthUnitAnnotation",
    "FrequencyUnitAnnotation",
    "FormAnnotation",
    "SubSectionAnnotation",
    "DrugMentionAnnotation",
    "ChunkAnnotation",
    "DrugLookupWindowAnnotation",
    "NegationContext",
    "UMLSConceptLink",
    "MedicalEntityMention",
    "MedicalArticle",
]


@dataclass
class ClinicalEntityMention(EntityMention):
    """
    A span based annotation `ClinicalEntityMention`, normally used to represent an Entity Mention in a piece of clinical text.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class Description(Annotation):
    """
    A span based annotation `Description`, used to represent the description in a piece of clinical note.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class Body(Annotation):
    """
    A span based annotation `Body`, used to represent the actual content in a piece of clinical note.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class FrequencyAnnotation(Annotation):
    """
    The frequency determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class DurationAnnotation(Annotation):
    """
    The duration determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class RouteAnnotation(Annotation):
    """
    The route determination for the Drug NER profile.
    Attributes:
        in_take_method (Optional[str]):
    """

    in_take_method: Optional[str]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.in_take_method: Optional[str] = None


@dataclass
class SuffixStrengthAnnotation(Annotation):
    """
    The suffix portion of dosage strength determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class FractionStrengthAnnotation(Annotation):
    """
    The fraction portion of dosages strength determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class RangeStrengthAnnotation(Annotation):
    """
    The range portion of dosages stength determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class DecimalStrengthAnnotation(Annotation):
    """
    The decimal portion of dosages stength determination for the Drug NER profile
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class DrugChangeStatusAnnotation(Annotation):
    """
    The change status of dosages determination for the Drug NER profile.
    Attributes:
        change_status (Optional[str]):	Indicates the drug change status of 'stop', 'start', 'increase', 'decrease', or 'noChange'.
    """

    change_status: Optional[str]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.change_status: Optional[str] = None


@dataclass
class DosagesAnnotation(Annotation):
    """
    The dosage determination for the Drug NER profile.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class StrengthAnnotation(Annotation):
    """
    Holds the value representing the unit of the drug dosage.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class StrengthUnitAnnotation(Annotation):

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class FrequencyUnitAnnotation(Annotation):
    """
    The value represents the unit portion of the drug frequency.
    Attributes:
        period (Optional[float]):	The periodic unit used, e.g day, month, hour, etc.
    """

    period: Optional[float]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.period: Optional[float] = None


@dataclass
class FormAnnotation(Annotation):
    """
    The value represents the form portion of the drug mention.
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class SubSectionAnnotation(Annotation):
    """
    Attributes:
        sub_ssection_body_begin (Optional[int]):	Sub-section body begin offset.
        sub_section_body_end (Optional[int]):	Sub-section body end offset.
        status (Optional[int]):	Status of 'possible', 'history of', or 'family history of'.
        sub_section_header_begin (Optional[int]):	Begin offset of subSection header
        sub_section_header_end (Optional[int]):	Ending offset of subsection header
        parent_section_id (Optional[str]):	The section in which the subsection was found.
    """

    sub_ssection_body_begin: Optional[int]
    sub_section_body_end: Optional[int]
    status: Optional[int]
    sub_section_header_begin: Optional[int]
    sub_section_header_end: Optional[int]
    parent_section_id: Optional[str]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.sub_ssection_body_begin: Optional[int] = None
        self.sub_section_body_end: Optional[int] = None
        self.status: Optional[int] = None
        self.sub_section_header_begin: Optional[int] = None
        self.sub_section_header_end: Optional[int] = None
        self.parent_section_id: Optional[str] = None


@dataclass
class DrugMentionAnnotation(Annotation):
    """
    Attributes:
        status (Optional[int]):
        confidence (Optional[float]):	The confidence of the annotation.
        frequency (Optional[str]):	Frequency refers to how often the patient needs to take the drug. Frequency is divided into frequency number and frequency unit. E.g. twice daily
        frequency_begin (Optional[int]):
        frequency_end (Optional[int]):
        duration (Optional[str]):	Duration refers to for how long the patient is expected to take the drug. E.g. 'for 2 weeks' Strongly encouraged to use bold text
        duration_begin (Optional[int]):
        duration_end (Optional[int]):
        route (Optional[str]):	Medication route refers to the way that a drug is introduced into the body. E.g oral Strongly encouraged to use bold text
        route_begin (Optional[int]):
        route_end (Optional[int]):
        drug_change_status (Optional[str]):	Status refers to the whether the medication is currently being taken or not.
        dosage (Optional[str]):	Dosage refers to how many of each drug the patient is taking. E.g. 5 mg
        dosage_begin (Optional[int]):
        dosage_end (Optional[int]):
        strength (Optional[str]):
        strength_begin (Optional[int]):
        strength_end (Optional[int]):
        strength_unit (Optional[str]):
        su_begin (Optional[int]):
        su_end (Optional[int]):
        form (Optional[str]):	Form refers to the physical appearance of the drug. E.g. cream
        form_begin (Optional[int]):
        form_end (Optional[int]):
        frequency_unit (Optional[str]):
        fu_begin (Optional[int]):
        fu_end (Optional[int]):
        start_date (Optional[str]):
        reason (Dict[str, int]):
        change_status_begin (Optional[int]):
        change_status_end (Optional[int]):
    """

    status: Optional[int]
    confidence: Optional[float]
    frequency: Optional[str]
    frequency_begin: Optional[int]
    frequency_end: Optional[int]
    duration: Optional[str]
    duration_begin: Optional[int]
    duration_end: Optional[int]
    route: Optional[str]
    route_begin: Optional[int]
    route_end: Optional[int]
    drug_change_status: Optional[str]
    dosage: Optional[str]
    dosage_begin: Optional[int]
    dosage_end: Optional[int]
    strength: Optional[str]
    strength_begin: Optional[int]
    strength_end: Optional[int]
    strength_unit: Optional[str]
    su_begin: Optional[int]
    su_end: Optional[int]
    form: Optional[str]
    form_begin: Optional[int]
    form_end: Optional[int]
    frequency_unit: Optional[str]
    fu_begin: Optional[int]
    fu_end: Optional[int]
    start_date: Optional[str]
    reason: Dict[str, int]
    change_status_begin: Optional[int]
    change_status_end: Optional[int]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.status: Optional[int] = None
        self.confidence: Optional[float] = None
        self.frequency: Optional[str] = None
        self.frequency_begin: Optional[int] = None
        self.frequency_end: Optional[int] = None
        self.duration: Optional[str] = None
        self.duration_begin: Optional[int] = None
        self.duration_end: Optional[int] = None
        self.route: Optional[str] = None
        self.route_begin: Optional[int] = None
        self.route_end: Optional[int] = None
        self.drug_change_status: Optional[str] = None
        self.dosage: Optional[str] = None
        self.dosage_begin: Optional[int] = None
        self.dosage_end: Optional[int] = None
        self.strength: Optional[str] = None
        self.strength_begin: Optional[int] = None
        self.strength_end: Optional[int] = None
        self.strength_unit: Optional[str] = None
        self.su_begin: Optional[int] = None
        self.su_end: Optional[int] = None
        self.form: Optional[str] = None
        self.form_begin: Optional[int] = None
        self.form_end: Optional[int] = None
        self.frequency_unit: Optional[str] = None
        self.fu_begin: Optional[int] = None
        self.fu_end: Optional[int] = None
        self.start_date: Optional[str] = None
        self.reason: Dict[str, int] = dict()
        self.change_status_begin: Optional[int] = None
        self.change_status_end: Optional[int] = None


@dataclass
class ChunkAnnotation(Annotation):
    """
    The value represents the unit portion of the drug frequency.
    Attributes:
        sentence_id (Optional[str]):
    """

    sentence_id: Optional[str]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.sentence_id: Optional[str] = None


@dataclass
class DrugLookupWindowAnnotation(Annotation):
    """
    Similar to LookupWindowAnnotation however, these annotations are restricted to the segments/sections specified in the parameter - sectionOverrideSet - in DrugCNP2LookupWindow
    """

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)


@dataclass
class NegationContext(Annotation):
    """
    A span based annotation `NegationContext`, used to represent the negation context of a named entity.
    Attributes:
        polarity (Optional[bool]):
    """

    polarity: Optional[bool]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.polarity: Optional[bool] = None


@dataclass
class UMLSConceptLink(Generics):
    """
    A umls concept entity, used to represent basic information of a umls concept
    Attributes:
        cui (Optional[str]):
        name (Optional[str]):
        definition (Optional[str]):
        tuis (List[str]):
        aliases (List[str]):
        score (Optional[str]):
    """

    cui: Optional[str]
    name: Optional[str]
    definition: Optional[str]
    tuis: List[str]
    aliases: List[str]
    score: Optional[str]

    def __init__(self, pack: DataPack):
        super().__init__(pack)
        self.cui: Optional[str] = None
        self.name: Optional[str] = None
        self.definition: Optional[str] = None
        self.tuis: List[str] = []
        self.aliases: List[str] = []
        self.score: Optional[str] = None


@dataclass
class MedicalEntityMention(EntityMention):
    """
    A span based annotation class MedicalEntityMention, used to represent an Entity Mention in medical domain
    Attributes:
        umls_link (Optional[str]):
        umls_entities (FList[UMLSConceptLink]):
    """

    umls_link: Optional[str]
    umls_entities: FList[UMLSConceptLink]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.umls_link: Optional[str] = None
        self.umls_entities: FList[UMLSConceptLink] = FList(self)


@dataclass
class MedicalArticle(Annotation):
    """
    An annotation which represents the whole medical text chunk/document
    Attributes:
        icd_version (Optional[int]):	The version of ICD-Coding being used.
        icd_code (Optional[str]):	The ICD code assigned to current medical article.
    """

    icd_version: Optional[int]
    icd_code: Optional[str]

    def __init__(self, pack: DataPack, begin: int, end: int):
        super().__init__(pack, begin, end)
        self.icd_version: Optional[int] = None
        self.icd_code: Optional[str] = None
