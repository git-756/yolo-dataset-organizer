import os
import random
import shutil
import glob

# --- 設定項目 ---

# 入力元ディレクトリ (画像ファイルとラベルファイルが混在)
source_dir = 'annotation_data'

# 出力先ベースディレクトリ
dataset_base_dir = 'dataset'

# 訓練用/検証用の分割比率 (訓練用データの割合)
train_ratio = 0.8

# --- ディレクトリパスの設定 ---
train_img_dir = os.path.join(dataset_base_dir, 'images', 'train')
valid_img_dir = os.path.join(dataset_base_dir, 'images', 'val')
train_label_dir = os.path.join(dataset_base_dir, 'labels', 'train')
valid_label_dir = os.path.join(dataset_base_dir, 'labels', 'val')

# --- 出力先ディレクトリを作成 ---
os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(valid_img_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(valid_label_dir, exist_ok=True)

print(f"出力先ディレクトリを作成しました（または既存です）:")
print(f" - {train_img_dir}")
print(f" - {valid_img_dir}")
print(f" - {train_label_dir}")
print(f" - {valid_label_dir}")
print("-" * 30)

# --- 全ての画像ファイルのリストアップ ---
image_paths = []
# jpg と png 両方を検索し、フルパスをリストに追加
for ext in ('*.jpg', '*.png', 'JPG'):
    image_paths.extend(glob.glob(os.path.join(source_dir, ext)))

# 画像ファイルが見つからなかった場合
if not image_paths:
    print(f"エラー: {source_dir} 内に画像ファイル (.jpg または .png) が見つかりません。")
    exit()

total_images = len(image_paths)
print(f"処理対象の画像ファイル総数: {total_images}")
print("-" * 30)

# --- 画像ファイルリストをシャッフル ---
random.shuffle(image_paths)

# --- 訓練用と検証用に分割 ---
split_index = int(total_images * train_ratio)
train_image_paths = image_paths[:split_index]
valid_image_paths = image_paths[split_index:]

print(f"訓練用 画像ファイル数: {len(train_image_paths)}")
print(f"検証用 画像ファイル数: {len(valid_image_paths)}")
print("-" * 30)

# --- ファイルを移動する関数 ---
def move_files(image_path_list, target_img_dir, target_label_dir):
    moved_img_count = 0
    moved_label_count = 0
    label_missing_count = 0

    for src_img_path in image_path_list:
        img_filename = os.path.basename(src_img_path)
        base_name = os.path.splitext(img_filename)[0]
        src_label_path = os.path.join(source_dir, base_name + '.txt')

        dest_img_path = os.path.join(target_img_dir, img_filename)
        dest_label_path = os.path.join(target_label_dir, base_name + '.txt')

        try:
            # 画像ファイルを移動
            shutil.move(src_img_path, dest_img_path)
            moved_img_count += 1

            # 対応するラベルファイルが存在すれば移動
            if os.path.exists(src_label_path):
                shutil.move(src_label_path, dest_label_path)
                moved_label_count += 1
            else:
                label_missing_count += 1
                # print(f"情報: ラベルファイルなし - {img_filename}") # 必要ならコメント解除

        except Exception as e:
            print(f"エラー: ファイル移動中にエラーが発生しました ({img_filename}): {e}")

    return moved_img_count, moved_label_count, label_missing_count

# --- 訓練用ファイルの移動 ---
print("訓練用ファイルを移動中...")
moved_train_img, moved_train_label, missing_train_label = move_files(train_image_paths, train_img_dir, train_label_dir)
print(f"訓練用ファイルの移動完了:")
print(f"  - 画像: {moved_train_img} 個")
print(f"  - ラベル: {moved_train_label} 個 (対応するもの)")
if missing_train_label > 0:
    print(f"  - ラベルなし画像: {missing_train_label} 個")
print("-" * 30)

# --- 検証用ファイルの移動 ---
print("検証用ファイルを移動中...")
moved_valid_img, moved_valid_label, missing_valid_label = move_files(valid_image_paths, valid_img_dir, valid_label_dir)
print(f"検証用ファイルの移動完了:")
print(f"  - 画像: {moved_valid_img} 個")
print(f"  - ラベル: {moved_valid_label} 個 (対応するもの)")
if missing_valid_label > 0:
    print(f"  - ラベルなし画像: {missing_valid_label} 個")
print("-" * 30)

print("すべての処理が完了しました。")

total_missing_labels = missing_train_label + missing_valid_label
if total_missing_labels > 0:
    print(f"合計 {total_missing_labels} 個の画像には対応するラベルファイルがありませんでした。")