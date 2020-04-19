import os

import PIL
from PIL import Image


class ImageResize:
    """
    Resize (reduce) any image (jpeg, jpg, png) with an aspect ratio of 1920 * 1080
    by 75%, 50%, and 25%.
    """

    def __init__(self, files):

        self.files = files
        self.original_width = 1920
        self.reduce_image_by = [75, 50, 25]
        self.valid_file_extensions = ['jpeg', 'jpg', 'png']

    @staticmethod
    def get_original_file_extension(file):
        """
        Identify original file extension
        """
        file_ext_break_point = file.rfind('.') + 1
        return file[file_ext_break_point:]

    @staticmethod
    def get_original_file_name(file):
        """
        Get original file name
        """
        root, name = file.split('/')

        return name[:-4].replace(' ', '-')

    def valid_files(self):
        """
        Remove invalid files by extension type
        """
        valid_files = []
        for file in self.files:
            if self.get_original_file_extension(file=file) in self.valid_file_extensions:
                valid_files.append(file)
            else:
                print(f'Incorrect file type: {file}')

        return valid_files

    @staticmethod
    def get_current_image_size(file):
        """
        Return aspect ratio of original image
        """
        file = PIL.Image.open(file)

        width, height = file.size

        return width, height

    def get_image_width_list(self):
        """
        Return image width list: Based on 16:9 (1920*1080) starting point
        """

        new_widths = []

        for size in self.reduce_image_by:
            new_width = self.original_width / 100 * size
            new_widths.append(int(new_width))

        return new_widths

    def processing(self):
        """
        Attempt to process image files
        """
        for file in self.valid_files():
            width, height = self.get_current_image_size(file=file)
            file_name = self.get_original_file_name(file=file)
            file_extension = self.get_original_file_extension(file=file)
            if width == self.original_width:
                file = Image.open(file)
                for width_size in self.get_image_width_list():
                    calculate_width_precentage = (width_size/float(width))
                    new_horizontal_size = int((float(height)*float(calculate_width_precentage)))
                    file = file.resize((width_size, new_horizontal_size), PIL.Image.ANTIALIAS)
                    file.save(f'./processed_images/{file_name}_{width_size}_x_{new_horizontal_size}.{file_extension}')
            else:
                print(f'Wrong aspect ratio: {file}')


def main():

    image_location_directory = 'images'
    processed_images_directory = 'processed_images'

    if os.path.exists(image_location_directory) and os.path.exists(processed_images_directory):
        all_file_paths = []

        for root, directory, files in os.walk('images'):
            for file in files:
                file_path = os.path.join(root, file)
                all_file_paths.append(file_path)

        convert = ImageResize(files=all_file_paths)
        convert.processing()

    else:
        print('Error: Either images and/or processed_images directories do not exist!')


if __name__ == "__main__":
    main()
