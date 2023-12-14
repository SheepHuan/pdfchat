from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.http import HttpResponseRedirect
import os
# Create your views here.
def translation(request):
     return HttpResponse("nougat")





import pypdfium2
import torch
from nougat import NougatModel
from nougat.postprocessing import markdown_compatible, close_envs
from nougat.utils.dataset import ImageDataset
from nougat.utils.checkpoint import get_checkpoint
from nougat.dataset.rasterize import rasterize_paper
from nougat.utils.device import move_to_device, default_batch_size
from tqdm import tqdm
from .forms import PdfForm
# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file
BATCHSIZE = int(os.environ.get("NOUGAT_BATCHSIZE", default_batch_size()))
NOUGAT_CHECKPOINT = get_checkpoint()



def nougat(request):
     if request.method == 'POST':
          form = PdfForm(request.POST)
     else:
          form = PdfForm()
     return render(request, 'form.html', {'form': form})