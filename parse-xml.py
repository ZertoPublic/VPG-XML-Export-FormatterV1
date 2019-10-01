#!/usr/bin/python3
#
#  SCRIPT NAME: parse-xml.py
#
#  SCRIPT VERSION: 0.0.005
#
#  PURPOSE: To extact data from a Zerto VPG export XML file into a legible CSV file
#
#  PARAMETER FILE: N/A
#
#  INPUT FILE: N/A
#
#  CALLED SCRIPTS: N/A
#
#  IMPORTED MODULES: xml.etree.ElementTree
#
#  SCRIPT USAGE: parse-xml.py ExportedSettings_date_time.xml
#
#  UPDATE HISTORY:
#        DATE               AUTHOR              UPDATE DESCRIPTION
#     05.09.2019       Lou Sassani              Initial script creation
#     30.09.2019       Lou Sassani              Hit an issue with a different XML export file which was causing
#                                               the ProcessXMLfile sub-routine to prematurely close the temp file.
#                                               I've removed the file close function in the sub-routine ProcessXMLfile
#     01.10.2019       Lou Sassani              Updated schema option to remove the reliance on the xml_elements_long.py file
#                                               to allow the parsing of the XML file.
#                                             
#                                               Include a further paramater to choose a raw dump of the XML file by providing a --raw
#                                               parameter after the xml file name
#                                               
#                                               Update the raw csv export format to change the vpgfield name from "Name" to "VPG-Name"
#                                               when an actual VPG name is found in that feild, you will still need to parse the raw
#                                               csv data to find which column the VPG-Name tag will be in as it will vary depening on
#                                               the number of elements in that VPG
#
#
#                                               Written By: LOU SASSANI,
#                                                           Systems Engineer
#                                                           AsiaPacific,
#                                                           Copyright Zerto Corporation
#                                               Email:  lou.sassani@zerto.com
#     Legal Disclaimer:
#
#     ----------------------
#     This script is an example script and is not supported under any Zerto support program or service.
#
#     The author and Zerto further disclaim all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for
#     a particular purpose.
#
#     In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever
#     (including, withoutlimitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) 
#     arising out of the use of or the inability to use the sample scripts or documentation, even if the author or Zerto has been advised of the possibility
#     of such damages.  The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.
#
## -- Set Global Veriables
#
import sys, os, re
Script_Version = "0.0.005"
#Script_Name = sys.argv[0]
Script_Name = os.path.basename(__file__)
global returncode
returncode = 0
#
## - Process filename passed
#
def ProcessPARAMETERS():
    #
    ## - Set Global parameters
    #
    global infile, RawOrCSV
    #
    ## - Set default output format
    #
    RawOrCSV = "CSV"
    #
    ## - Check how many paramaters have been passed
    #
    parmlen = len(sys.argv)
    if parmlen >= 2:
       infile = sys.argv[1]
       #
       ## - process the third paramarter passed
       #
       if parmlen == 3:
           RawOrCSV = sys.argv[2]
           x, RawOrCSV = RawOrCSV.split("--")
           RawOrCSV = RawOrCSV.upper()
       #
       ## - Make sure we have an XML file to process
       #
       if not infile.endswith('.xml'):
           print (Script_Name + " Version:" + Script_Version + " invalid file extention need a .xml file to process")
           exit(1)
    else:
        ShowSyntax()
#
## -- Define help subroutine
#
def ShowSyntax():
  print ("Usage: " + Script_Name + " Version:" + Script_Version + " </dir/xml_file_name.xml>")
  print ("       " + Script_Name + " Version:" + Script_Version + " </dir/xml_file_name.xml> [--raw]")
  print ("       " + Script_Name + " Version:" + Script_Version + " <xml_file_name.xml>")
  print ("       " + Script_Name + " Version:" + Script_Version + " --help\n")
  global returncode
  returncode = 1
  exit(1)
#
## - This sub-routine will generate the XML data in a raw CSV appened format
#
def ProcessXMLfileCSVRaw():
    #
    ## - import XML Element tree structure
    #
    import xml.etree.ElementTree as ET
    #
    ## - Generate CSV name
    #
    global CSVFileName
    CSVFileName = (str(infile)+".raw.csv")
    CSV = open(CSVFileName,"w")
    #
    ## - Zerto VPG export XML file
    #
    tree = ET.parse(infile)
    root = tree.getroot()
    #
    ## - Root element
    #
    VPGcount=0
    for S in root.iter("{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value"):
        for C0 in S.getchildren():
            cc=str(C0)
            s0,s1 = cc.split("}")
            s0,S1 = s1.split("'")
            VPGcount+=1
            CSV.write("\n")
            VPGdata=(s0,C0.text)
            VPGdata = str(VPGdata)
            VPGdata = VPGdata.replace("(","")
            VPGdata = VPGdata.replace(")","")
            CSV.write(str(VPGdata)+",")
            #
            ## - First Child Element
            #
            for C1 in C0.getchildren():
                cc=str(C1)
                s0,s1 = cc.split("}")
                s0,S1 = s1.split("'")
                VPGdata=(s0,C1.text)
                VPGdata = str(VPGdata)
                VPGdata = VPGdata.replace("(","")
                VPGdata = VPGdata.replace(")","")
                CSV.write(str(VPGdata)+",")
                #
                ## - First Child Element
                #
                for C2 in C1.getchildren():
                    cc=str(C2)
                    s0,s1 = cc.split("}")
                    s0,S1 = s1.split("'")
                    VPGdata=(s0,C2.text)
                    VPGdata = str(VPGdata)
                    VPGdata = VPGdata.replace("(","")
                    VPGdata = VPGdata.replace(")","")
                    CSV.write(str(VPGdata)+",")
                    #
                    ## - Second Child Element
                    #
                    for C3 in C2.getchildren():
                        cc=str(C3)
                        s0,s1 = cc.split("}")
                        s0,S1 = s1.split("'")
                        if s0 == "Name":
                            s0 = "VPG-Name"
                        VPGdata=(s0,C3.text)
                        VPGdata = str(VPGdata)
                        VPGdata = VPGdata.replace("(","")
                        VPGdata = VPGdata.replace(")","")
                        CSV.write(str(VPGdata)+",")
                        #
                        ## - Third Child Element
                        #
                        for C4 in C3.getchildren():
                            cc=str(C4)
                            s0,s1 = cc.split("}")
                            s0,S1 = s1.split("'")
                            VPGdata=(s0,C4.text)
                            VPGdata = str(VPGdata)
                            VPGdata = VPGdata.replace("(","")
                            VPGdata = VPGdata.replace(")","")
                            CSV.write(str(VPGdata)+",")
                            #
                            ## - Forth Child Element
                            #
                            for C5 in C4.getchildren():
                                cc=str(C5)
                                s0,s1 = cc.split("}")
                                s0,S1 = s1.split("'")
                                VPGdata=(s0,C5.text)
                                VPGdata = str(VPGdata)
                                VPGdata = VPGdata.replace("(","")
                                VPGdata = VPGdata.replace(")","")
                                CSV.write(str(VPGdata)+",")
                                #
                                ## - Fifth Child Element
                                #
                                for C6 in C5.getchildren():
                                    cc=str(C6)
                                    s0,s1 = cc.split("}")
                                    s0,S1 = s1.split("'")
                                    VPGdata=(s0,C6.text)
                                    VPGdata = str(VPGdata)
                                    VPGdata = VPGdata.replace("(","")
                                    VPGdata = VPGdata.replace(")","")
                                    CSV.write(str(VPGdata)+",")
                                    #
                                    ## - Sixth Child Element
                                    #
                                    for C7 in C6.getchildren():
                                        cc=str(C7)
                                        s0,s1 = cc.split("}")
                                        s0,S1 = s1.split("'")
                                        VPGdata=(s0,C7.text)
                                        VPGdata = str(VPGdata)
                                        VPGdata = VPGdata.replace("(","")
                                        VPGdata = VPGdata.replace(")","")
                                        CSV.write(str(VPGdata)+",")
                                        #
                                        ## - Seventh Child Element
                                        #
                                        for C8 in C7.getchildren():
                                            cc=str(C8)
                                            s0,s1 = cc.split("}")
                                            s0,S1 = s1.split("'")
                                            VPGdata=(s0,C8.text)
                                            VPGdata = str(VPGdata)
                                            VPGdata = VPGdata.replace("(","")
                                            VPGdata = VPGdata.replace(")","")
                                            CSV.write(str(VPGdata)+",")
                                            #
                                            ## - Eighth Child Element
                                            #
                                            for C9 in C8.getchildren():
                                                cc=str(C9)
                                                s0,s1 = cc.split("}")
                                                s0,S1 = s1.split("'")
                                                VPGdata=(s0,C9.text)
                                                VPGdata = str(VPGdata)
                                                VPGdata = VPGdata.replace("(","")
                                                VPGdata = VPGdata.replace(")","")
                                                CSV.write(str(VPGdata)+",")
                                                #
                                                ## - Ninth Child Element
                                                #
                                                for C10 in C9.getchildren():
                                                    cc=str(C10)
                                                    s0,s1 = cc.split("}")
                                                    s0,S1 = s1.split("'")
                                                    VPGdata=(s0,C10.text)
                                                    VPGdata = str(VPGdata)
                                                    VPGdata = VPGdata.replace("(","")
                                                    VPGdata = VPGdata.replace(")","")
                                                    CSV.write(str(VPGdata)+",")
    #
    ## - Close File
    #
    CSV.close()
    print (Script_Name + " Version:" + Script_Version + " " + str(VPGcount).zfill(4),"VPG's processed")
#
## - This sub-routine will generate the XML data in formatted CSV format 
#
def ProcessXMLfile():
    #
    ## - Generate a temp file name
    #
    import tempfile
    global VMFtemp
    VMFtemp = tempfile.NamedTemporaryFile(prefix="vpg")
    #
    ## - import XML Element tree structure
    #
    import xml.etree.ElementTree as ET
    #
    ## - Zerto VPG export XML file
    #
    tree = ET.parse(infile)
    root = tree.getroot()
    #
    ## - Root element
    #
    global VPGdata
    VWF = open(VMFtemp.name,"w+")
    VPGcount=0
    VPGdata=[]
    for S in root.iter("{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value"):
        for C0 in S.getchildren():
            cc=str(C0)
            s0,s1 = cc.split("}")
            s0,S1 = s1.split("'")
            VPGcount+=1
            VPGdata=("VPGN"+str(VPGcount),str(s0),str(C0.text))
            VWF.write(str(VPGdata))
            VWF.write("\n")
            #
            ## - First Child Element
            #
            for C1 in C0.getchildren():
                cc=str(C1)
                s0,s1 = cc.split("}")
                s0,S1 = s1.split("'")
                VPGdata=("VPGN"+str(VPGcount),str(s0),str(C1.text))
                VWF.write(str(VPGdata))
                VWF.write("\n")
                #
                ## - First Child Element
                #
                for C2 in C1.getchildren():
                    cc=str(C2)
                    s0,s1 = cc.split("}")
                    s0,S1 = s1.split("'")
                    VPGdata=("VPGN"+str(VPGcount),str(s0),str(C2.text))
                    VWF.write(str(VPGdata))
                    VWF.write("\n")
                    #
                    ## - Second Child Element
                    #
                    for C3 in C2.getchildren():
                        cc=str(C3)
                        s0,s1 = cc.split("}")
                        s0,S1 = s1.split("'")
                        VPGdata=("VPGN"+str(VPGcount),str(s0),str(C3.text))
                        VWF.write(str(VPGdata))
                        VWF.write("\n")
                        if s0 == "Name":
                            VPGdata = ("VPGN"+str(VPGcount),"VPG-Name=", str(C3.text))
                            VWF.write(str(VPGdata))
                            VWF.write("\n")
                        #
                        ## - Third Child Element
                        #
                        for C4 in C3.getchildren():
                            cc=str(C4)
                            s0,s1 = cc.split("}")
                            s0,S1 = s1.split("'")
                            VPGdata=("VPGN"+str(VPGcount),str(s0),str(C4.text))
                            VWF.write(str(VPGdata))
                            VWF.write("\n")
                            #
                            ## - Forth Child Element
                            #
                            for C5 in C4.getchildren():
                                cc=str(C5)
                                s0,s1 = cc.split("}")
                                s0,S1 = s1.split("'")
                                VPGdata=("VPGN"+str(VPGcount),str(s0),str(C5.text))
                                VWF.write(str(VPGdata))
                                VWF.write("\n")
                                #
                                ## - Fifth Child Element
                                #
                                for C6 in C5.getchildren():
                                    cc=str(C6)
                                    s0,s1 = cc.split("}")
                                    s0,S1 = s1.split("'")
                                    VPGdata=("VPGN"+str(VPGcount),str(s0),str(C6.text))
                                    VWF.write(str(VPGdata))
                                    VWF.write("\n")
                                    #
                                    ## - Sixth Child Element
                                    #
                                    for C7 in C6.getchildren():
                                        cc=str(C7)
                                        s0,s1 = cc.split("}")
                                        s0,S1 = s1.split("'")
                                        VPGdata=("VPGN"+str(VPGcount),str(s0),str(C7.text))
                                        VWF.write(str(VPGdata))
                                        VWF.write("\n")
                                        #
                                        ## - Seventh Child Element
                                        #
                                        for C8 in C7.getchildren():
                                            cc=str(C8)
                                            s0,s1 = cc.split("}")
                                            s0,S1 = s1.split("'")
                                            VPGdata=("VPGN"+str(VPGcount),str(s0),str(C8.text))
                                            VWF.write(str(VPGdata))
                                            VWF.write("\n")
                                            #
                                            ## - Eighth Child Element
                                            #
                                            for C9 in C8.getchildren():
                                                cc=str(C9)
                                                s0,s1 = cc.split("}")
                                                s0,S1 = s1.split("'")
                                                VPGdata=("VPGN"+str(VPGcount),str(s0),str(C9.text))
                                                VWF.write(str(VPGdata))
                                                VWF.write("\n")
                                                #
                                                ## - Ninth Child Element
                                                #
                                                for C10 in C9.getchildren():
                                                    cc=str(C10)
                                                    s0,s1 = cc.split("}")
                                                    s0,S1 = s1.split("'")
                                                    VPGdata=("VPGN"+str(VPGcount),str(s0),str(C10.text))
                                                    VWF.write(str(VPGdata))
                                                    VWF.write("\n")
    #
    ## - Close File 
    #
    VWF.close()
    print (Script_Name + " Version:" + Script_Version + " " + str(VPGcount).zfill(4),"VPG's processed")
#
## - This sub-routine will Process the XML data into a formatted CSV file
#
def ProcessXMLfileCSV():
    #
    ## - Create Array Name
    #
    VPGNameArray = []
    #
    ## - Generate CSV name
    #
    global CSVFileName
    CSVFileName = (str(infile)+".csv")
    CSV = open(CSVFileName,"w")
    #
    ## - Open XML data extra for reading
    #
    VWF = open(VMFtemp.name,"rt")
    VPGDetails = VWF.readlines()
    for VPGlines in VPGDetails:
        VPGnum, VPGfield, FieldDetails = VPGlines.split(",")
        if "VPG-Name" in VPGfield:
            VPGnum = VPGnum.replace("'","")
            VPGnum = VPGnum.replace("(","")
            FieldDetails = FieldDetails.replace("'","")
            VPGAddToArray = (VPGnum+":"+FieldDetails)
            VPGNameArray.append(VPGAddToArray)
    VPGnameToProcess = VPGNameArray
    CSVdata=("VPGname,"+"VPGfield,"+"FieldDetails")
    CSV.write(str(CSVdata))
    CSV.write("\n")
    for VPGnames in VPGnameToProcess:
        global VPGname
        VPGnumToFind, VPGname = VPGnames.split(":")
        VPGname, x = VPGname.split(")")
        VWF.seek(0,0)
        VPGDetails = VWF.readlines()
        for CSVBuild in VPGDetails:
            VPGnum, VPGfield, FieldDetails = CSVBuild.split(",")
            if VPGnumToFind in VPGnum:
                FieldDetails = FieldDetails.replace(")","")
                CSVdata=(VPGname+","+VPGfield+","+FieldDetails)
                if "VPG-Name" not in VPGfield:
                    CSV.write(str(CSVdata))
    #
    ## - Close File
    #
    VWF.close()
#
##
### -- Mainline Processing
##
#
ProcessPARAMETERS()
if RawOrCSV == "CSV":
    ProcessXMLfile()
    ProcessXMLfileCSV()
    print (Script_Name + " Version:" + Script_Version + " CSV filename", CSVFileName, "Created")
else:
    ProcessXMLfileCSVRaw()
    print (Script_Name + " Version:" + Script_Version + " CSV filename", CSVFileName, "Created")
