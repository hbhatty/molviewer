#include "mol.h"

void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
    // sets atom members to x,y,z
    strcpy(atom->element, element);
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
    //makes these variables point to the passed in parameters
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
    strcpy(element, atom->element);
}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs )
{
    //sets bond memebers to a1, a2, epairs
    // bond->atoms[*a1] = *atoms[*a1];
    // bond->atoms[*a2] = *atoms[*a2];
    bond->epairs = *epairs;
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    //call compute_coords
    compute_coords(bond);
}

void compute_coords(bond *bond){
    //set the coordinates of the values
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    bond->z = (bond->atoms[bond->a1].z  + bond->atoms[bond->a2].z) / 2;
    //formula for length
    bond->len = sqrt((bond->y2 - bond->y1) * (bond->y2 - bond->y1) + (bond->x2 - bond->x1) *  (bond->x2 - bond->x1));
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;

}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom
**atoms, unsigned char *epairs )
{
    //makes these variables point to the passed in args
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    // *atoms[*a1] = bond->atoms[*a1];
    // *atoms[*a2] = bond->atoms[*a2];
    *epairs = bond->epairs;
}

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    // create the temp molecule struct
    molecule *temp = malloc(sizeof(molecule));
    if(temp == NULL){
        return NULL;
    }
    // set the maxes passed in
    temp->atom_max = atom_max;
    temp->bond_max = bond_max;
    // set to 0 initally
    temp->atom_no = 0;
    temp->bond_no = 0;
    // create enough struct arrays for atom_max/bonds_max
    temp->atoms = malloc(sizeof(struct atom) * atom_max);
    temp->bonds = malloc(sizeof(struct bond) * bond_max);
    //checks if null
    if(temp->atoms == NULL || temp->bonds == NULL){
        return NULL;
    }
    //allocate enough space for the double pointers
    temp->atom_ptrs = (atom**)malloc(sizeof(struct atom*) *atom_max);
    temp->bond_ptrs = (bond**)malloc(sizeof(struct bond*) *bond_max);
    //checks if null
    if(temp->atom_ptrs == NULL || temp->bond_ptrs == NULL){
        return NULL;
    }
    return temp;
}

molecule *molcopy( molecule *src ){
    //variable to hold copied details of src
    molecule *newOne = molmalloc(src->atom_max, src->bond_max);
    //loops through amount of atoms and appends the atom struct onto the variable we created
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(newOne, &src->atoms[i]);
    }
    //loops through amount of bonds and appends the bond struct onto the variable we created
    for(int i = 0; i< src->bond_no; i++){
        molappend_bond(newOne, &src->bonds[i]);
    }
    //return the newly copied member
    return newOne;
}

void molfree(molecule *ptr)
{
    //frees everything we have allocated for
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

void molappend_atom(molecule *molecule, atom *atom)
{
    if (molecule->atom_no == molecule->atom_max && molecule->atom_max > 0)
    {
        //double atom_max
        molecule->atom_max *= 2;
        //realloc more space as atom max increases
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        //realloc enough space for the double pointer to the atom array
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);
    }
    else if (molecule->atom_no == molecule->atom_max && molecule->atom_max == 0)
    {
        //increase atom_max by 1
        molecule->atom_max += 1;
        //realloc more space as atom max increases
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * (molecule->atom_max));
        //realloc enough space for the double pointer to the atom array
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * (molecule->atom_max));
    }
    //makes atom pointers repoint to the atoms array again
    for (int i = 0; i < molecule->atom_no; i++){
        molecule->atom_ptrs[i] = &molecule->atoms[i];
    }
    //assigns values to arrays
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    //increments atom no
    molecule->atom_no++;
}

void molappend_bond(molecule *molecule, bond *bond)
{
    if (molecule->bond_no == molecule->bond_max && molecule->bond_max > 0)
    {
        //double bond max
        molecule->bond_max *= 2;
        //realloc more space as bond max increases
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        //realloc enough space for the double pointer to the bond array
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
    }
    else if (molecule->bond_no == molecule->bond_max && molecule->bond_max == 0)
    {
        //add one to bond max
        molecule->bond_max += 1;
        //realloc more space as bond max increases
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        //realloc enough space for the double pointer to the bond array
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
    }
    //makes bond double pointers point to bond pointer
    for (int i = 0; i < molecule->bond_no; i++){
        molecule->bond_ptrs[i] = &molecule->bonds[i];
    }
    //assigns values to bond and bond ptr
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    //increments bond no
    molecule->bond_no++;
}

//helper function for atom sort
int atom_comp(const void *a, const void *b){
    //temp double pointers
    struct atom **a_ptr, **b_ptr;
    a_ptr = (struct atom**)a;
    b_ptr = (struct atom**)b;
    //compares the z values and returns the corresponding numbers to qsort function
    if((*a_ptr)->z < (*b_ptr)->z){
        return -1;
    } else if((*a_ptr)->z == (*b_ptr)->z){
        return 0;
    } else{
        return 1;
    }
}

//helper function for bond sort
int bond_comp(const void *a, const void *b){
    //temp double pointers
    struct bond **a_ptr, **b_ptr;
    a_ptr = (struct bond**)a;
    b_ptr = (struct bond**)b;
    //the average of the z values
    double avg1 = (*a_ptr)->z;
    double avg2 = (*b_ptr)->z;
    //compares the avgerage values and returns the corresponding numbers to qsort function
    if(avg2 > avg1){
        return -1;
    } else if(avg2 == avg1){
        return 0;
    } else{
        return 1;
    }
}

void molsort( molecule *molecule ){
    //sorts the atom and bonds using qsort
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), atom_comp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_comp);
}

void xrotation( xform_matrix xform_matrix, unsigned short deg ){
    //convert to radians
    double rad = deg * (PI/180);
    //manually set the x rotation array/matrix
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);

}

void yrotation( xform_matrix xform_matrix, unsigned short deg ){
    //convert to radians
    double rad = deg * (PI/180);
    //manually set the x rotation array/matrix
    xform_matrix[0][0] = cos(rad); 
    xform_matrix[0][1] = 0; 
    xform_matrix[0][2] = sin(rad); 
    xform_matrix[1][0] = 0; 
    xform_matrix[1][1] = 1; 
    xform_matrix[1][2] = 0; 
    xform_matrix[2][0] = -sin(rad); 
    xform_matrix[2][1] = 0; 
    xform_matrix[2][2] = cos(rad); 
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ){
    //convert to radians
    double rad = deg * (PI/180);
    //manually set the x rotation array/matrix
    xform_matrix[0][0] = cos(rad); 
    xform_matrix[0][1] = -sin(rad); 
    xform_matrix[0][2] = 0; 
    xform_matrix[1][0] = sin(rad); 
    xform_matrix[1][1] = cos(rad); 
    xform_matrix[1][2] = 0; 
    xform_matrix[2][0] = 0; 
    xform_matrix[2][1] = 0; 
    xform_matrix[2][2] = 1; 
}

void mol_xform( molecule *molecule, xform_matrix matrix ){
    //loop through the amount of atoms
    for(int i = 0; i < molecule->atom_no; i++){
        //create temp values to hold inital values, so they dont get modified
        double tempX = molecule->atoms[i].x;
        double tempY = molecule->atoms[i].y;
        double tempZ = molecule->atoms[i].z;
        //multiply the corresponding x,y,z by the rotations to rotate the molecule
        molecule->atoms[i].x = (matrix[0][0] * tempX) + (matrix[0][1] * tempY)  + (matrix[0][2] *tempZ);
        molecule->atoms[i].y = (matrix[1][0] * tempX) + (matrix[1][1] * tempY)  + (matrix[1][2] *tempZ);
        molecule->atoms[i].z = (matrix[2][0] * tempX) + (matrix[2][1] * tempY)  + (matrix[2][2] *tempZ);
    }
    //call compute coords to set the new values
    for(int i =0; i <molecule->bond_no; i++){
        compute_coords(&molecule->bonds[i]);
    }
}
