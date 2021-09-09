# Сериализторы должны лежать в своей папке, а то неклево все закидывать в utils


from marshmallow import Schema, fields


class FIOApplicantSerializer(Schema):
    middle = fields.String()
    first = fields.String()
    last = fields.String()


class BirthdateApplicantSerializer(Schema):
    year = fields.Integer()
    month = fields.Integer()
    day = fields.Integer()


class PhotoApplicantSerializer(Schema):
    id = fields.Integer()
    url = fields.String()


class CompanyApplicantSerializer(Schema):
    position = fields.String()
    company = fields.String()


class SubFieldsApplicantSerializer(Schema):
    birthdate = fields.Nested(BirthdateApplicantSerializer)
    name = fields.Nested(FIOApplicantSerializer)
    email = fields.Email()
    phones = fields.List(fields.String())
    position = fields.String()
    experience = fields.List(fields.Nested(CompanyApplicantSerializer))
    salary = fields.String()


class InputApplicantSerializer(Schema):
    name = fields.String()
    id = fields.Integer()
    text = fields.String()
    photo = fields.Nested(PhotoApplicantSerializer)
    fields = fields.Nested(SubFieldsApplicantSerializer)


class SubApplicantStatusesSerializer(Schema):
    id = fields.Integer()
    name = fields.String()


class ApplicantStatusesSerializer(Schema):
    items = fields.List(fields.Nested(SubApplicantStatusesSerializer))


class SubVacancySerializer(Schema):
    id = fields.Integer()
    position = fields.String()


class VacancySerializer(Schema):
    items = fields.List(fields.Nested(SubVacancySerializer))
