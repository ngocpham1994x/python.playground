import psspy
import os, sys
import pandas as pd
import csv
import pyodbc

# check wx version
try:
    import wxversion
    wxversion.select("3.0")
    import wx
    import wx.grid as wxgrid
    from wx.lib.pubsub import pub 
except ImportError:
    raise ImportError('wx module cannot be found!!!')



lineDownloadLink = "http://doverdbrs/ReportServer/Pages/ReportViewer.aspx?%2fFacility+Ratings%2fUtility+Reports%2fApiPsseLineSegment&rs:command=render&rs:format=csv"
xfmDownloadLink = "http://doverdbrs/ReportServer/Pages/ReportViewer.aspx?%2fFacility+Ratings%2fUtility+Reports%2fApiPsseTransformer&rs:command=render&rs:format=csv"

areas = ['103','600','608','620','672','667']

#--------------------------------------------------------------------------------------------------------------------------------
# defining filenames
singlesCtg = '_Singles.ctg'
openendedCtg ='_Open_ended.ctg'
stkbrkCtg = '_Stuck_breaker.ctg'
cmtowerCtg = '_Common_tower.ctg'
rowCtg = '_Right_of_way.ctg'
linebusCsv = '_linebus.csv'

#--------------------------------------------------------------------------------------------------------------------------------
# defining subsystem
lineVoltage = [100,999]
xfm2wVoltage = [60,999]
xfm3wVoltage = [60,999]

# 1 = not-included, 3 = included
lineTies = 3
xfm2wTies = 1
xfm3wTies = 3


# Line reactors to Bus Shunts (Line Shunts)
#--------------------------------------------------------------------------------------------------------------------------------
B71T =      {'identifier': {667065,672614,'1'}, 'shunt': 667065, 'name':'B71T'}     # Birtle to Tantallon @ Birtle
R7B =       {'identifier': {667067,672613,'1'}, 'shunt': 667067, 'name':'R7B'}      # reston(667067) to auberton(672613) @ Reston
D54N =      {'identifier': {667071,667035,'1'}, 'shunt': 667071, 'name':'D54N'}     # neepawa(667071) to Dorsey(667035) @ Neepawa
G31V =      {'identifier': {667062,667028,'1'}, 'shunt': 667062, 'name':'G31V'}     # vermilion(667062) to grand rapids (667028) @ Vermillion
M39V =      {'identifier': {667062,667061,'1'}, 'shunt': 667062, 'name':'M39V'}     # vermilion(667062) to Minnitonas(667061) @ Vermillion
R25Y =      {'identifier': {667063,672615,'1'}, 'shunt': 667063, 'name':'R25Y'}     # Roblin(667063) to Yorkton(672615) @ Roblin
F27P =      {'identifier': {667060,667059,'1'}, 'shunt': 667060, 'name':'F27P'}     # Overflowing River(667060) to Ralls Is. (667059) @ Overflowing River
G8P =       {'identifier': {667028,667027,'1'}, 'shunt': 667028, 'name':'G8P'}      # Grand Rapids(667028) William River (667027) @ Grand Rapids
G9F =       {'identifier': {667028,667060,'1'}, 'shunt': 667028, 'name':'G9F'}      # Grand Rapids (667028) to Overflowing River (667060) @ Grand Rapids   
U91A =      {'identifier': {667029,667030,'1'}, 'shunt': 667029, 'name':'U91A'}     # Ashern (667029) to Silvertip (667030) @ Ashern
W73H =      {'identifier': {667054,667019,'1'}, 'shunt': 667054, 'name':'W73H'}     # Herblet Lake (667054) to Wuskwatim(667019) @ Herb Lake
W74H =      {'identifier': {667054,667019,'2'}, 'shunt': 667054, 'name':'W74H'}     # Herblet lake (667054) to Wuskwatim(667019) @ Herb Lake
H75P =      {'identifier': {667054,667059,'1'}, 'shunt': 667054, 'name':'H75P'}     # Herblet Lake (667054) to Ralls Is.(667059) @ Herb Lake
H59C =      {'identifier': {667055,667054,'1'}, 'shunt': 667055, 'name':'H59C'}     # Cliff Lake (667055) to Herblet Lake (667054) @ Cliff Lake
P52E =      {'identifier': {667059,672630,'1'}, 'shunt': 667059, 'name':'P52E'}     # Ralls Is. (667059) to EB Campbell(672630) @ Ralls
RC60_R =    {'identifier': {667216,667222,'1'}, 'shunt': 667216, 'name':'RC60_R'}   # Radison(667216) to Churchill South (667222) @ radison
RC60_C =    {'identifier': {667216,667222,'1'}, 'shunt': 667222, 'name':'RC60_C'}   # Radison(667216) to Churchill South (667222) @ churchill
HG61 =      {'identifier': {667215,667214,'1'}, 'shunt': 667215, 'name':'HG61'}     # Gods Lake Narrow (667215) to oxford house (667214) @ Gods Lake 
GG64 =      {'identifier': {667221,667215,'1'}, 'shunt': 667221, 'name':'GG64'}     # Garden Hill (667221) to Gods Lake Narrows(667215) @ Gard Hill
#--------------------------------------------------------------------------------------------------------------------------------

# Dorsey generators that terminated individually
#--------------------------------------------------------------------------------------------------------------------------------
dorsey11 = {'identifier': {669825,'11'}, 'name': 'DSYEEG11'}
dorsey12 = {'identifier': {669825,'12'}, 'name': 'DSYEEG12'}
dorsey13 = {'identifier': {669825,'13'}, 'name': 'DSYEEG13'}
dorsey21 = {'identifier': {669824,'21'}, 'name': 'DSYASEAG21'}
dorsey22 = {'identifier': {669824,'22'}, 'name': 'DSYASEAG22'} 
dorsey23 = {'identifier': {669824,'23'}, 'name': 'DSYASEAG23'}
#--------------------------------------------------------------------------------------------------------------------------------


# --------------------------------PSS/E--------------------------------
def createPsseSubsystem(caseName, usekv, basekv=[]):
    listAreas = [667]
    psspy.case(caseName)
    
    if usekv:
        # psspy.bsys(sid = 1, usekv=0, basekv=basekv, numarea = len(listAreas), areas = listAreas)
        psspy.bsys(sid = 1, usekv=1, basekv=basekv, numarea = len(listAreas), areas = listAreas)
    else:
        psspy.bsys(sid = 1, usekv=0, basekv=[0.2,999], numarea = len(listAreas), areas = listAreas)


def createPsseLine(caseName, usekv, basekv=[], ties=3):
    createPsseSubsystem (caseName, usekv, basekv)
    
    # ---- AC LINES ----
    psseLine = []
    psseLineInfo = []
    
    ierr, bus1 = psspy.abrnint(sid=1, ties=ties, flag=2, string=['FROMNUMBER'])
    bus1 = bus1[0]

    ierr, bus2 = psspy.abrnint(sid=1, ties=ties, flag=2, string=['TONUMBER'])
    bus2 = bus2[0]

    ierr, cct = psspy.abrnchar(sid=1, ties=ties, flag=2, string=['ID'])
    cct = cct[0]

    
    for i, onebus in enumerate(bus1):
        lineID = {bus1[i], bus2[i], cct[i].strip()}
        psseLine.append(lineID)

        ierr, name = psspy.brnnam(bus1[i], bus2[i], cct[i].strip())

        nameComponents = name.strip().split(':')
        for item in areas:
            if item in nameComponents:
                nameComponents.remove(item)

        line = {}
        line['identifier'] = lineID
        line['name'] =  ':'.join(nameComponents).replace(' ', '_')

        psseLineInfo.append(line)

    return psseLine, psseLineInfo


def createPsse2W(caseName, usekv, basekv=[], ties=1):
    createPsseSubsystem (caseName, usekv, basekv)
    
    # ---- 2 WINDINGS ----
    psse2W = []
    psse2WInfo = []

    ierr, bus1 = psspy.atrnint(sid=1, ties=ties, flag=2, string=['FROMNUMBER'])
    bus1 = bus1[0]


    ierr, bus2 = psspy.atrnint(sid=1, ties=ties, flag=2, string=['TONUMBER'])
    bus2 = bus2[0]

    ierr, cct = psspy.atrnchar(sid=1, ties=ties, flag=2, string=['ID'])
    cct = cct[0]


    for i, onebank in enumerate(bus1):
        bankID = {bus1[i], bus2[i], cct[i].strip()}
        psse2W.append(bankID)

        ierr, name = psspy.xfrnam(bus1[i], bus2[i], cct[i].strip())

        nameComponents = name.strip().split(':')
        for item in areas:
            if item in nameComponents:
                nameComponents.remove(item)
        
        bank = {}
        bank['identifier'] = bankID
        bank['name'] = ':'.join(nameComponents).replace(' ', '_')
        
        psse2WInfo.append(bank)

    return psse2W, psse2WInfo


def createPsse3W(caseName, usekv, basekv=[], ties=3):
    createPsseSubsystem (caseName, usekv, basekv)

    # ---- 3 WINDINGS ----
    psse3W = []
    psse3WInfo = []

    ierr, bus1 = psspy.atr3int(sid=1, ties=ties, flag=2, string=['WIND1NUMBER'])
    bus1 = bus1[0]

    ierr, bus2 = psspy.atr3int(sid=1, ties=ties, flag=2, string=['WIND2NUMBER'])
    bus2 = bus2[0]

    ierr, bus3 = psspy.atr3int(sid=1, ties=ties, flag=2, string=['WIND3NUMBER'])
    bus3 = bus3[0]

    ierr, cct = psspy.atr3char(sid=1, ties=ties, flag=2, string=['ID'])
    cct = cct[0]

    
    for i, onebank in enumerate(bus1):
        bankID = {bus1[i], bus2[i], bus3[i], cct[i].strip()}
        psse3W.append(bankID)

        ierr, name = psspy.tr3nam(bus1[i], bus2[i], bus3[i], cct[i].strip())

        nameComponents = name.strip().split(':')
        for item in areas:
            if item in nameComponents:
                nameComponents.remove(item)
                
        bank = {}
        bank['identifier'] = bankID
        bank['name'] =  ':'.join(nameComponents).replace(' ', '_')

        psse3WInfo.append(bank)

    return psse3W, psse3WInfo


def createPsseMachine(caseName, usekv, basekv=[]):
    createPsseSubsystem (caseName, usekv, basekv)

    # ---- Machine (Generator) ----
    psseMach = []
    psseMachInfo = []

    ierr, bus = psspy.amachint (sid=1,flag=4,string='NUMBER')
    bus = bus[0]

    ierr, busName = psspy.amachchar (sid=1,flag=4,string='NAME')
    busName = busName[0]
    
    ierr, cct = psspy.amachchar (sid=1,flag=4,string='ID')
    cct = cct[0]


    for i, onemach in enumerate(bus):
        machID = {bus[i], cct[i].strip()}
        psseMach.append(machID)

        mach = {}
        mach['identifier'] = machID
        mach['name'] = busName[i].strip().replace(' ', '')

        psseMachInfo.append(mach)

    return psseMach, psseMachInfo


def createPsseSwSh(caseName, usekv, basekv=[]):
    createPsseSubsystem (caseName, usekv, basekv)

    # ---- Switched Shunts ----
    psseSwSh = []
    psseSwShInfo = []

    ierr, bus = psspy.aswshint (sid=1,flag=4,string='NUMBER')
    bus = bus[0]

    ierr, busName = psspy.aswshchar (sid=1,flag=4,string='NAME')
    busName = busName[0]


    for i, onebus in enumerate(bus):
        shuntID = {bus[i], ''}
        psseSwSh.append(shuntID)

        shunt = {}
        shunt['identifier'] = shuntID
        shunt['name'] = busName[i].strip().replace(' ', '')

        psseSwShInfo.append(shunt)

    return psseSwSh, psseSwShInfo


# --------------------------------FRS--------------------------------
def cleanXfmData(xfmFile):
    stationNum = []
    stationInfo = []
    stationNum, stationInfo = readSQLStations()

    df = pd.read_csv(xfmFile)

    df['StationCode'] = ''

    df['HVBus'] = df['HVBus'].fillna(0.0).astype(int)
    df['LV1Bus'] = df['LV1Bus'].fillna(0.0).astype(int)
    df['TVBus'] = df['TVBus'].fillna(0.0).astype(int)

    df[['BankName']]=df[['BankName']].apply(lambda x : x.str.replace(' ', '_')) 
    df[['PsseName']]=df[['PsseName']].apply(lambda x : x.str.replace(' ', '_')) 
    df[['PsseName']]=df[['PsseName']].apply(lambda x : x.str[4:]) 

    for index, row in df.iterrows():
        if row['StationNumbers'] in stationNum:
            index1 = stationNum.index(row['StationNumbers'])
            df.at[index, 'StationCode'] = stationInfo[index1]['StationCode']
            df.at[index, 'PsseName'] = stationInfo[index1]['StationCode'] + ':' + row['BankName']

    return df


def createFrsLine(lineFile):
    base_kV = [63.5, 66, 110, 138, 230, 500]

    frsLine = []
    frsLineInfo = []

    with open(lineFile) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if pd.to_numeric(row['BaseKv']) in base_kV: 
                bus1 = pd.to_numeric(row['FromBus']) 
                bus2 = pd.to_numeric(row['ToBus'])
                cct = row['PsseCircuitNumber']
                lineID = {bus1, bus2, cct}
                frsLine.append(lineID)

                line = {}
                line['identifier'] = lineID
                line['name'] = row['PsseName'].strip()[4:].replace(' ', '_')
                frsLineInfo.append(line)

    return frsLine, frsLineInfo


def createFrs2W(xfmFile):
    df = cleanXfmData(xfmFile)

    frs2W = []
    frs2WInfo = []

    for index, row in df.iterrows():
        if row['NumOfWindings'] == 2:
            bus1 = row['HVBus']
            bus2 = row['LV1Bus']
            cct = row['PsseCircuitNumber']
            bankID = {bus1, bus2, cct}
            frs2W.append(bankID)

            bank = {}
            bank['identifier'] = bankID
            bank['name'] = row['PsseName']
            frs2WInfo.append(bank)

    return frs2W, frs2WInfo


def createFrs3W(xfmFile):
    df = cleanXfmData(xfmFile)

    frs3W = []
    frs3WInfo = []

    for index, row in df.iterrows():
        if row['NumOfWindings'] == 3:
            bus1 = pd.to_numeric(row['HVBus']) 
            bus2 = pd.to_numeric(row['LV1Bus'])
            bus3 = pd.to_numeric(row['TVBus'])
            cct = row['PsseCircuitNumber']
            bankID = {bus1, bus2, bus3, cct}
            frs3W.append(bankID)

            bank = {}
            bank['identifier'] = bankID
            bank['name'] = row['PsseName']
            frs3WInfo.append(bank)

    return frs3W, frs3WInfo


# --------------------------------Exception List--------------------------------
def readException_wIgnore(filePath):
    lineException = []
    xfm2WException = []
    xfm3WException = []

    with open(filePath) as file:
            reader = csv.DictReader(file)

            for row in reader:
                bus1 = pd.to_numeric(row['Bus1']) 
                bus2 = pd.to_numeric(row['Bus2'])
                bus3 = pd.to_numeric(row['Bus3'])
                cct = row['PsseCircuitNumber']

                item = {}
                item['name'] = row['PsseName'].strip()

                if row['Type'].lower() == 'line':
                    item['identifier'] = {bus1, bus2, cct}
                    lineException.append(item)

                if row['Type'].lower() == '2 winding': 
                    item['identifier'] = {bus1, bus2, cct}
                    xfm2WException.append(item)

                if row['Type'].lower() == '3 winding': 
                    item['identifier'] = {bus1, bus2, bus3, cct}
                    xfm3WException.append(item)

    return lineException, xfm2WException, xfm3WException

def readException_woIgnore(filePath):
    lineException = []
    xfm2WException = []
    xfm3WException = []

    with open(filePath) as file:
            reader = csv.DictReader(file)

            for row in reader:
                bus1 = pd.to_numeric(row['Bus1']) 
                bus2 = pd.to_numeric(row['Bus2'])
                bus3 = pd.to_numeric(row['Bus3'])
                cct = row['PsseCircuitNumber']

                item = {}
                item['name'] = row['PsseName'].strip()

                if item['name'] != 'ignore':
                    if row['Type'].lower() == 'line':
                        item['identifier'] = {bus1, bus2, cct}
                        lineException.append(item)

                    if row['Type'].lower() == '2 winding': 
                        item['identifier'] = {bus1, bus2, cct}
                        xfm2WException.append(item)

                    if row['Type'].lower() == '3 winding': 
                        item['identifier'] = {bus1, bus2, bus3, cct}
                        xfm3WException.append(item)

    return lineException, xfm2WException, xfm3WException


# --------------------------------SQL, db: SPLF--------------------------------
def readSQLStations ():

    # connect to localhost SQL, reading in tag list
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=SQL2019P1;'
                          'Database=SPLF;'
                          'Trusted_Connection=yes;')
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM Station")

    stations = mycursor.fetchall()

    stationNum = []
    stationInfo = []


    for item in stations:
        if item[0].isnumeric():
            station = {}
            station['StationNum'] = pd.to_numeric(item[0])
            station['StationCode'] = str(item[1].strip())
            stationInfo.append(station)
            stationNum.append(pd.to_numeric(item[0]))

    return stationNum, stationInfo


# --------------------------------Miscellaneous--------------------------------
def getLnSh():
    lineShuntInfo = [B71T, R7B, D54N, G31V, M39V, R25Y, F27P, G8P, G9F, U91A, W73H, W74H, H75P, H59C, P52E, RC60_R, RC60_C, HG61, GG64]

    lineShunt = []
    for item in lineShuntInfo:
        lineShunt.append(item['identifier'])

    return lineShunt, lineShuntInfo


def getDorseyMachine():
    dorseyMachineInfo = [dorsey11, dorsey12, dorsey13, dorsey21, dorsey22, dorsey23]

    dorseyMachine = []
    for item in dorseyMachineInfo:
        dorseyMachine.append(item['identifier'])

    return dorseyMachine, dorseyMachineInfo


def separateIdentifier(identifier):
    '''
    identifier = {bus1, bus2, cct}
    identifier = {bus1, bus2, bus3, cct}
    '''

    buses = []
    for bus in identifier:
        if isinstance(bus, str):
            cct = bus
        else:
            buses.append(bus)

    return buses, cct


def idToString(identifier):
    buses, cct = separateIdentifier (identifier)
    string = '        ' + '        '.join(str(e) for e in buses) + '        ' + cct + '        '

    return string

# does not apply to line shunts (lnsh)
def stringToId(command):
    string = command.split('=')[1]
    components = string.split(' ')

    identifier = set()

    for component in components:
        if component == '':
            pass
        elif component.lower().startswith('\''):
            identifier.add(component.strip('\''))
        else:
            identifier.add(pd.to_numeric(component))

    return identifier


def stringToKv(string):
    kv1 = pd.to_numeric(string.strip('[]').split(',')[0])
    kv2 = pd.to_numeric(string.strip('[]').split(',')[1])

    if kv1 < kv2:
        lowerKv = kv1
        upperKv = kv2
    else:
        lowerKv = kv2
        upperKv = kv1

    return lowerKv, upperKv


# --------------------------------Actions--------------------------------
# open the browse-popup window and return the selected file
def browseFile(parent, filetype = ''):
    filepath = ''

    myfdl = wx.FileDialog(parent, "Choose a file", os.getcwd(), '', filetype, wx.FD_OPEN)

    if myfdl.ShowModal() == wx.ID_OK:
        filepath = myfdl.GetPath()

    myfdl.Destroy()

    return filepath

def browseFolder(parent):
    myfdl = wx.DirDialog(parent, "Choose a folder")
    folder = ''

    if myfdl.ShowModal() == wx.ID_OK:
        folder = myfdl.GetPath()
    
    myfdl.Destroy()

    return folder

def browseAll(folderPath, filetype):
    allfiles = os.listdir(folderPath)
    specificfiles = []

    for onefile in allfiles:
        if onefile.lower().endswith(filetype):
            onefile = os.path.join(folderPath,onefile)
            specificfiles.append(onefile)

    return specificfiles

def separateFilePath(path):
    head_tail = os.path.split(path)
    head = head_tail[0]                 # directory
    tail = head_tail[1].split('.')[0]   # file name & extention

    return head, tail

def save(outputFile, info):
    theFile = file(outputFile, 'w')
    theFile.write(info)
    theFile.close()

# ----------------------------------------------------------------
def readConfigFile(filename):
    groups = []
    reader = csv.DictReader(open(filename))

    for row in reader:
        ctg = {}
        ctg['contingency name'] = ''
        ctg['assets'] = set()
        
        if 'BES?' in row:
            if row['BES?'] == 'Y':
                row.pop('BES?')
            else:
                row.pop('BES?')
                continue

        if 'contingency name' in row:
            ctg['contingency name'] = row['contingency name']
            row.pop('contingency name')

        ctg['assets'].update(s.strip() for s in row.values())
        if '' in ctg['assets']:
            ctg['assets'].remove('')

        if ctg not in groups:
            groups.append(ctg)

    return groups

def readCtgFile(filename):
    ctgs = []
    valid = 0

    theFile = file(filename)
    alltxt = theFile.read().splitlines()
    theFile.close()

    for oneline in alltxt:
        # single contingency signaled start
        if oneline.lower().startswith('{contingency}')  : # that's the start of a contingency
            valid = 1
            ctg = {}
            ctg['contingency name'] = ''
            ctg['commands'] = []

        # single contingency signaled done
        elif oneline.lower().startswith("{end contingency}"):
            if valid == 1:
                ctgs.append(ctg)
                valid = 0 # reset 

        # add ctg name & commands of the single contingency
        else:
            if valid == 1:
                if oneline.strip().lower().startswith("contingency name") : # read the name of a contingency
                    name = oneline.split("=")[1]
                    name = name.split("'")[1]
                    ctg['contingency name'] = name
                else:
                    ctg['commands'].append(oneline)


    return ctgs

def readCsvLinebus(filename):
    reader = csv.reader(open(filename))

    rows = []

    for row in reader:
        rows.append(row)

    return rows