# yolo-dataset-organizer

0_clear_dataset.py
    "/home/jetson/program/yolo/dataset/hansa_only"このフォルダ内の
    ディレクトリ構造を維持したままファイルを一括削除する。

1_preparation_dataset.py
    入力フォルダ'/home/jetson/gaibu_microSD/yolo/annotation/data'
    出力フォルダ'/home/jetson/gaibu_microSD/yolo/dataset/hansa_only'
    として　train(トレーニング用),vaild(検証用)へとファイル振り分け。
    ８：２の割合でランダムに振り分けるようにしている。

2_modify_labels_recursive.py
    labelImgでアノテーションするとテキストファイル先頭のラベル番号みたいなやつが
    15になっている。一つだけ学習したい場合は0しか割り当てられないので
    15＞0に一括自動変換する。