# file io, does things like reading and writing to textfiles

# save 1D list to text file (works for array too i think)
def save_list_to_text_file(the_list,file_name,overwrite=False):
    if file_name[-4:] != ".txt":
        print("There is a type in the file_name, your format is incorrect: should end with '.txt'")
        raise Exception
    if not overwrite:
        try:
            text_file = open(file_name,"r")
            text_file.close()
            print("The text file",file_name,"already exists")
            print("If you wish to overwrite it set overwrite=True")
            return
        except IOError:
            pass
    test_file = open(file_name,"w")
    for i in the_list:
        text_file.write(i+"\n")
    text_file.close()
    print("the list has been written to the file:",file_name)
    return
    

