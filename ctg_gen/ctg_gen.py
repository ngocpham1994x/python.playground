"""
REQUIRED PACKAGES:
    - python 2.7
    - pyodbc 4.0.32 (to install in cmd prompt: in Python27 folder, "pip install pyodbc==4.0.32")
    - pandas
    - webbrowser
    - os, sys
    - csv

Panel 1: COMPARISON (.sav to .csv)
inputs = .sav file, .csv files
output = warnings for lines/2w/3w
    - PSSE identifiers are not found in FRS
    - PSSE identifiers are found in FRS but multiple records

Panel 2: RELACE NAMES
input = folder for exporting '_linebus.csv' files to merge them later in task-tab 5.
Order of replacing PSSE names: 
    standard asset names
    replace PSSE names with names of IDENTIFIERS found-in-FRS
    replace PSSE names with names in explicit changes file
    
Errors could occur due to duplicated NAMES.
Errors could occur due to the asset to replace name is not in the current case (but could be in future cases).
Run the REPLACE button twice to clear errors.
CAUTION: Case will be overwritten! 

Panel 3: .ctg GENERATOR
inputs = .sav , folder for .ctg files, ctg config files
output = ALL contingencies .ctg files for 5 planning events
    - left panel: .ctg file contents
    - right pane: warnings on not-found ctgs

Panel 4: N11 ctg GENERATOR
input = two .ctg files from single contingencies
output = .ctg N11

Panel 5: MERGE '_linebus.csv' FILES
input = folder where '_linebus.csv' files located
output = 'Allassets_linebus.csv' in the same folder


Created on Aug 29, 2022
@author: npham (ngoc pham)

"""
import os, sys

exename = sys.executable
p, nx   = os.path.split(exename)
nx      = nx.lower()
PSSEon = 0


# check wx version
try:
    import wxversion
    wxversion.select("3.0")
    import wx
    import wx.grid as wxgrid
    from wx.lib.pubsub import pub 
except ImportError:
    raise ImportError('wx module cannot be found!!!')


# initiate PSS/E, for viewing in terminal window
_PSSPYPATH = r"C:\Program Files (x86)\PTI\PSSE34\PSSPY27"
_PSSBINPATH = r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN"
os.environ['PATH'] = _PSSBINPATH + ';' + os.environ['PATH']
sys.path.insert(0, _PSSPYPATH)
sys.path.insert(0, _PSSBINPATH)

import redirect
redirect.psse2py()

import psspy
import io_process as io
import panel1   # compare
import panel2   # replace
import panel3   # ctg gen
import panel4   # ctg N11
import panel5

# 667 area has 83,000 buses.
# choose here bus numbers you want. Default 150,000 which is enough to handle 83,000 buses.
ierr = psspy.psseinit(buses=150000)  
if ierr:
    PSSEon = 0
    raise Exception('PSS(R)E could not be initialized.')
else:
    PSSEon = 1


print _PSSBINPATH + ' was added to sys path!\n'



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="CTG GENERATOR")

        # main panel
        panel = wx.Panel(self,-1)

        # layout
        allsizer = wx.BoxSizer(wx.VERTICAL)
        bodysizer = wx.BoxSizer(wx.HORIZONTAL)

        # bodySizer components
        self.nb = wx.Notebook(panel, -1)
        
        self.pn1 = panel1.ComparisonPanel(self.nb)   # panel 1: compare .sav & .csv files
        self.pn1.BackgroundColour = panel.GetBackgroundColour()
        

        self.pn2 = panel2.NameChangePanel(self.nb) # panel 2: replace equipment names
        self.pn2.BackgroundColour = panel.GetBackgroundColour()

        self.pn3 = panel3.ContingencyGenPanel(self.nb) # panel 3: contingency generator
        self.pn3.BackgroundColour = panel.GetBackgroundColour()

        self.pn4 = panel4.BuildN11Panel(self.nb) # panel 4: Contingency N11
        self.pn4.BackgroundColour = panel.GetBackgroundColour()

        self.pn5 = panel5.MergePanel(self.nb) # panel 5: Merge _linebus.csv
        self.pn5.BackgroundColour = panel.GetBackgroundColour()

        self.nb.AddPage(self.pn1, "1  Compare .SAV to .CSV files")
        self.nb.AddPage(self.pn2, "2  Replace asset names")
        self.nb.AddPage(self.pn3, "3  Contingency generator")
        self.nb.AddPage(self.pn4, "4  Contingency N11")
        self.nb.AddPage(self.pn5, "5  Merge _linebus.csv")

        # bottom components
        self.btnExit = wx.Button(panel, -1, "Exit")
        
        # layout
        bodysizer.Add(self.nb, 1, wx.ALL|wx.EXPAND, 5)

        allsizer.Add(bodysizer, 1, wx.ALL|wx.EXPAND, 5)
        allsizer.Add(self.btnExit, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        panel.SetSizerAndFit(allsizer)

        # button binding
        self.Bind(wx.EVT_BUTTON, self.onExit, self.btnExit)


    # button methods
    def onExit(self, evt):
        self.Close()

class MainApp(wx.App):
    # Application __init__method is not defined here
    # the parent method wx.App.__init__() is automatically invoked on ojbect creation
    def OnInit(self):
        frame = MainFrame() # create  a frame object
        frame.Show(True)
        frame.Maximize(True)

        return True

def main():
    app = MainApp(0)
    app.MainLoop()

if __name__ == '__main__':
    main()
