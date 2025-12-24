import os
import json
import random
import subprocess

# Read Available Json
def read_json():
	json_file = 'files/locked_folders.json'
	if os.path.exists(json_file):
		with open(json_file, 'r') as file:
			dct = json.load(file)
	else:
		dct = {}

	return dct

# Write New Value To Json
def write_to_json(data):
	json_file = 'files/locked_folders.json'
	with open(json_file, 'w') as file:
		json.dump(data, file)

def get_from_json(fname):
	dct = read_json()
	return dct.get(fname, None)

# Generate New Key
def generate_key():
	string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	keygen = random.sample(string, 12)
	return ''.join(keygen)

# Set Lock
def lock(fpath, password):
	key = generate_key()

	fname = os.path.basename(fpath)
	cwd = '/'.join(fpath.split('/')[:-1]) + '/'
	command1 = ['ren', fname, f'"Control Panel.{{21EC2020-3AEA-1069-A2DD-{key}}}"']
	command2 = ['attrib', '+h', '+s', f'"Control Panel.{{21EC2020-3AEA-1069-A2DD-{key}}}"']

	dct = read_json()

	if not fname in dct.keys():
		dct[fname] = [fpath, key]
		write_to_json(dct)

		passwords = read_passwords()
		passwords[fname] = password
		write_passwords(passwords)

		subprocess.run(command1, shell=False, cwd=cwd)
		subprocess.run(command2, shell=False, cwd=cwd)

		status = 'locked'	
	else:
		status = 'failed'

	return status

# Unlock Path
def unlock(fpath, password, key):
	fname = os.path.basename(fpath)
	cwd = '/'.join(fpath.split('/')[:-1]) + '/'
	command1 = ['attrib', '-h', '-s', f'"Control Panel.{{21EC2020-3AEA-1069-A2DD-{key}}}"']
	command2 = ['ren', f'"Control Panel.{{21EC2020-3AEA-1069-A2DD-{key}}}"', fname]

	passwords = read_passwords()
	pass_ = passwords.get(fname)

	if pass_ == password:
		dct = read_json()
		del dct[fname]
		write_to_json(dct)

		subprocess.run(command1, shell=False, cwd=cwd)
		subprocess.run(command2, shell=False, cwd=cwd)

		del passwords[fname]
		write_passwords(passwords)

		status = 'unlocked'
	else:
		status = 'failed'

	return status

def read_passwords():
	password_file = 'files/pwd.json'
	if os.path.exists(password_file):
		with open(password_file, 'r') as file:
			return json.load(file)
	else:
		return {}

def write_passwords(passwords):
	password_file = 'files/pwd.json'
	with open(password_file, 'w') as file:
		json.dump(passwords, file)