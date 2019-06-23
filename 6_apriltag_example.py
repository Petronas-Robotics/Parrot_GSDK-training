# PETRONAS Technology Challange 6
# Written by: Tareq ALqutami (tareqazizhasan.al-q@petronas.com),  June 2019
# adapted from: https://github.com/swatbotics/apriltag/tree/master/python
# This code is provided as is and we are not liable for any consequential damages from using it.
# Use this code at your own risk.

# This code shows how to use apriltag pyhton wrapper (https://github.com/swatbotics/apriltag/tree/master/python)
# it uses a camera feed and calibration params (if available)

import apriltag
import cv2
import numpy
import collections

# helper function to draw actual pose of apriltag (from https://github.com/swatbotics/apriltag/tree/master/python)
def draw_pose(overlay, camera_params, tag_size, pose, z_sign=1):

    opoints = numpy.array([
        -1, -1, 0,
         1, -1, 0,
         1,  1, 0,
        -1,  1, 0,
        -1, -1, -2*z_sign,
         1, -1, -2*z_sign,
         1,  1, -2*z_sign,
        -1,  1, -2*z_sign,
    ]).reshape(-1, 1, 3) * 0.5*tag_size

    edges = numpy.array([
        0, 1,
        1, 2,
        2, 3,
        3, 0,
        0, 4,
        1, 5,
        2, 6,
        3, 7,
        4, 5,
        5, 6,
        6, 7,
        7, 4
    ]).reshape(-1, 2)

    fx, fy, cx, cy = camera_params

    K = numpy.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(pose[:3,:3])
    tvec = pose[:3, 3]

    dcoeffs = numpy.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = numpy.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    for i, j in edges:
        cv2.line(overlay, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)


# camera params fx, fy, cx, cy (optional to get apriltag pose)
camera_params = (871.3900560920833, 874.042504288542, 310.2749439858911, 229.99099528051528)
tag_size = 20

# create a cv2 window to show images
window = 'Camera'
cv2.namedWindow(window)
# open the first camera to get video stream
cap = cv2.VideoCapture(0)

# use DetectorOptions object ot intialize the detector paramters. Not required if using default values
# options  = apriltag.DetectorOptions(families='tag36h11',
#                  border=1,
#                  nthreads=4,
#                  quad_decimate=1.0,
#                  quad_blur=0.0,
#                  refine_edges=True,
#                  refine_decode=False,
#                  refine_pose=False,
#                  debug=False,
#                  quad_contours=True)
# detector = apriltag.Detector(options)

# create apriltag detector instance
detector = apriltag.Detector()
# use detector.add_tag_family(family) to add an apriltag family to the detector

# loop until either no new frames or esc was pressed
while True:
    success, frame = cap.read() # get new frame
    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) # convert to grayscale

    # detect the apriltags in the image
    detections, dimg = detector.detect(gray, return_image=True)

    num_detections = len(detections)
    print('Detected {} tags.\n'.format(num_detections))

    # overlay on the apriltag
    overlay = frame // 2 + dimg[:, :, None] // 2

    # loop through all detected apriltags and print their info,
    # get their pose if camera_params is available
    for i, detection in enumerate(detections):
        print('Detection {} of {}:'.format(i + 1, num_detections))
        print()
        print(detection.tostring(indent=2))

        if camera_params is not None:
            pose, e0, e1 = detector.detection_pose(detection,
                                                   camera_params,
                                                   tag_size)
            print(detection.tostring(
                    collections.OrderedDict([('Pose',pose),
                                             ('InitError', e0),
                                             ('FinalError', e1)]),
                                             indent=2))
            draw_pose(overlay,
                      camera_params,
                      tag_size,
                      pose)
        print()


    # show image with apriltags overlay
    cv2.imshow(window, overlay)
    cv2.imshow('two', dimg)

    # if ESC clicked, break the loop
    if  cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
