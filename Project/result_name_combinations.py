import pandas as pd 
import re
import itertools

def name_combination(name_for_split):
	
	names = [name_for_split]

	if "-" in name_for_split and "'" not in name_for_split:
		names = [name_for_split, name_for_split.replace("-", ""), name_for_split.replace("-", " "), name_for_split.split("-")[0].strip(), name_for_split.split("-")[1].strip()]

	if "'" in name_for_split and "-" not in name_for_split:
		names = [name_for_split, name_for_split.replace("'", ""), name_for_split.replace("'", " "), name_for_split.split("'")[0].strip(), name_for_split.split("'")[1].strip()]

	if "-" in name_for_split and "'" in name_for_split:
		names.append(name_for_split)                          
		names.append(name_for_split.split("-")[0] )            
		names.append(name_for_split.split("-")[1] )             
		names.append(name_for_split.replace('-', ' ') )                 
		names.append(name_for_split.replace('-', ' ').replace("'", '') )  
		names.append(name_for_split.replace('-', ' ').replace("'", ' ') )  
		names.append(name_for_split.split("-")[1] )         
		names.append(name_for_split.split("-")[1].replace("'", '') ) 
		names.append(name_for_split.split("-")[1].split("'")[1] )       

	if "jr" in name_for_split:
		names.append(name_for_split.strip())
		names.append(name_for_split.replace("jr", "").strip())
	
	if "sr" in name_for_split:
		names.append(name_for_split.strip())
		names.append(name_for_split.replace("sr", "").strip())

	romman_letter = [' i', ' ii', ' iii', ' iv', ' v', ' vi', ' vii', ' viii', ' ix', ' x']
	for letter in romman_letter:
		if letter in name_for_split:
			names.append(name_for_split.replace(letter, '').strip())
			names.append(name_for_split) 

	if "st." in name_for_split:
		names.append(name_for_split) 
		names.append(name_for_split.replace('.', ' '))
		names.append(name_for_split.replace('.', ''))
		names.append(name_for_split.replace('st.', '').strip())
	unique_names = []
	[unique_names.append(x) for x in names if x not in unique_names]
	return unique_names

def remove_roman_numerals_from_end(name):
	roman_letter = [' i', ' ii', ' iii', ' iv', ' v', ' vi', ' vii', ' viii', ' ix', ' x']
	for roman in roman_letter:
		if name.lower().endswith(roman):
			name = name[:-(len(roman))]
	return name


def remove_white_spaces(names):
	new_names = []
	for name in names:
		new_names.append(re.sub(' +', ' ', name))
	return new_names

def full_name_split(name):
#   print('name_split', name)

	comma_before = name.split(",")[0].lower().strip()
	comma_after = name.split(",")[1].lower().strip()
	lnames = name_combination(comma_before)
	fnames = [comma_after]
	mname = ""
	status = "success"

	if " jr" in comma_after:
		comma_after = comma_after.replace("jr", "").strip()

	if " sr" in comma_after:
		comma_after = comma_after.replace("sr", "").strip()

	comma_after = remove_roman_numerals_from_end(comma_after)

	len_comma_after = len(comma_after.split(" "))

	if len_comma_after == 1:
		fnames = fnames + name_combination(comma_after) 

	elif len_comma_after == 2:
		fname = comma_after.split(" ")[0]
		fnames = fnames + name_combination(fname)
		mname = comma_after.split(" ")[1]

	else:
		status = "manual"

	fnames = remove_white_spaces(fnames)
	lnames = remove_white_spaces(lnames)

	return status, fnames, lnames, mname
	

def df_name_combinations(name):

	name_combinations = full_name_split(name)

	# Generate all combinations of first names and last names
	combinations = list(itertools.product(name_combinations[1], name_combinations[2]))

	# Create dataframe
	df = pd.DataFrame(combinations, columns=['firstname', 'lastname'])

	df['middlename'] = name_combinations[3]
	# Display dataframe
	return name_combinations[0], df


if __name__ == "__main__":
	# name = 'James-Donald, Smith'
	# print(name)
	# print(full_name_split(name))
	# print('----')
	# print(name)
	# name = "D'ANNA, Donald"
	# print(full_name_split(name))
	# print(name)
	# print('----')
	# print(name)
	# name = "LUTZ-O'HARE, St.James ross"
	# print(full_name_split(name))

	# print('----')
	# print(name)
	# name = "ORTIZ IV, ALLAn"
	# print(full_name_split(name))
	# print(name)
	# name = "ST.LOUIS , MARK poo Jeeva"
	# print(full_name_split(name))

	name = 'REy sr iv, poovarasi-savitha rosy ix'
	# name_combinations = full_name_split(name)
	# print(name_combinations[3])
	status, df_res_names = df_name_combinations(name)
	# print(type(df_res_names))
	
	print(df_res_names)
	# F.	If Last Name is: LUTZ-O'HARE First name is: James



