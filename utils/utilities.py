__author__ = 'uwe'


from datetime import date, timedelta
from os import remove, makedirs
from os.path import exists
import bz2

def getBackDate(backDay):
    _back_date = date.today() - timedelta(backDay)
    return _back_date

def getDOY(_year, _month, _day):
    d1 = date(int(_year), int(_month), int(_day))
    d0 = date(int(_year)-1, 12, 31)
    delta=d1-d0
    return delta.days

def getBackDOY(backDay, _year=date.today().year):
    d0 = date(_year-1, 12, 31)
    d1 = date.today() - timedelta(int(backDay))
    delta=d1-d0
    return delta.days

def getDateFromDOY(_year, DOY):
    _now = date.today()
    first_of_year = _now.replace(year=int(_year), month=1, day=1)
    first_ordinal = first_of_year.toordinal()
    the_ordinal = first_ordinal - 1 + int(DOY)
    return date.fromordinal(the_ordinal)

def ensurePathExists(_thepath):
    if not exists(_thepath):
        try:
            makedirs(_thepath)
        except OSError as e:
            print("Error", e.errno, e.strerror)
            return False
        else:
            return True

def ensureTrailingSlash(path):
    if not path.endswith('/'):
        return path + '/'
    else:
        return path

def exit_on_empty_list(list):
    _size = len(list)
    if not _size:
        print("Nothing to do here. Now quitting.")
        exit(1)
    else:
        return _size

def filter_list(input_list, extension):
    output_list =[]
    for count in range(len(input_list)):
        item = input_list[count]
        print(count, item)
        if item.endswith(extension):
            output_list.append(item)
    return output_list

def bzip2CompressFile(path, removeInput):
    if exists(path):
        bzippedFilePath=path+'.bz2'
        if not exists(bzippedFilePath):
            print("Compressing ", path, "...")
            inputStream  = open(path, 'rb')
            outputStream = bz2.BZ2File(bzippedFilePath, 'wb')
            outputStream.writelines(inputStream)
            outputStream.close()
            inputStream.close()
            if removeInput:
                remove(path)
            return 1
        else:
            print("bzip2: ", bzippedFilePath, "exists already. Doing nothing.")
            return 0
    else:
        print("bzip2: ", path, "does not exist. Doing nothing.")
        return 0


def bzip2DecompressFile(path, removeInput):
    if exists(path):
        bunzippedFilePath=path[0:len(path)-4]
        if not exists(bunzippedFilePath):
            print("Uncompressing ", path, "...")
            inputStream  = bz2.BZ2File(path, 'rb')
            outputStream = open(bunzippedFilePath, 'wb')

            try:
                outputStream.writelines(inputStream)
            except EOFError:
                print("Unexpected EOF detected in file: ", path)
                return 0
            finally:
                print("Closing ", path, " and ", bunzippedFilePath)
                outputStream.close()
                inputStream.close()
                if removeInput:
                    remove(path)
                return 1
        else:
            print("gunzip:", bunzippedFilePath, "exists already. Doing nothing.")
            return 1
    else:
        print("gunzip:", path, "does not exist. Doing nothing.")
        return 0
