from django.core.validators import ValidationError

import os

def file_limit(value):
	file_size = value.size
	if file_size > 100000000:
		raise ValidationError("Maximum size for Video to be Uploaded is 100MB! Your Video Size exceeds this limit!")

def validate_image_extension(value):
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.png', '.jpeg', '.jgp']
	if not ext.lower() in valid_extensions:
		raise ValidationError("Unsupported Image File Extension.")



