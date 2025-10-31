# YOLO データセットオーガナイザー

YOLO (You Only Look Once) 形式のデータセットを整理・前処理するための一連のPythonスクリプト集です。アノテーション作業で生成されたデータを、YOLOでの訓練に適した形式（ディレクトリ構造やラベル番号）に一括で変換します。

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

### 3. `2_modify_labels_recursive.py`
**機能**: ラベルファイル（`.txt`）のクラスIDを一括で置換します。
- `dataset/labels` フォルダ内の `train` と `val` を再帰的に検索します。
- すべての `.txt` ファイルを開き、行の先頭にあるクラスIDが `15` の場合、それを `0` に書き換えます。
- （例: `15 0.5 0.5 0.1 0.1` → `0 0.5 0.5 0.1 0.1`）

---

## 🚀 使い方（実行順序）

1.  **アノテーションデータの準備**:
    - `annotation_data` フォルダ（`1_preparation_dataset.py`で指定）に、アノテーション済みの画像ファイル（.jpg, .png）とラベルファイル（.txt）をすべて入れます。

2.  **(オプション) データセットの初期化**:
    - 既に `dataset` フォルダにデータがある場合は、`0_clear_dataset.py` を実行して中身を空にします。
    ```bash
    python yolo_dataset/0_clear_dataset.py
    ```

3.  **データセットの振り分け**:
    - `1_preparation_dataset.py` を実行して、データを `train` と `val` に振り分けます。
    ```bash
    python yolo_dataset/1_preparation_dataset.py
    ```

4.  **ラベルIDの修正**:
    - `2_modify_labels_recursive.py` を実行して、クラスIDを（必要に応じて）一括置換します。
    ```bash
    python yolo_dataset/2_modify_labels_recursive.py
    ```

5.  **`data.yaml` の準備**:
    - `data.yaml.sample` を参考に、`data.yaml` ファイルを作成し、YOLOの訓練時に指定してください。

---

## 📜 ライセンス

このプロジェクトは **MIT License** のもとで公開されています。ライセンスの全文については、[LICENSE](LICENSE) ファイルをご覧ください。

## 作成者
[Samurai-Human-Go](https://samurai-human-go.com/%e9%81%8b%e5%96%b6%e8%80%85%e6%83%85%e5%a0%b1/)

## ブログ
[【PythonでYOLO自動化】面倒なデータセット準備を秒殺！3つの便利スクリプトを公開](https://samurai-human-go.com/python-yolo-dataset-organizer/)