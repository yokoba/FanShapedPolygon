import argparse
import datetime
import sys
from pathlib import Path
from pprint import pprint

import simplekml

from vincenty_direct import vincenty_direct

DEFAULT_OUTPUT_FILE_NAME = str(Path(__file__).stem)

def to_hex2(s):
    """sを2桁の16進数に変換した文字列を返す

    Args:
        s (string): 16進数で認識できる文字列

    Returns:
        string: sを16進変換した2桁の文字列
    """
    return to_hex(s, 2)

def to_hex6(s):
    """sを6桁の16進数に変換した文字列を返す

    Args:
        s (string): 16進数で認識できる文字列

    Returns:
        string: sを16進変換した6桁の文字列
    """
    return to_hex(s, 6)

def to_hex(s, digit):
    """sに指定された文字列をdigit桁の16進数の文字列を返す

    Args:
        s (string): 16進数で認識できる文字列
        digit (int): 桁数

    Raises:
        argparse.ArgumentTypeError: sを16進数に変換できない場合やsとdigitの桁数が異なる場合にエラー

    Returns:
        string: sを16進変換したdigit桁の文字列
    """

    if len(s) != digit:
        raise argparse.ArgumentTypeError('argument is short')

    try:
        h = format(int(s, 16), f'0{digit}x')
        return h
    except:
        raise argparse.ArgumentTypeError('invalid argument')

def get_argument():
    """プログラム実行に受け取る引数のパーサー
    """
    description = """表示名、緯度、経度、開始角、終了角、半径、地上高を指定して、KML上に円形のポリゴンを形成する"""

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('name', help='Google Earth上の表示名を指定')
    parser.add_argument('lat', type=float, help='緯度を10進数で指定')
    parser.add_argument('lon', type=float, help='経度を10進数で指定')
    parser.add_argument('start', type=int, help='開始角を北を0度して時計回りにプラス 0～360の10進数で指定')
    parser.add_argument('end', type=int, help='終了角をを北を0度して時計回りにプラス 0～360の10進数で指定')
    parser.add_argument('radius', type=int, help='半径(m)を10進数で指定')
    parser.add_argument('height', type=int, help='高さ(m)を10進数で指定')
    parser.add_argument('-s', '--step', type=int, help='何度毎に線を区切るか。開始角8, 終了角38 step 10の時 8,10,20,30,38となる。(def=10)', default=10)
    parser.add_argument('-a', '--altitudemode',
                        help='高さをどこを基準にするか。\nabsolute=地面から相対, clampToGround=地面に沿って配置, relativeToGround 標高+指定した高さ (def=absolute)',
                        choices=['absolute', 'clampToGround', 'relativeToGround'], default='absolute')
    parser.add_argument('-c', '--color', type=to_hex6, help='bbggrrを000000 ～ ffffffの16進形式で指定 (def=0000ff)', default='0000ff')
    parser.add_argument('-t', '--transparency', type=to_hex2, help='色の透明度を00 ～ ffの16進で指定 (def=50)', default='50')
    parser.add_argument('-l', '--outline', type=int, help='ポリゴンの枠線を表示するかどうか0,1で指定。 0 = 引かない, 1 = 引く (def=0)', default=0, choices=[0, 1])
    parser.add_argument('-e', '--extrude', type=int, help='地面から線を引くかどうか0,1で指定。0 = 引かない, 1 = 引く (def=1)', default=1, choices=[0, 1])
    parser.add_argument('-tes', '--tessellate', type=int, help='地面に沿って線を引くかどうか0,1で指定。0 = 引かない, 1 = 引く (def=1)', default=1, choices=[0, 1])
    parser.add_argument('-o', '--output', help='出力ファイル名 指定しなかった場合はkmlcircle_hhmmssff.kml')

    args = parser.parse_args()
    return args


def convert_angle(start, end):
    """開始角startと終了角endを適正に変換する
    start -60, end 60をstart 300, end 420とする

    Args:
        start (int): ポリゴンの開始角
        end (int): ポリゴンの終了角

    Returns:
        int, int: start, endを0以上の数値に変換した値
    """
    if start < 0:
        start = 360 + start
    if start > end:
        end = end + 360

    return start, end


def get_angle_list(start ,end, step):
    """start,endで指定された角度をstep毎にループさせるための配列を作成する

    Args:
        start (int): 開始角
        end (int): 終了角
        step (int): 角度の変化量

    Returns:
        list: start,endの間をstep毎に刻んだ配列
    """
    start, end = convert_angle(start, end)

    if start == end:
        start = 0
        end = 360

    angle_list = []
    for azimuth in range(start, end + step, step):
        angle_list.append(azimuth)

    return angle_list


def make_kml_polygon(name, coordinates, altitudemode, color, transparency, outline, extrude, tessellate, out_file_name):
    """KMLファイルを作成する

    Args:
        name (string): Google Earthの表示名
        coordinates (list[(lon, lat, height)...]): 緯度、経度、高さを含んだタプルの配列
        altitudemode (string): 何を基準に高さを決めるか
        color (string): 表示色 bbggrr形式の16進数の文字列
        transparency (string): 透明度 00 ～ ff形式の16進数の文字列
        outline (int): 外形線を引くかどうか
        extrude (int): 海面まで線を引くかどうか
        tessellate (int): 地形表面まで線を引くかどうか
        out_file_name (string): 出力ファイル名
    """
    kml = simplekml.Kml()

    pol = kml.newpolygon()
    pol.name = name
    pol.description = name
    pol.outerboundaryis = coordinates
    pol.polystyle.color = transparency + color
    pol.altitudemode = altitudemode
    pol.extrude = extrude
    pol.tessellate = tessellate
    pol.polystyle.outline = outline

    kml.save(out_file_name)


def main():
    args = get_argument()

    out_file_name = args.output
    if out_file_name is None:
        date = datetime.datetime.now()
        out_file_name = str(Path(f'{DEFAULT_OUTPUT_FILE_NAME}_{date.strftime("%H%M%S%f")}.kml'))
    elif Path(out_file_name).suffix != '.kml':
        out_file_name += '.kml'

    if Path(out_file_name).exists() and Path(out_file_name).is_file():
        print('出力ファイルが既に存在しています。上書きしてもいいですか？ (yes/no)')

        while True:
            res = input()
            if res.lower() in ['yes', 'y']:
                break
            elif res.lower() in ['no', 'n']:
                sys.exit(-1)

    angle_list = get_angle_list(args.start, args.end, args.step)

    coordinates = []
    coordinates.append((args.lon, args.lat, args.height))
    for azimuth in angle_list:
        geo = vincenty_direct(args.lat, args.lon, azimuth, args.radius)
        coordinates.append((geo['lon'], geo['lat'], args.height))
    coordinates.append((args.lon, args.lat, args.height))

    make_kml_polygon(args.name, coordinates, args.altitudemode, args.color, args.transparency, args.outline, args.extrude, args.tessellate, out_file_name)



if __name__ == '__main__':
    main()
