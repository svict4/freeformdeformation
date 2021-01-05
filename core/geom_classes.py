import geom_functions as gf
import numpy as np

class BSplineCurve:
    """
    Creates a B-Spline curve object.
    
    Keyword arguments:
    controlPoints -- list of Cartesian control point coordinates
    degree -- degree of polynomial segments
    knotVector -- list of parametric coords that define knot locations
    
    Constraints:
    len(controlPoints) - 1 >= degree >= 1
    """
    def __init__(self, **kwargs):
        pass
        
    def KnotLocations(self, **kwargs):
        # Returns a list that contains sublists of Cartesian knot coordinates.
        return [gf.BSplineCurvePoint(x, self.knotVector, self.degree, self.controlPoints) for x in self.knotVector]
    
    def Evaluate(self, N=100, **kwargs):
        """
        Returns a list of Cartesian curve coordinates.
        
        Keyword arguments:
        start -- parametric coordinate at which curve begins (default value shown below)
        stop -- parametric coordinate at which curve stops (default value shown below)
        N -- number of points evaluated between start and stop (default = 100)
        """
        start = kwargs.get('start', self.knotVector[self.degree])
        stop = kwargs.get('stop', self.knotVector[-(self.degree + 1)])
        parameterValues = np.linspace(start, stop, N)
        return [gf.BSplineCurvePoint(x, self.knotVector, self.degree, self.controlPoints) for x in parameterValues]

class NURBSCurve:
    """
    Creates a NURBS curve object.
    
    Keyword arguments:
    controlPoints -- list of Cartesian control point coordinates
    degree -- degree of polynomial segments
    knotVector -- list of parametric coords that define knot locations
    weights -- list of control point weights
    
    Constraints:
    len(controlPoints) - 1 >= degree >= 1
    len(weights) == len(controlPoints)
    """
    def __init__(self, **kwargs):
        pass
        
    def KnotLocations(self, **kwargs):
        # Returns a list that contains sublists of Cartesian knot coordinates.
        return [gf.NURBSCurvePoint(x, self.knotVector, self.degree, self.controlPoints, self.weights) for x in self.knotVector]
    
    def Evaluate(self, N=100, **kwargs):
        """
        Returns a list of Cartesian curve coordinates.
        
        start -- parametric coordinate at which curve begins (default value shown below)
        stop -- parametric coordinate at which curve stops (default value shown below)
        N -- number of points evaluated between start and stop (default = 100)
        """
        start = kwargs.get('start', self.knotVector[self.degree])
        stop = kwargs.get('stop', self.knotVector[-(self.degree + 1)])
        parameterValues = np.linspace(start, stop, N)
        return [gf.NURBSCurvePoint(x, self.knotVector, self.degree, self.controlPoints, self.weights) for x in parameterValues]

class NURBSSurface:
    """
    Creates a NURBS surface object.
    
    Keyword arguments:
    controlPoints -- list (structured like array) that contains Cartesian control point coordinates
    degree1 -- degree of polynomial segments in direction 1
    degree2 -- degree of polynomial segments in direction 2
    knotVector1 -- list of parametric coords that define knot locations in direction 1
    knotVector2 -- list of parametric coords that define knot locations in direction 2
    weights -- list of control point weights
    
    Constraints:
    shape(list) = number of control points in direction 1, and shape(list[0]) = number of control points in direction 2
    len(controlPoints) - 1 >= degree1 >= 1
    len(controlPoints[0]) - 1 >= degree2 >= 1
    len(weights) == len(controlPoints)
    len(weights[0]) == len(controlPoints[0])
    """
    def __init__(self, **kwargs):
        pass
    
    def KnotLocations(self, **kwargs):
        # Returns a list that contains sublists of Cartesian knot coordinates.
        knots = []
        for x in self.knotVector1:
            for y in self.knotVector2:
                knots.append(gf.NURBSSurfacePoint(x, y, self.knotVector1, self.knotVector2, self.degree1, self.degree2, self.controlPoints, self.weights))
        return knots
    
    def Evaluate(self, N1=50, N2=50, **kwargs):
        """
        Returns a list (structured like array) that contains Cartesian surface coordinates.
        
        Keyword arguments:.
        start1 -- parametric coordinate at which surface begins in direction 1 (default value shown below)
        stop1 -- parametric coordinate at which surface stops in direction 1 (default value shown below)
        start2 -- parametric coordinate at which surface begins in direction 2 (default value shown below)
        stop2 -- parametric coordinate at which surface stops in direction 2 (default value shown below)
        N1 -- number of points evaluated between start and stop in direction 1 (default = 50)
        N2 -- number of points evaluated between start and stop in direction 2 (default = 50)
        """
        start1 = kwargs.get('start1', self.knotVector1[self.degree1])
        stop1 = kwargs.get('stop1', self.knotVector1[-(self.degree1 + 1)])
        parameter1values = np.linspace(start1, stop1, N1)
        
        start2 = kwargs.get('start2', self.knotVector2[self.degree2])
        stop2 = kwargs.get('stop2', self.knotVector2[-(self.degree2 + 1)])
        parameter2values = np.linspace(start2, stop2, N2)
        
        parameter1mesh, parameter2mesh = np.meshgrid(parameter1values, parameter2values)
        S = np.nan * np.ones((len(parameter1mesh), len(parameter1mesh[0])), dtype=np.ndarray)
        for i in range(len(parameter1mesh)):
            for j in range(len(parameter1mesh[0])):
                S[i][j] = gf.NURBSSurfacePoint(parameter1mesh[i][j], parameter2mesh[i][j], self.knotVector1, self.knotVector2, self.degree1, self.degree2, self.controlPoints, self.weights)
        return S
    
