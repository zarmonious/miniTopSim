#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Georg Mikula
#e11902119

import sys
import os
import configparser

class MandetoryParamMissingException(Exception):
	""" """
	pass
class ConditionIncorrectException(Exception):
	""" """
	pass
class WrongTypeException(Exception):
	""" """
	pass
class WrongInputException(Exception):
	""" """
	pass

def __parse_file(filename):
	"""This function opens a file with the given filename and creates a dictonary of all parameters in the file. \
	The keys of the dictionary are the parameter names. Sections are completely ignored and have no effect on the returned dict."""
	if os.path.isfile(filename) is False:
		raise FileNotFoundError(filename + ' not found.')
	cp = configparser.ConfigParser()
	cp.read(filename)
	config = {}
	for section in cp.sections():
		for option in cp[section]:
			config[option.upper()] = eval(cp[section][option])
	return config

def __check_conditions(conditions_dict):
	"""Checks all parameter conditions. Raises a CondtionIncorrectException if at least one condition failed."""
	incorrect_conditions = 0
	for key, condition in conditions_dict.items():
		if(not eval(condition)):
			incorrect_conditions = incorrect_conditions + 1
			print("Error: The condition " + str(condition) +  " of parameter " + str(key) + " is not true!")
	if incorrect_conditions != 0:
		raise ConditionIncorrectException(str(incorrect_conditions) + " conditions are false")


def load_parameters(config_file_path, params_db_filename = 'parameters.db'):
	"""Loads all parameters from parameters.db (or argument 2) file.\
	Reads configuration for argument1 file and if the type of the config matches with the parameter it's stored.\
	Also all Help Strings are stored in the module variable HELP_STRINGS and can be accessed with the parameter name as key."""

	params_db_path = os.path.join(os.path.dirname(__file__), params_db_filename)
	params = __parse_file(params_db_path)
	config = __parse_file(config_file_path)
	param_dict = {}
	help_dict = {}
	conditions_dict = {}
	incorrect_params = 0
	for key, (default, condition, description) in params.items():
		try:
			globals()[key] = default
			if(key in config):
				float_as_int = False
				c = config[key]
				type_c = type(c)
				if((type(default) == float) or ((type(default) == type) and (default == float))):
					type_c = float
					float_as_int = True
				type_equal_cond = (type_c == type(default))
				type_is_cond = ((type(default) is type) and (type_c == default))

				if(type_equal_cond or type_is_cond):

					globals()[key] = config[key] if not float_as_int else float(config[key])
				else:
					raise WrongTypeException("Type mismatch!")

			elif (type(default) is type):
				raise MandetoryParamMissingException("Error: Mandatory parameter " + str(key) + " missing!")
			param_dict[key] = globals()[key]
			help_dict[key] = description
			if condition is not None:
				conditions_dict[key] = condition
		except MandetoryParamMissingException as e:
			print("MandetoryParamMissingException")
			print(e)
			incorrect_params = incorrect_params + 1
		except WrongTypeException as e:
			print("WrongTypeException")
			print(e)
			incorrect_params = incorrect_params + 1
	if incorrect_params != 0:
		raise WrongInputException(str(incorrect_params) + " Errors were detected.")

	__check_conditions(conditions_dict)

	globals()["HELP_STRINGS"] = help_dict
	return param_dict