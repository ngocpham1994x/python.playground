import os, sys
import io_process as io


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

class MergePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # layout
        allsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)

        # GUI components
        leftsizer.Add(wx.StaticText(self, -1, 'Select folder containing .csv exported from panel 2:'), 0, wx.ALL, 5)
        leftsizer.Add(wx.StaticText(self, -1, "**Note: only '_linebus.csv' files will be selected from the folder"), 0, wx.ALL, 5)
        self.folderPath = wx.TextCtrl(self, -1, '', )
        self.btnBrowse= wx.Button(self, -1, 'Browse', )
        self.btnBrowseAll = wx.Button(self, -1, '>>',) 

        self.files = wx.ListBox(self, -1, choices=[])

        self.btnMerge = wx.Button(self, -1, 'Merge') 

        self.infoText = wx.TextCtrl(self, -1, '', style=wx.MULTIPLE)

        # layout
        btnsizer.Add(self.btnBrowse, 0, wx.ALL, 5)
        btnsizer.Add(self.btnBrowseAll, 0, wx.ALL, 5)

        leftsizer.Add(self.folderPath, 1, wx.ALL|wx.EXPAND, 5)
        leftsizer.Add(btnsizer, 0, wx.ALL|wx.EXPAND, 5)

        topsizer.Add(leftsizer, 0, wx.ALL|wx.EXPAND, 5)
        topsizer.Add(self.files,  1, wx.ALL|wx.EXPAND, 5)

        allsizer.Add(topsizer, 0, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.btnMerge, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        allsizer.Add(self.infoText, 1, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizerAndFit(allsizer)

        # button binding
        self.Bind(wx.EVT_BUTTON, self.onBrowse, self.btnBrowse)
        self.Bind(wx.EVT_BUTTON, self.onBrowseAll, self.btnBrowseAll)
        self.Bind(wx.EVT_BUTTON, self.onMerge, self.btnMerge)


    def onBrowse(self, event):
        folder = io.browseFolder(self)
        self.folderPath.SetValue(folder)

        if not folder:
            wx.MessageBox("No folder selected. Please check!", "Info", wx.OK)

    def onBrowseAll(self, event):

        if self.folderPath.GetValue():
            allfiles = io.browseAll(self.folderPath.GetValue(), '.csv')
            allfiles = [onefile for onefile in allfiles if io.linebusCsv in onefile.lower()]

            self.files.SetItems(allfiles)

        else:
            wx.MessageBox("Please Select the Folder","Warning", wx.OK)

    def onMerge(self, event):
        info = ''
        allAssets = []

        files = self.files.GetItems()

        for i, onefilepath in enumerate(files):
            assets = io.readCsvLinebus(onefilepath)
            outliners = [asset for asset in assets if asset not in allAssets]

            print 'length .csv file #', i, len(assets)
            print 'length outliners', len(outliners)
            print '====================================================='
            allAssets.extend(outliners)

        for asset in allAssets:
            info = info + ','.join(str(e) for e in asset) + '\n'

        self.infoText.SetValue(info)

        output = self.folderPath.GetValue() + '\\' + 'AllAssets' + io.linebusCsv
        io.save (output, info)

        print 'length AllAssets: ', len(allAssets)

