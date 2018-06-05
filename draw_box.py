import matplotlib.pyplot as plt
import tensorflow as tf
import csv

image_raw_path = './picture/train/007de3d8-98da-416b-9acc-13b23d4e4f74.jpg'
image_name= '007de3d8-98da-416b-9acc-13b23d4e4f74.jpg'

image_raw_path = './picture/train/0a5c250c-ce88-4258-80d6-51e8a721f9a2.jpg'
image_name= '0a5c250c-ce88-4258-80d6-51e8a721f9a2.jpg'
# image_raw_data = tf.gfile.FastGFile(image_raw_path).read()

csvFile = open('./train_1w.csv','r')
reader = csv.reader(csvFile)

result = {}

for item in reader:
    if reader.line_num == 1:
        continue
    result[item[0]] = item[1] 

    # if reader.line_num ==3:
        # break

raw_box = result[image_name]
box_list = raw_box.split(';')
boxes = []
for box in box_list:
    box_coordinate = box.split('_')
    y_min = int(box_coordinate[1])/500
    x_min = int(box_coordinate[0])/1069
    y_max = (int(box_coordinate[1])+int(box_coordinate[3]))/500
    x_max = (int(box_coordinate[0])+int(box_coordinate[2]))/1069
    boxes.append([y_min,x_min,y_max,x_max])

image_raw_data_jpg = tf.gfile.FastGFile(image_raw_path, 'rb').read()  
  
with tf.Session() as sess:  
    img_data_jpg = tf.image.decode_jpeg(image_raw_data_jpg)  
    img_data_jpg = tf.expand_dims(tf.image.convert_image_dtype(img_data_jpg, dtype=tf.float32), 0)  
    # boxes = tf.constant([[[0.05, 0.5, 0.9, 0.7]]])  
    boxes = tf.constant([boxes])  
    result = tf.image.draw_bounding_boxes(img_data_jpg, boxes)  
    # print sess.run(img_data_jpg).shape  
  
    plt.figure(1)  
    plt.imshow(result.eval().reshape([500,1069,  3]))  
    plt.show()  
