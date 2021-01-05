import numpy as np

def KnotVector(nControlPoints, degree):
    """
    Returns a list of parametric knot locations.
    This is Eqn 5 from 'Freeform Deformation Versus B-Spline Representation in Inverse Airfoil Design' - Eleftherios I. Amoiralis, Ioannis K. Nikolos, 2008
    """
    a = nControlPoints - 1
    if degree > a:
        if degree < 1:
            print("Error: 1 <= degree <= a condition not satisfied!")  
    q = a + degree + 1
    knotVector = [None] * (q + 1) 
    for i in range(len(knotVector)):
        if 0 <= i:
            if i <= degree:
                knotVector[i] = 0
        if degree < i:
            if i <= q - degree - 1:
                knotVector[i] = i - degree
        if q - degree - 1 < i:
            if i <= q:
                knotVector[i] = q - 2*degree
    return np.array(knotVector)

def FindSpan(degree, parameter, knotVector):
    """
    Returns the index of the knot vector whose value is less than the parameter.
    This is algorithm A2.1 on pg 68 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    degree -- degree of polynomial segments
    parameter -- parameteric coordinate of B-Spline
    knotVector -- list of parametric coords that define knot locations
    """
    if parameter < knotVector[0] or parameter > knotVector[-1]:
        raise IndexError("parameter == {} out of range: [{}, {}]".format(parameter, knotVector[0], knotVector[-1]))
    m = len(knotVector) - 1
    n = m - degree - 1
    assert n + degree + 1 == m, "Invalid n. Should be: {} not {}".format(m - degree - 1, n)
    if parameter == knotVector[n+1]: return n # Special case
    # Do binary search
    low = degree
    high = n + 1
    mid = (low + high) // 2
    while parameter < knotVector[mid] or parameter >= knotVector[mid+1]:
        if parameter < knotVector[mid]: 
            high = mid
        else:
            low = mid
        mid = (low + high) // 2
    return mid

def WeightedControlPoints(controlPoints, weights, dimension):
    """
    Returns weight control point tensor with each 
    
    Arguments:
    controlPoints -- list of control point coordinates
    weights -- list of control point weights
    dimension -- dimension of geometric object
    
    Constraints:
    number of control points = number of weights
    dimension = 1 for curve
    dimension = 2 for surface
    dimension = 3 for volume
    """
    if dimension == 1:
        Pw = np.zeros((len(controlPoints), len(controlPoints[0]) + 1))
        for i in range(len(controlPoints)):
            Pw[i][len(controlPoints[0])] = weights[i]    
            for j in range(len(controlPoints[0])):
                Pw[i][j] = weights[i] * controlPoints[i][j]
    
    if dimension == 2:
        Pw = np.zeros((len(controlPoints), len(controlPoints[0]), len(controlPoints[0][0]) + 1))
        for i in range(len(controlPoints)):
            for j in range(len(controlPoints[0])):
                Pw[i][j][-1] = weights[i][j]
                for k in range(len(controlPoints[0][0])):
                    Pw[i][j][k] = weights[i][j] * np.array(controlPoints[i][j][k])
    return Pw

def BSplineBasisFuns(i, parameter, degree, knotVector):
    """
    Returns list of all non-zero B-Spline basis functions.
    This is algorthim A2.2 on pg 70 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    i -- index
    parameter -- parameteric coordinate
    degree -- degree of polynomial segments
    knotVector -- list of parametric coords that define knot locations
    """
    # 
    B = np.nan * np.ones(degree + 1)
    B[0] = 1.0
    left = np.nan * np.ones_like(B)
    right = np.nan * np.ones_like(B)
    for j in range(1, degree + 1):
        left[j] = parameter - knotVector[i+1-j]
        right[j] = knotVector[i+j]-parameter
        saved = 0.0
        for r in range(j):
            temp = B[r] / (right[r+1] + left[j-r])
            B[r] = saved + right[r+1] * temp
            saved = left[j-r] * temp
        B[j] = saved
    return B

def BSplineCurvePoint(parameter, knotVector, degree, controlPoints):
    """
    Returns a list of 3D Cartesian coordinates at a given parametric point on a B-Spline curve.
    This is algorithm A3.1 on pg 82 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    parameter -- parameteric coordinate
    knotVector -- list of parametric coords that define knot locations
    degree -- degree of polynomial segments
    controlPoints -- list of control point coordinates
    """
    span = FindSpan(degree, parameter, knotVector)
    B = BSplineBasisFuns(span, parameter, degree, knotVector)
    C = 0
    for i in range(degree + 1):
        C += B[i] * np.array(controlPoints[span-degree+i])
    return C

def NURBSCurvePoint(parameter, knotVector, degree, controlPoints, weights):
    """
    Returns a list of 3D Cartesian coordinates at a given parametric point on a NURBS curve.
    This is algorithm A4.1 on pg 124 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    parameter -- parameteric coordinate
    knotVector -- list of parametric coords that define knot locations
    degree -- degree of polynomial segments
    controlPoints -- list of control point coordinates
    weights -- list of control point weights
    """
    dimension = 1
    Pw = WeightedControlPoints(controlPoints, weights, dimension)
    span = FindSpan(degree, parameter, knotVector)
    B = BSplineBasisFuns(span, parameter, degree, knotVector)
    Cw = 0
    for j in range(degree+1):
        Cw += B[j] * Pw[span-degree+j]
    C = np.zeros(len(Cw)-1)
    for k in range(len(C)):
        C[k] = Cw[k] / Cw[-1]
    return C
    
def NURBSSurfacePoint(parameter1, parameter2, knotVector1, knotVector2, degree1, degree2, controlPoints, weights):
    """
    Returns a list of 3D Cartesian coordinates at a given parametric point on a NURBS surface.
    This is algorithm A4.3 on pg 134 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    controlPoints -- list (structured like array) that contains Cartesian control point coordinates
    degree1 -- degree of polynomial segments in direction 1
    degree2 -- degree of polynomial segments in direction 2
    knotVector1 -- list of parametric coords that define knot locations in direction 1
    knotVector2 -- list of parametric coords that define knot locations in direction 2
    weights -- list of control point weights
    """
    dimension = 2
    Pw = WeightedControlPoints(controlPoints, weights, dimension)
    parameter1span = FindSpan(degree1, parameter1, knotVector1)
    B1 = BSplineBasisFuns(parameter1span, parameter1, degree1, knotVector1)
    parameter2span = FindSpan(degree2, parameter2, knotVector2)
    B2 = BSplineBasisFuns(parameter2span, parameter2, degree2, knotVector2)
    temp = np.nan * np.ones(degree2 + 1, dtype=np.ndarray)
    for l in range(degree2 + 1):
        temp[l] = 0
        for k in range(degree1 + 1):
            temp[l] += B1[k] * np.array(Pw[parameter1span-degree1+k][parameter2span-degree2+l])
    Sw = 0
    for l in range(degree2 + 1):
        Sw += B2[l] * temp[l]
    S = np.zeros(len(Sw)-1)
    for k in range(len(S)):
        S[k] = Sw[k] / Sw[-1]
    return S


