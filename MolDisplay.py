import molecule;


header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;

#Atom class
class Atom:
    #set the values of the atom
    def __init__ (self, c_atom):
        self.c_atom = c_atom;
        self.z = c_atom.z;

    #print the values of the atom
    def __str__ (self):
        element = self.c_atom.element;
        x = self.c_atom.x;
        y = self.c_atom.y;
        z = self.c_atom.z;
        return "Element: %c X: %f Y: %f Z: %f"%(element,x,y,z );

    #calculate x and y coord then print the svg details of the atom
    def svg(self):
        xcord = self.c_atom.x * 100.0 + offsetx;
        ycord = self.c_atom.y * 100.0 + offsety;
        if self.c_atom.element in radius:
            rad = radius[self.c_atom.element];
            col = element_name[self.c_atom.element];
        else:
            col = "hold"
            rad = 20;
        # rad = radius[self.c_atom.element];
        # col = element_name[self.c_atom.element]; 
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n'%(xcord, ycord, rad, col);

#Bond class
class Bond:
    #initalize bond struct
    def __init__(self, c_bond):
        self.c_bond = c_bond;
        self.z = c_bond.z;

    #print to test if right values from bond 
    def __str__(self):
        return "A1: %d A2: %d EPair: %d x1: %f x2: %f y1: %f y2: %f z: %f len: %f dx: %f dy: %f "%(self.c_bond.a1 + 1, self.c_bond.a2 + 1, self.c_bond.epairs, self.c_bond.x1, self.c_bond.x2, self.c_bond.y1, self.c_bond.y2, self.c_bond.z, self.c_bond.len, self.c_bond.dx, self.c_bond.dy);
    
    #return rectangle that represents bonds from x1,x2,x3,x4 points
    def svg(self):
        x1 = (self.c_bond.x1 * 100 +offsetx) + self.c_bond.dy*10;
        y1 = (self.c_bond.y1 * 100 +offsety) - self.c_bond.dx*10;
        x2 = (self.c_bond.x1 * 100 +offsetx) - self.c_bond.dy*10;
        y2 = (self.c_bond.y1 * 100 +offsety) + self.c_bond.dx*10;
        x3 = (self.c_bond.x2 * 100 +offsetx) + self.c_bond.dy*10;
        y3 = (self.c_bond.y2 * 100 +offsety) - self.c_bond.dx*10;
        x4 = (self.c_bond.x2 * 100 +offsetx) - self.c_bond.dy*10;
        y4 =(self.c_bond.y2 * 100 +offsety) + self.c_bond.dx*10;
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n'%(x1,y1,x2,y2,x4,y4,x3,y3);

#molecule class that is a subclass of parent molecule
class Molecule(molecule.molecule):
    #prints out all atoms and bonds        
    def __str__(self):
        for i in range(self.atom_no):
            atom = self.get_atom(i);
            newAtom = Atom(atom)
            print(newAtom);
        for i in range(self.bond_no):
            bond = self.get_bond(i);
            newBond = Bond(bond);
            print(newBond);
        return ""
    #returns svg for the entire molecule
    def svg(self):
        #initalize lists for atom, bond, and combination of both
        atom_list = [];
        bond_list = [];
        order_list = [];
        #string to hold header
        temp = header;
        #loop through each atom and append to list
        for i in range(self.atom_no):
            atom = self.get_atom(i);
            newAtom = Atom(atom);
            atom_list.append(newAtom);
        #loop through each bond and append to list
        for i in range(self.bond_no):
            bond = self.get_bond(i);
            newBond = Bond(bond);
            bond_list.append(newBond);
        i = 0;
        j = 0;
        atom_no = self.atom_no;
        bond_no = self.bond_no;
        while i < atom_no and j < bond_no:
            if atom_list[i].z < bond_list[j].z:
                order_list.append(atom_list[i])
                i += 1
            else:
                order_list.append(bond_list[j])
                j += 1
        while i < atom_no:
            order_list.append(atom_list[i])
            i += 1
        while j < bond_no:
            order_list.append(bond_list[j])
            j += 1
        for i in range(len(order_list)):
            # print(order_list[i].z)
            temp = temp + order_list[i].svg();
        return temp + footer;


    #used to parse sdf files for molecules
    def parse(self, file_o):
        #read in lines from file
        content = file_o.readlines()
        #start at fourth line
        temp = content[3];
        #remove all existing spaces
        hold = temp.split();
        #store atom_no and bond_no
        atom_no = int(hold[0]);
        bond_no = int(hold[1]);
        start_atom = 4;
        stop_atom = atom_no+4
        #line ranges for atom information and then bond information
        atom_range = range(start_atom, stop_atom);
        bond_range = range(stop_atom, stop_atom + bond_no);
        #loop through atom section and append atom information
        for i in atom_range:
            temp = content[i];
            hold = temp.split();
            self.append_atom(hold[3], float(hold[0]), float(hold[1]), float(hold[2]));
        #loop through bond section and append bond information
        for i in bond_range:
            temp = content[i];
            hold = temp.split();
            self.append_bond(int(hold[0]) - 1, int(hold[1]) - 1, int(hold[2]));
        #close file
        file_o.close();
