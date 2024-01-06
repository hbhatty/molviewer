import MolDisplay;
import os;
import sqlite3;

class Database:
    # initalizes our connection to db
    def __init__(self, reset=False):
        if reset == True:
            os.remove("molecules.db");
        self.connec = sqlite3.connect("molecules.db");
    
    #creates inital tables
    def create_tables(self):
        #create elements table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS Elements 
                    ( ELEMENT_NO           INTEGER NOT NULL,
                    ELEMENT_CODE         VARCHAR(3) NOT NULL,
                    ELEMENT_NAME         VARCHAR(32) NOT NULL,
                    COLOUR1              CHAR(6) NOT NULL,
                    COLOUR2              CHAR(6) NOT NULL,
                    COLOUR3              CHAR(6) NOT NULL,
                    RADIUS               DECIMAL(3) NOT NULL,
                    PRIMARY KEY (ELEMENT_CODE) );""" );
        
        #create atoms table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS Atoms
                 ( ATOM_ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   ELEMENT_CODE     VARCHAR(3) NOT NULL,
                   X                DECIMAL(7,4) NOT NULL,
                   Y                DECIMAL(7,4) NOT NULL,
                   Z                DECIMAL(7,4) NOT NULL,
                   FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements
                   );""" );
        
        #create bonds table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS Bonds
                 ( BOND_ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                   A1       INTEGER NOT NULL,
                   A2       INTEGER NOT NULL,
                   EPAIRS   INTEGER NOT NULL
                   )""" );
        
        #create Molecules table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS Molecules
                 ( MOLECULE_ID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NUll,
                   NAME             TEXT NOT NULL UNIQUE
                   )""" );
        
        #create MoleculeAtom table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS MoleculeAtom
                 ( MOLECULE_ID      INTEGER NOT NULL,
                   ATOM_ID          INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (ATOM_ID) REFERENCES Atoms
                   );""" );
        
        #create MoleculeBond table, checks if it doesnt exist already
        self.connec.execute( """CREATE TABLE IF NOT EXISTS MoleculeBond
                 ( MOLECULE_ID      INTEGER NOT NULL,
                   BOND_ID          INTEGER NOT NULL,
                   PRIMARY KEY (MOLECULE_ID, BOND_ID),
                   FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                   FOREIGN KEY (BOND_ID) REFERENCES Bonds
                   );""" );
    
    #initalizes values in our table
    def __setitem__(self, table, values):
        self.connec.execute(f"""INSERT INTO {table} VALUES {values}""")

    #adds each atom passed in from add_molecule to our tables
    def add_atom(self, molname, atom):
         #insert inital atom values into atoms table
         self.connec.execute("INSERT INTO Atoms (ELEMENT_CODE, X, Y, Z) VALUES('%s', %f, %f, %f)" %(atom.element, atom.x, atom.y, atom.z));
         #create cursor object
         cursor = self.connec.cursor();
         #get all atom_ids from atom table
         atoms = cursor.execute("SELECT Atoms.ATOM_ID FROM Atoms").fetchall()
         #convert tuple into integer
         atom_last = int(''.join(map(str, atoms[len(atoms)- 1])))
         #initalize second cursor object
         cursor2 = self.connec.cursor();
         #fetch where molecule name is matched in molecules table
         id = cursor2.execute("SELECT * FROM Molecules WHERE Molecules.Name = '%s'"%(molname)).fetchall()
         #insert into molecule_atom with found IDs
         self.connec.execute("INSERT INTO MoleculeAtom (MOLECULE_ID, ATOM_ID) VALUES (%d, %d)" %(id[0][0], atom_last))
         
    #adds each bond passed in from add_molecule to our tables
    def add_bond(self, molname, bond):
        #insert inital bond values into bonds table
        self.connec.execute("INSERT INTO Bonds(A1, A2, EPAIRS) VALUES(%d, %d, %d)" %(bond.a1, bond.a2, bond.epairs));
        #create cursor objec
        cursor = self.connec.cursor()
        #select all bond_ids from table
        cursor.execute("SELECT Bonds.BOND_ID FROM Bonds")
        #fetch all of them
        bonds = cursor.fetchall()
        #convert tuple into integer
        bond_last = int(''.join(map(str, bonds[len(bonds)- 1])))
        #initalize second cursor object
        cursor2 = self.connec.cursor();
        #fetch where molecule name is matched in molecules table
        id = cursor2.execute("SELECT * FROM Molecules WHERE Molecules.Name = '%s'"%(molname)).fetchall()
        #insert into molecule_bond with found IDs
        self.connec.execute("INSERT INTO MoleculeBond (MOLECULE_ID, BOND_ID) VALUES (%d, %d)" %(id[0][0], bond_last))

    def add_molecule(self, name, fp):
        #initalize moldisplay object
        mol = MolDisplay.Molecule();
        #parse fp
        mol.parse(fp);
        #inert molecule name into molecules table
        self.connec.execute("INSERT INTO Molecules(NAME) VALUES('%s')" %(name));
        #hold atom_no and bond_no
        atom_num = mol.atom_no;
        bond_num = mol.bond_no;
        #loop to call add_atom and pass in the name, and each atom with get_atom
        for i in range(atom_num):
            self.add_atom(name, mol.get_atom(i));
        #loop to call add_bond and pass in name, and each bond with get_bond
        for i in range(bond_num):
            self.add_bond(name, mol.get_bond(i));

    def load_mol(self, name):
        #initalize object
        mol = MolDisplay.Molecule()
        #create cursor obj
        cursor1 = self.connec.cursor()
        #select where conditions fit
        cursor1.execute("SELECT * FROM Atoms, Molecules, MoleculeAtom WHERE Molecules.NAME = '%s' AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID AND MoleculeAtom.ATOM_ID=Atoms.ATOM_ID ORDER BY Atoms.ATOM_ID ASC" %(name))
        #fetch table results
        curs1 = cursor1.fetchall()
        #create cursor obj
        cursor2 = self.connec.cursor()
        #select where conditions fit
        cursor2.execute("SELECT * FROM Bonds, Molecules, MoleculeBond WHERE Molecules.NAME = '%s' AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID AND MoleculeBond.BOND_ID=Bonds.BOND_ID ORDER BY Bonds.BOND_ID ASC" %(name))
        #fetch table results
        curs2 = cursor2.fetchall()
        #loop through and append each result
        for i in range (len(curs1)):
            mol.append_atom(curs1[i][1], float(curs1[i][2]), float(curs1[i][3]), float(curs1[i][4]))
        #loop through and append each result
        for j in range (len(curs2)):
            mol.append_bond(int(curs2[j][1]), int(curs2[j][2]), int(curs2[j][3]))
        #return obj
        return mol
    
    def radius(self):
        #initalize cursor obj
        cursor1 = self.connec.cursor()
        #select element code and radius
        cursor1.execute("SELECT Elements.ELEMENT_CODE, Elements.RADIUS FROM Elements");
        #fetch results
        curs1 = cursor1.fetchall()
        #create empty dictionary
        dic = {
        }
        #loop through and populate dictionary
        for i in range (len(curs1)):
            dic[curs1[i][0]] = curs1[i][1]
        #return dictionary
        return dic;

    def element_name(self):
        #initalize cursor obj
        cursor1 = self.connec.cursor()
        #select element code and name
        cursor1.execute("SELECT Elements.ELEMENT_CODE, Elements.ELEMENT_NAME FROM Elements");
        #fetch results
        curs1 = cursor1.fetchall()
        #create empty dictionary
        dic = {
        }
        #loop through and populate dictionary
        for i in range (len(curs1)):
            dic[curs1[i][0]] = curs1[i][1]
        #return dictionary
        return dic
    
    def radial_gradients(self):
        #initalize empty string
        radialGradientSVG = """
            <radialGradient id="hold" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                <stop offset="0%" stop-color="#FFFFFF"/>
                <stop offset="50%" stop-color="#050505"/>
                <stop offset="100%" stop-color="#020202"/>
            </radialGradient>""";
        #create cursor obj
        cursor1 = self.connec.cursor();
        #select name and colours from element talbe
        cursor1.execute("SELECT Elements.ELEMENT_NAME, Elements.COLOUR1, Elements.COLOUR2, Elements.COLOUR3 FROM Elements");
        #fetch results
        curs1 = cursor1.fetchall()
        #loop through length of curs1 and string substitute tuple values from curs1
        for i in range(len(curs1)):
            radialGradientSVG += """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>"""%(curs1[i][0], curs1[i][1], curs1[i][2], curs1[i][3]);
        #return string
        return radialGradientSVG;

# if __name__ == "__main__":
#     db = Database(reset=True);
#     db.create_tables();
#     db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25.3 );
#     db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
#     db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
#     db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
#     fp = open( 'water.sdf' );
#     db.add_molecule( 'Water', fp );
#     fp = open( 'caffeine.sdf' );
#     db.add_molecule( 'Caffeine', fp );
#     fp = open( 'CID.sdf' );
#     db.add_molecule( 'Isopentanol', fp );
#     # mol = db.load_mol('Water');
#     # print(db.radial_gradients())
#     # db = Database(reset=False); # or use default
#     MolDisplay.radius = db.radius();
#     MolDisplay.element_name = db.element_name();
#     MolDisplay.header += db.radial_gradients();
#     for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
#         mol = db.load_mol( molecule );
#         mol.sort();
#         fp = open( molecule + ".svg", "w" );
#         fp.write( mol.svg() );
#         fp.close()
#     print("Elements Table")
#     for row in db.connec.execute(f"SELECT * from {'Elements'}").fetchall():
#         print(row)
#     print("Molecules Table")
#     for row in db.connec.execute(f"SELECT * from {'Molecules'}").fetchall():
#         print(row)
#     print("Atoms Table")
#     for row in db.connec.execute(f"SELECT * from {'Atoms'}").fetchall():
#         print(row)
#     print("Bonds Table")
#     for row in db.connec.execute(f"SELECT * from {'Bonds'}").fetchall():
#         print(row)
#     print("MoleculeAtom Table") 
#     for row in db.connec.execute(f"SELECT * from {'MoleculeAtom'}").fetchall():
#         print(row)
#     print("MoleculeBond Table")
#     for row in db.connec.execute(f"SELECT * from {'MoleculeBond'}").fetchall():
#         print(row)
#     print( db.connec.execute( "SELECT * FROM Elements;").fetchall() );
#     print("===========================================");
#     print("Molecules Table")
#     print( db.connec.execute( "SELECT * FROM Molecules;" ).fetchall() );
#     print("===========================================");
#     print("Atoms Table")
#     print( db.connec.execute( "SELECT * FROM Atoms;" ).fetchall() );
#     print("===========================================");
#     print("Bonds Table")
#     print( db.connec.execute( "SELECT * FROM Bonds;" ).fetchall() );
#     print("===========================================");
#     print("MoleculeAtom Table")
#     print( db.connec.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
#     print("===========================================");
#     print("MoleculeBond Table")
#     print( db.connec.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );