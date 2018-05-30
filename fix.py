# This program opens the post database and takes out the line containing the timestamp
fo = open('postdb.txt').readlines()
fw = open('postdb_fixed.txt', 'w')
for line in fo:
    if line[0] != 'T':
        fw.write(line);
        
