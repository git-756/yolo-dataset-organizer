import os
import shutil
import random
from pathlib import Path
from PIL import Image, ImageEnhance

# --- 設定パラメータ ---
INPUT_DIR_NAME = "annotation_data"   # 入力フォルダ名
OUTPUT_DIR_NAME = "augment_output"   # 出力フォルダ名
NUM_COPIES = 2                       # 1枚の画像から何枚生成するか（水増し数）
SUFFIX = "_cp"                       # ファイル名の後ろにつける接尾辞
# --------------------

def augment_data():
    # パスの設定 (実行ディレクトリを基準)
    base_dir = Path.cwd()
    input_dir = base_dir / INPUT_DIR_NAME
    output_dir = base_dir / OUTPUT_DIR_NAME

    # 入力フォルダの確認
    if not input_dir.exists():
        print(f"エラー: 入力フォルダ '{INPUT_DIR_NAME}' が見つかりません。")
        return

    # 出力フォルダの作成 (存在しない場合は作成)
    output_dir.mkdir(exist_ok=True)
    print(f"出力先: {output_dir}")

    # 画像ファイルのリストを取得 (jpg, jpeg, pngなど必要に応じて追加)
    image_extensions = {".jpg", ".jpeg", ".png"}
    image_files = [p for p in input_dir.iterdir() if p.suffix.lower() in image_extensions]
    
    print(f"対象ファイル数: {len(image_files)} 件 (x {NUM_COPIES}倍生成)")

    for img_path in image_files:
        stem = img_path.stem  # 拡張子なしのファイル名 (例: test01)
        
        # テキストファイルのパス確認
        txt_path = input_dir / f"{stem}.txt"
        has_txt = txt_path.exists()
        
        if not has_txt:
            print(f"警告: {img_path.name} に対応するテキストファイルがありません。スキップします。")
            # 必要であれば、continueせずに画像だけ処理するように変更してください
            continue

        # 設定された回数分ループして生成
        for i in range(NUM_COPIES):
            # ファイル名の決定
            if NUM_COPIES == 1:
                # 1回だけの時は "_cp" のみ (例: test01_cp.jpg)
                new_stem = f"{stem}{SUFFIX}"
            else:
                # 複数の時は連番を振る (例: test01_cp_0.jpg)
                new_stem = f"{stem}{SUFFIX}_{i}"

            new_img_name = f"{new_stem}{img_path.suffix}"
            new_txt_name = f"{new_stem}.txt"
            
            save_img_path = output_dir / new_img_name
            save_txt_path = output_dir / new_txt_name

            # --- 画像処理 ---
            try:
                with Image.open(img_path) as img:
                    img = img.convert("RGB")
                    
                    # コントラスト変更 (±20%)
                    contrast_factor = random.uniform(0.8, 1.2)
                    enhancer_c = ImageEnhance.Contrast(img)
                    img_contrasted = enhancer_c.enhance(contrast_factor)
                    
                    # 明るさ変更 (±20%)
                    brightness_factor = random.uniform(0.8, 1.2)
                    enhancer_b = ImageEnhance.Brightness(img_contrasted)
                    img_final = enhancer_b.enhance(brightness_factor)
                    
                    # 保存
                    img_final.save(save_img_path)
            except Exception as e:
                print(f"画像処理エラー {img_path.name}: {e}")
                continue

            # --- テキストファイルのコピー ---
            try:
                shutil.copy2(txt_path, save_txt_path)
            except Exception as e:
                print(f"テキストコピーエラー {txt_path.name}: {e}")

    print("すべての処理が完了しました。")

if __name__ == "__main__":
    augment_data()