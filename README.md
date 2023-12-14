## 项目介绍

1. 依赖 meta-ai 的[nougat](https://github.com/facebookresearch/nougat)模型将 pdf 处理成 mmd 格式。
2. 通过[api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm)等模型将 mmd 翻译成中文。

## 使用指南

### 安装

```bash
export https_proxy="http://172.16.101.75:7890"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

```bash
curl -X 'POST' \
  "http://172.16.101.75:8503/predict/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/home/yanghuan/pdfs/3579990.3580015.pdf;type=application/pdf"
```

### 创建 llm-api

```bash
git clone https://github.com/xusenlinzy/api-for-open-llm.git
cd api-for-open-llm/

docker run -it -d --gpus all --ipc=host -p 7891:8000 --name=llm-api \
    --ulimit memlock=-1 --ulimit stack=67108864 \
    -v `pwd`:/workspace \
    llm-api:pytorch \
    python api/server.py
```

## Django

```bash

django-admin startproject pdfchat .

python3 manage.py startapp ocr

python3 manage.py startapp chatllm

python manage.py migrate
python manage.py makemigrations
```
