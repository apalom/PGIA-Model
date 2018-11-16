#---- Define Parameters ----#
day = '2015-07-01'; # peak day for analysis

maxTrials = 300;
XFMR = 50; # Transformer rating (kVA)
XFMRlimit= 1.3 * XFMR;
secLimit = 218 # Amps for Overload Based [218 for 4/0 AL cables in DA411]
chgrRate = 12.9; # Average charger power rating (kW)
maxEV = 4;
maxPV = 4;
numHomes = 12;