'''
Obstacle Avoidance Library with different options

@author Lukas Huber
@date 2018-02-15

'''
import numpy as np
import numpy.linalg as LA
from numpy import pi

from math import cos, sin

import warnings

from lib_ds.dynamicalSystem_lib import *


def getGammmaValue_ellipsoid(ob, x_t, relativeDistance=True):
    if relativeDistance:
        return np.sum( (x_t/np.tile(ob.a, (x_t.shape[1],1)).T) **(2*np.tile(ob.p, (x_t.shape[1],1) ).T ), axis=0)
    else:
        return np.sum( (x_t/np.tile(ob.a, (x_t.shape[1],1)).T) **(2*np.tile(ob.p, (x_t.shape[1],1) ).T ), axis=0)

def get_radius_ellipsoid(x_t, a=[], ob=[]):
    # Derivation from  x^2/a^2 + y^2/b^2 = 1
    
    if not np.array(a).shape[0]:
        a = ob.a

    if x_t[0]:
        rat_x1_x2 = x_t[1]/x_t[0]
        x_1_val = np.sqrt(1./(1./a[0]**2+1.*rat_x1_x2**2/a[1]**2))
        return x_1_val*np.sqrt(1+rat_x1_x2**2)
    else:
        return a[1]
    
def get_radius(vec_ref2point, vec_cent2ref=[], a=[], obs=[]):
    dim = 2 # TODO higher dimensions

    if not np.array(vec_cent2ref).shape[0]:
        vec_cent2ref = np.array(obs.center_dyn) - np.array(obs.x0)
        
    if not np.array(a).shape[0]:
        a = obs.a
        
    if not LA.norm(vec_cent2ref): # center = ref
        return get_radius_ellipsoid(vec_ref2point, a)
    
    dir_surf_cone = np.zeros((dim, 2))
    rad_surf_cone = np.zeros((2))

    if np.cross(vec_ref2point, vec_cent2ref) > 0:
        dir_surf_cone[:, 0] = vec_cent2ref
        rad_surf_cone[0] = get_radius_ellipsoid(dir_surf_cone[:, 0], a)-LA.norm(vec_cent2ref)
        
        dir_surf_cone[:, 1] = -1*np.array(vec_cent2ref)
        rad_surf_cone[1] = get_radius_ellipsoid(dir_surf_cone[:, 1], a)+LA.norm(vec_cent2ref)
 
    else:
        dir_surf_cone[:, 0] = -1*np.array(vec_cent2ref)
        rad_surf_cone[0] = get_radius_ellipsoid(dir_surf_cone[:, 0], a)+LA.norm(vec_cent2ref)
        
        dir_surf_cone[:, 1] = vec_cent2ref
        rad_surf_cone[1] = get_radius_ellipsoid(dir_surf_cone[:, 1], a)-LA.norm(vec_cent2ref)
    
    ang_tot = pi/2
    for ii in range(12): # n_iter
        rotMat = np.array([[np.cos(ang_tot), np.sin(ang_tot)],
                           [-np.sin(ang_tot), np.cos(ang_tot)]])

        # vec_ref2dir = rotMat @ dir_surf_cone[:, 0]
        vec_ref2dir = np.matmul(rotMat , dir_surf_cone[:, 0])


        vec_ref2dir /= LA.norm(vec_ref2dir) # nonzero value expected
        
        rad_ref2 = get_radius_ellipsoid(vec_ref2dir, a)
        vec_ref2surf = rad_ref2*vec_ref2dir - vec_cent2ref

        if np.cross(vec_ref2surf, vec_ref2point)==0: # how likely is this lucky guess? 
            return LA.norm(vec_ref2surf)
        elif np.cross(vec_ref2surf, vec_ref2point) < 0:
            dir_surf_cone[:, 0] = vec_ref2dir
            rad_surf_cone[0] = LA.norm(vec_ref2surf)
        else:
            dir_surf_cone[:, 1] = vec_ref2dir
            rad_surf_cone[1] = LA.norm(vec_ref2surf)

        ang_tot /= 2.0
    return np.mean(rad_surf_cone)


def findRadius(ob, direction, a = [], repetition = 6, steps = 10):
    # NOT SURE IF USEFULL -- NORMALLY x = Gamma*Rad
    # TODO check
    if not len(a):
        a = [np.min(ob.a), np.max(ob.a)]
        # a = obs.a
        
    # repetition
    for ii in range(repetition):
        if a[0] == a[1]:
            return a[0]
        
        magnitudeDir = np.linspace(a[0], a[1], num=steps)
        Gamma = getGammmaValue_ellipsoid(ob, np.tile(direction, (steps,1)).T*np.tile(magnitudeDir, (np.array(ob.x0).shape[0],1)) )

        if np.sum(Gamma==1):
            return magnitudeDir[np.where(Gamma==1)]
        posBoundary = np.where(Gamma<1)[0][-1]

        a[0] = magnitudeDir[posBoundary]
        posBoundary +=1
        while Gamma[posBoundary]<=1:
            posBoundary+=1

        a[1] = magnitudeDir[posBoundary]
        
    return (a[0]+a[1])/2.0


def findBoundaryPoint(ob, direction):
    # Numerical search -- TODO analytic
    dirNorm = LA.norm(direction,2)
    if dirNorm:
        direction = direction/dirNorm
    else:
        print('No feasible direction is given')
        return ob.x0

    a = [np.min(x0.a), np.max(x0.a)]
    
    return (a[0]+a[1])/2.0*direction + x0


def compute_eigenvalueMatrix(Gamma, rho=1, dim=2, radialContuinity=True):
    if radialContuinity:
        Gamma = np.max([Gamma, 1])
        
    delta_lambda = 1./np.abs(Gamma)**(1/rho)
    lambda_referenceDir = 1-delta_lambda
    lambda_tangentDir = 1+delta_lambda

    return np.diag(np.hstack((lambda_referenceDir, np.ones(dim-1)*lambda_tangentDir)) )


         


def compute_weights(distMeas, N=0, distMeas_min=1, weightType='inverseGamma', weightPow=2):
    # UNTITLED5 Summary of this function goes here
    #   Detailed explanation goes here

    distMeas = np.array(distMeas)
    n_points = distMeas.shape[0]
    
    critical_points = distMeas < distMeas_min
    
    if np.sum(critical_points): # at least one
        if np.sum(critical_points)==1:
            w = critical_points*1.0
            return w
        else:
            # TODO: continuous weighting function
            warnings.warn('Implement continuity of weighting function.')
            w = critical_points*1./np.sum(critical_points)
            return w
        
    if weightType == 'inverseGamma':
        distMeas = np.max(np.vstack((distMeas-distMeas_min, np.zeros(distMeas.shape))) , axis=0)
        w = 1/distMeas**weightPow
        w = w/np.sum(w) # Normalization

    else:
        warnings.warn("Unkown weighting method.")

    return w


def compute_R(d, th_r):
    if th_r == 0:
        rotMatrix = np.eye(d)
    # rotating the query point into the obstacle frame of reference
    if d==2:
        rotMatrix = np.array([[np.cos(th_r), -np.sin(th_r)],
                              [np.sin(th_r),  np.cos(th_r)]])
    elif d==3:
        R_x = np.array([[1, 0, 0,],
                        [0, np.cos(th_r[0]), np.sin(th_r[0])],
                        [0, -np.sin(th_r[0]), np.cos(th_r[0])] ])

        R_y = np.array([[np.cos(th_r[1]), 0, -np.sin(th_r[1])],
                        [0, 1, 0],
                        [np.sin(th_r[1]), 0, np.cos(th_r[1])] ])

        R_z = np.array([[np.cos(th_r[2]), np.sin(th_r[2]), 0],
                        [-np.sin(th_r[2]), np.cos(th_r[2]), 0],
                        [ 0, 0, 1] ])

        rotMatrix = R_x.dot(R_y).dot(R_z)
    else:
        warnings.warn('rotation not yet defined in dimensions d > 3 !')
        rotMatrix = np.eye(d)

    return rotMatrix


def obs_check_collision_2d(obs_list, XX, YY):
    d = 2

    dim_points = XX.shape
    if len(dim_points)==1:
        N_points = dim_points[0]
    else:
        N_points = dim_points[0]*dim_points[1]

    # No obstacles
    if not len(obs_list):
        return np.ones((dim_points))
        
    points = np.array(([np.reshape(XX,(N_points,)) , np.reshape(YY, (N_points,)) ] ))
    # At the moment only implemented for 2D
    collision = np.zeros( dim_points )

    N_points = points.shape[1]

    noColl = np.ones((1,N_points))

    for it_obs in range(len(obs_list)):
        # on the surface, we have: \Gamma = \sum_{i=1}^d (xt_i/a_i)^(2p_i) == 1
        R = compute_R(d,obs_list[it_obs].th_r)

        # Gamma = np.sum( ( 1/obs_list[it_obs].sf * R.T @ (points - np.tile(np.array([obs_list[it_obs].x0]).T,(1,N_points) ) ) / np.tile(np.array([obs_list[it_obs].a]).T, (1, N_points)) )**(np.tile(2*np.array([obs_list[it_obs].p]).T, (1,N_points)) ), axis=0 )
        Gamma = np.sum( ( 1/obs_list[it_obs].sf * np.matmul(R.T , (points - np.tile(np.array([obs_list[it_obs].x0]).T,(1,N_points) ) ) ) / np.tile(np.array([obs_list[it_obs].a]).T, (1, N_points)) )**(np.tile(2*np.array([obs_list[it_obs].p]).T, (1,N_points)) ), axis=0 )


        noColl = (noColl* Gamma>1)

    return np.reshape(noColl, dim_points)


def obs_check_collision(points, obs_list=[]):
    # No obstacles
    if len(obs_list) == 0:
        return

    dim = points.shape[0]
    N_points = points.shape[1]

    # At the moment only implemented for 2D
    collision = np.zeros((N_points))

    noColl = np.ones((1,N_points))

    for it_obs in range(len(obs_list)):
        # \Gamma = \sum_{i=1}^d (xt_i/a_i)^(2p_i) = 1
        R = compute_R(dim,obs_list[it_obs].th_r)

        # Gamma = sum( ( 1/obs_list[it_obs].sf * R.T @ (points - np.tile(np.array([obs_list[it_obs].x0]).T,(1,N_points) ) ) / np.tile(np.array([obs_list[it_obs].a]).T, (1, N_points)) )**(np.tile(2*np.array([obs_list[it_obs].p]).T, (1,N_points)) ) )
        Gamma = sum( ( 1/obs_list[it_obs].sf * np.matmul(R.T , (points - np.tile(np.array([obs_list[it_obs].x0]).T,(1,N_points) ) ) ) / np.tile(np.array([obs_list[it_obs].a]).T, (1, N_points)) )**(np.tile(2*np.array([obs_list[it_obs].p]).T, (1,N_points)) ) )


        noColl = (noColl* Gamma>1)

    return noColl


def linearAttractor(x, x0=False, k_factor=1.0):
    x = np.array(x)
    
    if type(x0)==bool:
        x0 = np.zeros(x.shape)
        
    return (x0-x)*k_factor
    
    
def velConst_attr(x, vel, x0=False, velConst=6, distSlow=0.5):
    # change initial value for n dimensions
    # TODO -- constant velocity // maximum velocity
    if type(x0)==bool:
        dim = np.array(x).shape[0]
        x0 = np.zeros(dim)
        
    delta_x = x0-x
    dist_mag = np.sqrt(np.sum(delta_x**2))
    if dist_mag: # nonzero value
        new_mag = np.min([velConst, dist_mag/distSlow*velConst])


    vel_mag = np.sqrt(np.sum(vel**2))
    if vel_mag:
        vel = vel/vel_mag*new_mag
    
    return vel



