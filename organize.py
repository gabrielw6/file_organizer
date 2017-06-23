#! /usr/bin/python
#Organizer
import sys
import os
from shutil import move
from shutil import Error as ShError

def defaultVal(var):
    if var == "Y" or var=="y":
            return True
    elif var == "N" or var=="n":
            return False
    else:
        return None

def listcwd():
	return os.listdir(os.getcwd())

def checkIndex(dictionary, index):
	#'''Check the index of a dictionary.'''
    try:
        dictionary[index]
        return True
    except KeyError:
        return False

def checkType(element, what="file"):
	# '''Check type of unknown element in current
	# directory. Will return True if element is of
	# specified parameter arguments.'''
    # 'what' parameter argument may be 'dir' or 'file'
    try:
        directory = what=="dir"
        fil = what=="file"
    finally:
        if (fil==directory)==True:
            raise ValueError("'what' argument neither 'file' nor 'dir'")
	try:
		os.chdir(element)
		os.chdir("..")
		if directory:
			return True
		if fil:
			return False
	except:
		if directory:
			return False
		if fil:
			return True

def organize(tdir, vals):
    '''
    Each extension is a key, their target directory is the value.
    '''
    print ""
    verb=True
    #Cd to specified dir
    if tdir!=os.getcwd():
        os.chdir(os.getcwd() + tdir)
    print "Target directory: ", os.getcwd()
    #Create a list of items in that dir
    cdel = listcwd()
    directories = checkType(cdel)
    #Create the dirs for the extensions if they don't exist
    print "---"
    for d in vals.values():
        if d not in cdel:
            print "Directory will be created:", d
            os.mkdir(d)
            cdel = listcwd()
    #Final dictionary
    fdict = {}
    #Point the files to their destiny folders
    for ext in vals.keys():
        print "EXT",ext
        l = []
        extm = "." + str(ext)
        for i in cdel:                      #Items in current dir
            if len(i)>len(extm):            #Prevent file length error
                vrb = i[-len(extm):]
                if vrb == extm or vrb == extm.upper():#Basic check for file format
                    l.append(i)             #If the file have the extension, append to the list for that dir  
        if checkIndex(fdict, vals[ext]):    #Final dictionary[specified dir] = [files with extension]
            for el in l[:]:
                fdict[vals[ext]].append(el)
        else:
            fdict[vals[ext]] = l[:]
    #Copy the files to the folders and if verbose,
    #create the dict(dirname:file) to use in verbose 'for' loop
    vf = {}
    for n in fdict.keys():
        for arc in fdict[n]:
            vf[n] = fdict[n]
            try:
                move(arc, n)
            except ShError:
                print "Error: File %s already exists in target directory." % arc
                print "Do you want to replace the file in the directory with the"
                ans = raw_input("new one?(Y/N)")
                while defaultVal(ans) == None:
                    print ans
                    ans = raw_input("(Y/N)")
                if defaultVal(ans):
                    os.remove(n+os.sep+arc)
                    move(arc, n)
                    print ">>Moved."
                else:
                    pass                    
                
    #Verbose mode below
    if verb:
        print "+INFO"
        print ""
        for dr in vf.keys():
            os.chdir(os.getcwd()+os.sep+dr)
            for i in os.listdir(os.getcwd()):
                if i in vf[dr]:
                    print ">>FILE-", i
                else:
                    print "file--",i
            os.chdir("..")
        print ""
        print "-INFO"

def parseArgs(li, char):

    '''
    Returns dict with the words in items "i"
    of the list "li" separated by the specified char "char"
    '''

    finaldict = {}
    for i in li:
        #print "Before split:", i
        st = i.split(char)
        #print "After split:", st
        finaldict[st[0]] = st[1]
    return finaldict

def main(direc, kwargs):
    print "dict 1st:",kwargs
    organize(direc, kwargs)
    
def help():
    '''
    Prints help about the program.
    '''
    print "organize: usage:"
    print "    organize <target dir> <file=dir>"
    print ""
    print "    <target dir>: The directory to which the program\n    will run itself. Protects against recursivity."
    print "    <dir=file>: Specifies to which dir will the files\n    with 'file' extension will be moved(no need for the '.' before extension).\n    If the dir 'dir' doesn't exists, it will be created,\n    with user permission."
    #print "    If in the specified dirs at the command above have\n    even only one file with same name, the program will exit."

if __name__ == "__main__":
    #Run organize method with command line args
    #sys argv 1 is the target dir, the rest is the
    #file=dir specification
    if len(sys.argv)>2:
        main(sys.argv[1], parseArgs(sys.argv[2:], "="))
    else:
        if len(sys.argv)==1:
            help()
        else:
            if sys.argv[1]!="--help":
                print "organize: %s:invalid option" % sys.argv[1]
            else:
                help()
