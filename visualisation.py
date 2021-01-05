import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import geom_functions as gf
import geom_classes as gc

def CurvePlot(curve, showControlPoints=True, showKnots=True, showControlPolygon=True, dimension='3D', N=100, **kwargs):
    """
    Produces a plot of a given curve.
    
    Arguments & Keyword Arguments:
    curve -- a curve object defined by a class from geom_classes.py
    showControlPoints -- option to plot control points (default = True)
    showKnots -- option to plot knots (default = True)
    showControlPolygon -- option to plot control polygon (default = True)
    dimension -- dimension of plot (either '2D' or '3D', default = '3D')
    N -- number of points evaluated along curve (deafult = 100)
    """
    start = kwargs.get('start', curve.knotVector[curve.degree])
    stop = kwargs.get('stop', curve.knotVector[-(curve.degree + 1)])
    curvePoints = curve.Evaluate(start=start, stop=stop, N=N)
    
    # evaluting points along the curve
    curvePointXs, curvePointYs = [], []
    for i in range(len(curvePoints)):
        curvePointXs.append(curvePoints[i][0])
        curvePointYs.append(curvePoints[i][1])
    
    # plot curve
    fig = plt.figure()
    if dimension == '2D':
        plt.axes()
        plt.plot(curvePointXs, curvePointYs,'k', label='Curve')
    elif dimension == '3D':
        curvePointZs = [curvePoints[i][2] for i in range(len(curvePoints))]
        ax = plt.axes(projection='3d')
        ax.plot(curvePointXs, curvePointYs, curvePointZs, 'k', label='Curve')
    else:
        print('Invalid plot dimension specified.')
    
    # plot control points if desired
    if showControlPoints == True:
        controlPointXs, controlPointYs = [], []
        for i in range(len(curve.controlPoints)):
            controlPointXs.append(curve.controlPoints[i][0])
            controlPointYs.append(curve.controlPoints[i][1])
        if dimension == '2D':
            plt.plot(controlPointXs, controlPointYs, 'ro', label='Control Points')
            
        elif dimension == '3D':
            controlPointZs = [curve.controlPoints[i][2] for i in range(len(curve.controlPoints))]
            ax.plot(controlPointXs, controlPointYs, controlPointZs, 'ro', label='Control Points')
            
    # plot control polygon if desired
    if showControlPolygon == True:
        if dimension == '2D':
            plt.plot(controlPointXs, controlPointYs, 'b-', alpha=0.3, label='Control Polygon')
        if dimension == '3D':
            ax.plot(controlPointXs, controlPointYs, controlPointZs, 'b-', alpha=0.3, label='Control Polygon')
    
    # plot knots if desired
    if showKnots == True:
        knotLocations = curve.KnotLocations()
        knotXs, knotYs = [], []
        for i in range(len(knotLocations)):
            knotXs.append(knotLocations[i][0])
            knotYs.append(knotLocations[i][1])
        if dimension == '2D':
            plt.plot(knotXs, knotYs, 'gx', label='Knots')
        elif dimension == '3D':
            knotZs = [knotLocations[i][2] for i in range(len(knotLocations))]
            ax.plot(knotXs, knotYs, knotZs, 'gx', label='Knots')
    
    if dimension == '2D':
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.axis('equal')
        plt.grid()
    elif dimension == '3D':
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")
    
    plt.legend()
    plt.show()

def SurfacePlot(surface, showControlPoints=True, showKnots=True, showControlPolygon=True, N1=50, N2=50, **kwargs):
    """
    Produces a plot of a given surface.
    
    Arguments & Keyword Arguments:
    surface -- a surface object defined by a class from geom_classes.py
    showControlPoints -- option to plot control points (default = True)
    showKnots -- option to plot knots (default = True)
    showControlPolygon -- option to plot control polygon (default = True)
    dimension -- dimension of plot (either '2D' or '3D', default = '3D')
    N1 -- number of points evaluated along surface in direction 1 (deafult = 50)
    N2 -- number of points evaluated along surface in direction 2 (deafult = 50)
    """
    start1 = kwargs.get('start1', surface.knotVector1[surface.degree1])
    stop1 = kwargs.get('stop1', surface.knotVector1[-(surface.degree1 + 1)])

    start2 = kwargs.get('start2', surface.knotVector2[surface.degree2])
    stop2 = kwargs.get('stop2', surface.knotVector2[-(surface.degree2 + 1)])
    
    surfacePoints = surface.Evaluate(start1=start1, stop1=stop1, N1=N1, start2=start2, stop2=stop2, N2=N2)
    surfacePointXs, surfacePointYs, surfacePointZs = np.zeros((N2, N1)), np.zeros((N2, N1)), np.zeros((N2, N1))
    for i in range(len(surfacePoints)):
        for j in range(len(surfacePoints[0])):
            surfacePointXs[i][j] = surfacePoints[i][j][0]
            surfacePointYs[i][j] = surfacePoints[i][j][1]
            surfacePointZs[i][j] = surfacePoints[i][j][2]
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(surfacePointXs, surfacePointYs, surfacePointZs, color='black', label='Surface')
    
    if showControlPoints == True:
        controlPointXs, controlPointYs, controlPointZs = [], [], []
        Pw = gf.WeightedControlPoints(surface.controlPoints, surface.weights, dimension=2)
        for i in range(len(Pw)):
            for j in range(len(Pw[0])):
                controlPointXs.append(surface.controlPoints[i][j][0])
                controlPointYs.append(surface.controlPoints[i][j][1])
                controlPointZs.append(surface.controlPoints[i][j][2])
        ax.scatter3D(controlPointXs, controlPointYs, controlPointZs, color='red', label='Control Points')
    
    if showControlPolygon == True:
        # plotting control polygon 1
        for i in range(len(surface.controlPoints)):
            tempXs, tempYs, tempZs = [], [], []
            for j in range(len(surface.controlPoints[0])):
                tempXs.append(surface.controlPoints[i][j][0])
                tempYs.append(surface.controlPoints[i][j][1])
                tempZs.append(surface.controlPoints[i][j][2])
            if i == 0:
                ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3, label='Control Polygon')
            else:
                ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3)
        
        # plotting control polygon 2
        for j in range(len(surface.controlPoints[0])):
            tempXs, tempYs, tempZs = [], [], []
            for i in range(len(surface.controlPoints)):
                tempXs.append(surface.controlPoints[i][j][0])
                tempYs.append(surface.controlPoints[i][j][1])
                tempZs.append(surface.controlPoints[i][j][2])
            ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3)
    
    if showKnots == True:
        knotLocations = surface.KnotLocations()
        knotXs, knotYs, knotZs = [], [], []
        for i in range(len(knotLocations)):
            knotXs.append(knotLocations[i][0])
            knotYs.append(knotLocations[i][1])
            knotZs.append(knotLocations[i][2])
        ax.plot(knotXs, knotYs, knotZs, 'gx', label='Knots')
     
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    plt.legend()
    plt.show()
