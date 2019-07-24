# creates a description of all the methods in the python scripts 
# It's the method that generated the file you are currently reading 

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
            except: pass
            index+=1
        method_description_dictionary[name] = methods_descriptors
    return method_description_dictionary

# returns a dictionary key = filename ; value = dictionary with key = methodname, value = num lines
def get_size_methods_dictionary(filenames):
    size_methods_dictionary = {}
    for name in filenames:
        size_methods_dictionary[name] = {}
        f=open(name,"r")
        contents = f.readlines()
        f.close()
        index = 0
        inside_method=False# true if current line is inside a method
        methodname=None;count=0#init
        method_sizes = {}# yes a dictionary of dictionaries # delete this once working
        while index < len(contents):
            nextline = contents[index]
            if inside_method:
                try:
                    if nextline[:4]!="    " and nextline!='\n':
                        inside_method=False
                        size_methods_dictionary[name][methodname] = count# yes a dictionary of dictionaries
                        index-=1# want to reread the line
                    else: count+=1
                except: pass
            else:
                try:
                    if nextline[:3]=="def":
                        inside_method=True
                        # if there is a method, add it to the list
                        methodname = nextline[4:nextline.index("(")]
                        count=1
                except: pass
            index+=1
        # if the last method wasn't detected add it
        if inside_method==True: 
            size_methods_dictionary[name][methodname] = count
    return size_methods_dictionary

# get the ipynb number of blocks and descriptors dictionary
def get_ipynb_descriptors_dic(filenames):
    ipynb_descriptors_dic = {}
    for name in filenames:
        f=open(name,"r")
        contents = f.readlines()
        f.close()
        index = 0
        got_descriptor = False
        while index < len(contents):
            nextline = contents[index]
            # get the descriptor of the file, the first lines with # in them
            if not got_descriptor:
                if '"source":' in nextline:
                    i=1
                    des_line = contents[index+i]
                    descriptor = ""
                    while "#" in des_line:
                        indices_speech = [i for i,x in enumerate(des_line) if x =='"']
                        descriptor+=des_line[indices_speech[0]+2:indices_speech[1]]
                        i+=1
                        des_line = contents[index+i]
                    got_descriptor = True
                    blocks=1
            else:
                if '"source":' in nextline:
                    blocks+=1
            index +=1
        ipynb_descriptors_dic[name] = [blocks,descriptor]
    return ipynb_descriptors_dic

# returns dictionary key = script ; value = subheadding of script
def get_subheaders_dictionary(filenames):
    subheaders_dictionary = {}
    for name in filenames:
        f = open(name,"r")
        contents = f.readlines()
        f.close()
        index = 0
        subheader=""
        i=0
        nxt_line = contents[i]
        while nxt_line[0]=="#":
            if i==0:
                subheader += "***"+nxt_line[2:]
            else:
                subheader = subheader[:-1]+", "+nxt_line[2:]
            i+=1
            nxt_line = contents[i]
        subheader = subheader[:-1]+"***"
        subheaders_dictionary[name]=subheader
    return subheaders_dictionary

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

# write the main body of the readme file
def write_body(readme):
    py_filenames = get_py_filenames()
    subhead_dic = get_subheaders_dictionary(py_filenames)
    body_dictionary = get_method_description_dictionary(py_filenames)
    size_methods_dictionary = get_size_methods_dictionary(py_filenames)
    readme.write("## Python scripts, their methods and descriptors: \n\n")
    for script in body_dictionary:
        readme.write("### "+script+"\n")
        readme.write(subhead_dic[script]+"\n\n")
        for m in body_dictionary[script]:
            readme.write("**"+m[0]+"()**  ")
            readme.write("["+str(size_methods_dictionary[script][m[0]])+"]\t")
            readme.write(m[1]+"\n\n")
        readme.write("***\n\n")
    readme.write("\n\n")

# write the jupiter-notebooks section
def write_ipynb(readme):
    ipynb_filenames = get_ipynb_filenames()
    ipynb_descriptors_dic = get_ipynb_descriptors_dic(ipynb_filenames)
    readme.write("## Jupyter notebooks:\n\n")
    for script in ipynb_descriptors_dic:
        readme.write("**"+script+"**  ")
        try:
            readme.write("[code blocks = "+str(ipynb_descriptors_dic[script][0])+"]  ")# no of blocks
        except: pass
        readme.write(ipynb_descriptors_dic[script][1])# descriptor
        readme.write("\n\n")

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
    write_ipynb(readme)
    write_links(readme)
    readme.close()

write_readme()