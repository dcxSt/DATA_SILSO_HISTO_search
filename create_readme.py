# creates a description of all the methods in the python scripts

# import statements
from os import listdir

# method for returning all the .py filenames in the directory
def get_py_filenames():
    return [f for f in listdir('.') if f[-3:]==".py"]

# method for returning all the .ipynb filenames in the directory
def get_ipynb_filenames():
    return [f for f in listdir('.') if f[-6:]==".ipynb"]

# returns big dictionary of methods and descriptors in each file
# key = filename ; value = [[method_name,description],...]
def get_method_description_dictionary(filenames):
    method_description_dictionary = {}
    for name in filenames:
        f = open(name,"r")
        contents = f.readlines()
        f.close()
        index = 0
        methods_descriptors = []
        while index < len(contents):
            nextline = contents[index]
            try:
                if nextline[:3]=="def":
                    # if there is a method written, add it to the list
                    methodname = nextline[4:nextline.index("(")]
                    descriptor=""
                    i=1
                    lastline= contents[index-i]
                    while lastline[0]=="#":
                        descriptor+= lastline[1:]
                        i+=1
                        lastline= contents[index-i]
                    methods_descriptors.append((methodname,descriptor))
            except:
                pass
            index+=1
        method_description_dictionary[name] = methods_descriptors
    return method_description_dictionary

# write the title
def write_title(readme):
    title = open("readme/title.txt","r")
    readme.write("# "+title.readline()+"\n\n")
    title.close()

# write the preamble
def write_preamble(readme):
    preamble = open("readme/preamble.txt","r")
    contents = preamble.readlines()
    preamble.close()
    readme.write("## Preamble\n")
    for line in contents:
        readme.write(line)
    readme.write("\n")

# write the body
def write_body(readme):
    body_dictionary = get_method_description_dictionary(get_py_filenames())
    readme.write("## Python scripts, their methods and descriptors\n\n")
    for script in body_dictionary:
        readme.write("### "+script+"\n\n")
        for m in body_dictionary[script]:
            readme.write("##### "+m[0]+"():\t")
            readme.write(m[1]+"\n\n")

# write the links section
def write_links(readme):
    links = open("readme/links.txt")
    contents = links.readlines()
    links.close()
    readme.write("## Links and Resources\n\n")
    for line in contents:
        if line!="\n":
            readme.write("* "+line+"\n")

# writes the readme file
def write_readme():
    readme = open("README.md","w")
    write_title(readme)
    write_preamble(readme)
    write_body(readme)
    write_links(readme)
    readme.close()

write_readme()