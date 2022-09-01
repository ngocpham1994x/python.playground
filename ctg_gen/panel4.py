'''
Created on Oct 27, 2016
Create N-1-1 based on two sets of contingencies
@author: dhuang
'''

import os, sys
import io_process as io
from cStringIO import StringIO

exename = sys.executable
p, nx   = os.path.split(exename)
nx      = nx.lower()


#myversion = 32
if nx in ['python.exe', 'pythonw.exe']:
    if "python25" in exename.lower() :  # python 2.5 need to use PSSE32
        myversion = 32
        import wxversion
        wxversion.select("2.8")
        import wx
        import wx.grid as wxgrid
    elif "python27" in exename.lower() : # need to use psse 33
        myversion = 33
        import wx
        import wx.grid as wxgrid
    else:
        pass




class BuildN11Panel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        # layout
        allsizer = wx.BoxSizer(wx.VERTICAL)

        filesizer1 = wx.BoxSizer(wx.HORIZONTAL)
        filesizer2 = wx.BoxSizer(wx.HORIZONTAL)
        filesizer3 = wx.BoxSizer(wx.HORIZONTAL)

        infosizer = wx.BoxSizer(wx.HORIZONTAL)
        info1sizer = wx.BoxSizer(wx.VERTICAL)
        info2sizer = wx.BoxSizer(wx.VERTICAL)
        info3sizer = wx.BoxSizer(wx.VERTICAL)


        # GUI components
        filesizer1.Add(wx.StaticText(self, -1, 'Select 1st .ctg file:'), 0, wx.ALL, 5)
        self.file1Text = wx.TextCtrl(self, -1, "", )
        self.btnSelect1= wx.Button(self, -1, 'Browse', )

        filesizer2.Add(wx.StaticText(self, -1, 'Select 2nd .ctg file:'), 0, wx.ALL, 5)
        self.file2Text = wx.TextCtrl(self, -1, "", )
        self.btnSelect2= wx.Button(self, -1, 'Browse', )        

        filesizer3.Add(wx.StaticText(self, -1, 'Select N-1-1 ctg file:'), 0, wx.ALL, 5)
        self.file3Text = wx.TextCtrl(self, -1, "", )
        self.btnSave= wx.Button(self, -1, 'Save', )

        info1sizer.Add(wx.StaticText(self, -1, "1st Ctg File Information:"), 0, wx.ALL, 5)
        self.info1Text = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE)
        self.sum1Text = wx.TextCtrl(self, -1, "")

        info2sizer.Add(wx.StaticText(self, -1, "2nd Ctg File Information:"), 0, wx.ALL, 5)
        self.info2Text = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE)
        self.sum2Text = wx.TextCtrl(self, -1, "")

        info3sizer.Add(wx.StaticText(self, -1, "N-1-1 Ctg File Information:"), 0, wx.ALL, 5)
        self.info3Text = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE)
        self.sum3Text = wx.TextCtrl(self, -1, "")

        self.btnBuild = wx.Button(self, -1, "Build N-1-1" )


        # layout
        filesizer1.Add(self.file1Text, 1, wx.ALL|wx.EXPAND, 5)
        filesizer1.Add(self.btnSelect1, 0, wx.ALL, 5)

        filesizer2.Add(self.file2Text, 1, wx.ALL|wx.EXPAND, 5)
        filesizer2.Add(self.btnSelect2, 0, wx.ALL, 5)

        filesizer3.Add(self.file3Text, 1, wx.ALL|wx.EXPAND, 5)
        filesizer3.Add(self.btnSave, 0, wx.ALL, 5)


        info1sizer.Add(self.sum1Text, 0, wx.ALL|wx.EXPAND, 5)
        info1sizer.Add(self.info1Text, 1, wx.ALL|wx.EXPAND, 5)

        info2sizer.Add(self.sum2Text, 0, wx.ALL|wx.EXPAND, 5)
        info2sizer.Add(self.info2Text, 1, wx.ALL|wx.EXPAND, 5)

        info3sizer.Add(self.sum3Text, 0, wx.ALL|wx.EXPAND, 5)
        info3sizer.Add(self.info3Text, 1, wx.ALL|wx.EXPAND, 5)

        infosizer.Add(info1sizer, 1, wx.ALL|wx.EXPAND, 5)
        infosizer.Add(info2sizer, 1, wx.ALL|wx.EXPAND, 5)
        infosizer.Add(info3sizer, 1, wx.ALL|wx.EXPAND, 5)


        allsizer.Add(filesizer1, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(filesizer2, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(infosizer, 1, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(filesizer3, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.btnBuild, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.SetSizerAndFit(allsizer)


        # button binding
        self.Bind(wx.EVT_BUTTON, self.onSelect1, self.btnSelect1)
        self.Bind(wx.EVT_BUTTON, self.onSelect2, self.btnSelect2)
        self.Bind(wx.EVT_BUTTON, self.onSave, self.btnSave)
        self.Bind(wx.EVT_BUTTON, self.onBuildN11, self.btnBuild)


    def onBuildN11(self, evt):
        file1 = self.file1Text.GetValue().strip()
        file2 = self.file2Text.GetValue().strip()
        if file1 == "" or file2 == "":
            wx.MessageBox("Please select two contingency files!", "Info", wx.OK)
            return
        
        ctgnm1, ctgs1 = readctgs(file1, [])
        ctgnm2, ctgs2 = readctgs(file2, [])
        ctgN11, ctgnm, ctgs= buildN11ctg(ctgnm1, ctgs1, ctgnm2, ctgs2)
        
        self.info3Text.SetValue(ctgN11)
        self.sum3Text.SetValue("Total # of Ctgs: " + str(len(ctgnm)))
        
        pass

    def onSelect1(self, evt):
        filePath = io.browseFile(self, '*.ctg')
        self.file1Text.SetValue(filePath)

        # read file and list information
        readfile = file(self.file1Text.GetValue().strip())
        ctgs = readfile.read()
        readfile.close()
        self.info1Text.SetValue(ctgs)

        ctgnm1, ctgs1 = readctgs(self.file1Text.GetValue().strip(), [])
        self.sum1Text.SetValue("Total # of Ctgs: " + str(len(ctgnm1)))

    def onSelect2(self, evt):
        filePath = io.browseFile(self, '*.ctg')
        self.file2Text.SetValue(filePath)

        readfile = file(self.file2Text.GetValue().strip())
        ctgs = readfile.read()
        readfile.close()
        self.info2Text.SetValue(ctgs)
        
        ctgnm1, ctgs1 = readctgs(self.file2Text.GetValue().strip(), [])
        self.sum2Text.SetValue("Total # of Ctgs: " + str(len(ctgnm1)))

    # select a file to save the built N-1-1 ctg file
    def onSave(self, evt):
        if self.info3Text.GetValue().strip() == "":
            wx.MessageBox("There is no contingency to be saved!", "Info", wx.OK)
            return
        
        filePath = io.browseFile(self, '*.ctg')
        self.file3Text.SetValue(filePath)

        if self.file3Text.GetValue().strip() <> "":
            if self.info3Text.GetValue().strip() <> "":
                io.save(self.file3Text.GetValue(), self.info3Text.GetValue())
            else:
                pass
        else:
            wx.MessageBox("Please select a ctg file to save!", "Info", wx.OK)
            return

    def onExit(self, evt):
        #print 'nx, psseon', nx, PSSEon
        self.Close()


def buildN11ctg(ctgnm, outbranches, ctgnm2, outbranches2):
    print "Combining contingencies..."
    newctgnm=[]
    newoutbrch = []

    for i in range(len(ctgnm)):
        for j in range(len(ctgnm2)):
            if ctgnm[i].strip() <> ctgnm2[j].strip():
                if (ctgnm2[j]+"&"+ctgnm[i] not in newctgnm) and ctgnm[i]+"&"  +ctgnm2[j] not in newctgnm:
                    newname = ctgnm[i]+"&"  +ctgnm2[j]
                    newbrch = outbranches[i] + outbranches2[j]
                    newctgnm.append(newname)
                    newoutbrch.append(newbrch)


    file_str = StringIO()
    file_str.write("[VSAT 9.X Contingency]\n")
    file_str.write("\n")

    for i in range(len(newctgnm)):
        file_str.write("{Contingency}\n")
        file_str.write("  Contingency name = '" + newctgnm[i] + "'\n")
        for onebrch in newoutbrch[i]:
            file_str.write(onebrch + "\n")
        file_str.write("{End contingency}\n")
         
    file_str.write( "[End]")
    
    print "There are in total ", len(newctgnm) , " N-1-1 contingencies."

    return file_str.getvalue(), newctgnm, newoutbrch

# read from a file the ctg name and outage branches.
def readctgs(ctgfile, excludectgs):
    #print "Read CAT-B contingency file..."
    ctgnm = []
    outbranches = []
    # when reading contingency information ,
    # rule out those contingencies that don't run
    readfile = file(ctgfile)
    alllines = readfile.read().splitlines()
    readfile.close()
    startcount = 0   # this flag is used to see if the reading of a contingency shall start  
    for oneline in alllines:
        if oneline.lower().startswith("{contingency")  : # that's the start of a contingency
            if "don't run" in oneline.lower():  # this contingency will not be counted
                startcount = 0
                pass
            else:
                excludeflag = 0
                curoutbrch = []
                startcount = 1
        elif oneline.lower().startswith("{end contingency}"):
            if (startcount == 1 and excludeflag ==0):  # this is to rule out the don't run contingencies
                outbranches.append(curoutbrch)
                startcount = 0
                excludeflag = 0
        else:
            if startcount ==1 :  # this is a valid contingency
                if oneline.strip().lower().startswith("contingency name") : # read the name of a contingency
                    tempnm = oneline.split("=")
                    tempnm = tempnm[1]
                    tempnm = tempnm.split("'")
                    tempnm= tempnm[1]
                    # see if the contingency shall be excluded
                    for oneexclude in excludectgs:
                        if oneexclude.strip().lower() == tempnm.strip().lower():
                            print tempnm
                            excludeflag = 1
                            break
                            # this congitn
                    if excludeflag == 0:
                        ctgnm.append(tempnm)
                else :  # this is the outage branch information or outage buses...
                    if excludeflag == 0:
                        curoutbrch.append(oneline)

    print "There are in total " + str(len(ctgnm)) + " contingencies."
    for i in range(len(ctgnm)):
        print ctgnm[i], outbranches[i] 



    return ctgnm, outbranches

