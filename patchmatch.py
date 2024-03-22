#!/usr/bin/env python3

import sys
import csv
import getopt


def elog(*arg, **kwargs):
	print(*arg, file=sys.stderr, **kwargs)

def semver_is_smaller(version, target_version):
	'''
	if ver1 is smaller than ver2
	returns True, False or None if unsure
	
	take the shortest version string for comparison length
	'''

	target_version_dot_length = len(target_version.split("."))
	version_dot_length = len(version.split("."))
	version_comparison_length = min([version_dot_length, target_version_dot_length])
	for i in range(version_comparison_length):
		try:
			# TODO handle non-numeric versions
			version_component = int(version.split(".")[i])
			target_version_component = int(target_version.split(".")[i])
			if version_component < target_version_component:
				# elog("returning true for smaller", version_component, target_version_component)
				return True
			if version_component > target_version_component:
				return False
		except IndexError:
			elog(f"Warning: index error between versions: {version} {target_version}")
			return None



def smaller(s,s1):
	return semver_is_smaller(s, s1)

def smaller_eq(s,s1):
	if s == s1:
		return True
	else:
		return semver_is_smaller(s, s1)

def greater(s,s1):
	if semver_is_smaller(s, s1):
		return False
	elif s == s1:
		return False
	else:
		return True


def equal(s,s1):
	return s == s1

def neq(s,s1):
	return s != s1

def greater_eq(s,s1):
	if semver_is_smaller(s, s1):
		return False
	elif s == s1:
		return True
	else:
		return True


class Rule:
	def __init__(self, condition, version):
		self.condition = condition
		self.version = version

		if self.condition == '>':
			self.comparison_function = greater
		elif self.condition == '>=':
			self.comparison_function = greater_eq
		elif self.condition == '<':
			self.comparison_function = smaller
		elif self.condition == '<=':
			self.comparison_function = smaller_eq
		elif self.condition == '==':
			self.comparison_function = equal
		elif self.condition == '!=':
			self.comparison_function = neq
		else:
			print("Invalid condition:", self.condition, file=sys.stderr)


def load_rules(filepath):
	all_statements = [] # a list of rule statements, each being a list of rules
	with open(filepath, 'r') as f:
		for line in f:
			statement = []
			line = line.strip()

			if line.startswith('#') or line == '': # empty line
				continue
			conditions = line.split(',')
			for c in conditions:
				op = c.split()[0].strip()
				ver = c.split()[1].strip()
				statement.append(Rule(op, ver))
			all_statements.append(statement)
	return all_statements

def filter_lines(input_file, rule_statements, delim):
	matched_rows = []
	with open(input_file,'r') as f:
		reader = csv.reader(f, delimiter=delim)
		for row in reader:
			# version is always the last column
			version = row[-1].strip()
			# print('version:', version)
			for statement in rule_statements:
				# each statement is an OR, each rule is an AND
				rule_match_count = 0
				for rule in statement:
					res = rule.comparison_function(version, rule.version)
					# elog(version, rule.version, rule.comparison_function, res)
					if res:
						rule_match_count += 1
				if rule_match_count == len(statement):
					matched_rows.append(row)
					break
	return matched_rows

def help():
	print("Usage: %s [-o outfile] <rule file> <input file>" %(sys.argv[0]))
	print("Example:\n%s example.rules data.tsv" %(sys.argv[0]))

def main():
	opts, args = getopt.getopt(sys.argv[1:], 'ho:d:')
	custom_delimeter = None
	outfile = None
	for o,a in opts:
		if o == '-h':
			help()
			exit(0)

		if o == '-d':
			custom_delimeter = a

		if o == '-o':
			outfile = a



	if len(args) != 2:
		print("missing input / rule file")
		help()
		exit(0)
	rulefile = args[0]
	filename = args[1]

	rules = load_rules(rulefile)

	if custom_delimeter == None:
		if filename.endswith("tsv"):
			custom_delimeter = '\t'
		else:
			custom_delimeter = ','

	matched_rows = filter_lines(filename, rules, delim=custom_delimeter)
	# print(matched_rows)
	if outfile:
		with open(outfile, 'w+') as f:
			outwriter = csv.writer(f, delimiter=custom_delimeter)
			for r in matched_rows:
				outwriter.writerow(r)
	else:
		outwriter = csv.writer(sys.stdout, delimiter=custom_delimeter)
		for r in matched_rows:
			outwriter.writerow(r)


if __name__ == '__main__':
	main()







