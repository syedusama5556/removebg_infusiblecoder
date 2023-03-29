import requests
file_data = open("test.png", "rb")
mask_type = "rgba"  # rgba,green,blur,map
r = requests.post("https://www.taskswithcode.com/salient_object_detection_api/",
                  data={"mask": mask_type}, files={"test": file_data})
results = {"response": r.content, "size": len(r.content)}

with open('output_file.png', "wb") as output_file:
    output_file.write(r.content)
