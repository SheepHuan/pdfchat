```bash


pip install nougat-ocr


nougat D:/Downloads/3579990.3580015.pdf -o tmp/1


curl -X 'POST' \
  "http://172.16.101.75:8503/predict/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/home/yanghuan/pdfs/3579990.3580015.pdf;type=application/pdf"
```
