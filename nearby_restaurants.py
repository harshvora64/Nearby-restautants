class Point():                          # object of class Point stores a point's x and y co-ordinates
    def __init__(self,x,y):
        self._x = x
        self._y = y
    def __str__(self):
        return str(self._y)
    def __repr__(self):
        return str((self._x,self._y))

class Node():                               # Node class has objecs whose value corresponds to a y-sorted list
                                            # of Points which belong in the range of indices  self.range of the x-sorted list
    def __init__(self,v,parent,l,r,si,ei):
        self._value=v                       # Stores the y-sorted list of range (self._start_indes,self._end_index) of the x-sorted list 
        self._parent=parent
        self._left=l
        self._right=r
        self._start_index=si                # start index of the range in the original z-sorted list whose y-sorted order is stored in _value
        self._end_index=ei                  # end index of the range in the original z-sorted list whose y-sorted order is stored in _value
    def __repr__(self):
        return str((self._start_index,self._end_index))


def node_list(l):               # converts a list of Points to a list of nodes
    return [Node([l[i]],None,None,None,i,i) for i in range(len(l))]

def mergeY(a,b):                # merges two y-sorted lists of Points to give a y-sorted merged list of Points
    i,j=0,0
    ans=[]
    while i<len(a._value) and j<len(b._value):
        if a._value[i]._y<=b._value[j]._y:
            ans.append(a._value[i])
            i+=1
        else:
            ans.append(b._value[j])
            j+=1
    ans+=(a._value[i:len(a._value)])            # add the remaining elements of a or b are finally added to the end of the list
    ans+=(b._value[j:len(b._value)])
    return ans
def make_tree(l):       # Takes an x-sorted list of Nodes(which store only a single point) as input and
                        # returns a tree of nodes which store the y_sorted lists of different sub-ranges of the x-sorted set of points
                        # in mergesort fashion..., i.e. root stores the entire list,
                        # it's left child stores the y-sorted list of the first half points of the x-sorted set of points, and so on
    if len(l)==2:
        i=0
        val=mergeY(l[i],l[i+1]) # value lists of the 2 nodes are merged to form the value list of their parent node
        x=Node(val,None,l[i],l[i+1],l[i]._start_index,l[i+1]._end_index)
        l[i]._parent=x          # update their parents 
        l[i+1]._parent=x
        return x
    if len(l)==1:               # base case
        return l[0]
    elif len(l)==0:             # base case
        return None

    li=make_tree(l[0:len(l)//2])        # recursively make a tree of the first half of the list (according to the x-sorted list)
    li1=make_tree(l[len(l)//2:len(l)])  # recursively make a tree of the second half of the list (according to the x-sorted list)
    val=mergeY(li,li1)                  # value lists of the 2 nodes are merged to form the value list of their parent node
    x=Node(val,None,li,li1,li._start_index,li1._end_index)
    li._parent=x                        # update their parents 
    li1._parent=x
    return x
    

def next(t):            # returns the next node of the tree , in order of the range of the list it stores
    if t._parent != None:
        if t==t._parent._left:
            return t._parent._right
        else:
            return next(t._parent)      # because next(t._parent) will have a greater start index

def prev(t):            # returns the previous node of the tree , in order of the range of the list it stores
    if t._parent != None:
        if t==t._parent._right:
            return t._parent._left
        else:
            return prev(t._parent)      # because prev(t._parent) will have a smaller end index than t

def find_lists(s,e,t):                  # It finds the partitions of the range of x required [s,e]
                                        # such that each partition belongs to the created tree
                                        # therefore each partiton is y-sorted
                                        # and we can apply binary search on y in each partition separately
                                        # and combine their outputs so as to get the required set of points
    if t==None:
        return []                       # base case
    if s==t._start_index:
        if e==t._end_index:             # perfect match, so the value list is returned
            return [t._value]
        elif e<t._end_index:            # in this case, this range is not allowed because it has elements out of x allowed range, and t._left has the same start index, so that is used
            return find_lists(s,e,t._left)
        else:                           # in this case, the range is a subset of the allowed range, so that is added to the list of partitions, and now the tree from the next element of t is searched for the remainder of the list
            return [t._value] + find_lists(t._end_index+1,e,next(t))
    elif s>t._start_index:              # in this case, the range has extra elements, so it is not allowed
        if s>t._end_index:              # in this subcase, t does not contain even one allowed element, so we directly go to the next Node
            return find_lists(s,e,next(t))
        return find_lists(s,e,t._right) # t._right has a higher start index, which can resolve the issue of s>start index
    else:
        if e<t._start_index:            # in this subcase, t does not contain even one allowed element, so we directly go to the previous Node
            return find_lists(s,e,prev(t))
        elif e==t._end_index:           # the node's value is a subset, so that is added to the list of partitions, and we search the tree, previous node onwards for the remainder of the range not covered yet
            return find_lists(s,t._start_index-1,prev(t)) + [t._value]
        elif e<t._end_index:            # t._left has a lower end index, which can resolve the issue of e<end index
            return find_lists(s,e,t._left)
        else:                           # the Node's range is a subset of the required range, so it is added to the partitions list, and the search is run on both the subranges (one on each side of the current range)
            return find_lists(s,t._start_index-1,prev(t)) + [t._value] + find_lists(t._end_index+1,e,next(t))

def binary_search_x(l,lb,ub):           # binary search on an x sorted list to get the acceptable range of indices for values of x from query(x)-d to query(x) + d
    if l[-1]._x<lb or l[0]._x>ub:       # if the list does not have any acceptable value, then (0,-1) is returned, which when taken as the range of the for loop that makes the answer list, nothing is added to it
        return((0,-1))
    s=0                                 # binary search for the start index (using >= property)
    e=len(l)-1
    m=(s+e)//2                          # >= property requires the use of (s+e)//2
    while s<e:
        if l[m]._x>=lb:
            e=m
        else:
            s=m+1
        m=(s+e)//2
    start_index=m

    s=0                                 # binary search for the end index (using <= property)
    e=len(l)-1
    m=(s+e+1)//2                        # <= property requires the use of (s+e+1)//2
    while s<e:
        if l[m]._x<=ub:
            s=m
        else:
            e=m-1
        m=(s+e+1)//2
    end_index=m
    # print(start_index,end_index)
    return (start_index,end_index)


def binary_search_y(ls,lb,ub):          # binary search on a list of y sorted lists to get the acceptable ranges of indices for values of y from query(y)-d to query(y) + d
    ans=[]
    for l in ls:
        if l[-1]._y<lb or l[0]._y>ub:   # if the list does not have any acceptable value, then (0,-1) is returned, which when taken as the range of the for loop that makes the answer list, nothing is added to it
            ans.append((0,-1))
            continue
        s=0                             # binary search for the start index (using >= property)
        e=len(l)-1
        m=(s+e)//2                      # >= property requires the use of (s+e)//2
        while s<e:
            if l[m]._y>=lb:
                e=m
            else:
                s=m+1
            m=(s+e)//2
        start_index=m
        s=0                             # binary search for the end index (using <= property)
        e=len(l)-1
        m=(s+e+1)//2                    # <= property requires the use of (s+e+1)//2
        while s<e:
            if l[m]._y<=ub:
                s=m
            else:
                e=m-1
            m=(s+e+1)//2
        end_index=m
        ans.append((start_index,end_index))
    # print (ans)
    return ans


def xkey(a):                            # function which can be used as key in the sorting to sort according to x value
    return a[0]

class PointDatabase():
    def __init__(self,pointlist):
        pointlist.sort(key=xkey)
        self._lst=[Point(pointlist[i][0],pointlist[i][1]) for i in range(len(pointlist))]
        self._avl=make_tree(node_list(self._lst))       # make tree

    def searchNearby(self, q, d):
        if len(self._lst)==0:                           # edge case - empty input
            return []
        if d==0:
            return []                                   # edge case
        x1,x2,y1,y2=q[0]-d,q[0]+d,q[1]-d,q[1]+d
        # print(self._lst)
        b1=binary_search_x(self._lst,x1,x2)             # impose condition on range of x
        # print(b1)
        l1=find_lists(b1[0],b1[1],self._avl)
        # print(l1)
        l1_ans=binary_search_y(l1,y1,y2)                # impose conditon on range of y

        ans=[]
        for i in range(len(l1)):
            for j in range(l1_ans[i][0],l1_ans[i][1]+1):
                ans.append((l1[i][j]._x,l1[i][j]._y))       # appends the points to the answer list

        return ans
