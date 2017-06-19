import pprint as pp
import os,sys

def getCrimesList(borough):
  # Get current working path
  DIRPATH = os.path.dirname(os.path.realpath(__file__))

  keys = []
  crimes = []

  got_keys = False
  #with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:

  with open(DIRPATH+'\\'+'filtered_crimes_' + borough + '.csv') as f:
      for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            got_keys = True
            continue

        #d = {}
        # for i in range(len(line)-1):
        #     d[keys[i]] = line[i]
        if not(line[19] == '' or line[20] == ''):
          crimes.append((float(line[19]),float(line[20])))
      return crimes