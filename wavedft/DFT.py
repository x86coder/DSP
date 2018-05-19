#!/usr/bin/python

# Program:      wavedft - Obtains the DFT (discrete fourier transform) of a Wave audio file.
# Author:       Jaime Reyes Rdz.
# Date:         05-16-2018
# Target:       Python 2
# Control file number: dft755.py
#
# Line 58 and onwards: Solve DFT by calculating its real and imaginary parts individually.
# exp_e(i(theta)) is just one number, so we calculate its components
# individually of each other, as we've seen in any complex variable book.
# Also, if z=a+bi AND w=c+di THEN w+z=(a+c)+i(b+d)

import math
import sys
import wave             # for reading .wav files.
import struct           # for unpacking binary data in .wav file

N           = 0     # Number of audio frames (or signal length in points)
K           = N/2   # DFT size
x           = []    # time series (or signal)

verboseMode         = False
completedPercent    = 0

if ( len(sys.argv) > 1 ):
    try:
        F = wave.open(sys.argv[1], "rb")
        N = F.getnframes()

        if len(sys.argv) > 2:
            if sys.argv[2] == "--v" or sys.argv[2] == "--V":
                verboseMode = True

        #if verboseMode:
        #    print "\t > File: \t\t" + sys.argv[1]
        #    print "\t > N channels \t\t" + str( F.getnchannels() )
        #    print "\t > Sample width \t" + str( F.getsampwidth() )
        #    print "\t > Frame rate \t\t" + str( F.getframerate() )
        #    print "\t > Frame count \t\t" + str(N)

        for i in range(0,N):
            v = struct.unpack("<h", F.readframes(1)); # < stands for little-endian, h stands for signed short (16-bit)
            x.append(v[0])
        # To view value (shows error)
        #print int(W.readframes(1), 16)

        K = N/2     # Indeed, I'm not interested in calculating the upper half of frequencies.
                    # Since they may be aliased (?)

        X           = [0.0] * K    # Magnitude (fill array K times with 0.0)
        partialsRe  = [0.0] * K
        partialsIm  = [0.0] * K
        X2          = [0.0] * K    # Phase

        for k in range(0,K):
            # n/N = t = time
            # k = freq
            for n in range(0,N):
                partialsRe[k] += x[n] * math.cos(2*math.pi * k * (n/float(N)))
                partialsIm[k] -= x[n] * math.sin(2*math.pi * k * (n/float(N)))
            Mag = math.sqrt(partialsRe[k] * partialsRe[k] + partialsIm[k] * partialsIm[k])/N
            X[k] = Mag
            if verboseMode:
                print str(k) + "," + str(Mag)

            y1 = partialsIm[k]
            x1 = partialsRe[k]
            if partialsRe[k] == 0.0:
                x1 = 0.0000001          # Make it as close as possible to zero, to allow it as divisor.

            X2[k] = math.atan( y1/x1 )

            # Just an estimation
            if not verboseMode:
                if (k+1) % (K/100) == 0:
                    completedPercent = completedPercent + 1
                    if completedPercent < 100:
                        print str(completedPercent) + "%"

        if not verboseMode:
            import pyqtgraph as pq  # for plotting (graphing).
            pq.plot(x, title="Original waveform")
            pq.plot(X2, title="Fourier transform phase plot")
            pq.plot(X, title="Fourier transform spectrogram")

            if __name__ == '__main__':
                if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
                    pq.QtGui.QApplication.exec_()
    except IOError:
        print " * Cannot open file: " + sys.argv[1]

else:
    print " * Specify input *.WAV file!"
