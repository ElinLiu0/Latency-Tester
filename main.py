import subprocess as sb
import plotly.graph_objects as go
from tqdm import tqdm
import sys
import os
from datetime import datetime
testLoops = int(sys.argv[1])
latency = []
packetLoss = []
shake = []
with tqdm(total=testLoops,unit="发送包") as pbar:
    for i in range(0, testLoops):
        output = sb.check_output(['ping','-n','1','baidu.com'])
        currentLoop = [float(output.split(b'ms')[0].split(b'=')[-1])][0]
        packageLoss = [float(output.split(b'%')[0].split(b'(')[-1])][0]
        min = float(output.decode('gbk').split('最短')[-1].split('，')[0].split('=')[-1].replace(' ','').replace('ms',''))
        max = float(output.decode('gbk').split('最长')[-1].split('，')[0].split('=')[-1].replace(' ','').replace('ms',''))
        latency.append(currentLoop)
        packetLoss.append(packageLoss)
        shake.append(max-min)
        pbar.set_description("测试中")
        pbar.set_postfix({"时延": str(currentLoop)+"ms", "丢包率": str(packageLoss)+"%", "抖动": str(max-min)+"ms"})
        pbar.update(1)
# Draw the figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(0, 100)), y=latency, mode='lines', name='时延'))
fig.add_trace(go.Scatter(x=list(range(0, 100)), y=packetLoss, mode='lines', name='丢包率'))
fig.add_trace(go.Scatter(x=list(range(0, 100)), y=shake, mode='lines', name='抖动'))
# Set the title
fig.update_layout(title='网络测试结果', xaxis_title='发送包', yaxis_title='时延/丢包率/抖动')
# 创建当前时间的时间戳
now = datetime.now()
timestamp = datetime.timestamp(now)
fig.show()
print("测试完成!")