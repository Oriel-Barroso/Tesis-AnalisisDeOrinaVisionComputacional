# <<<<<<< HEAD
#Object Crop Using YOLOv7
import argparse
import time
from pathlib import Path
import os
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, \
    scale_coords, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel


class DetectCrop():
    def __init__(self, weights, source, image):
        self.image = image
        self.weights = weights
        self.source = source
        self.img_size = 640
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.device = ''
        self.project = 'rund/detect' 
        self.name = 'exp'
        self.exist_ok = False
        self.view_ig = False
        self.save_txt = False
        self.save_img = True
        self.save_conf = False
        self.nosave = False
        self.classes = None
        self.agnostic_nms=False
        self.augment=False
        self.update=False
        self.no_trace=False


    def binary_order(self, dictionary, place):
        lista_ordenada = dictionary.copy()
        for i in range(1, len(lista_ordenada)):
            actual = lista_ordenada[i]
            j = i
            while j > 0 and \
                    lista_ordenada[j-1][place] > actual[place]:
                lista_ordenada[j] = lista_ordenada[j-1]
                lista_ordenada[j-1] = actual
                j = j-1
        return lista_ordenada


    def detect(self):
        #self.main()
        print(self.weights, 'PESOSSSSS')
        print(self.source, 'PAAAAAAATH')
        print(self.image, 'IMAGEEEEEEEEEN')
        imgsz, trace = self.img_size, not self.no_trace
        save_txt = False
        

        # Directories
        save_dir = Path(increment_path(Path(self.project) / self.name, exist_ok=self.exist_ok))  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        set_logging()
        device = select_device(self.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(self.weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check img_size

        if trace:
            model = TracedModel(model, device, self.img_size)

        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

        # Set Dataloader
        vid_path, vid_writer = None, None
        dataset = LoadImages(self.source, img_size=imgsz, stride=stride)

        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    model(img, augment=self.augment)[0]

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=self.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=self.agnostic_nms)
            t3 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)
                if not os.path.exists(self.image+p.name[:p.name.index('.')]):
                    os.makedirs(self.image+p.name[:p.name.index('.')])
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    # Write results
                    object_coordinates = {}
                    val_listas = 0
                    for *xyxy, cls in reversed(det):
                        object_coordinates[val_listas] = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                        val_listas += 1
                    if old_img_h > old_img_w:
                        object_coordinates_ord = self.binary_order(object_coordinates, 3)
                    elif old_img_w > old_img_h:
                        object_coordinates_ord = self.binary_order(object_coordinates, 0)
                    else:
                        object_coordinates_ord = self.binary_order(object_coordinates, 3)
                    print(object_coordinates_ord)
                    for nro_imagen, coordenadas in object_coordinates_ord.items():
                        cropobj = im0[int(coordenadas[1]):int(coordenadas[3]),int(coordenadas[0]):int(coordenadas[2])]
                        crop_file_path = os.path.join(self.image+p.name[:p.name.index('.')],str(nro_imagen)+".jpg")
                        cv2.imwrite(crop_file_path, cropobj)

                # Print time (inference + NMS)
                print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

                # Save results (image with detections)
                if self.save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                        print(f" The image with the result is saved in: {save_path}")
                    

        if self.save_txt or self.save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            #print(f"Results saved to {save_dir}{s}")

        print(f'Done. ({time.time() - t0:.3f}s)')


# def main(self):
#     #check_requirements(exclude=('pycocotools', 'thop'))
#     #self.weights = "/mnt/c/Users/Admin/Documents/testIA/yolov7/runs/train/yolov7-custom/weights/best.pt"
#     #self.source = "/mnt/c/Users/Admin/Documents/imgEnt"
#     with torch.no_grad():
#         if self.update:  # update all models (to fix SourceChangeWarning)
#             for self.weights in ['yolov7.pt']:
#                 self.detect()
#                 strip_selfimizer(self.weights)
#         else:
#             self.detect()
# =======
# version https://git-lfs.github.com/spec/v1
# oid sha256:651f8fd1cdd2825da243a99d086bad3e3feb227706ff1eeb07fd9fb24950f756
# size 8932
# >>>>>>> 3c668efe401375465cf1a25007dde438f7e23e7f
