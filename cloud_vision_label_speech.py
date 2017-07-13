#!python2
# -*- coding: utf-8 -*-

import requests
import json
import base64
import photos
import console
import speech

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
                'type': 'LABEL_DETECTION',
                'maxResults': 10,
            }]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()

def img_to_base64(filepath):
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.b64encode(img_byte)

def get_descs_from_return(res_json):
    labels = res_json['responses'][0]['labelAnnotations']
    descs = []
    for value in labels:
        descs.append(value['description'])
    return json.dumps(descs)

def print_description(res_json):
    labels = res_json['responses'][0]['labelAnnotations']
    for value in labels:
        #print('{0} : {1}'.format('description', value['description']))
        print('{0} : {1}'.format(value['description'],value['score']))

def say_object_name(res_json):
    max_score = 0
    max_description = ''
    for data in res_json:
        score = data['score']
        if(score > max_score):
            max_score = score
            max_description = data['description']
    print(max_description)
    speech.say(max_description,'en-US',0.5)

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

#
# main
#
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
    #print json.dumps(res_json, indent=2, sort_keys=True)
    #print_description(res_json)
    say_object_name(res_json['responses'][0]['labelAnnotations'])
    #json_desc = get_descs_from_return(res_json)
    #print json_desc

if __name__ == '__main__':
    main()
    
