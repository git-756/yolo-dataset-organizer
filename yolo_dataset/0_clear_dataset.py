import os

def clear_dataset_files(root_dir):
    """
    指定されたルートディレクトリ内の images および labels フォルダ以下のファイルをすべて削除します。
    ディレクトリ構造は保持し、ルート直下のファイルは削除しません。

    Args:
        root_dir (str): データセットのルートディレクトリのパス。
    """
    target_subdirectories = ["images/train", "images/val", "labels/train", "labels/val"]

    deleted_count = 0
    for subdir_path in target_subdirectories:
        full_path = os.path.join(root_dir, subdir_path)
        if os.path.isdir(full_path):
            for filename in os.listdir(full_path):
                file_path = os.path.join(full_path, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"削除しました: {file_path}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"エラーが発生しました: {file_path} - {e}")
        else:
            print(f"警告: ディレクトリ '{full_path}' が見つかりません。")

    if deleted_count == 0:
        print("削除するファイルはありませんでした。")
    else:
        print(f"合計 {deleted_count} 個のファイルを削除しました。")

if __name__ == "__main__":
    dataset_root = "dataset"  # あなたのデータセットのルートディレクトリ名を指定してください
    print(f"データセット '{dataset_root}' 内のファイルを削除します。")

    confirmation = input("続行しますか？ [y/N]: ").lower()
    if confirmation == 'y':
        clear_dataset_files(dataset_root)
        print("処理が完了しました。")
    else:
        print("処理をキャンセルしました。")