## Name
FanShapedPolygon

## Overview
Google Earth上に緯度、経度、半径と円の開始角、終了角を指定してポリゴンを作成する

## Description
KMLファイルは円を作成することができず、円を作成したければ中心の緯度,経度,円のサイズを元に円周上の緯度経度を求めるということを何度も繰り返し、
求めた緯度経度を元に直線を引いて擬似的に円を作成する必要があり、手作業でKMLファイルを作るのは非常に面倒。

## Demo
```
exsample
python FanShapedPolygon.py hole 34.689639 135.530102 -60 60 100 50
````
![googleearth](https://user-images.githubusercontent.com/31529581/68363684-14c9f980-016f-11ea-8efd-85b90d5149de.png)

## Requirement
python 3.7  
simplekml

## Usage
FanShapedPolygon.py name lat lon start end radius height [-s|--step step] [-a|--altitudemode [absolute, clampToGround, relativeToGround] [-c|--color color] [-t|--transparency transparency] [-l|--outline outline] [-e|--extrude extrude] [-t|--tessellate tessellate] [-o|--output output]  

### default
```
step         = 10
altitudemode = absolute
color        = 0000ff
transparency = 50
outline      = 1
extrude      = 1
tessellate   = 1
output       = kmlcircle_hhmmssff.kml hhmmssffは実行時の時間(時分秒マイクロ秒)に置換される
```

```
example
holeの名称で34.689639 135.530102を中心として300 → 60の範囲で100mの扇型の円を高さ50の所に青色で作成
python FanShapedPolygon.py hole 34.689639 135.530102 -60 60 100 50 --color ff0000
```


### args
```
必須パラメーター
name       google earth上での表示名
lat        ポリゴンの中心緯度
lon        ポリゴンの中心経度
start      円の開始角 北を0度して時計回りに0～360で指定、または-60 = 300 の様な指定も可能
end        円の開始角 北を0度して時計回りに0～360で指定、または-60 = 300 の様な指定も可能
           start -60 end 60 とした場合は 300 → 60 どの範囲で 120度の円を作成
radiud     指定した緯度経度を中心として半径をmで指定
height     ポリゴンの天井を地上から何メートルに作成するかをmで指定
```
```
オプションパラメーター
-s, --step         デフォルトでは10度単位
                   何度の単位でポリゴンを作成するか。start -60 end 60とした場合120度となり、120本の線で円が構成されるが表示が重くなる。
                   この為step10とすると10度単位で線画作成されるため作成されたポリゴンが軽くなる。

-a, --altitudemode デフォルトではabsolute
                   何を基準としてheight(高さ)を決めるか。
                   absolute 地面から相対
                   clampToGround 地面に沿って配置
                   relativeToGround 標高+指定した高さ
                   
                   標高モード
                   https://developers.google.com/kml/documentation/altitudemode?hl=ja

-c, --color        デフォルトでは0000ff
                   作成するポリゴンの色 bbggrr(青緑赤)の形式で指定。00 ～ ffの16新形式で指定。
                   青色ならff0000のように指定する。

-t, -transparency デフォルトでは50
                  作成するポリゴンの透明度を指定。00 ～ ffの16新形式で指定。

-l --outline      デフォルトでは0 = 付けない。
                  作成するポリゴンに外形線をつけるかどうか。1 = つける 0 = つけない。

-e, --extrude     デフォルトでは1 = 線を引く
                  作成したポリゴンの天井から地面まで線を引くかどうか。線をつけない場合heightに指定した高さに平面のポリゴンが作成される。
                  1 = 線を引く 0 = 線を引かない。

-t, --tessellate  デフォルトでは1 = 線を引く
                  作成したポリゴンの地面の線を地形に合わせて線を引くかどうか。
                  extrude = 1の場合にのみ影響する。
                  1 = 線を引く 0 = 線を引かない。

-o, --output      デフォルトではkmlcircle_hhmmssff.kml hhmmssffは時分秒マイクロ秒に置換される
                  出力するファイル名
```
## Install
pip install simplekml


## Contribution

## Licence
[Apache License 2.0, please see the LICENSE file for full details](https://github.com/electron/fiddle/blob/master/LICENSE.md).

## Author

[yokoban](https://github.com/NightSorrow)
