# -*- coding: utf-8 -*-

import unittest

from subprocess import call
from tempfile import mkdtemp
from shutil import rmtree

from proctest import ProcTest
from subprocess import Popen, PIPE

class TrimNormalAndJoin(unittest.TestCase, ProcTest):
    inputs = ["abc", "ab", "y", "n",
              "jg", "jh", "kg"
    ]
    expectedOutputs = ["^abc/ab<n><def>$", "^ab/ab<n><ind>$", "^y/y<n><ind>$", "^n/*n$",
                       "^jg/j<pr>+g<n>$", "^jh/*jh$", "^kg/*kg$"
    ]
    expectedRetCode = 0

    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/minimal-mono.dix",
                                      tmpd+"/minimal-mono.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/minimal-bi.dix",
                                      tmpd+"/minimal-bi.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/minimal-mono.bin",
                                      tmpd+"/minimal-bi.bin",
                                      tmpd+"/minimal-trimmed.bin"],
                                     stdout=PIPE))

            self.cmdLine = ["../lttoolbox/.libs/lt-proc", "-z", tmpd+"/minimal-trimmed.bin"]
            self.proc = Popen(self.cmdLine, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            for inp,exp in zip(self.inputs, self.expectedOutputs):
                self.assertEqual( self.communicateFlush(inp+"[][\n]"),
                                  exp+"[][\n]" )

            self.proc.communicate() # let it terminate
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.assertEqual( self.proc.poll(),
                              self.expectedRetCode )


        finally:
            rmtree(tmpd)




class TrimCmp(unittest.TestCase, ProcTest):
    inputs = ["a", "b", "c", "d", "aa", "ab", "ac", "ad", "ba", "bb", "bc", "bd", "ca", "cb", "cc", "cd", "da", "db", "dc", "dd", ]
    expectedOutputs = ["^a/*a$", "^b/b<n>$", "^c/*c$", "^d/d<n>$", "^aa/*aa$", "^ab/a<n>+b<n>$", "^ac/*ac$", "^ad/a<n>+d<n>$", "^ba/*ba$", "^bb/*bb$", "^bc/*bc$", "^bd/*bd$", "^ca/*ca$", "^cb/d<n>+b<n>$", "^cc/*cc$", "^cd/d<n>+d<n>$", "^da/*da$", "^db/*db$", "^dc/*dc$", "^dd/*dd$"]
    expectedRetCode = 0

    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/cmp-mono.dix",
                                      tmpd+"/cmp-mono.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/cmp-bi.dix",
                                      tmpd+"/cmp-bi.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/cmp-mono.bin",
                                      tmpd+"/cmp-bi.bin",
                                      tmpd+"/cmp-trimmed.bin"],
                                     stdout=PIPE))

            self.cmdLine = ["../lttoolbox/.libs/lt-proc", "-e", "-z", tmpd+"/cmp-trimmed.bin"]
            self.proc = Popen(self.cmdLine, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            for inp,exp in zip(self.inputs, self.expectedOutputs):
                self.assertEqual( self.communicateFlush(inp+"[][\n]"),
                                  exp+"[][\n]" )

            self.proc.communicate() # let it terminate
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.assertEqual( self.proc.poll(),
                              self.expectedRetCode )


        finally:
            rmtree(tmpd)





class TrimLongleft(unittest.TestCase, ProcTest):
    inputs = ["herdende"]
    expectedOutputs = ["^herdende/herde<adj><pprs>$"]
    expectedRetCode = 0

    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/longleft-mono.dix",
                                      tmpd+"/longleft-mono.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/longleft-bi.dix",
                                      tmpd+"/longleft-bi.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/longleft-mono.bin",
                                      tmpd+"/longleft-bi.bin",
                                      tmpd+"/longleft-trimmed.bin"],
                                     stdout=PIPE))

            self.cmdLine = ["../lttoolbox/.libs/lt-proc", "-e", "-z", tmpd+"/longleft-trimmed.bin"]
            self.proc = Popen(self.cmdLine, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            for inp,exp in zip(self.inputs, self.expectedOutputs):
                self.assertEqual( self.communicateFlush(inp+"[][\n]"),
                                  exp+"[][\n]" )

            self.proc.communicate() # let it terminate
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.assertEqual( self.proc.poll(),
                              self.expectedRetCode )


        finally:
            rmtree(tmpd)

class BidixPardef(unittest.TestCase, ProcTest):
    inputs = ["c"]
    expectedOutputs = ["^c/c<vblex><inf>$"]
    expectedRetCode = 0

    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/bidixpardef-mono.dix",
                                      tmpd+"/bidixpardef-mono.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "rl", # rl!
                                      "data/bidixpardef-bi.dix",
                                      tmpd+"/bidixpardef-bi.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/bidixpardef-mono.bin",
                                      tmpd+"/bidixpardef-bi.bin",
                                      tmpd+"/bidixpardef-trimmed.bin"],
                                     stdout=PIPE))

            self.cmdLine = ["../lttoolbox/.libs/lt-proc", "-z", tmpd+"/bidixpardef-trimmed.bin"]
            self.proc = Popen(self.cmdLine, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            for inp,exp in zip(self.inputs, self.expectedOutputs):
                self.assertEqual( self.communicateFlush(inp+"[][\n]"),
                                  exp+"[][\n]" )

            self.proc.communicate() # let it terminate
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.assertEqual( self.proc.poll(),
                              self.expectedRetCode )


        finally:
            rmtree(tmpd)



class UnbalancedEpsilons(unittest.TestCase, ProcTest):
    inputs = ["re", "rer", "res", "ret"]
    expectedOutputs = ["^re/re<vblex><inf>$", "^rer/re<vblex><pres>$", "^res/re<vblex><pres>$", "^ret/re<vblex><pret>$"]
    expectedRetCode = 0

    def runTest(self):
        tmpd = mkdtemp()
        try:
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "lr",
                                      "data/unbalanced-epsilons-mono.dix",
                                      tmpd+"/unbalanced-epsilons-mono.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-comp",
                                      "rl", # rl!
                                      "data/unbalanced-epsilons-bi.dix",
                                      tmpd+"/unbalanced-epsilons-bi.bin"],
                                     stdout=PIPE))
            self.assertEqual(0, call(["../lttoolbox/lt-trim",
                                      tmpd+"/unbalanced-epsilons-mono.bin",
                                      tmpd+"/unbalanced-epsilons-bi.bin",
                                      tmpd+"/unbalanced-epsilons-trimmed.bin"],
                                     stdout=PIPE))

            self.cmdLine = ["../lttoolbox/.libs/lt-proc", "-z", tmpd+"/unbalanced-epsilons-trimmed.bin"]
            self.proc = Popen(self.cmdLine, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            for inp,exp in zip(self.inputs, self.expectedOutputs):
                self.assertEqual( self.communicateFlush(inp+"[][\n]"),
                                  exp+"[][\n]" )

            self.proc.communicate() # let it terminate
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.assertEqual( self.proc.poll(),
                              self.expectedRetCode )


        finally:
            rmtree(tmpd)