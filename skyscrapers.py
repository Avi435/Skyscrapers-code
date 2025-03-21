# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: avila
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
#building the markup
from itertools import chain
from time import perf_counter
def indexsquare(X,Y):
    return [x+y for x in X for y in Y]

#defining towers rows and columns
#grid='.22315.' \
 #    '3.....2' \
  #   '1.....4' \
   #  '2.....2' \
    # '2.....2' \
     #'4.....1' \
     #'.32321.'
#for sq in peers['f1']:
    #print(sq)
    #print(options[sq])
#grid='.22213.'\
 #    '2.....2'\
  #   '2.....3'\
   #  '3.....2'\
    # '1.....3'\
     #'4.....1'\
     #'.23251.'
     
grid='..1....'\
     '....2..'\
     '3.2....'\
     '......3'\
     '......1'\
     '......3'\
     '.2.....'  
          
    
rows='zabcdef'
cols='0123456'
solve_rows='abcde'
solve_cols='12345'
squares=indexsquare(rows,cols)
solve_squares=indexsquare(solve_rows,solve_cols)
clue_squares=sorted(list(set(squares)-set(solve_squares))) # convert each list to sets so they can be subtracted before returning to the list format
unitlist=([indexsquare([X], cols) for X in rows]+[indexsquare(rows,[Y]) for Y in cols])
          #each square only has 2 units as unlike sudoku there's no boxes. just rows and cols
units={sq:tuple(a for a in unitlist if sq in a) for sq in squares}

def cluedistance(sq1, sq2):
    #row1, col1= sq1[0], sq1[1]
    #row2, col2 = sq2[0], sq2[1]
    rowdist= ord(sq1[0])-ord(sq2[0]) 
    if rowdist==0: 
        coldist= abs(ord(sq1[1])-ord(sq2[1]))
        return coldist
    if rowdist>15:
        rowdist=-rowdist+26
    return rowdist
        
        
peers = {}
for sq in squares:
    if sq in solve_squares:
        # Solve squares: peers are other squares in the same units, excluding clue squares
        peers[sq] = set(chain(*units[sq])) - {sq} - set(clue_squares) # chain functions prevents operand errors when using lists. flattens into a single iterable
    else:
        # Clue squares: peers are from their row or column, excluding other clue squares
        
        clue_peers = set(chain(*units[sq])) - {sq} - set(clue_squares)
        peers[sq] = {peer:cluedistance(sq, peer) for peer in clue_peers}

reverse_peers={}
for sq in clue_squares:
    clue_peers = set(chain(*units[sq])) - {sq} - set(clue_squares)
    reverse_peers[sq]={cluedistance(sq, peer):peer for peer in clue_peers}
        
#converts sum into set so that we can subtract set sq from it
#uses e.g.cols[1:-1] to limit unitlist to options not clues. ignores outer rows and columns. 
#function to remove unwanted digits from the markup
towers='12345'


options={sq: towers for sq in solve_squares} 
def removevalue(options,s,t):
    t=str(t) # makes t a string to prevent errors with integers in strings
    if t not in options[s]:
        return options
    options[s]=options[s].replace(t,'') # replace is used because of the use of strings
    #if len(options[s])==1:
     #   solution_grid[s]=int(options[s])
    
def solution(options,s,t):
    t=str(t)
    for x in options[s]:
        if x!=t:
            removevalue(options,s,x) #remove everything but t from that sq and t from all peers
    for p in peers[s]:
        if len(options[p])!=1:
            removevalue(options,p,t)
            if len(options[p])==1:
                solution(options,p,int(options[p]))
# recursive so after one solution is made it will look to see if others are present.
        
    

def initgrid(grid):
  for sq, tow in zip(squares, grid): # zips to bring together the sqaures and initial grid to help input in correct location later
      if tow in towers:
          if sq in solve_squares:
              solution(options, sq, tow) 
          elif sq not in solve_squares:
              options[sq]=tow
      elif tow not in towers and sq not in solve_squares:
          options[sq]='0'         
  return options
  print(grid)
       
#
def rule_of_1 (grid):
    #print(clue_squares)
    for c in clue_squares:
        #print(options[c])
        if int(options[c])==1:
            #print(c)
            for p in peers[c]:
                #print(peers[c][p])
                if peers[c][p]==1:
                    #print(p)
                    solution(options,p,5)
    return grid    

    
#def rule_of_n(grid):
 #   for c in clue_squares:
  #      if int(options[c])==5:
   #         for p in peers[c]:
    #            solution(options,p,peers[c][p])
#rule_of_n(grid)

def rule_of_avi(grid):
    for c in clue_squares:
        for n in range (1,6):
            formula=int(options[c])+n-(5+1)
            for p in peers[c]:
                if peers[c][p]<=formula:
                    removevalue(options,p,n) # for each square - for each number - if the value of the formula is greater than or equal to the distance from the clue, remove the number from the options.
                    if len(options[p])==1:
                        solution(options,p,int(options[p])) # will solve a square if finds. with recursive solutions. should continue for the others too
       


def hidden_singles(grid):
    for c in clue_squares:
       # print(c)
        setoptions=[]
        for p in peers[c]:
            if len(options[p])!=1:
              #  print(options[p])
                setoptions.extend(options[p])
        #print(setoptions)
        for n in range(1,6):
            hidden=setoptions.count(str(n)) # used this to allow for increasing the size of grid while still using strings
            #print(hidden)
            if hidden==1:
               # print('there is only 1 {n}')
                for p in peers[c]:
                    if str(n) in options[p]:
                        solution(options,p,n)



def search(potentials):
    global options # confirms the use of global options instead of a local version
    guess_squares= {ssq for ssq in solve_squares if len(potentials[ssq])>1}
    guessing_square=min((ssq for ssq in guess_squares), key=lambda sq:  len(potentials[sq]))# finds smallest length using anonymous lambda function
    for n in potentials[guessing_square]:
    #    print(guessing_square,n)
        solution(potentials,guessing_square,n)# loops through sq to try solve
       # print(potentials)
        if all(len(potentials[sq])==1 for sq in solve_squares):
   #         print(potentials)
      #      for csq in clue_squares:
  #              print( csq, countcheck(potentials,csq))
            if all(str(countcheck(potentials,csq))==potentials[csq] for csq in clue_squares):
                options=potentials # if succeeds, great
                #print('success')
               # print(options)
                return options
            else:
                potentials=options
                continue
        
        elif any(potentials[sq]=='' for sq in solve_squares):
            potentials=options
            continue
        
        elif any(len(potentials[sq])>1 for sq in solve_squares):
            optcopy=potentials.copy()
            search(optcopy)
            

def gridopt(tow):
    if options[tow]==towers or options[tow]=='0':
        return '.'
    if len(options[tow])==1:
        return options[tow]
    else:
        return '{'+options[tow]+'}'

def cells(row,col):
    return gridopt(row+col) +('|' if col in '05' else '') # based off norvig's lines
def rowmake(row):
    return ''.join(cells(row,col) for col in cols) +('\n' + '---------------------------' if row in 'ze' else '')
def gridmake(grid):
    for r in (rows):
        #print(r)
        print(rowmake(r))



def countcheck(options,csq):
    if any(len(options[sq])>1 for sq in peers[csq]):
        return None
    count=0
    if options[csq]=='0':
        return('0')
    for n in range(1,len(peers[csq])+1):
        if n==1:
            count+=1 
        else:
            #for r in range (1,n):
                #print(options[reverse_peers[csq][r]])
                #print(options[reverse_peers[csq][n]])
            if all (options[reverse_peers[csq][r]]< options[reverse_peers[csq][n]] for r in range(1,n)):
                count+=1              
                #print('Success')
    return(count) # can't check this works until i can complete a grid
t1=perf_counter()
initgrid(grid)       
rule_of_1(grid)
rule_of_avi(grid)
hidden_singles(grid)
optionscopy=options.copy()
search(optionscopy)
t2=perf_counter()
print(gridmake(grid))
print(t2-t1)