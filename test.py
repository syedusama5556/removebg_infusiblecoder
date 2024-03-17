import requests

try:
    # Open the file in binary mode
    with open("test.png", "rb") as file_data:
        mask_type = "rgba"  # rgba,green,blur,map
        
        r = requests.post("https://www.taskswithcode.com/salient_object_detection_api/",
                          data={"mask": mask_type}, files={"test": file_data})
        
        r.raise_for_status()
        
        with open('output_file.png', "wb") as output_file:
            output_file.write(r.content)
        
        results = {"response": r.content, "size": len(r.content)}
        print("API request successful!")
        
except requests.exceptions.RequestException as e:
    # Handle request exceptions
    print("Error making the request:", e)

except IOError as e:
    # Handle file-related errors
    print("Error reading or writing files:", e)

except Exception as e:
    # Handle other unexpected errors
    print("An unexpected error occurred:", e)
