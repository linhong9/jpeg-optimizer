import os
import subprocess
import glob
from PIL import Image
import tinify
from pathlib import Path

tinify.key = 'G26qTFngkhXFgjLZzVdj6t7Y6Kz2p5b1'

src_path = '/mnt/f/work/JHG/idea-board/s3-sync/idea-board'
dst_path = '/mnt/f/work/JHG/idea-board/s3-sync/idea-board-optimized'
width_limit = 1200
height_limit = 900
optimum_width = 1090
optimum_height = 842

def optimizeAll():
    os.chdir(src_path)
    jpg_imgs = glob.glob('*.jp[e|g]*')
    for jpg_img in jpg_imgs:
        src_file = jpg_img
        im = Image.open(jpg_img)
        width, height = im.size
        
        dst_file = f'{dst_path}/{jpg_img}'

        scale = 1
        if width > width_limit:
            scale = optimum_width / width
        elif height > height_limit:
            scale = optimum_height / height
        if scale < 1:
            width = int(width * scale)
            height = int(height * scale)
            im = im.resize((width, height))
            src_file = f'resized_{src_file}'
            im.save(src_file)
        im.close()
        if Path(dst_file).exists():
            continue
        # subprocess.run(['jpegtran', '-copy', 'all', '-optimize', '-perfect', '-outfile', dst_file, f'{src_path}/{src_file}'])

        source = tinify.from_file(f'{src_path}/{src_file}')
        source.to_file(dst_file)

        if src_file.startswith('resized'):
            os.remove(f'{src_path}/{src_file}')
        print(dst_file)


if __name__ == '__main__':
    optimizeAll()