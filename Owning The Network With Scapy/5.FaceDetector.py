import cv2
import os

ROOT = '/home/kali/Pictures'
FACES = '/home/kali/Pictures/faces'
TRAIN = '/home/kali/Pictures/training'

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        # Preassuming the images are JPG here.
        if not fname.upper().endswith('.JPG'):
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)
        # Read the image by using OpenCV "Computer Vision" Library cv2.
        img = cv2.imread(fullname)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Load the .XML library and create cv2 face detector object. This detector is trained in advance.
        training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml')
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            # For images in which faces are found:
            if rects.any():
                print('Got a face!')
                # The classifier will return coordinates of a rectangle that corresponds to the detected face.
                # Slice is used here to convert 1 form to another. Converting the returned rects data to coordinates.
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}')
            continue

        # Highlights the faces in the image
        for x1, y1, x2, y2 in rects:
            # For the detected faces, draw a green box around them
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
        # Write the image to the directory mentioned previously.
        cv2.imwrite(newname, img)

if __name__ == '__main__':
    detect()
