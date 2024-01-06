from http.server import HTTPServer, BaseHTTPRequestHandler
import sys;
import json
import molsql
import MolDisplay;
import molecule;

db = molsql.Database(reset=False)
db.create_tables()

class myHandler(BaseHTTPRequestHandler):
    #used for client get request
    def do_GET(self):
        if self.path == "/":
            file = open("index.html", "r")
            home = file.read();
            #valid response if everything is working
            self.send_response(200)
            #print out html information on screen
            self.send_header("Content-type", 'text/html')
            self.send_header( "Content-length", len(home) );
            self.end_headers()
            self.wfile.write(bytes(home, "utf-8"))
            file.close()
        elif self.path == "/script.js":
            file = open("script.js", "r")
            scripts = file.read()
            self.send_response(200)
            #print out html information on screen
            self.send_header("Content-type", 'text/javascript')
            self.send_header( "Content-length", len(scripts) );
            self.end_headers()
            self.wfile.write(bytes(scripts, "utf-8"))
            file.close()
        elif self.path == "/styles.css":
            file = open("styles.css", "r")
            style = file.read()
            self.send_response(200)
            #print out html information on screen
            self.send_header("Content-type", 'text/css')
            self.send_header( "Content-length", len(style) );
            self.end_headers() 
            self.wfile.write(bytes(style, "utf-8")) 
            file.close() 
        elif self.path == "/sdfpage.html":
            file = open("sdfpage.html", "r")
            next = file.read();
            #valid response if everything is working
            self.send_response(200)
            #print out html information on screen
            self.send_header("Content-type", 'text/html')
            self.send_header( "Content-length", len(next) );
            self.end_headers()
            self.wfile.write(bytes(next, "utf-8"))
            file.close()
        elif self.path == '/info':
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            cursor = db.connec.cursor()
            cursor.execute("SELECT Elements.ELEMENT_NAME From Elements")
            element_name = cursor.fetchall()
            new = str(element_name);
            new = new.replace("[", "");
            new = new.replace("]", "");
            new = new.replace("(", "");
            new = new.replace("'", "");
            new = new.replace(")", "");
            new = new.replace(",", "");
            self.end_headers() 
            self.wfile.write(bytes(new, "utf-8"))
            # self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        elif self.path == '/checkcode':
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            cursor = db.connec.cursor()
            cursor.execute("SELECT Elements.ELEMENT_CODE From Elements")
            element_name = cursor.fetchall()
            new = str(element_name);
            new = new.replace("[", "");
            new = new.replace("]", "");
            new = new.replace("(", "");
            new = new.replace("'", "");
            new = new.replace(")", "");
            new = new.replace(",", "");
            print(new)
            self.end_headers() 
            self.wfile.write(bytes(new, "utf-8"))
        elif self.path == "/checkmol":
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            cursor = db.connec.cursor()
            cursor.execute("SELECT Molecules.Name From Molecules")
            element_name = cursor.fetchall()
            new = str(element_name);
            new = new.replace("[", "");
            new = new.replace("]", "");
            new = new.replace("(", "");
            new = new.replace("'", "");
            new = new.replace(")", "");
            new = new.replace(",", "");
            self.end_headers() 
            self.wfile.write(bytes(new, "utf-8"))
        elif self.path == "/getno":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            cursor = db.connec.cursor()
            cursor.execute("SELECT Molecules.Name From Molecules")
            hold = cursor.fetchall()
            hold_length = len(hold)
            send = ""
            for i in range(hold_length):
                hold[i] = str(hold[i])
                hold[i] = hold[i].replace("[", "");
                hold[i] = hold[i].replace("]", "");
                hold[i] = hold[i].replace("(", "");
                hold[i] = hold[i].replace("'", "");
                hold[i] = hold[i].replace(")", "");
                hold[i] = hold[i].replace(",", "");
                data = db.load_mol(hold[i]);
                send += "Molecule: "+hold[i] + " Atom #: "+ str(data.atom_no) + " Bond #: "+ str(data.bond_no) + ","
            self.end_headers()
            print(send)
            self.wfile.write(bytes(send, "utf-8"))
        else:
            #error message if error occurs
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 not found", "utf-8"))
            
    #used for client post request
    def do_POST(self):
        if self.path == "/addelement":
            #valid response if everything is fine
            self.send_response(200)
            #find length of the request, used to read in that amount
            length = int(self.headers.get('Content-Length'))
            info = self.rfile.read(length)
            #decode file information into proper format
            convert = info.decode("utf-8");
            data = json.loads(convert)
            # print(data)
            db['Elements'] = (data["elnum"], data["elcode"], data["elname"], data["elecol1"], data["elecol2"], data["elecol3"], data["rad"]);
            print(db.connec.execute("SELECT * FROM Elements;").fetchall())
            self.end_headers()
        elif self.path == "/displaymol":
            self.send_response(200);
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            length = int(self.headers.get("Content-Length"))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            data = json.loads(convert)
            molD = db.load_mol(data["select"]);
            molD.sort();
            svgSend = molD.svg()
            self.send_header("Content-type", "text/html");
            self.end_headers()
            self.wfile.write(bytes(svgSend, "utf-8"))
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/rotatemolx":
            self.send_response(200);
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            length = int(self.headers.get("Content-Length"))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            data = json.loads(convert)
            molD = db.load_mol(data["select"]) 
            molD.sort()
            mx = molecule.mx_wrapper(int(data["xInput"]),0,0);
            molD.xform(mx.xform_matrix);
            molD.sort()
            svgSend = molD.svg()
            print(svgSend)
            self.send_header("Content-type", "text/html");
            self.end_headers()
            self.wfile.write(bytes(svgSend, "utf-8"))
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/rotatemoly":
            self.send_response(200);
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            length = int(self.headers.get("Content-Length"))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            data = json.loads(convert)
            molD = db.load_mol(data["select"]) 
            molD.sort()
            mx = molecule.mx_wrapper(0,int(data["yInput"]),0);
            molD.xform(mx.xform_matrix);
            molD.sort()
            svgSend = molD.svg()
            print(svgSend)
            self.send_header("Content-type", "text/html");
            self.end_headers()
            self.wfile.write(bytes(svgSend, "utf-8"))
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/rotatemolz":
            self.send_response(200);
            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()
            length = int(self.headers.get("Content-Length"))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            data = json.loads(convert)
            molD = db.load_mol(data["select"]) 
            molD.sort()
            mx = molecule.mx_wrapper(0,0,int(data["zInput"]));
            molD.xform(mx.xform_matrix);
            molD.sort()
            svgSend = molD.svg()
            print(svgSend)
            self.send_header("Content-type", "text/html");
            self.end_headers()
            self.wfile.write(bytes(svgSend, "utf-8"))
            MolDisplay.radius = ""
            MolDisplay.element_name = ""
            MolDisplay.header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""
        elif self.path == "/deleteelement":
            self.send_response(200)
            print(MolDisplay.header)
            length = int(self.headers.get('Content-Length'))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            db.connec.execute("DELETE FROM Elements WHERE Elements.ELEMENT_NAME = '%s'"%(convert))
            print(db.connec.execute("SELECT * FROM Elements;").fetchall())
            self.end_headers() 
        elif self.path == "/addmol":
            self.send_response(200)
            length = int(self.headers.get("Content-Length"))
            info = self.rfile.read(length)
            convert = info.decode("utf-8")
            data = json.loads(convert)
            f = open(data["fname"])
            db.add_molecule(data["name"], f)
            print(db.connec.execute("SELECT * FROM Molecules").fetchall())
            self.end_headers() 
        else:
            #error response msg
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 not found", "utf-8"))


#instantiate http and used to choose which port to start server on
httpd = HTTPServer(('localhost', int(sys.argv[1])), myHandler)
httpd.serve_forever()