# Image watermarker

A basic tool to apply a watermark to image(s)

Features:
- Multiprocessing
- File dialogs

Notes:
- Windows only
- Watermarked files are saved to the same directory as their input files
- Watermark is applied to the top left corner of the image

If you want to change this behaviour, you can build from source with this script:
```ps1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
pyinstaller .\main.pyw -F
rm .\main.spec
rm .\build --recurse --force
mv .\dist\main.exe .\ --force
rm .\dist --force
```