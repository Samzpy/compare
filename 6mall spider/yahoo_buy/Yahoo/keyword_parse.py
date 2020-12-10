import re

class Keyword_Parse:
    # def __init__(self,r_list,keyword):
    #     self.r_list=r_list
    #     self.keyword=keyword

    def median(self,lst):
        lst.sort()  # Sort the list first
        if len(lst) % 2 == 0:  # Checking if the length is even
            # Applying formula which is sum of middle two divided by 2
            return (lst[len(lst) // 2] + lst[(len(lst) - 1) // 2]) / 2
        else:
            # If length is odd then get middle value
            return lst[len(lst) // 2]

    def mercy(self,lst):
	    return int(((max(lst) - min(lst)) / 100) * 30)

    def outOfRange(self,lst):
        priceMedian = self.median([i[2] for i in lst])
        leftEdge = priceMedian - self.mercy([i[2] for i in lst])
        rightEdge = priceMedian + self.mercy([i[2] for i in lst])
        # print(leftEdge,rightEdge)
        r2_list = []
        for index in range(len(lst)):
            if leftEdge < lst[index][2] < rightEdge:
                if "售" not in lst[index][1]:
                    r2_list.append(lst[index])
        return r2_list

    def notNatural(self,lst):
        r2_list = []
        for item in lst:
            itemlst = re.split('_|/|\s|【|】',item[1])
            if not [i for i in itemlst if len(i) > 25]:
                r2_list.append(item)
        return r2_list

    def accOut(self,lst):
        r2_list = []
        acc = ['皮套','錄影筆','可議價','香港版','攜碼','月繳','競標','月付','分期','保護貼','門號專案價','鋼化模','充電線','microusb','type-c','type c','lightning','隨身碟','保護套','保護軟套','插卡','磁扣','支架','福利機','福利品','烤網']
        for item in lst:
            if not [i for i in acc if i in item[1]]:
                r2_list.append(item)
        return r2_list

    #lst=總列表   keyword=關鍵字  keywordlist=關鍵字列表  item=for 總列表   
    def nokeyword(self,lst,keyword):
        keywordList = keyword.split()
        
        isGB = keywordList[-1][-2:] == "GB"
        

        if re.findall('\d+',keywordList[-1]) and (not isGB) and ("-" not in keywordList[-1]):
            number = re.findall('\d+',keyword)[0]
            other = keyword.split(number)
            other = sum([i.split() for i in other],[])
            keywordList = [i for i in other if len(i) >2]
            keywordList.append(number)
        r2_list=[]

        for item in lst:
            if len([j for j in keywordList if j.lower() in item[1].lower()]) == len(keywordList):
                if 'iphone' in item[1].lower():
                    a=len([i for i in keywordList if i.lower() in item[1].lower()]) == len(keywordList) \
                    and (('max' in "".join([i.lower() for i in item[1]]) and ('max' in [i.lower() for i in keywordList])))
                    if 'max' in "".join([i.lower() for i in keywordList]):
                        if a:
                            r2_list.append(item)
                    else:
                        b = (len([i for i in keywordList if i.lower() in item[1].lower()]) == len(keywordList)) and ('max' not in "".join([i.lower() for i in item[1]]))
                        if b:
                            r2_list.append(item)
                else:
                    r2_list.append(item)
        
        return r2_list

    def run(self,r_list,keyword):
        newlst=self.accOut(self.notNatural(self.nokeyword(r_list,keyword)))
        if len(newlst) > 4 :
        	newlst = self.outOfRange(newlst)
        if newlst:
            newlst=sorted(newlst,key=lambda x: x[2])[0]
        return newlst
