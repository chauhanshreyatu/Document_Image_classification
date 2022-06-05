import os
from PIL import Image
import numpy as np 
import shutil
import csv
'''
# ---------------- Creating Separate Directories for different folders -----------------------
classes = {'0': 'letter', '1': ' form', '2': 'email', '3' : 'handwritten', '4': 'advertisement', '5':
'scientific report', '6': 'scientific publication ', '7': 'specification', '8' : 'file folder ', '9':
'news article', '10' : 'budget', '11' : 'invoice',
'12' :'presentation', '13': 'questionnaire', '14':'resume', '15':
'memo'}
def make_doc_dirs( path) :
    for label in classes. values ( ):
        if not os.path.exists( path + str(label) ) :
            os.mkdir( path + str(label ) )
make_doc_dirs ('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/testing/')
make_doc_dirs('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/training/')
make_doc_dirs('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/validation/')


# ---------------------------------- Separating Images --------------------------------
root_path = '/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/images/images'
def sort_Images(labels, root_path, final_directory, scenario):
    csv_file_path = final_directory+'/'+scenario+'.csv'
    labels = labels.read()
    labels_split = labels.split('images')
    full_paths = []
    for image_label_path in labels_split:
        label = root_path + image_label_path
        full_paths.append(label)
        

    full_paths = full_paths[1:]
    csv_data = []
    for path in full_paths:
        info = path.split(' ')
        label = info[1].strip('\n')
        src_dir = info[0]
        original_image_label = classes[label]
        dst_dir = '/'.join([final_directory,original_image_label,src_dir.split('/')[-1]])
        csv_data.append([dst_dir, int(label)])
        root_folder = '/'.join(src_dir.split('/')[:-1])
        os.chdir(root_folder)
        if not os.path.exists(dst_dir) :
            for f in os.listdir():
                shutil.copy(f, dst_dir)
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        fieldnames = ['file_address', 'label']
        for data in csv_data:
            writer.writerow(data)
            
            

train_labels = open('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/labels/train.txt','r' )
test_labels = open('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/labels/test.txt','r' )
val_labels = open('/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/labels/val.txt','r' )
train_final_directory = '/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/training'
test_final_directory = '/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/testing'
val_final_directory = '/Users/shreyachauhan/PycharmProjects/mmselfsup/data/rvl-cdip/DocImages/validation'
sort_Images(train_labels, root_path, train_final_directory, 'train')
sort_Images(test_labels, root_path, test_final_directory, 'test')
sort_Images(val_labels, root_path, val_final_directory, 'val')
    
'''
#----------------------EDA-----------------------
'''_, _, files = next(os.walk("data/rvl-cdip/DocImages/testing"))
file_count = len(files)
print(files)'''

file = open("data/rvl-cdip/DocImages/training/train.csv")
reader = csv.reader(file)
lines= len(list(reader))
print(lines)