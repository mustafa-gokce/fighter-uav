import random
import time
import cv2
import numpy
import qrcode
import pyzbar.pyzbar as pyzbar


def merge_image(background, foreground, upper_left_x, upper_left_y):
    """
    merge two images as background and foreground
    """

    # convert to rgba
    if background.shape[2] == 3:
        background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)
    if foreground.shape[2] == 3:
        foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2BGRA)

    # crop the overlay from both images
    bh, bw = background.shape[:2]
    fh, fw = foreground.shape[:2]
    x1, x2 = max(upper_left_x, 0), min(upper_left_x + fw, bw)
    y1, y2 = max(upper_left_y, 0), min(upper_left_y + fh, bh)
    front_cropped = foreground[y1 - upper_left_y:y2 - upper_left_y, x1 - upper_left_x:x2 - upper_left_x]
    back_cropped = background[y1:y2, x1:x2]

    # calculate alpha channels
    alpha_front = front_cropped[:, :, 3:4] / 255
    alpha_back = back_cropped[:, :, 3:4] / 255

    # replace an area in result with overlay
    result = background.copy()
    result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:, :, :3] + (1 - alpha_front) * back_cropped[:, :, :3]
    result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front * alpha_back) * 255

    # return to result image
    return result


def rotate_image(image, angle, background_color):
    """
    rotate an image
    """
    image = image.copy()
    rows, columns = image.shape[:2]
    image_center = (columns // 2, rows / 2)
    rotate_matrix = cv2.getRotationMatrix2D(image_center, angle, 0.5)
    image = cv2.warpAffine(image, rotate_matrix, (columns, rows), borderValue=background_color)
    image = cv2.resize(image, (rows * 2, columns * 2))
    return image


# settings
background_image_width = 1366
background_image_height = 768

# qr code generator
qr_generator = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=5,
    border=2,
)

# generate a qr code
qr_generator.add_data("TESTUCUSU")
qr_generator.make(fit=True)
qr_code = qr_generator.make_image(fill_color="black", back_color="white")
qr_code = qr_code.convert("RGB")
qr_code = numpy.array(qr_code)
qr_code = qr_code[:, :, ::-1].copy()

while True:
    # create background image
    background_image_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # rotate qr code
    new_qr_code = rotate_image(image=qr_code, angle=random.randint(0, 359), background_color=background_image_color)

    # create background
    background_image = numpy.full((background_image_height, background_image_width, 3), background_image_color,
                                  dtype=numpy.uint8)

    # create image frame
    upper_left_x = random.randint(new_qr_code.shape[0] // 2, background_image_width - new_qr_code.shape[0] // 2)
    upper_left_x -= new_qr_code.shape[0] // 2
    upper_left_y = random.randint(new_qr_code.shape[1] // 2, background_image_height - new_qr_code.shape[1] // 2)
    upper_left_y -= new_qr_code.shape[1] // 2
    image_frame = merge_image(background=background_image,
                              foreground=new_qr_code,
                              upper_left_x=upper_left_x,
                              upper_left_y=upper_left_y)

    # plot decoded data on image frame
    for data in pyzbar.decode(image_frame):
        decoded_text = data.data.decode("utf-8")
        polygon = numpy.array([data.polygon], numpy.int32)
        polygon = polygon.reshape((-1, 1, 2))
        cv2.polylines(image_frame, [polygon], True, (0, 255, 0), 5)
        rectangle = data.rect
        cv2.putText(image_frame, decoded_text, (rectangle[0], rectangle[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # show image frame
    cv2.imshow("QR Generate", image_frame)

    # break if requested
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

    # limit frame rate
    time.sleep(1)
