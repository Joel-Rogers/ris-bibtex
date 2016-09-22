from sys import argv
import os

script, target_file = argv
input_folder = os.getcwd()

print "This script converts a .ris into a .bib format, and appends the result \
to a specified file."
raw_input("So we will append all ris files in %r to %r in .bib format (CTRL-C to abort)" % (input_folder, target_file))

		
# These functions take the kind of information contained within a particular
# line, and assigns the information to the appropriate output variable(s).
def typ(right, ty):
	if 'JOUR' in right:
		if ty is "":
			ty = '@article'
		else:
			ty = '@multipleTYs????'
	else:
		ty = '@unrecognisedTY'
	return ty
		
def auth(right, au, au1):
	# Tests if format is <surname, firstnames>, and does nothing if so.
	if ',' in right:
		pass
	# If format is not the above, test for a middle name or initial, and assign these
	# to a "forenames" string.
	elif ' ' in right:
		# Assigns the first word to forenames and the last word to surnames,
		right = right.split(' ')
		forenames = right[0]
		surnames = right[-1]
		tempfore = ""
		tempsur = ""
		for word in right[1:-1]:
		# I'm making the assumption that only "de" or "van/ von"s will be 
		# attached to the surnames, and initials (one letter) or longer names
		# (i.e. middle names) should be grouped with the forenames.
		# Does this iteration occur in ORDER of index? (I think so, although
		# it wouldn't for DICTIONARIES).
			if len(word) == (2 or 3):
				tempsur += word + ' '
			else:
				tempfore += ' ' + word
		forenames += tempfore
		surnames = tempsur + surnames
		# Regenerates 'right' in the appropriate format.
		right = surnames + ',' + forenames
	if au is "":
		au1 = ((right[:right.index(',')]).replace(' ', '_')).lower()
		au = right
	else:
		au += ' and ' + right
	return au, au1
		
def title(right, t1):
	if t1 is "":
		t1 = right
	elif right != t1: 
		t1 = 'multiple titles????'
	return t1
	
def journal(right, j1):
	# If you're seeing the first "journal" label, assign its value to the variable.
	if j1 is "":
		j1 = right
	# If this is just a repetition, do nothing.
	elif j1 == right:
		pass
	# Otherwise, test if this might be the abbreviated version (what I personally want);
	# if it is, make this your new favourite (assume that short and non-empty =
	# abbreviated version).
	else:
		if len(right) < len(j1):
			j1 = right	
		# ****** Maybe get rid of this print? ******
		print "\t ^ Multiple journal entries found?"
	return j1
	
def volume(right, vl):
	if vl is "":
		vl = right
	elif right != vl:
		vl = 'Multiple volumes????'
	return vl
	
def number(right, IS):
	if IS is "":
		if '-' in right and '--' not in right:
			right = right.replace('-', '--')
		IS = right
	elif right != IS:
		IS = 'Multiple issues????'
	return IS
	
def startpage(right, sp):
	if sp is "":
		sp = right
	elif right != sp:
		sp = "Too many start pages????"
	return sp
	
def endpage(right, ep):
	if ep is "":
		ep = right
	elif right != ep:
		ep = "Too many end pages????"
	return ep
	
def date(right, yr):
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
		'Sep', 'Oct', 'Nov', 'Dec']
	if len(right) > 10:
		right = right[:10]
	if yr is "":
		yr = right[:4]
		monthn = right[5:7]
		if monthn.isdigit():
			monthn = int(monthn)
			mnth = months[monthn - 1]
		else:
			mnth = 'Can\'t get month value????'
	elif right != yr:
		yr = 'Multiple '
		mnth = 'years????'
	return yr, mnth
	
def year(right, yr):
	if yr is "":
		yr = right
	elif right != yr:
		yr = 'Multiple years????'
	return yr
	
def publisher(right, pb):
	if pb is "":
		pb = right
	elif right != pb:
		pb = "Multiple publishers????"
	return pb
	
# Unclear whether multiple keywords would be given in a single line or not.
# Therefore may need to change the following function.
def keyw(right, kw):
	if kw is "":
		kw = right
	else:
		kw = kw + ', ' + right
	return kw
	
def abstract(right, ab):
	if ab is "":
		ab = right
	# If you've been given multiple, non-equivalent abstracts, there's (probably) something wrong.
	elif right != ab:
		ab = 'Multiple abstracts????'
	# If you've been given multiple, equivalent abstracts, do nothing.
	# (This logic is applied to all functions above and below with similar statements.)
	return ab
	
def doi(right, do):
	if "doi:" in right:
		right = (right[4:]).lstrip()
	if do is "":
		do = right
	elif right != do:
		do = 'Multiple dois????'
	return do
	
def issn(right, sn):
	if sn is "":
		sn = right
	elif right != sn:
		sn = 'Multiple serial numbers????'
	return sn
	
def url(right, ur):
	if ur is "":
		ur = right
	else: 
		ur += ', ' + right
	return ur
	
# This function evaluates the line, deciding what values it contains, and updates
# the appropriate script variable.
def test_value(left, right, ty, key, au, au1, t1, j1, vl, IS, sp, ep, yr, mnth, pb, kw, ab,
	do, sn, ur, end_file):
	possauth = ["AU", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A0"]
	posstitle = ["T1", "TI"]
	possjourn = ["J1", "JF", "J2", "T2", "JO", "JA"]
	possdate = ["Y1", "Y2", "DA", "PY"]
	possab = ["AB", "N2"]
	possdo = ["DO", "N1", "M3"]
	if 'TY' in left: 
		ty = typ(right, ty)
	elif any(x in left for x in possauth):
		au, au1 = auth(right, au, au1)
	elif any(x in left for x in posstitle):
		t1 = title(right, t1)
	elif any(x in left for x in possjourn):
		j1 = journal(right, j1)
	elif 'VL' in left:
		vl = volume(right, vl)
	elif 'IS' in left:
		IS = number(right, IS)
	elif 'SP' in left:
		sp = startpage(right, sp)
	elif 'EP' in left:
		ep = endpage(right, ep)
	elif any(x in left for x in possdate):
		yr, mnth = date(right, yr)
	# I've commented the below out, as the example .ris file seems
	# to misuse PY (or, perhaps, Y1. Check this).
	#elif 'PY' in left:
		#yr = year(right, yr)
	elif 'PB' in left:
		pb = publisher(right, pb)
	elif 'KW' in left:
		kw = keyw(right, kw)
	elif any(x in left for x in possab):
		ab = abstract(right, ab)
	elif any(x in left for x in possdo):
		do = doi(right, do)
	elif 'SN' in left:
		sn = issn(right, sn)
	elif 'UR' in left:
		ur = url(right, ur)
	elif 'KW' in left:
		kw = keyw(right, kw)
	elif 'ER' in left:
		# ***** How do I break out of this function, and also the for-loop
		# ("line in g") "above" it?
		end_file = True
	return (ty, key, au, au1, t1, j1, vl, IS, sp, ep, yr, mnth, pb, kw, ab,
	do, sn, ur, end_file)
	

# This function runs test_value on each line of the file in turn, and formats
# the final results of this appropriately.
def assign_value(f):
	(ty, key, au, au1, t1, j1, vl, IS, sp, ep, yr, mnth, pb, kw, ab,
	do, sn, ur) = [""]*18
	end_file = False
	with open(f) as g:
		for line in g:
			# This should be '  - ' (i.e. TWO spaces), but people are often stupid so
			# I have to let them get away with one; needs the \n to account for
			# empty fields.
			if ' - ' in line or ' -\n' in line:
				left = line[:line.index('-')]
				right = line[line.index('-') + 1:]
				right = right.strip()
				if right != "":
					# This updates the values according to the 'type' identified in the left 
					# part of the string, using the information contained in the right.
					(ty, key, au, au1, t1, j1, vl, IS, sp, ep, yr, mnth, pb, kw, ab,
					do, sn, ur, end_file) = test_value(left, right, ty, key, au, au1, t1, j1, 
					vl, IS, sp, ep, yr, mnth, pb, kw, ab, do, sn, ur, end_file)
					# We then store the 'type' of this line for future reference, 
					# just in case the next line does NOT have a type, in which case
					# we assume it's the same type as the previous line, and run
					# the conditional statement below.
					lastleft = left
				# If right is the empty string, just ignore it and move on.
			elif line.strip() != "":
			# This will run the most recently-run function on any lines which don't
			# themselves have a label (unless the line is an empty string/ whitespace
			# only, in which case do nothing (move to next line)).
				line = line.strip()
				(ty, key, au, au1, t1, j1, vl, IS, sp, ep, yr, mnth, pb, kw, ab,
				do, sn, ur, end_file) = test_value(lastleft, line, ty, key, au, au1, t1, j1, 
				vl, IS, sp, ep, yr, mnth, pb, kw, ab, do, sn, ur, end_file)
			if end_file == True:
				break
	# The following statements just reformat the final output values into
	# a sensible format to be written to the output file. They also construct
	# a new 'key' so that the entry can be called within LaTeX.
	# Take the last two numbers of the year, ready to assign to the key.
	y = yr[2:]
	# 'au1' represents the lower-case/underscored version of the first author's
	# surname, as created by auth().
	key = au1 + y
	# Sometimes people don't separate sp and ep, so we'll deal with this possibility
	# here.
	if sp is "" or ep is "":
		pages = sp + ep
		# Add a double-hyphen if they didn't.
		if '-' in pages and '--' not in pages:
			pages = pages.replace('-', '--')
	else:
		pages = sp + '--' + ep
	return (ty, key, au, t1, j1, vl, IS, pages, yr, mnth, pb, kw, ab,
	do, sn, ur)
	
# Takes the outputs of assign_value and arranges them correctly for writing
# to a .bib file.
def assemble_content(f):
	new = '},\n\t'
	(ty, key, au, t1, j1, vl, IS, pages, yr, mnth,
	pb, kw, ab, do, sn, ur) = assign_value(f)
	content = (ty + '{' + key + ',\n\t' + 'author = {' + au+ new + 'title = {' 
	+ t1 + new + 'journal = {\emph{' + j1+ '}'+ new + 'volume = {' + vl + new + 
	'number = {' + IS + new + 'pages = {' + pages + new + 'year = {' + yr + 
	new + 'month = {' + mnth + new + 'publisher = {' + pb + 
	new + 'keywords = {' + kw + new + 'abstract = {' + ab + new + 'doi = {' 
	+ do + new + 'issn = {' + sn + new + 'url = {' + ur + '}' + '\n}\n\n')
	return content
	
	

files = next(os.walk(input_folder))[2]
# Do all the following operations with the target_file's FileObject.
with open(target_file, 'a') as f:
	print "I have found and appended the following files to %r:" % target_file
	# Iterate through all files in the cwd...
	for file in files:
		# ...then, with any .ris files...
		if file.endswith('.ris'):
			print file
			# ...assign the output of assemble_content to the 'content' variable...
			content = assemble_content(file)
			# ...and append the result of this to the 'target_file'. This file is closed
			# at the end of each write operation.
			f.write(content)
		# If it's not a .ris file, do nothing!
	
# Consider adding a feature which deletes the .ris files once everything is done
# ASSUMING that this script works well.