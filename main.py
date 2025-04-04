import os
from openai import OpenAI
import requests
import base64
import re
from pathlib import Path

# Get current working directory (root of the project)
base_dir = Path(__file__).resolve().parent.parent  # or use Path.cwd() if running from root

# Navigate to your folder
directory_name = base_dir / 'image_summarization' / 'image' / 'consumer' / 'Consumer-Report-Thailand-2024_pages-to-jpg-'

api_key = os.getenv("API_KEY")
#directory_name = r'C:\Users\suthichai_p\OneDrive - Real Smart Co.,Ltd\Documents\python\image_summarization\image\consumer\Consumer-Report-Thailand-2024_pages-to-jpg-'
#directory_name = r'\image\consumer\Consumer-Report-Thailand-2024_pages-to-jpg-'
pagelist = [f'{i:04}' for i in range(19, 41)]
prompt = "rewrite this slide into markdown format. for each chart, try to interpret the data into table format with table header. This data is from a consumer report of Thailand 2024, Please do not add any additional information or summarize the content in your own words. Just rewrite the content as it is presented in the slide."
#prompt = "rewrite this slide into markdown format. It's a social listening report of brand TCP, comparing their performance against their competitor Osotspa, Sappe Beauti, Nestle, Coca Cola Thailand, Thaibev, คาราบาว and Ichitan
#prompt = "เขียนสไลด์หน้านี้ใหม่ในรูปแบบ markdown format   เขียนตามที่หน้าสไลด์เขียนโดยไม่เพิ่มข้อความ หรือย่อสรุปด้วยตัวเอง"
#directory_name = r'C:\Users\suthichai_p\Documents\python\image_summarization\image\WeareSocial\Wearesocial2025-Thailand_pages-to-jpg-'
#pagelist = ['0007', '0008', '0019', '0020']
filetype = '.jpg'

result_file_name = 'result_consumer_report'



# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def markdown(dir_or_page, pattern = False):
    client = OpenAI()
    
    if pattern:
        # Path to your image
        image_path = rf'{directory_name}{dir_or_page}{filetype}'

        # Getting the Base64 string
        base64_image = encode_image(rf'{image_path}')
    
    else:
        # Path to your image
        image_path = rf'{dir_or_page}'

        # Getting the Base64 string
        base64_image = encode_image(rf'{image_path}')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"},
                    },
                ],
            }
        ],
    )

    result = response.choices[0].message.content

    # Write the result to result.txt
    with open(f"{result_file_name}.txt", "a", encoding="utf-8") as file:
        file.write(f'Page:{dir_or_page}\nResult:{result}\n\n')
    print(f'Page:{dir_or_page}\nResult:{result}\n\n')
    

for page in pagelist:
    markdown(page, pattern=True)





