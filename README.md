



## 项目介绍

1. 依赖meta-ai的[nougat](https://github.com/facebookresearch/nougat)模型将pdf处理成mmd格式。
2. 通过[api-for-open-llm](https://github.com/xusenlinzy/api-for-open-llm)等模型将mmd翻译成中文。

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

### 创建llm-api

```bash
git clone https://github.com/xusenlinzy/api-for-open-llm.git
cd api-for-open-llm/


```

## TODO

1. 实现并发
