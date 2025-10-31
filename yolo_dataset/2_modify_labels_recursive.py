import os

def modify_label_files(root_directory):
    subdirectories = ['train', 'val']
    """
    指定されたルートディレクトリ内の train および val サブディレクトリにある
    すべての .txt ファイルを検索し、各ファイルの各行の先頭の '15' を '0' に変更します。

    Args:
        root_directory (str): ラベルファイルのルートディレクトリのパス。
    """
    subdirectories = ['train', 'val']
    for subdir in subdirectories:
        target_directory = os.path.join(root_directory, subdir)
        if os.path.isdir(target_directory):
            for filename in os.listdir(target_directory):
                if filename.endswith('.txt'):
                    filepath = os.path.join(target_directory, filename)
                    with open(filepath, 'r') as f:
                        lines = f.readlines()

                    modified_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if parts and parts[0] == '15':
                            parts[0] = '0'
                            modified_lines.append(' '.join(parts) + '\n')
                        else:
                            modified_lines.append(line)

                    with open(filepath, 'w') as f:
                        f.writelines(modified_lines)
                    print(f"処理しました: {filepath}")

    print("処理が完了しました。")

if __name__ == "__main__":
    target_root_directory = "dataset/labels"  # ラベルファイルのルートディレクトリを指定
    print(f"ディレクトリ '{target_root_directory}' 内の .txt ファイルを修正します。")
    modify_label_files(target_root_directory)