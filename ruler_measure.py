import sys
import cv2
import numpy as np
from pathlib import Path
from measure.matcher import MATCHER_TYPE

from model.camera_model import CameraModel
from calib.rectification import StereoRectify
from utils.utils import snap_subpix_corner, imshow
from measure.ruler import Ruler


try:
    id = sys.argv[1]
except:
    id = 1


# pick image
operation_folder = '0617_IMX477_5000'
test_folder = Path('datasets') / operation_folder / 'scenes' 
test_folder = Path('datasets') / operation_folder / 'test' 
assert test_folder.is_dir()
img_path = list(test_folder.iterdir())[int(id)-1]
print("Measuring", img_path.name)

# load camera model
cam_path = Path("datasets") / operation_folder / "calibration_data" / "camera_model.npz"
camera = CameraModel.load_model(cam_path)

# rectify image
sbs_img = cv2.imread(str(img_path))
rectifier = StereoRectify(camera, operation_folder)
imgL, imgR = rectifier.rectify_image(sbs_img)


# measure
ruler = Ruler(camera, imgL, imgR)
ruler.click_segment(automatch=True, matcher=MATCHER_TYPE.SIFT)
len = ruler.measure_segment()
print(len)

ruler.show_endpoints()
