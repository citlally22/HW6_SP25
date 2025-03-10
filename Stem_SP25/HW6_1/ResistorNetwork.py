#region imports
from scipy.optimize import fsolve
from Resistor import Resistor
from VoltageSource import VoltageSource
from Loop import Loop
#endregion

#region class definitions
class ResistorNetwork():
    #region constructor
    def __init__(self):
        """
        The resistor network consists of Loops, Resistors and Voltage Sources.
        This is the constructor for the network and it defines fields for Loops, Resistors and Voltage Sources.
        You can populate these lists manually or read them in from a file.
        """
        #region attributes
        self.Loops = []  # initialize an empty list of loop objects in the network
        self.Resistors = []  # initialize an empty a list of resistor objects in the network
        self.VSources = []  # initialize an empty a list of source objects in the network
        #endregion
    #endregion

    def LoadNetwork(self, filename):
        """
        Reads a resistor network from a text file and builds the circuit.
        :param filename: Name of the text file containing the circuit data.
        """
        with open(filename, "r") as file:
            Txt = file.readlines()  # Read all lines into a list

        N = 0  # Line index
        while N < len(Txt):
            line = Txt[N].strip().lower()

            if "<resistor>" in line:
                N = self.MakeResistor(N, Txt)  # Call MakeResistor to process resistors

            elif "<source>" in line:
                N = self.MakeVSource(N, Txt)  # Call MakeVSource to process voltage sources
            elif "<loop>" in line:
                N = self.MakeLoop(N, Txt)  # Call MakeLoop to process loops

            else:
                N += 1  # Move to the next line
         # 🛑 DEBUG PRINT: Show all resistors after loading
        print(f"✅ Final Resistors List: {self.Resistors}")

    #region methods
    def BuildNetworkFromFile(self, filename):
        """
        This function reads the lines from a file and processes the file to populate the fields
        for Loops, Resistors and Voltage Sources
        :param filename: string for file to process
        :return: nothing
        """
        FileTxt = open(filename,"r").read().split('\n')  # reads from file and then splits the string at the new line characters
        LineNum = 0  # a counting variable to point to the line of text to be processed from FileTxt
        # erase any previous
        self.Resistors = []
        self.VSources = []
        self.Loops = []
        LineNum = 0
        lineTxt = ""
        FileLength = len(FileTxt)
        while LineNum < FileLength:
            lineTxt = FileTxt[LineNum].lower().strip()
            if len(lineTxt) <1:
                pass # skip
            elif lineTxt[0] == '#':
                pass  # skips comment lines
            elif "resistor" in lineTxt:
                LineNum = self.MakeResistor(LineNum, FileTxt)
            elif "source" in lineTxt:
                LineNum = self.MakeVSource(LineNum, FileTxt)
            elif "loop" in lineTxt:
                LineNum = self.MakeLoop(LineNum, FileTxt)
            LineNum+=1
        pass

    def MakeResistor(self, N, Txt):
        """
        Make a resistor object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a resistor object
        """
        name = None
        resistance = None
        N += 1  # Move to the next line

        if N >= len(Txt):
            return N  # Prevent out-of-bounds errors

        txt = Txt[N].strip().lower()

        while N < len(Txt) and "</resistor>" not in txt:  # Read until </Resistor> tag
            if "<source>" in txt or "<loop>" in txt or "<resistor>" in txt:
                print(f"⚠️ Error: Unexpected section {txt} while reading resistor. Skipping.")
                return N

            if "name" in txt and "=" in txt:
                parts = txt.split("=")
                if len(parts) > 1:
                    name = parts[1].strip()
                else:
                    print(f"⚠️ Warning: Malformed name line at {N}: {txt}")

            elif "resistance" in txt and "=" in txt:
                parts = txt.split("=")
                if len(parts) > 1:
                    try:
                        resistance = float(parts[1].strip())  # Extract resistance
                    except ValueError:
                        print(f"❌ Error: Invalid resistance value at {N}: {txt}")
                else:
                    print(f"⚠️ Warning: Malformed resistance line at {N}: {txt}")

            N += 1
            if N >= len(Txt):
                break  # Prevent out-of-bounds error
            txt = Txt[N].strip().lower()

        # 🛑 DEBUG PRINT: Show extracted resistor info
        print(f"✅ Found Resistor - Name: {name}, Resistance: {resistance}")

        # Only add the resistor if it has both name and resistance
        if name and resistance is not None:
            R = Resistor(R=resistance, name=name)  # Create Resistor with extracted data
            self.Resistors.append(R)
        else:
            print(f"❌ Error: Skipping invalid resistor at line {N}. Missing name or resistance.")

        return N

    def MakeVSource (self, N, Txt):
        """
        Make a voltage source object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a voltage source object
        """
        VS=VoltageSource()
        N+=1
        txt = Txt[N].lower()
        while "source" not in txt:
            if "name" in txt:
                VS.Name = txt.split('=')[1].strip()
            if "value" in txt:
                VS.Voltage = float(txt.split('=')[1].strip())
            if "type" in txt:
                VS.Type = txt.split('=')[1].strip()
            N+=1
            txt=Txt[N].lower()

        self.VSources.append(VS)
        return N

    def MakeLoop(self, N, Txt):
        """
        Make a Loop object from reading the text file
        :param N: (int) Line number for current processing
        :param Txt: [string] the lines of the text file
        :return: a resistor object
        """
        L=Loop()
        N+=1
        txt = Txt[N].lower()
        while "loop" not in txt:
            if "name" in txt:
                L.Name = txt.split('=')[1].strip()
            if "nodes" in txt:
                txt=txt.replace(" ","")
                L.Nodes = txt.split('=')[1].strip().split(',')
            N+=1
            txt=Txt[N].lower()

        self.Loops.append(L)
        return N

    def AnalyzeCircuit(self):
        """
        Use fsolve to find currents in the resistor network.
        :return:
        """
        print(f"🔍 Debug: Resistors in Network BEFORE solving: {self.Resistors}")
        for r in self.Resistors:
            print(f"🛠️ Resistor: {r}, Name: {getattr(r, 'Name', 'MISSING')}, Resistance: {getattr(r, 'Resistance', 'MISSING')}")
        # need to set the currents to that Kirchoff's laws are satisfied
        i0 = [0.1, 0.1, 0.1]  #define an initial guess for the currents in the circuit
        i = fsolve(self.GetKirchoffVals,i0)

        print("✅ Computed Currents:")
        for idx, current in enumerate(i):
            print(f"I{idx + 1} = {current:.1f} A")

        # print output to the screen
        print("I1 = {:0.1f}".format(i[0]))
        print("I2 = {:0.1f}".format(i[1]))
        print("I3 = {:0.1f}".format(i[2]))
        return i

    def GetKirchoffVals(self,i):
        """
        This function uses Kirchoff Voltage and Current laws to analyze this specific circuit
        KVL:  The net voltage drop for a closed loop in a circuit should be zero
        KCL:  The net current flow into a node in a circuit should be zero
        :param i: a list of currents relevant to the circuit
        :return: a list of loop voltage drops and node currents
        """
        print(f"🔍 Debug: Resistors in Network DURING Kirchhoff Calculation: {self.Resistors}")

        # Now attempt to set current values
        for r in self.Resistors:
            print(
                f"🛠️ Checking Resistor: {r}, Name: {getattr(r, 'Name', 'MISSING')}, Resistance: {getattr(r, 'Resistance', 'MISSING')}")

        # set current in resistors in the top loop.
        self.GetResistorByName('ad').Current=i[0]  #I_1 in diagram
        self.GetResistorByName('bc').Current=i[0]  #I_1 in diagram
        self.GetResistorByName('cd').Current=i[2]  #I_3 in diagram
        #set current in resistor in bottom loop.
        self.GetResistorByName('ce').Current=i[1]  #I_2 in diagram
        #calculate net current into node c
        Node_c_Current = sum([i[0],i[1],-i[2]])

        KVL = self.GetLoopVoltageDrops()  # two equations here
        V1 = self.GetResistorByName('ad').DeltaV() + self.GetResistorByName('bc').DeltaV() - 32
        V2 = self.GetResistorByName('cd').DeltaV() + self.GetResistorByName('ce').DeltaV() - 0
        KVL.append(Node_c_Current)  # one equation here
        V3 = i[0] + i[1] - i[2]  # Kirchhoff’s Current Law (KCL)

        return KVL

    def GetElementDeltaV(self, name):
        """
        Need to retrieve either a resistor or a voltage source by name.
        :param name:
        :return:
        """
        for r in self.Resistors:
            if name == r.Name:
                return -r.DeltaV()
            if name[::-1] == r.Name:
                return -r.DeltaV()
        for v in self.VSources:
            if name == v.Name:
                return v.Voltage
            if name[::-1] == v.Name:
                return -v.Voltage

    def GetLoopVoltageDrops(self):
        """
        This calculates the net voltage drop around a closed loop in a circuit based on the
        current flowing through resistors (cause a drop in voltage regardless of direction of traversal) or
        the value of the voltage source that have been set up as positive based on the direction of traversal.
        :return: net voltage drop for all loops in the network.
        """
        loopVoltages=[]
        for L in self.Loops:
            # Traverse loops in order of nodes and add up voltage drops between nodes
            loopDeltaV=0
            for n in range(len(L.Nodes)):
                if n == len(L.Nodes)-1:
                    name = L.Nodes[0] + L.Nodes[n]
                else:
                    name = L.Nodes[n]+L.Nodes[n+1]
                loopDeltaV += self.GetElementDeltaV(name)
            loopVoltages.append(loopDeltaV)
        return loopVoltages

    def GetResistorByName(self, name):
        """
        A way to retrieve a resistor object from self.Resistors based on resistor name
        :param name:
        :return:
        """
        for r in self.Resistors:
            # 🛑 DEBUG PRINT: Print resistor details before accessing Name
            print(f"🔍 Checking Resistor: {r}")

            if not hasattr(r, "Name"):  # Check if Name exists
                print(f"❌ Error: Resistor object {r} has no attribute 'Name'")
                continue

            if r.Name == name:
                return r

        print(f"⚠️ Warning: Resistor {name} not found in network.")
        return None
    #endregion

class ResistorNetwork_2(ResistorNetwork):
    #region constructor
    def __init__(self):
        super().__init__()  # runs the constructor of the parent class
        #region attributes
        #endregion
    #endregion

    #region methods
    def AnalyzeCircuit(self):
        """Overrides AnalyzeCircuit to handle the modified circuit."""
        print("Analyzing modified resistor network (with 5Ω parallel resistor).")
        return super().AnalyzeCircuit()
        pass

    def GetKirchoffVals(self,i):
        """Overrides Kirchhoff analysis for the modified network."""
        print("Applying Kirchhoff’s laws to modified network.")
        return super().GetKirchoffVals(i)
        pass
    #endregion
#endregion
