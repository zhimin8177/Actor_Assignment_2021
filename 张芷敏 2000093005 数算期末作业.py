import json
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
class Queue:
    def __init__(self,item):
        self.items = [item]
    def isEmpty(self):
        return self.items == []    
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    
    
class Movie:
    def __init__(self,_id,title,year,types,star,director,actor,pp,time,film_page):
        self.id = _id
        self.title = title
        self.year = year
        types0 = types.split(",")
        self.types = [x.strip() for x in types0]
        self.star = star
        self.director = director
        actor0 = actor.split(",")
        self.actor = [x.strip() for x in actor0]
        self.pp = pp
        self.time = time
        self.film_page = film_page
        
        
class Vertex:
    def __init__(self,key,movies):
        self.id = key
        self.connectedTo = {} #人名：剧集
        self.movies = movies
        self.color = "white"
        
    def addNeighbour(self,nbr,samemovie,weight=1):
        if nbr not in self.connectedTo:
            self.connectedTo[nbr] = [weight,set()]
            self.connectedTo[nbr][1].add(samemovie)
        else:
            self.connectedTo[nbr][1].add(samemovie)
            
    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])
    
    def getConnections(self):
        return self.connectedTo.keys()
    

    def getId(self):
        return self.id
    
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
    
class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.ccList = []
        self.demandList = []
        
    def addVertex(self,key,movies):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key,movies)
        self.vertList[key] = newVertex
        return newVertex
    
    def getActorMovie(self,actor):
        return self.getVertex(actor).movies
    
    def getCoMovie(self,actor1,actor2):
        return self.getVertex(actor1).connectedTo[self.vertList[actor2]][1]
        
    def getCoActor(self,actor1):
        return [x.id for x in self.vertList[actor1].connectedTo]
    
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
    
    def __contains__(self,n):
        return n in self.vertList
    
    def addEdge(self,f,t,fmovies,tmovies,samemovie):
        if f not in self.vertList:
            nv = self.addVertex(f,fmovies)
        if t not in self.vertList:
            nv = self.addVertex(t,tmovies)
        self.vertList[f].addNeighbour(self.vertList[t],samemovie)
        self.vertList[t].addNeighbour(self.vertList[f],samemovie)
        
    def getVertices(self):
        return self.vertList.keys()
    
    def __iter__(self):
        return iter(self.vertList.values())
    
    def getActorColor(self,actor):
        return self.getVertex(actor).color
    
    def setActorColor(self,actor,color0):
        # print(self.getVertex(actor) == None)
        # print(actor)
        self.getVertex(actor).color = color0
        
    def bfs(self,actor,ccList0,oriColor,changeColor):
        q = Queue(actor)
        while not q.isEmpty():
            actor0 = q.dequeue()
            for coActor in self.getCoActor(actor0):
                if self.getActorColor(coActor) == oriColor:
                    self.setActorColor(coActor,changeColor) #探查过就标黑色
                    ccList0[0].append(coActor)
                    q.enqueue(coActor)
        ccList0[1] = len(ccList0[0])
        return ccList0
    
    def ccCount(self,actor_list): #actor_list是一个全部演员的名单，共100177
        count = 0 #算连通分支
        totalrun = 0 #确保有跑到100177次
        oriColor = "white"
        changeColor = "black"
        for actor in actor_list:      
            ccList0 = [[],[]] #用小表记录这个联通分支里的演员 0收演员，1收演员数量
            totalrun+=1
            if self.getActorColor(actor) == oriColor:
                ccList0[0].append(actor)
                self.setActorColor(actor,changeColor)
                ccList0 = (self.bfs(actor,ccList0,oriColor,changeColor)) #小表输入大表
                self.ccList.append(ccList0)
                count+=1
        return count

    def ccDemand(self):
        sortList = sorted(self.ccList,key=lambda x: x[1],reverse=True)
        for x in range(20):
            self.demandList.append(sortList[x])
        for x in range(20,0,-1):
            self.demandList.append(sortList[-x])


                
            


def top3MovieStar(g,i): #用来算前20和后20，i是0-39
    movieset = set() #记录这个分支有什么电影
    totalStar = 0
    for actor in g.demandList[i][0]:
        for x in g.getVertex(actor).movies:
            movieset.add(x)
    ansType = calType(g, movieset) #
    for movie0 in movieset:
        totalStar += movie[movie0].star
    averageStar = totalStar/len(movieset)
    return ansType,averageStar

def calType(g,movieset): #计算电影类别排行
    typedict = {} #记录这些电影的类别加总
    for movie0 in movieset:
        for type0 in movie[movie0].types:
            if type0 not in typedict:
                typedict[type0] = 1
            else:
                ans = typedict[type0]+1
                typedict[type0]=ans
    sort_orders = sorted(typedict.items(), key=lambda x: x[1], reverse=True)
    ansType = []
    for i in range(len(typedict)):
        ansType.append(sort_orders[i][0])
    return ansType[:3]

def calStar(g,actor):
    totalStar = 0
    for movie0 in g.getActorMovie(actor):
        totalStar += movie[movie0].star
    averageStar = totalStar/len(g.getActorMovie(actor))
    return averageStar

def actorProp(g,actor):
    averageStar = calStar(g,actor)
    numCoActor = len(g.getCoActor(actor))
    print("%s所出演电影平均星级：%.2f"%(actor,averageStar)," ,共同出演者数量：%s"%numCoActor)
    for coActor in g.getCoActor(actor):
        averageStar = calStar(g,coActor)
        ansType = calType(g, g.getActorMovie(coActor))
        print(coActor,",","出演电影数:",len(g.getActorMovie(coActor)),", 出演的电影平均星级：","%.2f"%averageStar,", 出演电影前3类别：", ansType)
    return numCoActor,averageStar

###这边开始画图
def ccSizePlt(g):  # 通分支规模，ccSize,用demandList
    fig=plt.figure(figsize=(14,6))
    ccSizeList = []
    x1 = np.arange(39) #只画39个，第一个太大会压缩其他
    for i in range(1,40):
        ccSizeList.append(len(g.demandList[i][0]))
    for a,b in zip(x1,ccSizeList):
        plt.text(a, b+0.25, b, ha='center', va= 'bottom',fontsize=12)

    plt.bar(x1,ccSizeList)
    plt.title("连通分支规模",fontsize=20)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xlabel("连通分支",fontsize=16)
    plt.ylabel("连通分支演员数量",fontsize=16)

def ccStarPlt(ansStarList): #平均星级
    fig=plt.figure(figsize=(16,6))
    x2 = np.arange(40)
    for a,b in zip(x2,ansStarList):
        plt.text(a, b+0.1, "%.2f"%b, ha='center', va= 'bottom',fontsize=8)

    plt.bar(x2,ansStarList,width=0.7)
    plt.title("连通分支电影平均星级",fontsize=20)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xlabel("连通分支",fontsize=16)
    plt.ylabel("电影平均星级",fontsize=16)
##画图代码完结

###运行主体
f = open("Film.json",encoding="utf8")
filmDict = json.load(f)
actorDict = {}
movie = {}
n=0
for film in filmDict:
        movie[film["_id"]["$oid"]] = Movie(film['_id']["$oid"],film['title'],film['year'],film['type'],film['star'],film['director'],film['actor'],film['pp'],film['time'],film['film_page'])
        actor_list0 = film["actor"].split(",")
        actor_list = [x.strip() for x in actor_list0]
        for actor0 in actor_list:
            if actor0 not in actorDict:
                actorDict[actor0] = [movie[film["_id"]["$oid"]].id]
            else:
                zz = actorDict[actor0]
                zz.append(movie[film["_id"]["$oid"]].id)
                actorDict[actor0] = zz
        n+=1



g = Graph()
for film in movie:
    filmTitle = film
    
for actor1 in actorDict:
    if g.getVertex(actor1) == None:
        g.addVertex(actor1,actorDict[actor1])
    for filmTitle in actorDict[actor1]:
        for i in range(len(movie[filmTitle].actor)):
            actor2 = str(movie[filmTitle].actor[i])
            if actor1 != actor2:   
                g.addEdge(actor1,actor2,actorDict[actor1],actorDict[actor2],filmTitle)
f.close()
g.ccCount(actorDict)
g.ccDemand()
###运行主体###

##答案输出###
print("所有演员分为几个连通分支： %s"%len(g.ccList))
ansStarList = []
for i in range(40):
    num = g.demandList[i][1]
    ansType,ansStar = top3MovieStar(g, i)
    ansStarList.append(ansStar)
    print("该分支演员数量：",num,", 前三类别： %s"%ansType,",电影平均星级： %.2f"%ansStar)
    
actorProp(g, "周星驰")
ccSizePlt(g)
ccStarPlt(ansStarList)
##答案输出完毕###