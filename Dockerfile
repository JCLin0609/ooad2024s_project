# 使用官方的Python 3.10.12鏡像作為基礎鏡像
FROM python:3.10.12

# 設定工作目錄，所有後續操作均以此目錄作為當前目錄
# 如果目錄不存在，Docker將自動創建該目錄
WORKDIR /app

# 複製Pipfile和Pipfile.lock到工作目錄中
# 假定已經生成了Pipfile.lock來鎖定依賴版本
# 如果沒有Pipfile.lock，則需要先生成，或者在安裝依賴時去除--ignore-pipfile選項
COPY Pipfile /app/

# 安裝依賴，使用pipenv管理
# 首先安裝pipenv，然後按照Pipfile.lock安裝準確版本的依賴
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install

# 複製應用程式源代碼到工作目錄中
COPY . /app

# 配置環境變量
# 是否需要依據應用程式需要設置其他環境變量，可以根據實際情況添加
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=development

# 暴露應用程式運行時所使用的端口
EXPOSE 5000

# 定義容器啟動時執行的命令
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
