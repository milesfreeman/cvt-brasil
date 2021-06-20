# import pandas as pd
import sys
import os

# símbolos não encontrados: à, ü
decoder = {
    '&Aacute;' : 'Á', '&aacute;' : 'á',
    '&Acirc;' : 'Â' , '&acirc;' : 'â',
    '&Atilde;' : 'Ã' , '&atilde;' : 'ã',

    '&Eacute;' : 'É' , '&eacute;' : 'é' ,
    '&Ecirc;' : 'Ê' ,  '&ecirc;' : 'ê' ,

    '&Iacute;' : 'Í' , '&iacute;' : 'í' ,	

    '&Oacute;' : 'Ó' , '&oacute;' : 'ó' ,
    '&Ocirc;' : 'Ô' , '&ocirc;' : 'ô' ,
    '&Otilde;' : 'Õ' , '&otilde;' : 'õ' ,

    '&Uacute;' : 'Ú' , '&uacute;' : 'ú' ,

    '&Ccedil;' : 'Ç' , '&ccedil;' : 'ç' ,

    '&lt;span&gt;' : '(' , '&lt;/span&gt;' : ')' ,
    '&sup2;' : '^2' , '&times;' : '*'
}

def main():
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        lines = f.readlines()
    with open('REVISED_' + fname, 'w') as f:
        for line in lines[1:-1]:
            print(line)
            for k,v in decoder.items():
                if line[0] == '<' : continue
                line = line.replace(k,v)
            f.write(line)
    
        

main()



