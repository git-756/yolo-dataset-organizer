# YOLO データセットオーガナイザー

YOLO (You Only Look Once) 形式のデータセットを整理・前処理・拡張するための一連のPythonスクリプト集です。アノテーション作業で生成されたデータを、YOLOでの訓練に適した形式に一括変換したり、データの水増し（Data Augmentation）を行ったりします。

---

## ✨ 主な機能（スクリプト一覧）

このリポジトリには、以下のスクリプトが含まれています。

### 1. `0_clear_dataset.py`
**機能**: 既存のデータセットをクリーンアップします。
- `dataset/images/train`, `dataset/images/val`
- `dataset/labels/train`, `dataset/labels/val`
上記フォルダ内にあるすべてのファイル（画像、ラベル）を削除し、データセットを準備する前の状態に戻します。

### 2. `1_preparation_dataset.py`
**機能**: アノテーションデータを訓練用と検証用に分割します。
- `annotation_data` フォルダ（設定変更可能）にある画像とラベルファイルを読み込みます。
- 全データをシャッフルし、デフォルトで 8:2 の割合で訓練用(`train`)と検証用(`val`)にランダムに振り分けます。
- 振り分けたファイルをYOLOの標準的なディレクトリ構造（`dataset/images/train`など）に移動します。

### 3. `augment.py` (New!)
**機能**: Albumentationsを使用して学習データを拡張（水増し）します。
- `dataset/images/train` 内の既存の画像とラベルを読み込み、様々な変換（明るさ変更、ノイズ付加、ぼかしなど）を適用して新しいデータを生成します。
- 生成されたデータは `aug_` という接頭辞付きで保存され、元のデータ数に対して指定倍率（デフォルトは20倍）までデータを増やします。
- **対応している変換**:
    - RandomBrightnessContrast (明るさ・コントラスト)
    - GaussNoise (ガウシアンノイズ)
    - Blur (ぼかし)
    - CLAHE (適応的ヒストグラム均等化)
    - ImageCompression (JPEG圧縮ノイズ)
    - ChannelShuffle (チャンネルシャッフル)

### 4. `2_modify_labels_recursive.py`
**機能**: ラベルファイル（`.txt`）のクラスIDを一括で置換します。
- `dataset/labels` フォルダ内の `train` と `val` を再帰的に検索します。
- 指定したクラスID（例: `15`）を別のID（例: `0`）に一括書き換えします。

---

## ⚙️ 動作要件

- Python 3.8 以上
- **albumentations** (画像拡張用)
- **opencv-python** (画像処理用)

---

## 🚀 使い方（実行順序）

1.  **アノテーションデータの準備**:
    - `annotation_data` フォルダに、アノテーション済みの画像(.jpg/.png)とラベル(.txt)を入れます。

2.  **データセットの初期化**:
    ```bash
    python yolo_dataset/0_clear_dataset.py
    ```

3.  **データセットの振り分け**:
    ```bash
    python yolo_dataset/1_preparation_dataset.py
    ```

4.  **データの拡張（オプション）**:
    - 学習データを増やしたい場合に実行します。
    ```bash
    python yolo_dataset/augment.py
    ```

5.  **ラベルIDの修正（オプション）**:
    - クラスIDを変更する必要がある場合に実行します。
    ```bash
    python yolo_dataset/2_modify_labels_recursive.py
    ```

6.  **学習の開始**:
    - `dataset` フォルダが完成したら、`data.yaml` を指定してYOLOの学習を開始してください。

---

## 📜 ライセンス

このプロジェクトは **MIT License** のもとで公開されています。ライセンスの全文については、[LICENSE](LICENSE) ファイルをご覧ください。

また、このプロジェクトはサードパーティ製のライブラリ（Albumentations, OpenCVなど）を利用しています。これらのライブラリのライセンス情報については、[NOTICE.md](NOTICE.md) ファイルに記載しています。

## 作成者
[Samurai-Human-Go](https://samurai-human-go.com/%e9%81%8b%e5%96%b6%e8%80%85%e6%83%85%e5%a0%b1/)

## ブログ
[【PythonでYOLO自動化】面倒なデータセット準備を秒殺！3つの便利スクリプトを公開](https://samurai-human-go.com/python-yolo-dataset-organizer/)
[【Python】画像データ拡張を自動化！アノテーション(txt)もセットで水増しするスクリプト
](https://samurai-human-go.com/python-image-augmentation-tool/)