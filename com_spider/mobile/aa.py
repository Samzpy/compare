import datetime,re
tar='iPhone SE（第 2 代）64GB'
ttt=re.findall(r'(（.*?）)',tar)
print(ttt)
