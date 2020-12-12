from PIL import Image, ImageChops


class ImageUtils:

    @staticmethod
    def is_two_images_equal(image1, image2):
        img1 = Image.open(image1).convert('RGB')
        img2 = Image.open(image2).convert('RGB')
        dif = ImageChops.difference(img1, img2)
        return True if dif.getbbox() is None else False
