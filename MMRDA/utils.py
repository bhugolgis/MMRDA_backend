import re

def deep_flatten(lst):

    flat = []

    while lst:
        val = lst.pop()
        if isinstance(val,list):
            lst.extend(val)
        else:
            flat.append(val)

    return flat


def error_simplifier(error_dict):
    error_key = error = ""
    value = []
    for key,val in error_dict.items():
        error_key = key
        error = val
        break

    if isinstance(error,str):
        if "field" in error:
            return error_key + ", " + error
        return error
    else:
        value = deep_flatten(error)
        if "field" in value:
            return error_key + ", " + value[0]
        return value[0]

class Validator(object):

	def __init__(self):
		self.text = None

	def validate(self, regex_pattern) -> bool:

		if re.fullmatch(regex_pattern, self.text):
			return True
		else:
			return False

	def email_validator(self, text:str) -> bool:

		self.text = text
		_valid_email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[a-zA-Z0-9]+@[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+')
		return self.validate(_valid_email_regex)

	def username_validator(self, text:str) -> bool:

		self.text = text
		_valid_username_regex = re.compile(r'^(?=.{4,20}$)[a-zA-Z0-9]+([_@-]?[a-zA-Z0-9])*$')
		return self.validate(_valid_username_regex)

	def password_validator(self, text:str) -> bool:

		self.text = text
		_valid_password_regex = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,120}$')
		return self.validate(_valid_password_regex)

	def phone_number_validator(self, text:str) -> bool:

		self.text = text
		_valid_phone_regex = re.compile(r'\d{10}')
		return self.validate(_valid_phone_regex)

__validator = None

def get_validator():
	global __validator
	if __validator is None:
		__validator = Validator()
	return __validator

def reset_validator():
	global __validator
	__validator = Validator()
	return __validator