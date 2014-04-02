
years = ['2004', '2005', '2006', '2007']
days_min = [105, 239, 244, 146]
days_max = [213, 365, 365, 365]
hours =    [ 900, 905, 910, 915, 920, 925, 930, 935, 940, 945, 950, 955, 960, \
            1000, 1005, 1010, 1015, 1020, 1025, 1030, 1035, 1040, 1045, 1050, 1055, \
            1100, 1105, 1110, 1115, 1120, 1125, 1130, 1135, 1140, 1145, 1150, 1155, \
            1200, 1205, 1210, 1215, 1220, 1225, 1230, 1235, 1240, 1245, 1250, 1255, \
            1300, 1305, 1310, 1315, 1320, 1325, 1330, 1335, 1340, 1345, 1350, 1355, \
            1400, 1405, 1410, 1415, 1420, 1425, 1430, 1435, 1440, 1445, 1450, 1455, \
            1500, 1505, 1510, 1515, 1520, 1525, 1530, 1535, 1540, 1545, 1550, 1555, 1600]
# data between 9:00 and 16:00: A2004001003000.L1A_LAC.bz2
#wget -nc -S -O - http://oceandata.sci.gsfc.nasa.gov/MODISA/L2/2012/131/ |grep OC|wget -N --wait=0.5 --random-wait --force-html -i -

batch_script_file = open("download_batch.txt", 'a')

for year in range(len(years)):
    for day in range(days_min[year], days_max[year]+1):
        for hour in hours:
            product_name = 'A'+years[year]+str(day) + str(hour).zfill(4) + '00.L1A_LAC.bz2'
            destURL = 'http://oceandata.sci.gsfc.nasa.gov/MODISA/L1/'+years[year]+'/'+str(day)+'/' + product_name
            wgetCommand = "wget -nc -S -O - " + destURL
            batch_script_file.write(wgetCommand + '\n')


batch_script_file.close()

#EOF