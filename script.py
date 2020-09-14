import patoolib
import os
patoolib.extract_archive("models/en/pretrain/ewt.rar", outdir="models/en/pretrain/")
if os.path.exists("models/en/pretrain/ewt.rar"):
  os.remove("models/en/pretrain/ewt.rar")
else:
  print("The file does not exist")