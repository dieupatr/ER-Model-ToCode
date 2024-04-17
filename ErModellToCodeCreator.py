from LexDrawio import *

import os
import sys

# Generate by AI


def create_file(file_path, content=None):
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            
            if content:
                file.write(content)  
    else:
        pass

# Generate by AI
# Valid +

def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
        
    except :
        pass
        



def FindId(source,target,Dic):

       if source in Dic:

              return source

       if target in Dic:

              return target



def ConvertTabelColumn(tabelcolumn):

       FormatColumn=[]

       for var in  tabelcolumn:

              if "*" in var:
                     var=var.replace("*"," ")
                     var=var+" PRIMARY KEY"

              FormatColumn.append( var.replace(":"," ") )


       return FormatColumn
       
       



def ExtractTabelsAndRelations(Diagramm):

       Attributes= {   }
       Tabels= {    }
       Relationen= {  }


       for block in Diagramm.blocks:
              
              Id=block.Attr["id"]
              Type=block.Attr["style"][0]
              value=block.Attr["value"]

              if Type=='ellipse':
                     
                     Attributes[Id]=value
                     
              if Type=="rounded=0":

                     Tabels[Id]=value

              if Type=="rhombus":
                     Relationen[Id]=value


       SQLTabels={}
       PrimeKey={   }

       for arrow in Diagramm.arrows:
              
              source=arrow.Attr["source"]
              target=arrow.Attr["target"]

              #Error connect two Tabels
              if (source in Tabels) and (target in Tabels):
                     print("Syntax error: ")
                     return False

              IdTabel=FindId(  source,target,Tabels  )
              IdAttr=FindId(  source,target, Attributes  )

              if IdTabel!=None and IdAttr!=None:

                     valueTabel=Tabels[IdTabel]
                     valueAttr=Attributes[IdAttr]

                     if "*" in valueAttr:
                            PrimeKey[valueTabel]=valueAttr.replace("*","")
                            

                     try:
                            SQLTabels[valueTabel]
                     except:
                             SQLTabels[valueTabel]=[   ]

                     SQLTabels[valueTabel].append(valueAttr)

       SQLRelation={    }
       
       for arrow in Diagramm.arrows:
              
              source=arrow.Attr["source"]
              target=arrow.Attr["target"]

              IdRelation=FindId(  source,target,  Relationen)

              if IdRelation==None:  continue

              RelaValue=Relationen[IdRelation]
              
              try:
                     SQLRelation[RelaValue]
              except:
                     SQLRelation[RelaValue]=[   ]
                     
                     

              IdAttr=FindId(  source,target, Attributes  )

              if IdAttr!=None:

                     value=Attributes[IdAttr]
                     SQLRelation[RelaValue].append(value)
                     continue


              IdTabel=FindId(  source,target,Tabels  )

              if IdTabel!=None:

                     value=Tabels[IdTabel]
                     value=PrimeKey[value]
                     SQLRelation[RelaValue].append(value)
                     continue

       return [SQLTabels, SQLRelation]


def CreateSQLCodeFromTabels(SQLTabels):


       SqlSkript=""""""

       for tabel in SQLTabels:

              tabelcolumn=ConvertTabelColumn( SQLTabels[tabel]  )

              StrinVar=",\n".join(tabelcolumn)
              
              Tabel=f"""

CREATE TABLE {tabel} (

{StrinVar}

); 
              """

              
              SqlSkript=SqlSkript+Tabel


       return SqlSkript


def CreateDeploySkript(file_path,DiagrammName):

       return f"""
import os


RootPath=""
Command=RootPath+"ErModellToCodeCreator.py "+"{file_path} "+"{DiagrammName}"

print("Deploy {DiagrammName} ")

os.system(Command)
print("")
print("Complete")

print("")
print("")
input("Press enter to continue")
       """


              


def GenerateDataBaseModell(file_path,DiagrammName):
       
       Diagramm=ParseDiagramsFromXmlFile(file_path)

       Diagramm=Diagramm[DiagrammName]


       [SQLTabels, SQLRelation]=ExtractTabelsAndRelations(Diagramm)

       SqlSkript_Tabels=CreateSQLCodeFromTabels(SQLTabels)

       SqlSkript_Relations=CreateSQLCodeFromTabels(SQLRelation)

       #Create Files

       RootFolder="DataModell_"+DiagrammName
       
       create_folder(RootFolder)

       create_file(RootFolder+"/"+"Tabels_"+DiagrammName+".sql", SqlSkript_Tabels)

       create_file(RootFolder+"/"+"Relations_"+DiagrammName+".sql", SqlSkript_Relations)

       Code=CreateDeploySkript(file_path,DiagrammName)

       

       create_file("Deploy_"+DiagrammName+".py", Code )

       


       
############Main##########
       

file_path=sys.argv[1]
#"ErModellTest.drawio"

DiagrammName=sys.argv[2]
#"ErModellTest"


GenerateDataBaseModell(file_path,DiagrammName)















