import os.path
from paddleocr import PaddleOCR

from pid_project_extract.services.utils import OcrItem

default_ignore_list = ['H', '张', 'OTHER', 'DES', 'DWG', 'SHEET', "NO.", 'REV', 'Eng',
                       '未经SEI书面许可', 'ISSUE DATE', 'DISC', 'DRAWN', 'APPR',
                       'SCALE', 'OF']


class PIDProjectOCR(PaddleOCR):
    def __init__(self, ignore_list=None, **kwargs):
        if ignore_list is None:
            ignore_list = default_ignore_list
        self.ignore_list = ignore_list
        super().__init__(**kwargs)

    def detect(self, pid_dir, cls=True, det=True, rec=True):
        if not os.path.exists(pid_dir):
            print("PID directory does not exist.")
            return None

        se_position = None
        incorporation_position = None
        projects_info = {}
        for root, dirs, files in os.walk(pid_dir):
            for file in files:
                if file.endswith('.jpg'):
                    img_path = os.path.join(pid_dir, file)
                    # 判断文件是否存在
                    if not os.path.exists(img_path):
                        continue

                    print('Performing ocr on file: ', img_path)

                    result = self.ocr(img_path, cls=cls, det=det, rec=rec)
                    item_list = []
                    for idx in range(len(result)):
                        result = result[idx]
                        for item in result:
                            val = item[1][0]
                            if 'SE' in val and se_position is None:
                                se_position = item[0]
                            if 'INCORPORATION' in val and incorporation_position is None:
                                incorporation_position = item[0]

                            if any(word in val for word in self.ignore_list):
                                continue

                            item_list.append(OcrItem(item[0], item[1][0]))

                    if not item_list:
                        print("ocr result is empty")
                        continue

                    # 按照 position 进行排序
                    item_list.sort(key=lambda x: x.position)

                    proofreader_info_list = []
                    project_info_list = []
                    for obj in item_list:
                        if (se_position is None) or (incorporation_position is None):
                            print("anchor item（SEI、 incorporation Position）not exists")
                            break

                        left = obj.position[0]
                        obj_top_left_x = left[0]
                        obj_top_left_y = left[1]
                        se_top_left_x = se_position[0][0]
                        se_top_left_y = se_position[0][1]
                        incorp_right_bottom_y = incorporation_position[0][1]

                        if (obj_top_left_y < se_top_left_y - 5) or (
                            obj_top_left_x < (se_top_left_x - 150)):
                            proofreader_info_list.append(obj)
                        elif obj_top_left_y > incorp_right_bottom_y:
                            # Y轴大于 incorporation_position.y
                            project_info_list.append(obj)

                    filename = os.path.basename(file)
                    projects_info[os.path.splitext(filename)[0]] = (
                        project_info_list, proofreader_info_list)

        return projects_info
