import pandas as pd
import random
data = []
for i in range(1, 401):
    area_id = i
    area_name = f"Area{area_id}"
    security_level = random.randint(1, 5)
    data.append([area_id, area_name, security_level])

df = pd.DataFrame(data, columns=["AreaID","AreaName","SecurityLevelRequired"])

df.to_csv("data.csv", index=False, encoding="utf-8-sig")