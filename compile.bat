@REM 使用pyinstaller打包main.py，导入依赖库plotly和tqdm
pyinstaller -F --hidden-import plotly --hidden-import tqdm main.py