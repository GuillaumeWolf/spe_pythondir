import csv
import ROOT
ROOT.gROOT.SetBatch(True)


def Get_resolution_from_file_for_plane_p(file_path, p):
    print("Opening file: " + file_path)
    file_data = ROOT.TFile(file_path,"READ")
    TGE_resolution = file_data.Get("TGE_sipm-1")
    return [TGE_resolution.GetPointY(p),TGE_resolution.GetErrorY(p)]

def Get_value_from_csvFile_atLine_atRow_withHeader(path_csv,l,r,header):
    with open(path_csv, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        if header:
            next(csvreader)
        for current_line, row in enumerate(csvreader, start=1):
            if current_line == l:
                return float(row[r])















""" Defining variables """
path_csv = "../datadir/reconstructedDatas/Testbeam.csv"
planes = [6]
runs = range(41,71)

""" output """
path_output = "../datadir/reconstructedDatas/timeResolution_inFunctionOf_overV_position.root"
file_output = ROOT.TFile.Open(path_output,"RECREATE")
    
""" Loop """
for p in planes:
    TG2DE = ROOT.TGraph2DErrors()
    TG2DE.SetTitle("sigma(over_v,position)_plane_"+str(p))
    for run in runs:
        print(f"run = {run}")
        """ Resolution (Z axis) """
        path_input = "../datadir/reconstructedDatas/run_0000"+str(run)+"/sigmaResolution.root"
        resolution = Get_resolution_from_file_for_plane_p(path_input,p)
        # resolution = [run,0]
        print(f"resolution = {resolution[0]}({resolution[1]})")

        """ over voltage (x axis) and position of mat (y axis) """
        over_v = Get_value_from_csvFile_atLine_atRow_withHeader(path_csv,run+1,6,True)
        position = Get_value_from_csvFile_atLine_atRow_withHeader(path_csv,run+1,7,True)
        print(f"over_v = {over_v}, position = {position}")

        """ Fill """
        TG2DE.SetPoint(TG2DE.GetN(),over_v,position,resolution[0])
        TG2DE.SetPoint(TG2DE.GetN()-1,0,0,resolution[1])        

        print("")
    
    # Output
    file_output.cd()
    TG2DE.Write()




file_output.Close()






