"""Extracts the previews from all .ggb files and adds them to the readme"""
import os
import shutil


def extract_thumbnail(filename, base):
    os.system(f'7z x "{filename}" -o"screenshots" > /dev/null')
    os.chdir('screenshots')
    empty_dir_except_png()
    os.rename('geogebra_thumbnail.png', f'{base}.png')
    os.chdir('..')

def empty_dir_except_png():
    for filename in os.listdir('.'):
        _, inner_ext = os.path.splitext(filename)
        if inner_ext != ".png":
            try:
                os.remove(filename)
            except IsADirectoryError:
                shutil.rmtree(filename)

def append_to_readme(f, path):
    for filename in os.listdir(f'{path}/screenshots'):
        base, ext = os.path.splitext(filename)
        if ext == '.png':
            full_path = f'{path}/screenshots/{filename}'
            # https://github.com/Microsoft/vscode/issues/7871
            full_path_sanitized = full_path.replace(' ', '&#32;')
            f.write(f'{full_path}\n\n')
            f.write(f'![{filename} preview]({full_path_sanitized})\n')
            f.write('\n')

def main(path):
    curdir = os.getcwd()
    os.chdir(path)
    os.mkdir('screenshots')
    for filename in os.listdir('.'):
        base, ext = os.path.splitext(filename)
        if ext == ".ggb":
            extract_thumbnail(filename, base)
    os.chdir(curdir)

    with open('README.md', 'a') as f:
        append_to_readme(f, path)


main('.')
main('IB')
main('IB/Physics')
main('IB/Physics/Diffraction pattern')
