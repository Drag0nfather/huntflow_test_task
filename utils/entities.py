from dataclasses import dataclass


@dataclass
class FIOEntity:
    first: str
    last: str
    middle: str


@dataclass
class BirthdateApplicantEntity:
    year: int
    month: int
    day: int


@dataclass
class CompanyApplicantEntity:
    position: int


@dataclass
class SubFieldsApplicantEntity:
    birthdate: BirthdateApplicantEntity
    name: FIOEntity
    email: str
    phones: str
    position: str
    experience: CompanyApplicantEntity
    salary: str


@dataclass
class PhotoApplicantEntity:
    id: int
    url: str


@dataclass
class ApplicantEntity:
    fields: SubFieldsApplicantEntity
    name: str
    id: int
    text: str
    photo: PhotoApplicantEntity


@dataclass
class SubApplicantEntity:
    id: int
    name: str


@dataclass
class ApplicantStatusesEntity:
    items: SubApplicantEntity


@dataclass
class SubVacancyEntity:
    id: int
    position: str


@dataclass
class VacancyEntity:
    items: SubVacancyEntity
