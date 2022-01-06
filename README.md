# BSoD-Detection-Model
Worked on a BSoD Detection Python Script during my internship in Intel Microelectronics (M) Sdn. Bhd.

BSOD Detection using OpenCV
Pytesseract – Optical Character Recognition (OCR) Engine in Python
- Recognise & extract text form images
- Image processing operations for better accuracy

Masking Technique
- Setting lower and upper range of blue colour to be detected
- Convert the image/frame from BGR to HSV
- Perform masking
    - Detected blue colour region within specified range will be in white color (255)
    - Undetected region will be in black color (0)

Percentage of blue
- Calculate percentage of blue colour detected in image/frame using (mask > 0).mean() function.

BSOD Detection in Video Files
- Create a folder to store video frames in it.
- Extract video frames based on the frame rate (in seconds) entered.
- Check through every frame to detect BSOD and update in a text file.
- Print the final output.

GUI of BSOD Detection Model
- Tkinter - Python GUI Package

