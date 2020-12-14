#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Georg Mikula
#e11902119

import sys
import os
import configparser


def _parse_file(filename):
	"""This function opens a file with the given filename and creates a 
	dictonary of all parameters in the file. 
	The keys of the dictionary are the parameter names. Sections are 
	completely ignored and have no effect on the returned dict."""
	if not os.path.isfile(filename):
		raise FileNotFoundError(filename + ' not found.')
	cp = configparser.ConfigParser()
	cp.read(filename)
	config = {}
	for section in cp.sections():
		for option in cp[section]:
			config[option.upper()] = eval(cp[section][option])
	return config

def _check_conditions(conditions_dict):
	"""Checks all parameter conditions. Raises a CondtionIncorrectException 
	if at least one condition failed."""
	incorrect_conditions = 0
	for key, condition in conditions_dict.items():
		if(not eval(condition)):
			incorrect_conditions = incorrect_conditions + 1
			print("Error: The condition " + str(condition) +  " of parameter "
				+ str(key) + " is not true!")

	if incorrect_conditions != 0:
		print(str(incorrect_conditions) + " conditions are false")
		sys.exit()
	

def load_parameters(config_file_path, params_db_filename = 'parameters.db'):
	"""Loads all parameters from parameters.db (or argument 2) file.
	Reads configuration for argument1 file and if the type of the config 
	matches with the parameter it's stored.	Also all Help Strings are stored 
	in the module variable HELP_STRINGS and can be accessed with the parameter 
	name as key."""

	params_db_path = os.path.join(os.path.dirname(__file__), params_db_filename)
	params = _parse_file(params_db_path)
	config = _parse_file(config_file_path)
    
	param_dict = {}
	conditions_dict = {}
	incorrect_params = 0
	
	for key, (default, condition, description) in params.items():
		globals()[key] = default
		if key in config:
			
			float_as_int = False
			c = config[key]
			type_c = type(c)
			if((type(default) == float) and (type_c == int)) or \
				((type(default) == type) and (default == float)):
				
				type_c = float
				float_as_int = True

			if(type_c == type(default)) or \
				((type(default) is type) and (type_c == default)):
				if float_as_int:
					globals()[key] = float(config[key])
				else:
					globals()[key] = config[key]
			else:
				print("Error: Wrong type of " + str(key) + "!")
				incorrect_params = incorrect_params + 1
				break;

		elif type(default) is type:
			print("Error: Mandatory parameter " + str(key) + " missing!")
			incorrect_params = incorrect_params + 1
			break;

		param_dict[key] = globals()[key]

		if condition is not None:
			conditions_dict[key] = condition

	if incorrect_params != 0:
		print(str(incorrect_params) + " Errors were detected.")
		sys.exit()

	_check_conditions(conditions_dict) 

	return param_dict