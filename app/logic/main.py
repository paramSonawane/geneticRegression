import pandas as pd
import numpy as np

import random

from scipy import optimize

from miniProject.settings import BASE_DIR

df = pd.read_csv(BASE_DIR / "app/logic/Mumbai.csv")
df['Price'] = df['Price']/100000
X1 = np.array(df['Area'])
X1 = X1.reshape((len(X1),1))
X2 = np.array(df['No. of Bedrooms'])
X2 = X2.reshape((len(X2),1))
Y = np.array(df['Price'])
Y = Y.reshape(len(Y), 1)

split = int(0.7 * X1.shape[0])

X1_train = X1[:split]
X1_test = X1[split:]
X2_train = X2[:split]
X2_test = X2[split:]
y_train = Y[:split]
y_test = Y[split:]

Dn = 3
M = 0.7
NP = 1000
G = 290

graphData = {
    'X' : [],
    'Y' : [],
    'Z' : []
}
def getData():
    return graphData

def hypothesis(w, x1=X1_train, x2 = X2_train):
    return x1*w[0] + x2*w[1] + w[2]

# Loss Function
def f(w):
    y = hypothesis(w)
    y = np.reshape(y,(-1,1))
    return ((y_train - y)**2).sum()

def crossover(parent_1, parent_2):
    child_1 = np.zeros(parent_1.shape)
    child_2 = np.zeros(parent_2.shape)
    dim = int(parent_1.shape[0] / 2.0)
#     child_1[:dim] = (parent_1[:dim] + parent_2[:dim])/2
#     child_1[dim:] = (parent_1[dim:] + parent_2[dim:])/2
    child_1 = 0.5 * (parent_1 + parent_2)
#     child_2[:dim] = parent_2[:dim]
#     child_2[dim:] = parent_1[dim:]
    child_2 = 1.5 * parent_1 - 0.5 * parent_2

    return child_1, child_2

def mutate(x):
    for ix in range(x.shape[0]):
        # Generate a random number for probability
        R = np.random.random()

        if R < M:
            # Mutate random index
            x[ix] = np.random.normal(0, 10000)
        else:
            pass
    return x

loss = []
pop = []

for ix in range(NP):
    vec = np.random.normal(10, 1000, (Dn,))
    pop.append(vec)


def trainGenAlgo():
    # global graphData
    global pop
    # Main Genetic Algo loop

    oldVal = 0
    for gx in range(G):
        pop = sorted(pop, key=lambda z: f(z))
        # if True:#gx%10 == 0:

        print ("Generation: {} | Best Value: {}".format(gx, f(pop[0])))

        loss.append(f(pop[0]))

        # create a temp population
        temp = []

        while not len(temp) == NP:
            # Select 2 parents from good section of population
    #         p1, p2 = random.sample(pop[:int(NP/2.0)], 2)
            index1 = random.randint(0, 100000) % int(NP / 4)
            index2 = random.randint(0, 10000000) % int(NP / 4)
            p1 = pop[index1]
            p2 = pop[index2]

            # Apply crossover
            c1, c2 = crossover(p1, p2)

            # mutate
            c1 = mutate(c1)
            c2 = mutate(c2)

            temp.append(c1)
            temp.append(c2)

        # create a combined population
        comb = temp + pop

        # survival of the fittest
        pop = sorted(comb, key=lambda z: f(z))[:NP]

        if f(pop[0])!= oldVal and gx>50:
            x,y,z = getGraphData()
            graphData['Z'].append(z)
            print("added at", gx)

        oldVal = f(pop[0])

def hypothesis_test(w, x1=X1_test, x2 = X2_test):
    return x1*w[0] + x2*w[1] + w[2]

def f_test(w):
    y = hypothesis_test(w)
    print(y.shape)
    y = np.reshape(y,(-1,1))
    return ((y_test - y)**2)

def predictPrice(area, rooms) :
    return pop[0][0] * area + pop[0][1] * rooms + pop[0][2]

def curvedModel(data, a, b, c, Offset):
    x = data[0]
    y = data[1]
    return np.exp(a+b/y+c*np.log(x)) + Offset

def flatModel(data, a, b, Offset):
    x = data[0]
    y = data[1]
    return a*x + b*y + Offset

def getGraphData():
    graphWidth = 800
    graphHeight = 600
    numberOfContourLines = 16

    xData = X1_train.reshape(1,-1)[0]
    yData = X2_train.reshape(1,-1)[0]
    zData = hypothesis(pop[0]).reshape(1, -1)[0]

    func = curvedModel
    initialParameters = [1.0, 1.0, 1.0, 1.0]

    data = [xData, yData, zData]
    fittedParameters, pcov = optimize.curve_fit(func, [xData, yData], zData, p0 = initialParameters, maxfev=1000)

    x_data = data[0]
    y_data = data[1]
    z_data = data[2]

    xModel = np.linspace(min(x_data), max(x_data), 20)
    yModel = np.linspace(min(y_data), max(y_data), 20)
    X, Y = np.meshgrid(xModel, yModel)

    Z = func(np.array([X, Y]), *fittedParameters)

    return X.tolist(),Y.tolist(),Z.tolist()

if __name__ == "__main__" :
    trainGenAlgo()
    print(graphData['Z'][-2] == graphData['Z'][1])
    # print(graphData['Z'][1])