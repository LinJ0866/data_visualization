import os
import chardet
import json
import cv2

class visual(object):
    def __init__(self, img_dir, anno_dir, output_dir, type):
        self.img_dir= img_dir
        self.anno_dir = anno_dir
        self.output_dir = output_dir
        self.type = type
        assert os.path.exists(img_dir), "The image folder does not exist!"
        assert os.path.exists(anno_dir), "The anno folder does not exist!"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def is_pic(self, filename):
        return filename.split('.')[-1] in ['JPEG', 'jpeg', 'JPG', 'jpg', 'BMP', 'bmp', 'PNG', 'png']

    def get_encoding(self, path):
        f = open(path, 'rb')
        data = f.read()
        file_encoding = chardet.detect(data).get('encoding')
        f.close()
        return file_encoding


    # 绘图，targets为rectangle列表，每个元素为[class, (左上角x, 左上角y), (右下角x, 右下角y)]
    def draw_rectangle(self, img, targets):
        for target in targets:
            cv2.rectangle(img, target[1], target[2], (0, 0, 255), 3)
            cv2.putText(img, target[0], (10, 500), cv2.FONT_HERSHEY_SIMPLEX,
                4, (255, 255, 255), 2, lineType=cv2.LINE_AA)
        return img

class planthopperVisual(visual):
    def __init__(self, img_dir, output_dir):
        self.img_dir = img_dir
        self.output_dir = output_dir
        assert os.path.exists(img_dir), "The image folder does not exist!"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def parse_json(self, annoPath):
        targets = []
        with open(annoPath, mode='r', \
                      encoding=self.get_encoding(annoPath)) as f:
            json_info = json.load(f)
            for region in json_info['regions']:
                regionOrigin = region['region']
                targets.append([str(region['cls']), (regionOrigin[0], regionOrigin[1]), (regionOrigin[2], regionOrigin[3])])
        return targets
    
    def run(self):
        for dic in os.listdir(self.img_dir):
            dic_detail = os.path.join(self.img_dir, dic)
            for file in os.listdir(dic_detail):
                if self.is_pic(file):
                    print(file)
                    filePath = os.path.join(dic_detail, file)
                    annoPath = os.path.join(dic_detail, file.replace(file.split('.')[-1], 'txt'))
                    savePath = os.path.join(self.output_dir, file)

                    img = cv2.imread(filePath)
                    targets = self.parse_json(annoPath)
                    img = self.draw_rectangle(img, targets)

                    cv2.imwrite(savePath, img)

planthopperVisual('planthopper', 'visual_planthopper').run()