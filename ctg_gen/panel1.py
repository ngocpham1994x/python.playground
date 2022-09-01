import os, sys
import webbrowser
import io_process as io
import pandas as pd

# check wx version
try:
    import wxversion
    wxversion.select("3.0")
    import wx
    import wx.grid as wxgrid
    from wx.lib.pubsub import pub 
except ImportError:
    raise ImportError('wx module cannot be found!!!')


class ComparisonPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # layout
        allsizer = wx.BoxSizer(wx.VERTICAL)
        savsizer = wx.BoxSizer(wx.HORIZONTAL)
        subsyssizer = wx.BoxSizer(wx.HORIZONTAL)
        sublinesizer = wx.BoxSizer(wx.VERTICAL)
        sub2wsizer = wx.BoxSizer(wx.VERTICAL)
        sub3wsizer = wx.BoxSizer(wx.VERTICAL)
        tempsizer = wx.BoxSizer(wx.VERTICAL)
        linecsvsizer = wx.BoxSizer(wx.HORIZONTAL)
        xfmcsvsizer = wx.BoxSizer(wx.HORIZONTAL)
        filesizer = wx.BoxSizer(wx.HORIZONTAL)
        resultsizer = wx.BoxSizer(wx.VERTICAL)

        # GUI components
        self.savText = wx.StaticText(self, -1, "Select .sav file")
        self.savPath = wx.TextCtrl(self, -1, "")
        self.btnBrowse1 = wx.Button(self, -1, "Browse")

        subsyssizer.Add(wx.StaticText(self, -1, "Define subsystems (if changed, click SET):"))
        self.text1 = wx.StaticText(self, -1, "Voltage range:")
        self.text2 = wx.StaticText(self, -1, "Ties (1: not included, 3: included):")
        self.btnSet = wx.Button(self, -1, "SET")

        self.sublineText = wx.StaticText(self, -1, "AC lines:")
        self.sublineVoltage = wx.TextCtrl(self, -1, str(io.lineVoltage))
        self.sublineTies = wx.TextCtrl(self, -1, str(io.lineTies))

        self.sub2wText = wx.StaticText(self, -1, "2-winding transformers:")
        self.sub2wVoltage = wx.TextCtrl(self, -1, str(io.xfm2wVoltage))
        self.sub2wTies = wx.TextCtrl(self, -1, str(io.xfm2wTies))

        self.sub3wText = wx.StaticText(self, -1, "3-winding transformers:")
        self.sub3wVoltage = wx.TextCtrl(self, -1, str(io.xfm3wVoltage))
        self.sub3wTies = wx.TextCtrl(self, -1, str(io.xfm3wTies))

        self.lineText = wx.StaticText(self, -1, "Input URL for lines")
        self.lineURL = wx.TextCtrl(self, -1, io.lineDownloadLink)
        self.btnDownloadLine = wx.Button(self, -1, "Download")
        
        self.xfmText = wx.StaticText(self, -1, "Input URL for transformers")
        self.xfmURL = wx.TextCtrl(self, -1, io.xfmDownloadLink)
        self.btnDownloadXfm = wx.Button(self, -1, "Download")

        self.fileText = wx.StaticText(self, -1, "Select Exception List file")
        self.filePath = wx.TextCtrl(self, -1, "")
        self.btnBrowse2 = wx.Button(self, -1, "Browse")

        self.btnCompare = wx.Button(self, -1, "Compare")


        # GUI result components
        self.resultText = wx.StaticText(self, -1, "**The comparison is based on IDENTIFIERS (bus1, bus2, bus3, cct) "
                                                    "between case and FRS. \n\n" 
                                                    "Warnings:\n")
        self.resultNb = wx.Notebook(self, -1)

        # GUI result panel 1
        self.pn1 = wx.Panel(self.resultNb)
        self.pn1.BackgroundColour = parent.GetBackgroundColour()
        
        self.pn1sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pn1subsizer = wx.BoxSizer(wx.VERTICAL)

        self.pn1Text = wx.StaticText(self.pn1, -1, "The following PSSE identifiers are not found in FRS: ")
        self.pn1PsseNotFrs = wx.CheckListBox(self.pn1, -1, choices=[])
        self.pn1Dup = wx.TextCtrl(self.pn1, -1, "", style = wx.MULTIPLE)

        self.pn1subsizer.Add(self.pn1Text, 0, wx.ALL|wx.EXPAND,5)
        self.pn1subsizer.Add(self.pn1PsseNotFrs, 1, wx.ALL|wx.EXPAND,5)

        self.pn1sizer.Add(self.pn1subsizer, 1, wx.ALL|wx.EXPAND,5)
        self.pn1sizer.Add(self.pn1Dup, 1, wx.ALL|wx.EXPAND,5)

        self.pn1.SetSizerAndFit(self.pn1sizer)

        # GUI result panel 2
        self.pn2 = wx.Panel(self.resultNb)
        self.pn2.BackgroundColour = parent.GetBackgroundColour()
        
        self.pn2sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pn2subsizer = wx.BoxSizer(wx.VERTICAL)

        self.pn2Text = wx.StaticText(self.pn2, -1, "The following PSSE identifiers are not found in FRS: ")
        self.pn2PsseNotFrs = wx.CheckListBox(self.pn2, -1, choices=[])
        self.pn2Dup = wx.TextCtrl(self.pn2, -1, "", style = wx.MULTIPLE)

        self.pn2subsizer.Add(self.pn2Text, 0, wx.ALL|wx.EXPAND,5)
        self.pn2subsizer.Add(self.pn2PsseNotFrs, 1, wx.ALL|wx.EXPAND,5)

        self.pn2sizer.Add(self.pn2subsizer, 1, wx.ALL|wx.EXPAND,5)
        self.pn2sizer.Add(self.pn2Dup, 1, wx.ALL|wx.EXPAND,5)

        self.pn2.SetSizerAndFit(self.pn2sizer)

        # GUI result panel 3
        self.pn3 = wx.Panel(self.resultNb)
        self.pn3.BackgroundColour = parent.GetBackgroundColour()
        
        self.pn3sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pn3subsizer = wx.BoxSizer(wx.VERTICAL)

        self.pn3Text = wx.StaticText(self.pn3, -1, "The following PSSE identifiers are not found in FRS: ")
        self.pn3PsseNotFrs = wx.CheckListBox(self.pn3, -1, choices=[])
        self.pn3Dup = wx.TextCtrl(self.pn3, -1, "", style = wx.MULTIPLE)

        self.pn3subsizer.Add(self.pn3Text, 0, wx.ALL|wx.EXPAND,5)
        self.pn3subsizer.Add(self.pn3PsseNotFrs, 1, wx.ALL|wx.EXPAND,5)

        self.pn3sizer.Add(self.pn3subsizer, 1, wx.ALL|wx.EXPAND,5)
        self.pn3sizer.Add(self.pn3Dup, 1, wx.ALL|wx.EXPAND,5)

        self.pn3.SetSizerAndFit(self.pn3sizer)

        # GUI result panel adding pages
        self.resultNb.AddPage(self.pn1, "AC Lines")
        self.resultNb.AddPage(self.pn2, "Transformer 2-winding")
        self.resultNb.AddPage(self.pn3, "Transformer 3-winding")

        # layout
        savsizer.Add(self.savText, 1, wx.ALL, 5)
        savsizer.Add(self.savPath,  1, wx.ALL, 5)
        savsizer.Add(self.btnBrowse1,  0, wx.ALL, 5)

        tempsizer.Add(wx.StaticText(self, -1, "\n"))
        tempsizer.Add(self.text1, 1, wx.ALL, 5)
        tempsizer.Add(self.text2, 1, wx.ALL, 5)

        sublinesizer.Add(self.sublineText, 1, wx.ALL, 5)
        sublinesizer.Add(self.sublineVoltage, 1, wx.ALL, 5)
        sublinesizer.Add(self.sublineTies, 1, wx.ALL, 5)

        sub2wsizer.Add(self.sub2wText, 1, wx.ALL, 5)
        sub2wsizer.Add(self.sub2wVoltage, 1, wx.ALL, 5)
        sub2wsizer.Add(self.sub2wTies, 1, wx.ALL, 5)

        sub3wsizer.Add(self.sub3wText, 1, wx.ALL, 5)
        sub3wsizer.Add(self.sub3wVoltage, 1, wx.ALL, 5)
        sub3wsizer.Add(self.sub3wTies, 1, wx.ALL, 5)

        linecsvsizer.Add(self.lineText, 1, wx.ALL, 5)
        linecsvsizer.Add(self.lineURL, 1, wx.ALL, 5)
        linecsvsizer.Add(self.btnDownloadLine, 0, wx.ALL, 5)

        xfmcsvsizer.Add(self.xfmText, 1, wx.ALL, 5)
        xfmcsvsizer.Add(self.xfmURL, 1, wx.ALL, 5)
        xfmcsvsizer.Add(self.btnDownloadXfm, 0, wx.ALL, 5)

        filesizer.Add(self.fileText, 1, wx.ALL, 5)
        filesizer.Add(self.filePath, 1, wx.ALL, 5)
        filesizer.Add(self.btnBrowse2, 0, wx.ALL, 5)

        resultsizer.Add(self.resultText, 0, wx.ALL, 5)
        resultsizer.Add(self.resultNb, 1, wx.ALL|wx.EXPAND, 5)

        subsyssizer.Add(tempsizer, 1, wx.ALL|wx.EXPAND, 5)
        subsyssizer.Add(sublinesizer, 1, wx.ALL|wx.EXPAND, 5)
        subsyssizer.Add(sub2wsizer, 1, wx.ALL|wx.EXPAND, 5)
        subsyssizer.Add(sub3wsizer, 1, wx.ALL|wx.EXPAND, 5)
        subsyssizer.Add(self.btnSet, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        allsizer.Add(savsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(subsyssizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(linecsvsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(xfmcsvsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(filesizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.btnCompare, 0,  wx.ALL|wx.ALIGN_CENTER, 5)
        allsizer.Add(resultsizer, 1, wx.ALL|wx.EXPAND, 5)

        self.SetSizerAndFit(allsizer)

        # button binding
        self.Bind(wx.EVT_BUTTON, self.onBrowse1, self.btnBrowse1)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onDownload (evt, 'line'), self.btnDownloadLine)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onDownload (evt, 'xfm'), self.btnDownloadXfm)
        self.Bind(wx.EVT_BUTTON, self.onBrowse2, self.btnBrowse2)
        self.Bind(wx.EVT_BUTTON, self.onCompare, self.btnCompare)
        self.Bind(wx.EVT_BUTTON, self.onSetSubsys, self.btnSet)

        #
        self.username = os.getenv("username")
        self.lineFile = os.path.join("C:\\Users", self.username, "Downloads\\ApiPsseLineSegment.csv")
        self.xfmFile = os.path.join("C:\\Users", self.username, "Downloads\\ApiPsseTransformer.csv")
        # self.sendPath()


    # button methods
    def onBrowse1(self, evt):
        savFilePath = io.browseFile(self, '*.sav')
        self.savPath.SetValue(savFilePath)

        if not savFilePath:
            wx.MessageBox("No .sav file selected. Please check!", "Info", wx.OK)

    def onBrowse2(self, evt):
        path = io.browseFile(self, '*.csv')
        self.filePath.SetValue(path)

        if not path:
            wx.MessageBox("No .csv file selected. Please check!", "Info", wx.OK)

    def onSetSubsys(self, evt):
        io.lineVoltage = list(io.stringToKv(self.sublineVoltage.GetValue()))
        io.xfm2wVoltage = list(io.stringToKv(self.sub2wVoltage.GetValue()))
        io.xfm3wVoltage = list(io.stringToKv(self.sub3wVoltage.GetValue()))

        # 1 = not-included, 3 = included
        io.lineTies = pd.to_numeric(self.sublineTies.GetValue())
        io.xfm2wTies = pd.to_numeric(self.sub2wTies.GetValue())
        io.xfm3wTies = pd.to_numeric(self.sub3wTies.GetValue())

    def onDownload(self, evt, category):
        if category == 'line':
            filePath = os.path.join("C:\\Users", self.username, "Downloads\\ApiPsseLineSegment.csv")
            url = self.lineURL.GetValue()
        elif category == 'xfm':
            filePath = os.path.join("C:\\Users", self.username, "Downloads\\ApiPsseTransformer.csv")
            url = self.xfmURL.GetValue()

        # download .csv and ensure only latest file exist in \Downloads folder
        if url:
            if os.path.exists(filePath):
                os.remove(filePath)
                webbrowser.open(url, new = 2)
            else:
                webbrowser.open(url, new = 2)
        else:
            self.pn1.SetValue("No URL for downloading FRS branch or transformer info! Please check!\n")

    def onCompare(self, evt):
        # print information as string in textbox
        infoPn1 = ''
        infoPn2 = ''
        infoPn3 = ''

        caseName = self.savPath.GetValue()
        exceptionFile = self.filePath.GetValue()

        if caseName and exceptionFile and os.path.exists(self.lineFile) and os.path.exists(self.xfmFile):
            self.sendPath()

            lineException, xfm2WException, xfm3WException = io.readException_wIgnore(exceptionFile)

            lineCommon, lineFrsDuplicates, linePsseNotInFrs = compareLine(caseName, self.lineFile)
            xfm2WCommon, xfm2WFrsDuplicates, xfm2WPsseNotInFrs = compare2Windings(caseName, self.xfmFile)
            xfm3WCommon, xfm3WFrsDuplicates, xfm3WPsseNotInFrs = compare3Windings(caseName, self.xfmFile)

            linePsseNotInFrs_string, linePsseNotInException_index = cmpLine(linePsseNotInFrs, lineException)
            xfm2WPsseNotInFrs_string, xfm2WPsseNotInException_index = cmpXfm2W(xfm2WPsseNotInFrs, xfm2WException)
            xfm3WPsseNotInFrs_string, xfm3WPsseNotInException_index = cmpXfm3W(xfm3WPsseNotInFrs, xfm3WException)

            infoPn1 = self.printDups (infoPn1, lineFrsDuplicates)
            infoPn2 = self.printDups (infoPn2, xfm2WFrsDuplicates)
            infoPn3 = self.printDups (infoPn3, xfm3WFrsDuplicates)

        else:
            wx.MessageBox("No .sav case selected, or\n"
                            "No .csv of line, transformer in \Downloads folder. \n"
                            "Please check!", "Info", wx.OK)


        self.pn1PsseNotFrs.SetItems(linePsseNotInFrs_string)
        self.pn1PsseNotFrs.SetChecked(linePsseNotInException_index)
        self.pn1Dup.SetValue(infoPn1)

        self.pn2PsseNotFrs.SetItems(xfm2WPsseNotInFrs_string)
        self.pn2PsseNotFrs.SetChecked(xfm2WPsseNotInException_index)
        self.pn2Dup.SetValue(infoPn2)

        self.pn3PsseNotFrs.SetItems(xfm3WPsseNotInFrs_string)
        self.pn3PsseNotFrs.SetChecked(xfm3WPsseNotInException_index)
        self.pn3Dup.SetValue(infoPn3)

    def printDups(self, infoPn, FrsDuplicates):
        infoPn = ''

        for i, oneidentifier in enumerate(FrsDuplicates):
            infoPn = infoPn + '  The following PSSE identifier is found in FRS and has duplicates: \n'
            for j, oneduplicate in enumerate(oneidentifier):
                infoPn = infoPn + io.idToString(oneduplicate['identifier']) + oneduplicate['name'] + '\n'


        return infoPn

    # send paths
    def sendPath(self):
        pub.sendMessage("paths", message1=self.savPath.GetValue(), message2=self.lineFile, message3=self.xfmFile, message4=self.filePath.GetValue())


# ------------------- case .sav vs .csv files -------------------
def compareLine(caseName, lineFile):
    psseLine = []       # [{bus1, bus2, cct}]
    psseLineInfo = []     # [{'name': BE1:1, 'identifier': {bus1, bus2, cct}}]
    psseLine, psseLineInfo = io.createPsseLine(caseName, True, io.lineVoltage, ties=io.lineTies)

    frsLine = []
    frsLineInfo = []
    frsLine, frsLineInfo = io.createFrsLine(lineFile)
    
    lineCommon = []         # [{'name': BE1:1, 'identifier': {bus1, bus2, cct}
    lineFrsDuplicates = []  # [{'name': BE1:1, 'identifier': {bus1, bus2, cct
    linePsseNotInFrs = []   # [{'name': BE1:1, 'identifier': {bus1, bus2, cct}

    # Senario 1: PSSE lines are found in FRS (lines are in both PSSE and FRS).
    # Action:
    # One PSSE line could match multiple name(s) in FRS. 
    #   Overwrite name by adding to Exception List.
    lineCommon_identifier = [line for line in psseLine if line in frsLine]   # [{bus1, bus2, cct}]

    # find duplicates in FRS, and 
    # add detailed info to common list (identifier & name)
    for i, oneline in enumerate(lineCommon_identifier):
        matches = []
        for line in frsLineInfo:
            result = oneline.intersection(line['identifier'])
            if len(result) == 3:    # found common identifiers
                matches.append(line)

                '''
                if intersects, add to common list. Correction (of duplicates) will be done in Exeption list.
                below code saying:
                    if so far that line hasn't been identified in the common list, then append. FRS name is used.
                    if so far that line has been identified in the common list, don't append. 
                    This to prevent duplicated identifier appended to common list.'''
                if not any(lineCommonInfo['identifier'] == line['identifier'] for lineCommonInfo in lineCommon): 
                    lineCommon.append(line)

        # add to list of duplicates to print on warning screen
        if len(matches) >= 2:
            lineFrsDuplicates.append(matches)


    # Senario 2: FRS lines are not in PSSE lines 
    # Action: 
    # Analyze case by case basis.
    #   If line is needed to be in PSSE, add to Exception List.
    #   If line is not needed to be in PSSE, email Model Group, or ignore.
    linePsseNotInFrs_index = [index for index, line in enumerate(psseLine) if line not in frsLine]

    for index in linePsseNotInFrs_index:
        line = psseLineInfo[index]
        line['name'] = line['name'].replace('-',':').replace(' ', '_')
        linePsseNotInFrs.append(line)

    print "length psseLine: ", len(psseLine)
    print "length frsLine: ", len(frsLine)
    print "length lineCommon: ", len(lineCommon)
    print "length linePsseNotInFrs: ", len(linePsseNotInFrs)

    return lineCommon, lineFrsDuplicates, linePsseNotInFrs

def compare2Windings(caseName, xfmFile):
    psse2W = []
    psse2WInfo = []
    psse2W, psse2WInfo = io.createPsse2W(caseName, True, io.xfm2wVoltage, ties=io.xfm2wTies)

    frs2W = []
    frs2WInfo = []
    frs2W, frs2WInfo = io.createFrs2W(xfmFile)

    xfm2WCommon = []
    xfm2WFrsDuplicates = []
    xfm2WPsseNotInFrs = []

    # Scenario 1: PSSE's 2-winding (s) are in FRS
    # duplicates will be printed on warning screen
    xfm2WCommon_identifier = [bank for bank in psse2W if bank in frs2W]
    
    for i, onebank in enumerate(xfm2WCommon_identifier):
        matches = []
        for bank in frs2WInfo:
            result = onebank.intersection(bank['identifier'])
            if len(result) == 3:
                matches.append(bank)

                # if not exist in common list, then add.
                # if exist, do nothing. Correction will be done in Exeption list.
                if not any(bankCommon['identifier'] == bank['identifier'] for bankCommon in xfm2WCommon):
                    xfm2WCommon.append(bank)
        
        # add to list of duplicates to print on warning screen
        if len(matches) >= 2:
            xfm2WFrsDuplicates.append(matches)

    # Scenario 2: PSSE's 2-winding (s) are not in FRS
    # list of 'not-found' will be printed on warning screen
    xfm2WPsseNotInFrs_index = [index for index, bank in enumerate(psse2W) if bank not in frs2W]
    
    for index in xfm2WPsseNotInFrs_index:
        bank = psse2WInfo[index]
        bank['name'] = bank['name'].replace(' ', '_')
        xfm2WPsseNotInFrs.append(bank)
    
    print "length psse2W: ", len(psse2W)
    print "length frs2W: ", len(frs2W)
    print "length xfm2WCommon: ", len(xfm2WCommon)
    print "length xfm2WPsseNotInFRS: ", len(xfm2WPsseNotInFrs)


    return xfm2WCommon, xfm2WFrsDuplicates, xfm2WPsseNotInFrs

def compare3Windings(caseName, xfmFile):
    psse3W = []
    psse3WInfo = []
    psse3W, psse3WInfo = io.createPsse3W(caseName, True, io.xfm3wVoltage, ties=io.xfm3wTies)
    
    frs3W = []
    frs3WInfo = []
    frs3W, frs3WInfo = io.createFrs3W(xfmFile)

    xfm3WCommon = []
    xfm3WFrsDuplicates = []
    xfm3WPsseNotInFrs = []

    # Scenario 1: PSSE's 2-winding (s) are in FRS
    # duplicates will be printed on warning screen
    xfm3WCommon_identifier = [bank for bank in psse3W if bank in frs3W]

    for i, onebank in enumerate(xfm3WCommon_identifier):
        matches = []
        for bank in frs3WInfo:
            result = onebank.intersection(bank['identifier'])
            if len(result) == 4:
                matches.append(bank)

                # if not exist in common list, then add.
                # if exist, do nothing. Correction will be done in Exeption list.
                if not any(bankCommon['identifier'] == bank['identifier'] for bankCommon in xfm3WCommon):
                    xfm3WCommon.append(bank)
                
        # add to list of duplicates to print on warning screen
        if len(matches) >= 2:
            xfm3WFrsDuplicates.append(matches)

    # Scenario 2: PSSE's 2-winding (s) are not in FRS
    # list of 'not-found' will be printed on warning screen
    xfm3WPsseNotInFrs_index = [index for index, bank in enumerate(psse3W) if bank not in frs3W]
    
    for index in xfm3WPsseNotInFrs_index:
        bank = psse3WInfo[index]
        bank['name'] = bank['name'].replace(' ', '_')
        xfm3WPsseNotInFrs.append(bank)

    print "length psse3W: ", len(psse3W)
    print "length frs3W: ", len(frs3W)
    print "length xfm3WCommon: ", len(xfm3WCommon)
    print "length xfm3WPsseNotInFRS: ", len(xfm3WPsseNotInFrs)

    return xfm3WCommon, xfm3WFrsDuplicates, xfm3WPsseNotInFrs

# ------------------- not in FRS vs exception -------------------
def cmpLine(linePsseNotInFrs, lineException):
    linePsseNotInFrs_id = []
    linePsseNotInFrs_string = []

    lineException_id = []
    linePsseNotInException = []

    for line in linePsseNotInFrs:
        linePsseNotInFrs_id.append(line['identifier'])

        string = io.idToString(line['identifier']) + line['name']
        linePsseNotInFrs_string.append(string)

    for item in lineException:
        lineException_id.append(item['identifier'])


    linePsseNotInException_id = [line for line in linePsseNotInFrs_id if line not in lineException_id]
    linePsseNotInException_index = [index for index, line in enumerate(linePsseNotInFrs_id) if line in lineException_id]

    for item in linePsseNotInException_id:
        for line in linePsseNotInFrs:
            if item == line['identifier']:
                string = io.idToString(line['identifier']) + line['name']
                linePsseNotInException.append(string)


    print '\nlinePsseNotInFrs: ', len(linePsseNotInFrs)
    print 'lineException: ', len(lineException)
    print 'linePsseNotInException: ', len(linePsseNotInException)

    return linePsseNotInFrs_string, linePsseNotInException_index

def cmpXfm2W(xfm2WPsseNotInFrs, xfm2WException):
    xfm2WPsseNotInFrs_id = []
    xfm2WPsseNotInFrs_string = []

    xfm2WException_id = []
    xfm2WPsseNotInException = []

    for xfm2W in xfm2WPsseNotInFrs:
        xfm2WPsseNotInFrs_id.append(xfm2W['identifier'])

        string = io.idToString(xfm2W['identifier']) + xfm2W['name']
        xfm2WPsseNotInFrs_string.append(string)

    for item in xfm2WException:
        xfm2WException_id.append(item['identifier'])


    xfm2WPsseNotInException_id = [xfm2W for xfm2W in xfm2WPsseNotInFrs_id if xfm2W not in xfm2WException_id]
    xfm2WPsseNotInException_index = [index for index, xfm2W in enumerate(xfm2WPsseNotInFrs_id) if xfm2W in xfm2WException_id]

    for item in xfm2WPsseNotInException_id:
        for xfm2W in xfm2WPsseNotInFrs:
            if item == xfm2W['identifier']:
                string = io.idToString(xfm2W['identifier']) + xfm2W['name']
                xfm2WPsseNotInException.append(string)


    print '\nxfm2WPsseNotInFrs: ', len(xfm2WPsseNotInFrs)
    print 'xfm2WException: ', len(xfm2WException)
    print 'xfm2WPsseNotInException: ', len(xfm2WPsseNotInException)

    return xfm2WPsseNotInFrs_string, xfm2WPsseNotInException_index

def cmpXfm3W(xfm3WPsseNotInFrs, xfm3WException):
    xfm3WPsseNotInFrs_id = []
    xfm3WPsseNotInFrs_string = []

    xfm3WException_id = []
    xfm3WPsseNotInException = []

    for xfm3W in xfm3WPsseNotInFrs:
        xfm3WPsseNotInFrs_id.append(xfm3W['identifier'])

        string = io.idToString(xfm3W['identifier']) + xfm3W['name']
        xfm3WPsseNotInFrs_string.append(string)

    for item in xfm3WException:
        xfm3WException_id.append(item['identifier'])


    xfm3WPsseNotInException_id = [xfm3W for xfm3W in xfm3WPsseNotInFrs_id if xfm3W not in xfm3WException_id]
    xfm3WPsseNotInException_index = [index for index, xfm3W in enumerate(xfm3WPsseNotInFrs_id) if xfm3W in xfm3WException_id]

    for item in xfm3WPsseNotInException_id:
        for xfm3W in xfm3WPsseNotInFrs:
            if item == xfm3W['identifier']:
                string = io.idToString(xfm3W['identifier']) + xfm3W['name']
                xfm3WPsseNotInException.append(string)


    print '\nxfm3WPsseNotInFrs: ', len(xfm3WPsseNotInFrs)
    print 'xfm3WException: ', len(xfm3WException)
    print 'xfm3WPsseNotInException: ', len(xfm3WPsseNotInException)

    return xfm3WPsseNotInFrs_string, xfm3WPsseNotInException_index

