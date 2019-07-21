"""Schemas."""
from marshmallow import Schema, fields, ValidationError, validates


class JobSchema(Schema):
    """Schema for job dict."""
    task_id = fields.Integer(required=True)
    form_id = fields.Integer(required=True)
    groups = fields.List(fields.Integer(), required=True)
    export_format = fields.String(required=True)
    email = fields.Email(required=True)
    from_date = fields.Date()
    to_date = fields.Date()


    @validates('export_format')
    # pylint: disable=no-self-use
    def validate_format(self, export_format):
        """
        Validate 'export_format'.
        :param : str: Input format file.
        :return:
        """
        formats = ['csv', 'pdf', 'xls']
        if export_format not in formats:
            raise ValidationError("Incorrect format!")

