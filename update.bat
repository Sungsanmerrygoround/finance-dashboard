@echo off
call C:\Users\admin\anaconda3\Scripts\activate.bat base
cd /d C:\Users\admin\HJ\finance-dashboard
python main.py
git add .
git commit -m "자동 업데이트: %date%"
git push origin main