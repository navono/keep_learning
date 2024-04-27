import os
import datetime
from pdf2image import convert_from_path
from PIL import Image
from fastapi import APIRouter

from pid_project_extract.services.ocr import PIDProjectOCR
from pid_project_extract.services.project_xml import PIDProjectXml
from pid_project_extract.settings import settings

router = APIRouter()

det_model_dir = "./inference/ch_ppocr_server_v2.6_det_infer/"
rec_model_dir = "./inference/ch_ppocr_server_v2.6_rec_infer/"
cls_model_dir = "./inference/ch_ppocr_mobile_v2.6_cls_infer/"


def get_project_info_from_ocr(pid_dir, ignore_list):
    ocr_engine = PIDProjectOCR(ignore_list, use_angle_cls=True, use_gpu=True, lang='ch',
                               det_model_dir=det_model_dir, rec_model_dir=rec_model_dir,
                               cls_model_dir=cls_model_dir)

    return ocr_engine.detect(pid_dir)


@router.post('/img')
def img_process() -> str:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """

    current_dir = os.getcwd()
    pid_dir = os.path.join(current_dir, settings.pid_dir)
    count = 0

    try:
        for root, dirs, files in os.walk(pid_dir):
            for file in files:
                if file.endswith('.pdf'):
                    # file_path = os.path.join(pid_dir, file)
                    file_path = os.path.join(settings.pid_dir, file)
                    file_name = os.path.splitext(file_path)[0] + '.jpg'
                    images = convert_from_path(file_path)
                    images[0].save(file_name, 'JPEG')
                    # 从底部裁剪上述的图片
                    im = Image.open(file_name)
                    w, h = im.size

                    preserved_height = w - (w * 0.35) + 100
                    preserved_width = h - 750

                    # 从底部裁剪
                    im = im.crop((int(preserved_height), preserved_width, w, h))
                    im.save(file_name, 'JPEG')
                    print("save image file: ", file_name)
                    count += 1
    except Exception as e:
        print(e)
        return "error: " + str(e)
    return "result: " + str(count) + " files processed."


@router.post('/extract')
def detect() -> str:
    """
    使用 paddleocr 对图片进行文字识别

    Paddleocr supports Chinese, English, French, German, Korean and Japanese.
    You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
    to switch the language model in order.

    坐标为左上角起，顺时针方向
    """

    current_dir = os.getcwd()
    pid_dir = os.path.join(current_dir, settings.pid_dir)

    ignore_list = ['H', '张', 'OTHER', 'DES', 'DWG', 'SHEET', "NO.", 'REV', 'Eng',
                   '未经SEI书面许可', 'ISSUE DATE', 'DISC', 'DRAWN', 'APPR', 'SCALE',
                   'OF']
    try:
        projects_info = get_project_info_from_ocr(pid_dir, ignore_list)

        project_xml = PIDProjectXml()
        project_xml.construct(projects_info)

        # 保存工作簿为Excel文件
        # 获取当前日期和时间
        current_datetime = datetime.datetime.now()
        # 格式化日期时间，使用下划线作为分隔符
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
        project_xml.save(f"./test_data/项目信息_{formatted_datetime}.xlsx")

        return "files processed."
    except Exception as e:
        print(e)
        return "error: " + str(e)
