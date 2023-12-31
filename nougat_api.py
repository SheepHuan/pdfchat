import os
from PIL import Image, UnidentifiedImageError
from functools import partial
from django.shortcuts import redirect
import pypdfium2
import torch
import hashlib
from pathlib import Path
from nougat import NougatModel
from nougat.postprocessing import markdown_compatible, close_envs
from nougat.utils.dataset import ImageDataset
from nougat.utils.checkpoint import get_checkpoint
from nougat.dataset.rasterize import rasterize_paper
from nougat.utils.device import move_to_device, default_batch_size
from tqdm import tqdm
import markdown
# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
# BATCHSIZE = int(os.environ.get("NOUGAT_BATCHSIZE", default_batch_size()))
BATCHSIZE = 4
NOUGAT_CHECKPOINT = get_checkpoint()
SAVE_PATH = "tmp/nougat"
os.makedirs(SAVE_PATH,exist_ok=True)



model = None
def load_model(
    checkpoint: str = NOUGAT_CHECKPOINT,
):
     global model, BATCHSIZE
     if model is None:
          model = NougatModel.from_pretrained(checkpoint)
          model = model.to(torch.bfloat16)
          model = model.to("cuda:2")
          if BATCHSIZE <= 0:
               BATCHSIZE = 1
          model.eval()

load_model()

def predict(
    file, start: int = None, stop: int = None
) -> str:
     pdfbin = open(file, "rb").read()
     pdf = pypdfium2.PdfDocument(pdfbin)
     md5 = hashlib.md5(pdfbin).hexdigest()
     save_path = os.path.join(SAVE_PATH,md5)
     os.makedirs(save_path,exist_ok=True)
     save_path = Path(save_path)
     
     if start is not None and stop is not None:
          pages = list(range(start - 1, stop))
     else:
          pages = list(range(len(pdf)))
     predictions = [""] * len(pages)
     dellist = []
     if save_path.exists():
          for computed in (save_path / "pages").glob("*.mmd"):
               try:
                    idx = int(computed.stem) - 1
                    if idx in pages:
                         i = pages.index(idx)
                         print("skip page", idx + 1)
                         predictions[i] = computed.read_text(encoding="utf-8")
                         dellist.append(idx)
               except Exception as e:
                    print(e)
     compute_pages = pages.copy()
     for el in dellist:
          compute_pages.remove(el)
     images = rasterize_paper(pdf, pages=compute_pages)
     global model

     dataset = ImageDataset(
          images,
          partial(model.encoder.prepare_input, random_padding=False),
     )

     dataloader = torch.utils.data.DataLoader(
          dataset,
          batch_size=BATCHSIZE,
          pin_memory=True,
          shuffle=False,
     )

     for idx, sample in tqdm(enumerate(dataloader), total=len(dataloader)):
          if sample is None:
               continue
          model_output = model.inference(image_tensors=sample)
          for j, output in enumerate(model_output["predictions"]):
               if model_output["repeats"][j] is not None:
                    if model_output["repeats"][j] > 0:
                         disclaimer = "\n\n+++ ==WARNING: Truncated because of repetitions==\n%s\n+++\n\n"
                    else:
                         disclaimer = (
                              "\n\n+++ ==ERROR: No output for this page==\n%s\n+++\n\n"
                         )
                    rest = close_envs(model_output["repetitions"][j]).strip()
                    if len(rest) > 0:
                         disclaimer = disclaimer % rest
                    else:
                         disclaimer = ""
               else:
                    disclaimer = ""

               predictions[pages.index(compute_pages[idx * BATCHSIZE + j])] = (
                    markdown_compatible(output) + disclaimer
               )

     (save_path / "pages").mkdir(parents=True, exist_ok=True)
     pdf.save(save_path / "doc.pdf")
     if len(images) > 0:
          thumb = Image.open(images[0])
          thumb.thumbnail((400, 400))
          thumb.save(save_path / "thumb.jpg")
     for idx, page_num in enumerate(pages):
          (save_path / "pages" / ("%02d.mmd" % (page_num + 1))).write_text(
               predictions[idx], encoding="utf-8"
          )
     final = "\n".join(predictions).strip()
     (save_path / "doc.mmd").write_text(final, encoding="utf-8")
     
     html = f"""
               <!DOCTYPE html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css" crossorigin="anonymous"><script src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/mathtex-script-type.min.js" defer></script>

</head>
    <body>
{final}
    </body> 
</html>
               """
     
     (save_path / "doc.html").write_text(html, encoding="utf-8")
     return "\n".join(predictions),md5


if __name__=="__main__":
     pass