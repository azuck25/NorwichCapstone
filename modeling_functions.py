import pandas as pd
import numpy as np



def meanAbsoluteDev(vec1,n):
    mean = np.average(vec1)
    sum = 0
    for i in vec1:
        sum += abs(i - mean)
    return sum/n

def sampleVariance(vec1,n):
    mean = np.average(vec1)
    sum = 0
    for i in vec1:
        tempNum1 = (i - mean)
        tempNum2 = pow(tempNum1,2)
        sum += tempNum2
    return (sum/(n-1))

def sampleStndDev(vec1,n):
    mean = np.average(vec1)
    sum = 0
    for i in vec1:
        tempNum1 = (i - mean)
        tempNum2 = pow(tempNum1,2)
        sum  += tempNum2
    return np.sqrt(sum/(n-1))


def downsideDeviation(vec1,B,n):
    sum = 0
    for i in vec1:
        tempNum1 = pow((i - B),2)
        tempNum2 = tempNum1/(n-1)
        sum += tempNum2
    return np.sqrt(sum)

def geometricMean(vec1):
    geoR = 1
    for i in vec1:
        geoR *= (1+i)
    return np.sqrt(geoR)-1


def covariance(vecX,vecY,n):
    meanX = np.average(vecX)
    meanY = np.average(vecY)
    sumXY = 0
    for i,j in zip(vecX,vecY):
        sumXY += (i - meanX)*(j - meanY)
    return sumXY/(n-1)

def geometricMeanReturn(vecX, n): 
    product = 1
    for i in zip(vecX):
        product *= (1+vecX)
    prodExp = np.power(product,n)
    return prodExp-1

def arithmeticReturn(vecX,n):
    sumReturns = 0
    for i in zip(vecX):
        sumReturns += vecX
    arithR = sumReturns / n
    return arithR

def holdingPeriodReturn(n1,n2)