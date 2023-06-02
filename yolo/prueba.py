from detect_and_crop import DetectCrop

dtt = DetectCrop('yolo/best.pt', 'imagenes/imagen_17.jpg', 'imagen')
dtt.detect()