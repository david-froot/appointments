from django.core.exceptions import ValidationError


def validate_code(value):
	if value != 'mysecretcode':
		raise ValidationError(
            _('%(value)s is incorrect code'),
            params={'value': value},
        )

def validate_rating(value):
	if value > 1 or value > 5:
		raise ValidationError(
            _('Rating must be between 1 and 5'),
            params={'value': value},
        )


	validators=[validate_even]