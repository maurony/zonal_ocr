import pdf2image as pi
from PIL import Image, ImageDraw
import pytesseract


def extract_pages(input_path, destination_directory):
    """
    @param input_path: file with multiple pages
    @param destination_directory: directory to save destination images
    """
    pages = pi.convert_from_path(input_path)
    for i in range(len(pages)):
        pages[i].save("./{0}/page_{1}.jpg".format(destination_directory, i), 'JPEG')


def draw_boxes(input_path, coordinates, output_path):
    """
    @param input_path: The path to the image to edit
    @param coordinates: An array of tuples of x/y coordinates (x1, y1, x2, y2)
    @param output_path: Path to save the drawn image
    """
    img = Image.open(input_path)
    draw = ImageDraw.Draw(img)
    for coords in coordinates:
        draw.rectangle(coords, outline=(255, 0, 0, 255), width=3)

    del draw
    img.save(output_path)


def crop(input_path, coordinates, output_path=None):
    """
    @param input_path: The path to the image to edit
    @param coordinates: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param output_path: Path to save the cropped image
    """
    image_obj = Image.open(input_path)
    cropped_image = image_obj.crop(coordinates)

    if output_path is not None:
        cropped_image.save(output_path)
    else:
        return cropped_image


def perform_ocr(input_path, coordinates):
    """
    @param input_path: The path to the image to edit
    @param coordinates: A tuple of x/y coordinates (x1, y1, x2, y2)
    """
    text_list = []
    config = '-l deu --oem 1 --psm 3'
    for coords in coordinates:
        cropped_image = crop(input_path=input_path, coordinates=coords)
        recognized_text = pytesseract.image_to_string(cropped_image, config=config)
        text_list.append(recognized_text)

    return text_list


# -------------
# testing
# -------------
# get the pdf
pdf_path = './docs/scans.pdf'
# and extract each page into a jpeg
extract_pages(pdf_path, 'img')

# define image path
image_path = 'img/page_0.jpg'
# coordinates from top left
# these can be easily be defined using gimp
zones = [
    (240, 900, 1400, 975),
    (237, 2220, 456, 2253)
]

# draw boxes in images
draw_boxes(image_path, zones, 'extraction_zones.jpg')

# if boxes are correct, then perform ocr indexing on them
perform_ocr(input_path=image_path, coordinates=zones)




