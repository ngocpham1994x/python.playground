import io_process as io
import os, sys


# check wx version
try:
    import wxversion
    wxversion.select("3.0")
    import wx
    import wx.grid as wxgrid
    from wx.lib.pubsub import pub 
except ImportError:
    raise ImportError('wx module cannot be found!!!')



class ContingencyGenPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # layout
        allsizer = wx.BoxSizer(wx.VERTICAL)
        savsizer = wx.BoxSizer(wx.HORIZONTAL)
        outputsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizerSingles = wx.BoxSizer(wx.HORIZONTAL)
        sizerOpenEnded = wx.BoxSizer(wx.HORIZONTAL)
        sizerStkBrk = wx.BoxSizer(wx.HORIZONTAL)
        sizerCmTower = wx.BoxSizer(wx.HORIZONTAL)
        sizerROW = wx.BoxSizer(wx.HORIZONTAL)
        textsizer = wx.BoxSizer(wx.HORIZONTAL)

        # GUI components
        self.savText = wx.StaticText(self, -1, "Select .sav file")
        self.savPath = wx.TextCtrl(self, -1, "")
        self.btnBrowseInput = wx.Button(self, -1, "Browse")

        self.outputText = wx.StaticText(self, -1, "Choose location for .ctg output files")
        self.outputPath = wx.TextCtrl(self, -1, "")
        self.btnBrowseOutput = wx.Button(self, -1, "Browse")

        self.txtSingles = wx.StaticText(self, -1, "Select single/co-terminated equipment file")
        self.configSingles = wx.TextCtrl(self, -1, "")
        self.btnBrowseSingles = wx.Button(self, -1, "Browse")
        self.btnGenSingles = wx.Button(self, -1, "Generate Single contingencies")

        self.txtOE = wx.StaticText(self, -1, "Open-ended contingencies")
        self.btnGenOpenEnded = wx.Button(self, -1, "Generate Open-ended", size=(500,27))

        self.txtStkBrk = wx.StaticText(self, -1, "Select Stuck breaker config file")
        self.configStkBrk = wx.TextCtrl(self, -1, "")
        self.btnBrowseStkBrk = wx.Button(self, -1, "Browse")
        self.btnGenStkBrk = wx.Button(self, -1, "Generate Stuck breaker")

        self.txtCmTower = wx.StaticText(self, -1, "Select Common Tower config file")
        self.configCmTower = wx.TextCtrl(self, -1, "")
        self.btnBrowseCmTower = wx.Button(self, -1, "Browse")
        self.btnGenCmTower = wx.Button(self, -1, "Generate Common Tower")

        self.txtROW = wx.StaticText(self, -1, "Select Right-of-way config file")
        self.configROW = wx.TextCtrl(self, -1, "")
        self.btnBrowseROW = wx.Button(self, -1, "Browse")
        self.btnGenROW = wx.Button(self, -1, "Generate Right-of-way")

        self.infoText = wx.TextCtrl(self, -1, "", style=wx.MULTIPLE)
        self.statText = wx.TextCtrl(self, -1, "", style=wx.MULTIPLE)

        # layout
        savsizer.Add(self.savText, 1, wx.ALL, 5)
        savsizer.Add(self.savPath,  1, wx.ALL, 5)
        savsizer.Add(self.btnBrowseInput,  0, wx.ALL, 5)

        outputsizer.Add(self.outputText, 1, wx.ALL, 5)
        outputsizer.Add(self.outputPath,  1, wx.ALL, 5)
        outputsizer.Add(self.btnBrowseOutput,  0, wx.ALL, 5)

        sizerSingles.Add(self.txtSingles, 1, wx.ALL, 5)
        sizerSingles.Add(self.configSingles, 1, wx.ALL, 5)
        sizerSingles.Add(self.btnBrowseSingles, 0, wx.ALL, 5)
        sizerSingles.Add(self.btnGenSingles, 1, wx.ALL, 5)

        sizerOpenEnded.Add(self.txtOE, 1, wx.ALL, 5)
        sizerOpenEnded.Add(self.btnGenOpenEnded, 0, wx.ALL, 5)

        sizerStkBrk.Add(self.txtStkBrk, 1, wx.ALL, 5)
        sizerStkBrk.Add(self.configStkBrk, 1, wx.ALL, 5)
        sizerStkBrk.Add(self.btnBrowseStkBrk, 0, wx.ALL, 5)
        sizerStkBrk.Add(self.btnGenStkBrk, 1, wx.ALL, 5)

        sizerCmTower.Add(self.txtCmTower, 1, wx.ALL, 5)
        sizerCmTower.Add(self.configCmTower, 1, wx.ALL, 5)
        sizerCmTower.Add(self.btnBrowseCmTower, 0, wx.ALL, 5)
        sizerCmTower.Add(self.btnGenCmTower, 1, wx.ALL, 5)
        
        sizerROW.Add(self.txtROW, 1, wx.ALL, 5)
        sizerROW.Add(self.configROW, 1, wx.ALL, 5)
        sizerROW.Add(self.btnBrowseROW, 0, wx.ALL, 5)
        sizerROW.Add(self.btnGenROW, 1, wx.ALL, 5)

        textsizer.Add(self.infoText, 1, wx.ALL|wx.EXPAND, 5)
        textsizer.Add(self.statText, 1, wx.ALL|wx.EXPAND, 5)

        allsizer.Add(savsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(outputsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(sizerSingles, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(sizerOpenEnded, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(sizerStkBrk, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(sizerCmTower, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(sizerROW, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(textsizer, 1, wx.ALL|wx.EXPAND, 5)

        self.SetSizerAndFit(allsizer)

        # button binding
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'input'), self.btnBrowseInput)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'output'), self.btnBrowseOutput)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'singles'), self.btnBrowseSingles)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'stkbrk'), self.btnBrowseStkBrk)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'cmtower'), self.btnBrowseCmTower)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.onBrowse (evt, 'ROW'), self.btnBrowseROW)
        
        self.Bind(wx.EVT_BUTTON, self.onGenSingles, self.btnGenSingles)
        self.Bind(wx.EVT_BUTTON, self.onGenOpenEnded, self.btnGenOpenEnded)
        self.Bind(wx.EVT_BUTTON, self.onGenStkBrk, self.btnGenStkBrk)
        self.Bind(wx.EVT_BUTTON, self.onGenCmTower, self.btnGenCmTower)
        self.Bind(wx.EVT_BUTTON, self.onGenROW, self.btnGenROW)


    # button methods
    def onBrowse(self, event, category):
        if category in ['singles','stkbrk','cmtower','ROW']:
            filepath = io.browseFile(self, '*.csv')
        elif category == 'input':
            filepath = io.browseFile(self, '*.sav')
        elif category == 'output':
            filepath = io.browseFolder(self)

        if filepath:
            if category == 'input':
                self.savPath.SetValue(filepath)
            elif category == 'output':
                self.outputPath.SetValue(filepath)
            elif category == 'singles':
                self.configSingles.SetValue(filepath)
            elif category == 'stkbrk':
                self.configStkBrk.SetValue(filepath)
            elif category == 'cmtower':
                self.configCmTower.SetValue(filepath)
            elif category == 'ROW':
                self.configROW.SetValue(filepath)

        else:
            wx.MessageBox("No path selected. Please check!", "Info", wx.OK)

    def onGenSingles(self, event):
        info = ''
        stats = ''
        # input
        caseName = self.savPath.GetValue()
        root, case = io.separateFilePath(caseName)

        # output
        path = self.outputPath.GetValue()
        output = path + '\\' + case + io.singlesCtg

        if (self.configSingles.GetValue()):
            coterms = io.readConfigFile(self.configSingles.GetValue())
        else:
            wx.MessageBox ('No config file selected. Please check!', 'Info', wx.OK)

        if caseName and path:

            self.ctgBranch = self.genCtgCmd ('line', caseName)
            self.ctg2W = self.genCtgCmd ('2W', caseName)
            self.ctg3W = self.genCtgCmd ('3W', caseName)
            self.ctgGen = self.genCtgCmd ('machine', caseName)
            self.ctgSwSh = self.genCtgCmd ('swsh', caseName)
            self.ctgLnSh = self.genCtgCmd ('lnsh', caseName)

            self.allCtgs = self.ctgBranch + self.ctg2W + self.ctg3W + self.ctgGen + self.ctgSwSh + self.ctgLnSh
            self.ctgCoterm = self.genGroupedCtg(self.allCtgs, coterms)
            self.allCtgs = self.allCtgs + self.ctgCoterm

            stats = stats + 'count ctgBranch: ' + str(len(self.ctgBranch)) + '\n'
            stats = stats + 'count ctg2W: ' + str(len(self.ctg2W)) + '\n'
            stats = stats + 'count ctg3W: ' + str(len(self.ctg3W)) + '\n'
            stats = stats + 'count ctgGen: ' + str(len(self.ctgGen)) + '\n'
            stats = stats + 'count ctgSwSh: ' + str(len(self.ctgSwSh)) + '\n'       # fetched from PSS/E
            stats = stats + 'count ctgLnSh: ' + str(len(self.ctgLnSh)) + '\n'       # provided in io_process.py
            stats = stats + 'count ctgCoterm: ' + str(len(self.ctgCoterm)) + '\n'
            stats = stats + 'allCtgs + ctgCoterms: ' + str(len(self.allCtgs)) + '\n'


            info = info + self.printCtg (self.allCtgs)

            io.save (output, info)

        else:
            wx.MessageBox('No .sav file or output path selected. Please check!', 'Info', wx.OK)

        self.infoText.SetValue(info)
        self.statText.SetValue(stats)

    def onGenOpenEnded(self, event):
        info = ''
        # input
        caseName = self.savPath.GetValue()
        root, case = io.separateFilePath(caseName)

        # outputs
        path = self.outputPath.GetValue()
        output = path + '\\' + case + io.openendedCtg
        outputP1 = path + '\\' + case + io.singlesCtg


        if caseName and os.path.exists(outputP1):
            self.ctgOE = self.genOECtg(self.ctgBranch)

            info = info + self.printCtg (self.ctgOE)

            io.save (output, info)

        else:
            wx.MessageBox('No .sav file selected, or no P1 coterminated file existed. Please check!', 'Info', wx.OK)

        self.infoText.SetValue(info)

    def onGenStkBrk(self, event):
        info = ''
        # input
        caseName = self.savPath.GetValue()
        root, case = io.separateFilePath(caseName)

        # outputs
        path = self.outputPath.GetValue()
        output = path + '\\' + case + io.stkbrkCtg
        outputP1 = path + '\\' + case + io.singlesCtg
        outputOE = path + '\\' + case + io.openendedCtg

        if (self.configStkBrk.GetValue()):
            sbGroups = io.readConfigFile(self.configStkBrk.GetValue())
        else:
            wx.MessageBox ('No config file selected. Please check!', 'Info', wx.OK)

        if caseName and os.path.exists(outputP1) and os.path.exists(outputOE):
            ctgs = self.allCtgs + self.ctgOE
            ctgStckBrk = self.genGroupedCtg(ctgs, sbGroups)

            info = info + self.printCtg (ctgStckBrk)

            io.save (output, info)

        else:
            wx.MessageBox('No .sav file selected, or no P1 coterminated or OE file existed. Please check!', 'Info', wx.OK)

        self.infoText.SetValue(info)

    def onGenCmTower(self, event):
        info = ''
        # input
        caseName = self.savPath.GetValue()
        root, case = io.separateFilePath(caseName)

        # outputs
        path = self.outputPath.GetValue()
        output = path + '\\' + case + io.cmtowerCtg
        outputP1 = path + '\\' + case + io.singlesCtg

        if (self.configCmTower.GetValue()):
            ctGroups = io.readConfigFile(self.configCmTower.GetValue())
        else:
            wx.MessageBox ('No config file selected. Please check!', 'Info', wx.OK)

        if caseName and os.path.exists(outputP1):
            ctgCmTower = self.genGroupedCtg(self.allCtgs, ctGroups)

            info = info + self.printCtg (ctgCmTower)

            io.save (output, info)

        else:
            wx.MessageBox('No .sav file selected, or no P1 coterminated file existed. Please check!', 'Info', wx.OK)

        self.infoText.SetValue(info)

    def onGenROW(self, event):
        info = ''
        # input
        caseName = self.savPath.GetValue()
        root, case = io.separateFilePath(caseName)

        # outputs
        path = self.outputPath.GetValue()
        output = path + '\\' + case + io.rowCtg
        outputP1 = path + '\\' + case + io.singlesCtg

        if (self.configROW.GetValue()):
            rowGroups = io.readConfigFile(self.configROW.GetValue())
        else:
            wx.MessageBox ('No config file selected. Please check!', 'Info', wx.OK)

        if caseName and os.path.exists(outputP1):
            ctgROW = self.genGroupedCtg(self.allCtgs, rowGroups)

            info = info + self.printCtg (ctgROW)

            io.save (output, info)

        else:
            wx.MessageBox('No .sav file selected, or no P1 coterminated file existed. Please check!', 'Info', wx.OK)

        self.infoText.SetValue(info)

    def printCtg(self, ctgList):
        info = '[VSAT 4.X Contingency]\n'

        for item in ctgList:
            info = info + '{Contingency}\n'

            info = info + "Contingency name = '" + item['contingency name'] + "'\n"
            for command in item['commands']:
                info = info + command + '\n'

            info = info + '{END Contingency}\n'

        info = info + '[End]'

        return info


    # single contingencies generator
    def genCtgCmd(self, category, caseName):
        allCtgs = []
        names = set()

        psseIdentifiers = []
        psseInfo = []
        psseIdentifiers, psseInfo = getIdentifierAndInfo(category, caseName)

        dorseyMachineInfo = []
        dorseyMachineIdentifiers, dorseyMachineInfo = io.getDorseyMachine()


        # remove duplicate ctg names
        for item in psseInfo:
            # take the first component of line name as contingency name
            if category == 'line':
                names.add(item['name'].split(':')[0])
                item['name'] = item['name'].split(':')[0].strip()

            # MACHINE EXCEPTION: Dorsey machines that terminated individually
            elif category == 'machine':
                if item['identifier'] in dorseyMachineIdentifiers:
                    pass
                else:
                    names.add(item['name'].strip())

            else:
                names.add(item['name'].strip())

        if '' in names:
            names.remove('')


        # Dorsey machines that terminated individually
        if category == 'machine':
            for i, item in enumerate(dorseyMachineInfo):

                if item['identifier'] in psseIdentifiers:
                    psseIdentifiers.remove(item['identifier'])
                    psseInfo = [machine for machine in psseInfo if not (machine['identifier'] == item['identifier'])]

                buses, cct = io.separateIdentifier (item['identifier'])

                ctg = {}
                ctg['contingency name'] = item['name'].strip()
                ctg['commands'] = []

                command = 'Change Generation = ' + " ".join(str(e) for e in buses) + " '" + cct + "' 0"
                ctg['commands'].append(command)

                allCtgs.append(ctg)


        # generate ctg commands
        for i, name in enumerate(names):
            ctg = {}
            ctg['contingency name'] = name.strip()
            ctg['commands'] = []

            for item in psseInfo:
                if item['name'] == name and (name):
                    buses, cct = io.separateIdentifier (item['identifier'])

                    if category == 'line' or category == '2W':
                        command = 'Outage Branch = ' + " ".join(str(e) for e in buses) + " '" + cct + "'"

                    elif category == '3W':
                        command = 'Outage 3W-Transformer = ' + " ".join(str(e) for e in buses) + " '" + cct + "'"

                    elif category == 'machine':
                        command = 'Change Generation = ' + " ".join(str(e) for e in buses) + " '" + cct + "' 0"

                    elif category == 'swsh':
                        ctg['contingency name'] = item['name'] + '_SWSH'
                        command = 'Turn off Switched Shunt = ' + " ".join(str(e) for e in buses) + " '" + cct + "'"

                    # line shunts that terminated individually
                    elif category == 'lnsh':
                        ctg['contingency name'] = item['name'] + '_LNSH'
                        command = 'Turn off Switched Shunt = ' + str(item['shunt']) +  " '" + item['name'] + "'"

                    ctg['commands'].append(command)

            allCtgs.append(ctg)


        # line shunts that co-terminated with the line
        if category == 'line':
            lineShuntInfo = []
            lineShuntIdentifiers, lineShuntInfo = io.getLnSh()
            
            for lineShunt in lineShuntInfo:
                for ctg in allCtgs:
                    if lineShunt['name'] == ctg['contingency name']:
                        command_lineShunt = 'Turn off Switched Shunt = ' + str(lineShunt['shunt']) +  " '" + lineShunt['name'] + "'"
                        ctg['commands'].append(command_lineShunt)

                    # special instance: RC60
                    if (lineShunt['name'] == 'RC60_C' or lineShunt['name'] == 'RC60_R') and ctg['contingency name'] == 'RC60':
                        command_lineShunt = 'Turn off Switched Shunt = ' + str(lineShunt['shunt']) +  " '" + lineShunt['name'] + "'"
                        ctg['commands'].append(command_lineShunt)

        return allCtgs

    # stuck breaker, common tower, right-of-way contingencies generator
    def genGroupedCtg(self, allCtgs, groups):
        ctgNames = set()
        for i, ctg in enumerate(allCtgs):
            ctgNames.add(ctg['contingency name'])

        ctgs = []
        error = ''

        # generate coterminated contingencies
        for group in groups:
            ctg = {}
            ctg['contingency name'] = ''
            ctg['commands'] = []

            if group['contingency name'] == '':
                ctg['contingency name'] = '+'.join(str(e).strip() for e in group['assets'])
            else:
                ctg['contingency name'] = group['contingency name']

            for asset in group['assets']:
                if asset in ctgNames:
                    for onectg in allCtgs:
                        if onectg['contingency name'] == asset:
                            ctg['commands'].append('/ctg: ' + onectg['contingency name'])
                            ctg['commands'].extend(onectg['commands'])
                else:
                    ctg['commands'].append('/no ctg for ' + asset)
                    error = error + '/no ctg for ' + asset + '\n'

            ctgs.append(ctg)

        error = error + '\ncount ctgs ' + str(len(ctgs))
        self.statText.SetValue(error)

        return ctgs

    # open-ended contingencies generator
    def genOECtg(self, ctgs):
        oeBranches = []
        oeCtgs = []

        # found branches with >= 2 segments, hence have ends
        for ctg in ctgs:
            count = countOutageBranch(ctg)
            if count >= 2:
                oeBranches.append(ctg)

        # generate OE contingencies
        for ctg in oeBranches:
            endInfo = countEnds(ctg)
            for end in endInfo:
                if end['count'] == 1:
                    newctg = {}
                    newctg['contingency name'] = ctg['contingency name'] + 'OE' + str(end['bus'])
                    newctg['commands'] = [cmd for cmd in ctg['commands'] if str(end['bus']) in cmd]
                    oeCtgs.append(newctg)


        self.statText.SetValue('count oeCtgs: ' + str(len(oeCtgs)))

        return oeCtgs



def getIdentifierAndInfo(category, caseName):
    # create equipment info from case
    if category == 'line':
        psseIdentifiers, psseInfo = io.createPsseLine(caseName, True, io.lineVoltage, ties=io.lineTies)

    elif category == '2W':
        psseIdentifiers, psseInfo = io.createPsse2W(caseName, True, io.xfm2wVoltage, ties=io.xfm2wTies)

    elif category == '3W':
        psseIdentifiers, psseInfo = io.createPsse3W(caseName, True, io.xfm3wVoltage, ties=io.xfm3wTies)

    elif category == 'machine':
        psseIdentifiers, psseInfo = io.createPsseMachine(caseName, False, [0.2,999])

    elif category == 'swsh':
        psseIdentifiers, psseInfo = io.createPsseSwSh(caseName, False, [0.2,999])

    # Line reactors to Bus Shunts terminated individually
    elif category == 'lnsh':
        psseIdentifiers, psseInfo = io.getLnSh()


    return psseIdentifiers, psseInfo

# count how many "Outage Branch" commands
def countOutageBranch(ctg):
    count = 0
    for command in ctg['commands']:
        if command.lower().startswith('outage branch'):
            count += 1

    return count

# just "Outage Branch" commands have ends counted ("Turn off..." not counted)
def countEnds(ctg):
    ends = set()
    endInfo = []

    for command in ctg['commands']:
        if command.lower().startswith('outage branch'):
            identifier = io.stringToId(command)
            buses, cct = io.separateIdentifier(identifier)
            for bus in buses:
                if bus not in ends:
                    onebus = {}
                    onebus['bus'] = bus
                    onebus['count'] = 1

                    ends.add(bus)
                    endInfo.append(onebus)
                else:
                    for onebus in endInfo:
                        if onebus['bus'] == bus:
                            onebus['count'] += 1

    return endInfo