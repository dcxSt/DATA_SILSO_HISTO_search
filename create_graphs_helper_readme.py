#!/home/steve/anaconda3/bin/python3

# creates a description of all the methods in the python scripts

# import statements
from os import listdir

# returns the contents of the specified file, thows exception if no file found
def get_contents(fname):
    f = open(fname,"r")
    contents = [line for line in f]
    f.close()
    return contents

# writes the main part of the file - the important stuff
def write_body(gh,contents):
    for i in range(len(contents)):
        if contents[i][:3] == 'def':
            # write the comment before the methodname
            j=1
            while contents[i-j][:1] == "#":
                j+=1
            j-=1
            gh.write("*")
            while j>0:
                gh.write(contents[i-j][2:-1])
                j-=1
            # write the method name
            gh.write('*\n\n')
            gh.write(contents[i][:-1])
            j=i
            while '):' not in contents[j][:-1]:
                j+=1
                gh.write(contents[j][:-1])
            gh.write('\n\n')


# writes to the file 'GRAPHS_HELPER_README.md'
def main():
    gh = open("GRAPHS_HELPER_README.md","w")
    # write the title and the preamble
    gh.write('# GRAPHS HELPER README\n\n')
    gh.write('### This readme is bascially the documentation for the methods found in graphs_helper.py\n\n')
    contents = get_contents("graphs_helper.py")
    write_body(gh,contents)
    gh.close()

main()

