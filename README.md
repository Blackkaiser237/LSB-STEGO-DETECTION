*Author:* DONGHO NONGNI GUIROLE FRANCIS  
*Purpose:* B.Eng Final Year Project, University of Buea | MEXT 2027 Research Proposal

## Project Overview
Python implementation of LSB image steganography to embed/extract arbitrary data in an image. Developed to prove that hidden payload size creates measurable changes in network transmission characteristics.

## Key Finding
*1KB hidden payload = 1KB increase in image file size.* This linear relationship creates detectable anomalies in network flow statistics: packet size distribution, flow duration, and inter-arrival times.

## Tools Used
- *Python 3* + *OpenCV* for image manipulation
- *Numpy* for array manipulation
- *Wireshark* for academic validation of network-level changes

## Research Application
This tool provides the threat model for my MEXT 2027 proposal: "Network Traffic-Based Detection of Steganographic Image Transmission in IoT Environments." The goal is to detect covert channels using only network metadata, without payload inspection.

## Usage
```bash
# Encode: Hide data.txt in image.png
python stego_encode.py image.png data.txt output.png

# Decode: Extract hidden data
python stego_decode.py output.png recovered.txt
## MEXT 2027 Research
Full research plan available upon request. This work aligns with privacy-preserving network security data analytics frameworks.

## Contact
Douala, Cameroon | [donghonongni@gmail.com]
