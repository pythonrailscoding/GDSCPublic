from django.core.validators import ValidationError

import os

def file_limit(value):
	file_size = value.size
	if file_size > 100000000:
		raise ValidationError("Maximum size for Image to be Uploaded is 100MB! Your Video Size exceeds this limit!")

def validate_image_extension(value):
	ext = os.path.splitext(value.name)[1]
	# valid_extensions = ['.png', '.jpeg', '.gif', '.tif', '.tiff', '.eps', '.jpg', '.raw', '.svg']
	invalid_extensions = ['.tif', '.tiff', '.heif', '.heic', '.raw', '.psd', '.ai', '.eps', '.indd', '.pdf', '.xcf', '.jp2']
	if ext.lower() in invalid_extensions:
		raise ValidationError("Unsupported Image File Extension. If you submit again, and it is an edit portal, your existing thumbnail will be submitted.")



