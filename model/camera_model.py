import numpy as np
from pathlib import Path

class CameraModel():
    def __init__(self, image_size, is_fisheye) -> None:
        """
        Create camera model from init state.
        """
        self.image_size = image_size
        self.is_fisheye = is_fisheye

        # init params
        self.cm1 = self.cm2 = self.cd1 = self.cd2 = None
        self.R = self.T = None
        
    @classmethod
    def load_model(cls, npz_path) -> None:
        """
        Create camera model from a saved file.
        """
        print(f"Loading camera model at {npz_path}")
        params = np.load(npz_path)

        # dummy camera instance
        camera = CameraModel('IMX477', False)

        # make sure camera info exist, else raise Errors
        try:
            camera.image_size = params['image_size']
            camera.is_fisheye = params['is_fisheye']
        except:
            raise Exception(f"No camera info found at {npz_path}")
        
        # modify dummy camera 
        try:
            camera.cm1 = params['cm1']
            camera.cd1 = params['cd1']
            camera.cm2 = params['cm2']
            camera.cd2 = params['cd2']
            camera.R = params['R']
            camera.T = params['T']
        except: # if encounter None object, then no assignment
            pass

        return camera
    
    def save_model(self, npz_path):
        """
        Save this model to Path.
        """
        print(f"Saving camera model to {npz_path}")
        # mkdir if folder not exist
        npz_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(npz_path,
            image_size = self.image_size,
            is_fisheye = self.is_fisheye,
            cm1 = self.cm1, 
            cd1 = self.cd1, 
            cm2 = self.cm2, 
            cd2 = self.cd2,
            R = self.R, 
            T = self.T, 
        )


    def is_calibrated(self):
        """
        Check if this model is calibrated.
        """
        if  self.cm1 is None or self.cd1 is None or self.cm2 is None or self.cd2 is None or \
            self.R is None or self.T is None:
            return False
        else:
            return True

    def update_intrinsic(self, cm1, cd1, cm2, cd2):
        """
        Update intrinsic parameters
        """
        self.cm1 = cm1
        self.cd1 = cd1
        self.cm2 = cm2
        self.cd2 = cd2

    def update_extrinsic(self, R, T):
        """
        Update extrinsic parameters
        """
        self.R = R
        self.T = T


    def __str__(self) -> str:
        """
        Camera info"""
        str = f"""
image_size = {self.image_size}
is_fisheye = {self.is_fisheye}
cm1: \n {self.cm1}
cd1: \n {self.cd1}
cm2: \n {self.cm2}
cd2: \n {self.cd2}
R: \n {self.R}
T: \n {self.T}"""
        return str
