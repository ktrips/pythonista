#!python2
# -*- coding: utf-8 -*-

import requests
import json
import base64
import photos
import console
from PIL import Image, ImageDraw

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = 'YOUR-GOOGLE-CLOUD-VISION-API-KEY'
def goog_cloud_vison (image_content):
    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': [{
                'type': 'FACE_DETECTION',
                'maxResults': 40,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()

def img_to_base64(filepath):
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.b64encode(img_byte)

def get_emotion_data(json_dict,key):

    #print json.dumps(json_dict, indent=2, sort_keys=False)
    for value in json_dict:
        emotion = value[key]
        data = value['landmarks']
        #print json.dumps(data, indent=2, sort_keys=False)
        for pos in data:
          type = pos['type']
          
          if(type=='MIDPOINT_BETWEEN_EYES'):
              print(key + ' : '+ emotion)
              print(type)
              #print(json.dumps(pos['position'], indent=2, sort_keys=False))
              xyz = pos['position']
              print('{0}:{1}'.format('x', xyz['x']))
              print('{0}:{1}'.format('y', xyz['y']))
              print('{0}:{1}'.format('z', xyz['z']))

def highlight_faces(imagebuffer,faces):
	
    drawbuffer = ImageDraw.Draw(imagebuffer)
    for face in faces:
        box = [(v.get('x', 0.0), v.get('y', 0.0))
               for v in face['fdBoundingPoly']['vertices']]
        drawbuffer.line(box + [box[0]], width=5, fill='#00ff00')

    imagebuffer.show()

def take_photo(filename='.temp.jpg'):
    img = photos.capture_image()
    if img:
        img.save(filename)
        return filename

def pick_photo(filename='.temp.jpg'):
    img = photos.pick_image()
    if img:
        img.save(filename)
        return filename

def main():
    console.clear()
    i = console.alert('Info', '画像の入力方法を選択して下さい。', 'Take Photo', 'Pick from Library')
    if i == 1:
        filename = take_photo()
    else:
        filename = pick_photo()
    if not filename:
        return
    console.show_image(filename)
    img = img_to_base64(filename)
    res_json = goog_cloud_vison(img)
    #print res_json
    imagebuffer = Image.open(filename)
    highlight_faces(imagebuffer,res_json['responses'][0]['faceAnnotations'])
    #get_emotion_data(res_json['responses'][0]['faceAnnotations'],'joyLikelihood')

if __name__ == '__main__':
    main()
