from flask import Flask, render_template, request,make_response,jsonify
import numpy as np
import cv2
import pandas as pd
import math

class Knn:
    def __init__(self, data):
        self.data = data
     
    def classificationFruit(self, x,n):
        def distance(WorldPoint,currentPoint):
            vecxtov = [WorldPoint[i] - currentPoint[i] for i in range(len(WorldPoint))] 
            distacc = 0
            for pos in vecxtov:
                distacc += pos**2
            return math.sqrt(distacc)
        
        knndf  = self.data.copy()
        knndf["distance"] = knndf.iloc[:, 3:].apply(distance,currentPoint=x, axis=1)
        knndf = knndf.sort_values(by='distance', ascending=True).fruit
        
        knnselection = knndf.head(n)
        classification = knnselection.value_counts().index[0]

        keys = knnselection.value_counts().index.tolist()
        classes = knnselection.value_counts().tolist()
        classes = list(map(lambda x: x/n, classes))
        report = dict(zip(keys, classes))
        return  classification,report
    def classificationRotten(self, x,n,fruit):
        def distance(WorldPoint,currentPoint):
            vecxtov = [WorldPoint[i] - currentPoint[i] for i in range(len(WorldPoint))] 
            distacc = 0
            for pos in vecxtov:
                distacc += pos**2
            return math.sqrt(distacc)
        
        knndf  = self.data.copy()
        knndf = knndf[knndf.fruit ==fruit]
        knndf["distance"] = knndf.iloc[:, 3:].apply(distance,currentPoint=x, axis=1)
        knndf = knndf.sort_values(by='distance', ascending=True).state
        
        knnselection = knndf.head(n)
        classification = knnselection.value_counts().index[0]

        keys = knnselection.value_counts().index.tolist()
        classes = knnselection.value_counts().tolist()
        classes = list(map(lambda x: x/n, classes))
        report = dict(zip(keys, classes))
        return  classification,report


app =Flask(__name__)
df = pd.read_csv("fruitdata.csv")
#print(df.head(2))
df.fruit= df.fruit.astype('category')
df.state = df.state.astype('category')
df["fruit"] = df["fruit"].map({"apple": 0, "banana": 1,"oranges":2})
df["state"] = df["state"].map({"good": 1, "bad": 0})
fruitKnn = Knn(df)



def classification(img):
    global fruitKnn
    img = img.astype(np.float32)
    img [img >240]=-1
    (b,g,r) = cv2.split(img)

    dimension = img.shape[0]*img.shape[1]
    histR = cv2.calcHist([r], [0], None, [256], [0, 256]).ravel()
    histG = cv2.calcHist([g], [0], None, [256], [0, 256]).ravel()
    histB = cv2.calcHist([b], [0], None, [256], [0, 256]).ravel()
    hist = np.concatenate([histR,histG,histB])
    hist = hist.astype(np.float32)
    hist = hist/dimension
    hist = list(hist)
    
    fruitInt,reportFruit = selectFruit(hist)
    rottenInt,reportState = selectRottenLevel(hist,fruitInt)

    inverseMapFruit = {0: "apple",1:"banana",2:"oranges"}
    inverseMapRotten = {1:"good",0: "bad"}

    return [inverseMapFruit[fruitInt],reportFruit,inverseMapRotten[rottenInt],reportState]

def selectFruit(hist):
    neighboorhods = 4
    classificationFruit = fruitKnn.classificationFruit(hist,neighboorhods)
    return classificationFruit

def selectRottenLevel(hist,fruitInt):
    neighboorhods = 5
    classificationRotten = fruitKnn.classificationRotten(hist,neighboorhods,fruitInt)
    return classificationRotten
    

    #print(hist)
#Configurar ruta de inicio
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/edges',methods=['POST'])
def edges():
    if request.method == 'POST':
        #Leer imagen desde interfaz a formato de python
        File = request.files['picture'].read()
        npimg = np.fromstring(File, np.uint8)
        img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        fruit,reportFruit,rotten,reportState = classification(img)
        FinalResults = {"fruit":fruit,"state":rotten}
        FinalResults["good"]= reportState[1]
        FinalResults["bad"]= reportState[0]
        FinalResults["apple"]= reportFruit[0]
        FinalResults["banana"]= reportFruit[1]
        FinalResults["oranges"]= reportFruit[2]
        print(FinalResults)
        #prediction = trainexample(img)
        return jsonify(FinalResults)  
    else:
        return "none"


if __name__ == '__main__':
    app.run(debug=True)