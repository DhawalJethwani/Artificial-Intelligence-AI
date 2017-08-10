def order(sym1):
    if sym1=='!':
        return 6
    elif sym1=='&':
        return 5
    elif sym1=='|':
        return 4
    elif sym1=='>':
        return 3
    elif sym1=='=':
        return 2
    elif sym1==')':
        return 1
    if sym1=='(':
        return 0
    else:
        return -1

def isalphanum(c):
    if c>='a' and c<='z':
        return 1
    elif c>='A' and c<='Z':
        return 1
    elif c>='0' and c<='9':
        return 1
    return 0

def in2post(infix):
    poststr=""
    sym=[]
    for i in range(len(infix)):
        c=infix[i]
        if isalphanum(c):
            poststr+=str(c)
        elif c=='(' or c==')' or c=='=' or c=='>' or c=='|' or c=='&' or c=='!':
            o1=order(c)
            if len(sym):
                o2=order(sym[-1])
            else:
                o2=-1
            if o1==0:
                sym.append(c)
            elif o1==1:
                while sym[-1]!='(':
                    o3=sym.pop()
                    poststr+=str(o3)
                sym.pop()
            elif o1>=o2:
                sym.append(c)
            else:
                while o1<o2:
                    o3=sym.pop()
                    poststr+=str(o3)
                    if len(sym):
                        o2=order(sym[-1])
                    else:
                        o2=-1
                sym.append(c)
    while len(sym):
        c=sym.pop()
        poststr+=str(c)
    return poststr

def atm_st(str):
    s=set()
    for i in str:
        if isalphanum(i):
            s.add(i)
    s=sorted(list(s))
    return s

def evalpost(poststr,atom,mat):
    n=len(atom)
    mat.append([])
    for i in range(2**n):
        b=list(str(bin(i)[2:].zfill(n)))
        stk=[]
        for j in range(len(poststr)):
            c=poststr[j]
            if isalphanum(c):
                val=int(b[atom.index(c)])
                stk.append(val)
            elif c=='!':
                stk.append(int(not stk.pop()))
            elif c=='&':
                p2=stk.pop()
                p1=stk.pop()
                stk.append(p1 & p2)
            elif c=='|':
                p2=stk.pop()
                p1=stk.pop()
                stk.append(p1 | p2)
            elif c=='>':
                p2=stk.pop()
                p1=stk.pop()
                stk.append(int(not(p1 & int(not p2))))
            elif c=='=':
                p2=stk.pop()
                p1=stk.pop()
                stk.append(int((p1 & p2) | (int(not p1) & int(not p2))))
        mat[-1].append(stk.pop())
    return mat

def chk_tauto(mat):
    l=[]
    for i in range(len(mat)):
        for j in mat[i]:
            if j==0:
                break
        else:
            l.append(i)
    return l

def chk_slfcontra(mat):
    l=[]
    for i in range(len(mat)):
        for j in mat[i]:
            if j==1:
                break
        else:
            l.append(i)
    return l

def chk_conten(mat):
    l=[]
    for i in range(len(mat)):
        if (i not in chk_tauto(mat)) and (i not in chk_slfcontra(mat)):
            l.append(i)
    return l

def chk_eq(mat):
    l=[]
    for i in range(len(mat)):
        for j in range(len(mat)):
            if i!=j and mat[i]==mat[j] and (j,i) not in l:
                l.append((i,j))
    return l

def chk_lgent(mat):
    l=[]
    for i in range(len(mat)):
        for j in range(len(mat)):
            for k in range(len(mat[i])):
                if mat[i][k]==1 and mat[j][k]==0:
                    break
            else:
                l.append((i,j))
    return l

def chk_lgcons(mat):
    mat1=zip(*mat)
    flag=False
    for i in mat1:
        for j in i:
            if j==0:
                break
        else:
            flag=True
            break
    return flag

mat=[]
statements=[]

a=input("Enter the number of logical statements to evaluate:")

print "Enter logically correct statements as strings:"
for i in range(a):
    statements.append(in2post(raw_input()))

d=set()
for p in statements:
    d=d.union(atm_st(p))

for p in statements:
    evalpost(p,list(d),mat)
#evalpost(in2post("(((a)))"),atm_st("!a&!(b=c&a)|(a>!c)"),mat)
#evalpost("a!bca&=!>",atm_st("a!bca&=!>"),mat)
#evalpost(in2post("(!a&a)>(b=a)"),atm_st("(!a&a)>(b=c&a)"),mat)
#evalpost(in2post("(a=a)&(b=c&a)"),atm_st("(!a&a)&(b=c&a)"),mat)
#evalpost(in2post("(!b&c)|(a|!a)"),atm_st("(!b&c)&(a&!a)"),mat)
#evalpost(in2post("(!a&(b>c=b)|(c&b=!a))"),atm_st("(!b&c)&(a&!a)"),mat)
for i in mat:
    print i
print "Tautologies : ",chk_tauto(mat)
print "Self-contradictions : ",chk_slfcontra(mat)
print "Contingencies : ",chk_conten(mat)
print "Equivalences : ",chk_eq(mat)
print "Ordered pairs of Logical Entailment : ",chk_lgent(mat)
print "Logically Consistent set: ",chk_lgcons(mat)
