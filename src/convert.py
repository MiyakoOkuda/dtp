import argparse
import glob
import logging
import os

from PIL import Image

logger = logging.getLogger(__name__)


def convert(dpi_threshold, indir):
    """dpi_threshold以下のCMYKに変換
    ../img/に入っている全ての画像を変換する

    Args:
        indir (str): 変換したい画像が入っているdirectory
    """
    infiles = glob.glob(f'{indir}*.*')
    for infile in infiles:
        logger.info(f'infile: {infile}')
        stem = os.path.splitext(os.path.basename(infile))[0]
        outfile = f'../result/{stem}_e.jpg'
        img = Image.open(infile)
        try:
            if img.mode == 'RGB':
                img = img.convert('CMYK')
            elif img.mode == 'RGBA':
                img = img.convert('RGB').convert('CMYK')
            else:
                logger.info(f'{infile} is not in (RGB, RGBA)')
            if 'dpi' in img.info.keys():
                dpi = dpi_threshold if img.info['dpi'][0] > dpi_threshold else img.info['dpi'][0]
                img.save(outfile, dpi=(dpi, dpi))
            else:
                img.save(outfile)
        except Exception:
            logger.error(infile, exc_info=True)


def main(args):
    convert(args.dpi_threshold, args.indir)


if __name__ == '__main__':
    """基本的には引数不要
    ひとつ上の階層のimg/に変換したい画像を入れてsrc内で
    python convert.py [-dt <dpi_threshold> -d <input_directory_name>]
    を実行。結果はresult/に保存される。保存ファイル名は
    file_basename = stem + extention(include dot)
    として
    result/{stem}_e{extention}
    となる。
    photoshopの
    ファイル -> スクリプト -> イメージプロセッサー
    でresult/を絶対パスで指定し実行すると、指定箇所にpsdファイルとして書き出される。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-dt', '--dpi_threshold', type=int, default=350, help='dpi threshold')
    parser.add_argument('-d', '--indir', type=str, default='../img/', help='input directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='True means debug mode')
    args = parser.parse_args()
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s (%(lineno)s) %(levelname)s %(message)s', level=level)

    main(args)
