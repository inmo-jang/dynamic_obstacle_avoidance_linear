#!/usr/bin/python3
import numpy as np
from numpy import pi

import time

from dynamic_obstacle_avoidance.obstacle_avoidance.obstacle import *
from dynamic_obstacle_avoidance.obstacle_avoidance.modulation import *
from dynamic_obstacle_avoidance.visualization.animated_simulation import run_animation, samplePointsAtBorder


def main():
    N = 1
    x_init = np.vstack((np.ones(N)*1.22485,
                        np.ones(N)*8))

    ### Create obstacle 
    obs = []
    a = np.array([1.7051, 1.22958]) 
    x0 = np.array([-0.530183, 0.999465])
    sf = 1 + 0.46373
    th_r = 2 * np.pi - 2.31767
    obs.append(Obstacle(a=a, x0=x0, sf=sf, th_r=th_r))

    # a = np.array([1, 1]) 
    # x0 = np.array([0.5, -0.5])
    # obs.append(Obstacle(a=a, x0=x0, sf=sf))

    # a = np.array([1, 1]) 
    # x0 = np.array([1, 1.5])
    # obs.append(Obstacle(a=a, x0=x0, sf=sf))

    attractorPos = np.array([4.90769, -8])

    xRange = [-10, 10]
    yRange = [-10, 10]
    zRange = [-10, 10]

    animationName = 'test.mp4'
    run_animation(x_init, obs, xRange=xRange, yRange=yRange, dt=0.01, N_simuMax=1040, convergenceMargin=0.3, sleepPeriod=0.01, attractorPos=attractorPos, animationName=animationName, saveFigure=False)


if __name__ == '__main__':
    main()