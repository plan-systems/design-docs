#!/usr/bin/python
#
# Inspired by http://preshing.com/20110504/hash-collision-probabilities/
#
# The purpose of this script is to print out the hash collision odds various hashspace sizes,
#    also known as a the "birthday problem" in another form.  See the above link.
#
# For example, in a hashspace size of 2^160, the chances of a hash collision occurring if you
#    generate 10^17 random hashes is about the odds of a meteor hitting your home. In software design, 
#    this question appears as: what hashspace size do I need in order to effectively rule out
#    hash collisions, given that I expect there to be N "draws" in the hashspace and I want
#    the odds to be no worse than P. 
#
# Output:
"""
Collision Odds        4 bytes          8 bytes          16 bytes         20 bytes         24 bytes         32 bytes         64 bytes
--------- ----        - -----          - -----          -- -----         -- -----         -- -----         -- -----         -- -----

1 in 2                65536            4.3 billion      1.8e+19          1.2e+24          7.9e+28          3.4e+38          1.2e+77
1 in 100              9269             607 million      2.6e+18          1.7e+23          1.1e+28          4.8e+37          1.6e+76
1 in 1000             2931             192 million      8.2e+17          5.4e+22          3.5e+27          1.5e+37          5.2e+75
1 in 10000            927              60 million       2.6e+17          1.7e+22          1.1e+27          4.8e+36          1.6e+75
1 in 100000           294              19 million       8.2e+16          5.4e+21          3.5e+26          1.5e+36          5.2e+74
1 in 1 million        93               6 million        2.6e+16          1.7e+21          1.1e+26          4.8e+35          1.6e+74
1 in 10 million       30               1 million        8.2e+15          5.4e+20          3.5e+25          1.5e+35          5.2e+73
1 in 100 million      10               607401           2.6e+15          1.7e+20          1.1e+25          4.8e+34          1.6e+73
1 in 1 billion        3                192077           825 trillion     5.4e+19          3.5e+24          1.5e+34          5.2e+72
1 in 10 billion       1                60741            260.9 trillion   1.7e+19          1.1e+24          4.8e+33          1.6e+72
1 in 100 billion      1                19208            82.5 trillion    5.4e+18          3.5e+23          1.5e+33          5.2e+71
1 in 1 trillion       1                6075             26.1 trillion    1.7e+18          1.1e+23          4.8e+32          1.6e+71
1 in 10 trillion      1                1921             8.2 trillion     5.4e+17          3.5e+22          1.5e+32          5.2e+70
1 in 100 trillion     1                608              2.6 trillion     1.7e+17          1.1e+22          4.8e+31          1.6e+70
1 in 1e+15            1                193              825 billion      5.4e+16          3.5e+21          1.5e+31          5.2e+69
1 in 1e+16            1                61               260.9 billion    1.7e+16          1.1e+21          4.8e+30          1.6e+69
1 in 1e+17            1                20               82.5 billion     5.4e+15          3.5e+20          1.5e+30          5.2e+68
1 in 1e+18            1                7                26.1 billion     1.7e+15          1.1e+20          4.8e+29          1.6e+68
1 in 1e+19            1                2                8.2 billion      540.6 trillion   3.5e+19          1.5e+29          5.2e+67
"""



import math

N = 2^32
probUnique = 1.0

oddsList = [
    2,
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
    100000000,
    1000000000,     # 1 billion
    1e10,
    1e11,
    1e12,
    1e13,
    1e14,
    1e15,
    1e16,
    1e17,
    1e18,
    1e19,
]

bitList = [
    32,
    64,
    128,
    160,
    192,
    256,
    512,
]


def getPrettyInt(N):
    fN = float(N)
    if fN < 1000000.:
        s = "%d" % int(fN)
    elif fN < 1e9:
        s = "%.1f million" % math.floor(fN/1e6)
    elif fN < 1e12:
        s = "%.1f billion" % (fN/1e9)
    elif fN < 1e15:
        s = "%.1f trillion" % (fN/1e12)
    else:
        s = "%.1e" % fN

    s = s.replace( ".0", "", 1 )
    s = s.replace( " 1 ", " a " )

    return "%-17s" % s


if 1:
    line = "%-22s" % "Collision Odds"
    for numBits in bitList:
        line += "%-17s" % ("%d bytes" % (numBits/8))
    print line

    lineChars = []
    for i in xrange(len(line)):
        if line[i] == ' ':
            lineChars.append( ' ' )
        else:
            lineChars.append( '-' )

    print "".join(lineChars)
    print

for odds in oddsList:
    line = '1 in ' + getPrettyInt(odds)
    Pcollision = 1./float(odds)
    for numBits in bitList:
        N = float(2**numBits)
        numPicksNeeded = math.ceil( math.sqrt(2. * N * Pcollision) )
        line += getPrettyInt(numPicksNeeded)
    print line




