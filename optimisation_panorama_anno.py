import numpy as np
import random as rd
import time
from math import *

"""
Please read the reddit post associated to understand how the program works and how to use it!
"""


"""
Definition of the useful functions
"""


def extraction_position(L,l1,l2): #when L is the list that is given from anno designer, this function extracts the position of the houses placed in the layout; L has to be a string, l1 and l2 too
    i1=0 #we set a position counter at 0
    (a,b)=(0,0)
    extract=[] #we create a list to save the positions
    while i1<len(L): #we screen the hole string
        if L[i1:i1+len(l1)]==l1: #if we spot the l1 string within L
            i2=i1+1
            while L[i2:i2+len(l2)]!=l2: #we look for string l2 within L
                i2+=1
            i3=i2+len(l2)
            while L[i3]!=',': #when we found l2, we extract the positions and as we don't know how many digits are written, we look for the character right after the last digit; both for x and y
                i3+=1
            a=int(L[i2+len(l2):i3])
            i4=i3+5
            while L[i4]!='}':
                i4+=1
            b=int(L[i3+6:i4])
            extract.append([a,b])
            i1=i4-1 #the main counter is incremented
        i1+=1
    return extract


def size_matrix(l): #function that will give the matrix size from the list of the coordinates of the houses
    (min1,min2,max1,max2)=(100,100,0,0) #we set arbitrary values for min and max
    for k in range (len(l)): #classic min and max program
        if l[k][0]>max1:
            max1=l[k][0]
        if l[k][1]>max2:
            max2=l[k][1]
        if l[k][0]<min1:
            min1=l[k][0]
        if l[k][1]<min2:
            min2=l[k][1]
    return ((max2-min2+9,max1-min1+9),min1,min2) #the +9 comes from the double belt of 0 in either dimensions, which gives a +6; the other +3 commes from the width of a house; note that Anno Designer and Python use x and y axis in opposite ways, so we have to operate a switch in the output; min1 and min2 are in the output to save computing time



def world_generation(M,l,min1,min2): #this function will generate the matrix corresponding to your layout with all the conventions we will be using for the whole programm; don't forget Anno Designer gives the coordinates of the top left corner of houses and not those of the center
    for k in range (len(l)): #we are adjusting the min on x and y to avoid useless rows/columns
        l[k][0]+=3-min1
        l[k][1]+=3-min2
    for k in range (len(l)): #for each positions of a skyscraper
        M[l[k][1]+1,l[k][0]+1]=100+rd.randint(0,5) #in the initial state, the skyscraper tier is randomly set between 0 and 5
    for k in range (len(l)):
        (b,a)=(l[k][0],l[k][1]) #don't forget to switch x and y
        p=score_panorama(a+1,b+1,M) #we compute the panorama score of the building
        for i in range (a,a+3):
            for j in range (b,b+3): #we create here the eight tiles surrounding the center of the building; remember Anno Designer gives the position of the house using its top left corner position which gives the a+3 and b+3 final loop values
                if (i,j)!=(a+1,b+1):
                    M[i,j]=200+p
    return M




def coord_centre(i,j,M): #function to find the coordinates of the center of the building that corresponds to the position (i,j) in matrix M
    for k in range (i-1,i+2):
        for l in range (j-1,j+2): #the centre must be in the eight tiles surrounding coordinates (i,j)
            if floor(M[k,l]/100)==1:
                return (k,l) #centres are written in the form 100+tier
    return ('Road','Road') #only roads have no centre in thir eight surrounding tiles, it will allow us to quickly go over cases where a road is randomly selected



def radius(tier): #function that gives the radius of influence of a skyscraper given its tier
    if tier==0:
        return 0
    if tier==1:
        return 4
    if tier==2:
        return 4.25
    if tier==3:
        return 5
    if tier==4:
        return 6
    if tier==5:
        return 6.75



def coord_influencing(i,j,M):#function that gives the coordinates of the building centers that are used to compute the panorama score of the building in coordinates (i,j) in matrix M; be careful: M[i,j] has to correspond to the center of a skyscraper!
    liste_coord_influencing=[] #we create the list of these coordinates
    r=radius(M[i,j]-100) #gives the radius of influence of the considered skyscraper
    for k in range (floor(i-r),floor(i+r)+1):
        for l in range (floor(j-r),floor(j+r)+1): #all the tiles in a square that is 2*radius long are screened; it's not important if i-r, i+r, j-r or j+r are out of the matrix, python will just search at the begining or end of the row/column and the belts of 0 prevent any center to be found because of that
            if k>=len(M): #to prevent boundary problems
                k=len(M)-k
            if l>=len(M[0]):
                l=len(M)-l
            if floor(M[k,l]/100)==1: #if it is the center of a building
                if sqrt((i-k)**2+(j-l)**2)<=r: #we test if the center is within the radius of influence of the considered building
                    if (k,l)!=(i,j): #we eliminate the case where the center found is the considered center itself
                        liste_coord_influencing.append([k,l]) #if it's the case, we save the center coordinates
    return liste_coord_influencing



def coord_influenced(i,j,M): #function that gives the coordinates of the building centers that consider the skycraper in coordinates (i,j) in matrix M to compute their panorama score; be careful: M[i,j] has to correspond to the center of a skyscraper!
    liste_coord_influenced=[] #we create the list of these coordinates
    for k in range (floor(i-6.75),floor(i+6.75)+1):
        for l in range (floor(j-6.75),floor(j+6.75)+1):
            if k>=len(M): #to prevent boundary problems
                k=len(M)-k
            if l>=len(M[0]):
                l=len(M)-l #we screen every tile within the max influence radius around the considered skyscraper
            if floor(M[k,l]/100)==1 and (k,l)!=(i,j): #if the tile is a center and not the building itself
                r=radius(M[k,l]-100) #then we compute its own influence radius
                if sqrt((i-k)**2+(j-l)**2)<=r: #and check if the considered building is within this range
                    liste_coord_influenced.append([k,l]) #if yes, we save the coordinates of the detected center
    return liste_coord_influenced



def score_panorama(i,j,M): #function that computes the panorama score of the skyscraper which center is (i,j) in matrix M; be careful: M[i,j] has to correspond to the center of a skyscraper!
    if M[i,j]==100:
        return 0
    liste_coord_influencing=coord_influencing(i,j,M) #first we compute all the skyscrapers that are in the influence radius of the considered skyscraper
    s_p=M[i,j]-100 #we set a counter of panorama score
    for k in range (len(liste_coord_influencing)): #for each influencing skyscraper
        if M[liste_coord_influencing[k][0],liste_coord_influencing[k][1]]==100:
            s_p+=0
        elif M[i,j]>M[liste_coord_influencing[k][0],liste_coord_influencing[k][1]]: #if its tier is lower than that of the considered skyscraper and it is not a normal house
            s_p+=1 #then it counts as +1
        elif M[i,j]<=M[liste_coord_influencing[k][0],liste_coord_influencing[k][1]]:
            s_p-=1 #else it counts as -1
    if s_p<0:  #the game considers panorama scores between 0 and 5, so here if a score is negative we set it back to 0, and if it is higher than 5 we set it back to 5.
        s_p=0
    if s_p>5:
        s_p=5
    return s_p



def score_panorama_global(M): #function that computes the global panoramic score of the entire matrix M
    s_p_global=0 #we set a counter of global panorama score
    (x,y)=(len(M),len(M[0])) #this is the size of matrix M
    for k in range (3,x-3):
        for l in range (3,y-3): #we screen all the matrix
            if floor(M[k,l]/100)==1: #if we are on a center
                s_p_global+=score_panorama(k,l,M) #we add to the global panorama score the panorama score of the given building
    return s_p_global



def population_global(M): #function that computes the global population in matrix M
    pop_global=0 #we set a counter of global population
    (x,y)=(len(M),len(M[0])) #this is the size of matrix M
    for k in range (3,x-3):
        for l in range (3,y-3): #we screen all the matrix where a center could be (so not in the 0 belts)
            if floor(M[k,l]/100)==1: #if we are on a center
                pop_global+= 50 + (M[k,l]-100)*25 + (M[k+1,l+1]-200)*25 #we add to the global population the population of the given building
    return pop_global



def replace_panorama(i,j,M,p): #function that replaces the panorama value in the eight tiles surrounding the center of coordinates (i,j) by another panorama value p; modifies the matrix without returning anything; (i,j) has to be a center
    for k in range (i-1,i+2):
        for l in range (j-1,j+2): #we screen the tiles surrounding the center
            if floor(M[k,l]/200)==1: #if they are panorama values they have the form 200+panorama score
                M[k,l]=p #we modify the value



def position_from_matrix(M): #function to obtain the coordinates of the building centers from matrix M
    (a,b)=(len(M),len(M[0])) #we compute the dimension of the matrix
    liste_position=[] #we create a list to save the building center positions
    for k in range (3,a-3):
        for l in range (3,b-3): #we screen all the matrix positions where a center can be
            if floor(M[k,l]/100)==1: #we test if the tile is a center
                liste_position.append([k,l,M[k,l]-100]) #if yes we save its coordinates and the building tier
    return liste_position


"""
Main code! The input document 'layout.txt' has to be obtained through Anno Designer.

!!WARNING!! This program only works if you place old world residence, designated as A7_resident in Anno Designer. Any other kind of house won't be supported!

When your layout is ready, save your file under layout.ad. Then right click on it, open with textbook and save it as layout.txt in your User/User directory. Don't modify anything in the .txt file!
"""
def run(nbr_iter):
    fichier=open('layout.txt')
    lignes=fichier.readlines()[0]
    house_position=extraction_position(lignes,'Residence_Old_World',':{"_x":') #extraction of the houses position from the Anno Designer file
    ((x,y),min1,min2)=size_matrix(house_position)
    M=np.zeros((x,y)) #creation of a matrix full of 0 that has the right size
    World=world_generation(M,house_position,min1,min2) #generation of the layout using this program conventions
    fichier.close()
    (a,b)=(len(World),len(World[0])) #re-definition of the size of the matrix
    pop_global=population_global(World) #global population calculation
    s_p_global=score_panorama_global(World) #global panorama score calculation
    for k in range (nbr_iter):
        (x,y)=(rd.randint(3,a-4),rd.randint(3,b-4)) #a random tile that is not in the zero belts is chosen
        (c1,c2)=coord_centre(x,y,World) #the center of the corresponding building is detected
        if c1!='Road': #eliminates the case where the tile is part of a road
            tier_init=World[c1,c2]-100 #we save the initial tier and panorama score of the selected building
            p_init=World[c1+1,c2+1]-200
            liste_d_pop=[] #we create a list that will gather the differences induced by the change of tier of the selected building
            for l in range (0,6):  #the tier of the selected building is varied between 0 and 5
                World[c1,c2]=100+l #we set the new tier value to the building
                World[c1+1,c2+1]=score_panorama(c1,c2,World)+200 #we compute the new panorama score of the selected building and we stor it in an adjacent tile in the matrix World
                d_pop=(World[c1,c2]-100-tier_init)*25+(World[c1+1,c2+1]-200-p_init)*25 #we compute the difference of population induced by the change of tier of the selected building
                liste_coord_influenced=coord_influenced(c1,c2,World) #we look after the buildings which panorama score will be changed by the change of tier of the selected building
                liste_modif=[l,World[c1+1,c2+1]] #we create a list that will gather all the modifications of panorama scores and the coordinates of the impacted buildings induced by the change of tier of the selected building; this is to save computing time
                for m in range (len(liste_coord_influenced)):
                    (z1,z2)=(liste_coord_influenced[m][0],liste_coord_influenced[m][1]) #simplifying notations for the following
                    World[z1+1,z2+1]=200+score_panorama(z1,z2,World) #we compute and store the new panorama value of the building
                    d_pop+=(World[z1+1,z2+1]-World[z1,z2+1])*25 #the population difference is here induced only by the change of panorama score of the building; the old one is still stored in M[z1,z2+1] whereas the new one is in M[z1+1,z2+1] one
                    liste_modif.append([z1,z2,World[z1+1,z2+1]-200]) #we store in the modification list the centre of the building and the new panorama score
                liste_modif.append(d_pop) #we store the difference of population induced by the tier change
                liste_d_pop.append(liste_modif) #all the modifications of panorama scores for centers affected by the tier change and the tier itself are saved here
            max_d_pop=-10**10 #now we search in the previous list what maximum population increase we could get; the following is basically a research of the maximum and the corresponding index in a list
            index=0
            for l in range (len(liste_d_pop)):
                if liste_d_pop[l][-1]>max_d_pop:
                    max_d_pop=liste_d_pop[l][-1]
                    index=l
            if max_d_pop>0: #here we eliminate the case where the population cannot increase with a tier change to save computing time
                World[c1,c2]=liste_d_pop[index][0]+100 #we replace the old tier by the new one for the randomly designated building
                replace_panorama(c1,c2,World,liste_d_pop[index][1]) #we replace the panorama score by the new one in the eight surrounding tiles
                for l in range (len(liste_d_pop[index])): #we go over every impacted building, which is stored in liste_d_pop[index]; the end loop index is len -4 because there are 4 values (respectively the new tier, new panorama score of the randomly chosen building, difference of population and difference of global panorama score) we are not interested in here
                    if type(liste_d_pop[index][l]) is list:
                            replace_panorama(liste_d_pop[index][l][0],liste_d_pop[index][l][1],World,liste_d_pop[index][l][2]+200) #we use l+2 as the loop index to avoid the first two values in liste_d_pop[index] which are respectively the new tier and the new panorama score of the randomly selected building
                pop_global+=liste_d_pop[index][-1] #we add to the old total population value the difference of population generated by the change of tier
            else: #if no better layout has been found
                World[c1,c2]=tier_init+100 #as the matrix has been modified, we put the initial tier and panorama score back to the randomly designated building
                World[c1+1,c2+1]=p_init+200
                for l in range (len(liste_coord_influenced)): #and we set the old panorama score back for the influenced buildings
                    World[liste_coord_influenced[l][0]+1,liste_coord_influenced[l][1]+1]=World[liste_coord_influenced[l][0],liste_coord_influenced[l][1]+1]
    liste_position=position_from_matrix(World) #we gather the positions of all the building centers in the layout
    fichier=open('layout.txt','w') #we open the layout file to overwrite it
    fichier.write('{"FileVersion":3,"Objects":[') #beginning of every Anno Designer txt file
    for k in range (len(liste_position)):
        fichier.write('{"Identifier":"Residence_Old_World","Label":"","Position":')
        fichier.write('{"_x":')
        fichier.write(str(liste_position[k][1]))
        fichier.write(',"_y":')
        fichier.write(str(liste_position[k][0])) #the position of the cener is implemented in the output file
        fichier.write('},"Size":{"_height":3,"_width":3},"Icon":"A7_resident","Template":"ResidenceBuilding7","Color":{"A":255,')
        if liste_position[k][2]==0:
            fichier.write('"R":255,"G":0,"B":0},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},')
        elif liste_position[k][2]==1:
            fichier.write('"R":0,"G":255,"B":0},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},')
        elif liste_position[k][2]==2:
            fichier.write('"R":0,"G":0,"B":255},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},')
        elif liste_position[k][2]==3:
            fichier.write('"R":255,"G":255,"B":0},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},')
        elif liste_position[k][2]==4:
            fichier.write('"R":255,"G":0,"B":255},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},')
        elif liste_position[k][2]==5:
            fichier.write('"R":0,"G":255,"B":255},"Borderless":false,"Road":false,"Radius":0,"InfluenceRange":-2,"PavedStreet":false},') #each tier will be represented by a color on the final Anno Designer layout: red for normal houses, green for tier 1, blue for tier 2, yellow for tier 3, magenta for tier 4 and cyan for tier 5
    fichier.close() #we close the file to save everything
    fichier=open('layout.txt') #here we want to erase the last comma that must not be in the file
    line1=fichier.readlines()[0] #we save what is currently written in the file
    fichier.close() #close it
    fichier=open('layout.txt','w') #and reopen it in writing mode
    for k in range (len(line1)-1): #we write evrything except the last comma
        fichier.write(line1[k])
    fichier.close() #and close the file again
    fichier=open('layout.txt','a') #finally we write the last two characters
    fichier.write(']}')
    fichier.close() #and close it
    fichier=open('layout.txt')
    output=fichier.readlines()[0]
    fichier.close()
    return(pop_global,output) #as the output we have the global population reached and the corresponding Anno Designer file

def optimisation(nbr_iter,nbr_try): #function that executes the main program nbr_try times with a number of iteration of nbr_iter to detect the best layout
    optimized_layout=''
    opt_pop=0
    for k in range(nbr_try):
        (pop_global,output)=run(nbr_iter)
        if pop_global>opt_pop:
            opt_pop=pop_global
            optimized_layout=output
        print(k)
    fichier=open('layout.txt','w')
    fichier.write(optimized_layout)
    fichier.close()
    print('The best global population reached is',opt_pop)



"""
You can now open your layout.txt file in Anno Designer and enjoy the optimised pattern!
"""