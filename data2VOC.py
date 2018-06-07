from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os
import csv


src_file = './VOC_trans/train_1w.csv'
dst_dir = './VOC_trans/Annotations/'


def make_xml(boxes, image_name):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name+'.jpg'
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = '1069'
    node_height = SubElement(node_size, 'height')
    node_height.text = '500'
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    for box in boxes:
        if len(box) == 4:
            node_object = SubElement(node_root,'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = 'car'
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'
            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = box[0]
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = box[1]
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(int(float(box[0]))+int(float(box[2])))
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(int(float(box[1]))+int(float(box[3])))


    xml = tostring(node_root )#pretty_print = True)
    dom = parseString(xml)
    #print xml 打印查看结果
    return dom

if __name__ == '__main__':
    
    with open(src_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for item in reader:
            if reader.line_num == 1:
                continue
            image_name = item[0]
            image_name = image_name.split('.')[0]
            raw_boxes = item[1]
            boxes = raw_boxes.split(';')
            for i in range(len(boxes)):
                boxes[i] = boxes[i].split('_') 
            print(image_name, boxes)
            dom = make_xml(boxes, image_name)
            xml_name = os.path.join(dst_dir,image_name+'.xml')
            with open(xml_name, 'wb+') as xml_file:
                xml_file.write(dom.toprettyxml(indent='\t', newl='\n', encoding = 'utf-8'))

