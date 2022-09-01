import psspy
import os, sys
import csv
import pandas as pd
import io_process as io
import panel1

# check wx version
try:
    import wxversion
    wxversion.select("3.0")
    import wx
    import wx.grid as wxgrid
    from wx.lib.pubsub import pub 
except ImportError:
    raise ImportError('wx module cannot be found!!!')



class NameChangePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        allsizer = wx.BoxSizer(wx.VERTICAL)
        outputsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.caseName = ''
        self.lineFile = ''
        self.xfmFile = ''
        self.explicitFile = ''

        pub.subscribe(self.listener, "paths")

        # GUI components
        self.note = wx.StaticText(self, -1, "Order of replacing PSSE names: \n"
                                            "\tstandard asset names\n"
                                            "\treplace PSSE names with names of IDENTIFIERS found-in-FRS\n"
                                            "\treplace PSSE names with names in explicit changes file\n\n"
                                            "**Errors could occur due to duplicated NAMES.\n"
                                            "**Errors could occur due to the asset to replace name is not in the current case (but could be in future cases).\n"
                                            "**Run the REPLACE button twice to clear errors.\n\n"
                                            "**CAUTION: Case will be overwritten!")

        self.btnReplace = wx.Button(self, -1, "Replace")

        self.outputText = wx.StaticText(self, -1, "Choose location for LineBus output files")
        self.outputPath = wx.TextCtrl(self, -1, "")
        self.btnBrowse = wx.Button(self, -1, "Browse")
        self.btnExportCSV = wx.Button(self, -1, "Export .csv")

        self.infoText = wx.TextCtrl(self, -1, "", style=wx.MULTIPLE)

        # layouts
        outputsizer.Add(self.outputText, 1, wx.ALL, 5)
        outputsizer.Add(self.outputPath,  1, wx.ALL, 5)
        outputsizer.Add(self.btnBrowse,  0, wx.ALL, 5)
        outputsizer.Add(self.btnExportCSV,  0, wx.ALL, 5)

        allsizer.Add(self.note, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.btnReplace, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        allsizer.Add(outputsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.infoText, 1, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizerAndFit(allsizer)

        # button binding
        self.Bind(wx.EVT_BUTTON, self.onReplace, self.btnReplace)
        self.Bind(wx.EVT_BUTTON, self.onBrowse, self.btnBrowse)
        self.Bind(wx.EVT_BUTTON, self.onExportCSV, self.btnExportCSV)

    # button methods
    def onBrowse(self, event):
        folder = io.browseFolder(self)
        self.outputPath.SetValue(folder)

        if not folder:
            wx.MessageBox("No folder selected. Please check!", "Info", wx.OK)

    def onReplace(self, evt):
        answer = wx.MessageBox("Case will be overwritten!", "Warning", wx.OK|wx.CANCEL)

        info = ''

        if answer == wx.OK:
            if os.path.exists(self.explicitFile) and os.path.exists(self.caseName) and os.path.exists(self.lineFile) and os.path.exists(self.xfmFile):
                lineException, xfm2WException, xfm3WException = io.readException_woIgnore(self.explicitFile)

                lineCommon, lineFrsDuplicates, linePsseNotInFrs = panel1.compareLine(self.caseName, self.lineFile)
                xfm2WCommon, xfm2WFrsDuplicates, xfm2WPsseNotInFrs = panel1.compare2Windings(self.caseName, self.xfmFile)
                xfm3WCommon, xfm3WFrsDuplicates, xfm3WPsseNotInFrs = panel1.compare3Windings(self.caseName, self.xfmFile)

                info = info + '\n'
                # replace PSSE names with PSSE not found in FRS (conventionalize the name)
                info = info + self.replaceName ('line', linePsseNotInFrs, 'standard names')
                # replace PSSE names with FRS names 
                info = info + self.replaceName ('line', lineCommon, 'FRS') 
                # replace PSSE names with Explicit file
                info = info + self.replaceName ('line', lineException, 'exception') 

                info = info + '\n'
                info = info + self.replaceName ('2W', xfm2WPsseNotInFrs, 'standard names')
                info = info + self.replaceName ('2W', xfm2WCommon, 'FRS')
                info = info + self.replaceName ('2W', xfm2WException, 'exception')

                info = info + '\n'
                info = info + self.replaceName ('3W', xfm3WPsseNotInFrs, 'standard names')
                info = info + self.replaceName ('3W', xfm3WCommon, 'FRS')
                info = info + self.replaceName ('3W', xfm3WException, 'exception')


                info = info + '\n================================================================\n\n'
                info = info + '\nSee detailed error messages in command prompt window.\n'
                info = info + '\nNames are replaced. \nCase saved in file: ' + self.caseName

            else:
                wx.MessageBox("No Case file or Explicit file selected. \n"
                                "No FRS line or FRS xfm in Downloads folder. \n"
                                "Case has not been compared before replacement. \n"
                                "Please check!", "Info", wx.OK)


        self.infoText.SetValue(info)

    def onExportCSV(self, evt):
        info = ''

        explicitFile = self.explicitFile

        if explicitFile and os.path.exists(self.caseName) and (self.outputPath.GetValue()):

            psseLineIdentifier, psseLineInfo = io.createPsseLine (self.caseName, True, io.lineVoltage, ties=io.lineTies)
            psse2WIdentifier, psse2WInfo = io.createPsse2W(self.caseName, True, io.xfm2wVoltage, ties=io.xfm2wTies)
            psse3WIdentifier, psse3WInfo = io.createPsse3W(self.caseName, True, io.xfm3wVoltage, ties=io.xfm3wTies)

            info = info + self.printListInfo(psseLineInfo)
            info = info + self.printListInfo(psse2WInfo)
            info = info + self.printListInfo(psse3WInfo)

            root, case = io.separateFilePath(self.caseName)
            output = self.outputPath.GetValue() + '\\' + case + io.linebusCsv
            io.save (output, info)

        else:
            wx.MessageBox("No Explicit file or Case or Output folder selected.\n"
                            "Case has not been compared before replacement.\n"
                            "Please check!", "Info", wx.OK)

        self.infoText.SetValue(info)

    def replaceName(self, category, newNameList, listName):
        info = 'Replacing ' + category + ' names in the case with ' + listName + '\n'
        ierr = 0

        for i, item in enumerate(newNameList):
            name = item['name'].replace(' ', '_')
            buses, cct = io.separateIdentifier(item['identifier'])
            if category == 'line':
                ierr = psspy.branch_chng_3(buses[0],buses[1],cct, namear= name)
            elif category == '2W':
                ierr, realaro = psspy.two_winding_chng_6(buses[0],buses[1],cct, namear= name)
            elif category == '3W':
                ierr, realaro = psspy.three_wnd_imped_chng_4(buses[0],buses[1],buses[2],cct, namear= name)
            
            if ierr != 0:
                info = info + '\tError occurred when trying to replace: ' + io.idToString(item['identifier']) + ' to have name defined in ' + listName + ' as    ' + item['name'] + '\n'

        psspy.save(self.caseName)

        return info

    def printListInfo(self, listInfo):
        info = ''

        for item in listInfo:
            buses, cct = io.separateIdentifier(item['identifier'])
            info = info + item['name'] + ',' + ','.join(str(e) for e in buses) + ',' + cct + '\n'

        return info

    def listener(self, message1, message2=None, message3=None, message4=None):
        self.caseName = message1
        self.lineFile = message2
        self.xfmFile = message3
        self.explicitFile = message4

