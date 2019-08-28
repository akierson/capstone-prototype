string = "test',.?!;:><{}[]+=_- fin"
punc = [",",".","<","?","!",";",":",">","<","{","}","[","]","+","=","_","-"]
for punc1 in punc:
     string = string.replace(punc1,'')
print(string)
