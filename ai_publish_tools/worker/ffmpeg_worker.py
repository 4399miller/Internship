import glob
import os
import shutil
import pathlib
import subprocess

from utility.commandlineutility import subprocess_may_error


def check_ffmpeg_exist():
    cmd = "where ffmpeg"
    cp = subprocess_may_error(cmd, "", True)
    if cp is None:
        return False

    filepath = cp.stdout.strip("\n")
    if os.path.exists(filepath):
        return True

    return False


def del_all_avi(folder):
    avi_files = []
    for rel, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".avi"):
                avi_files.append(os.path.join(rel, file))

    for file in avi_files:
        os.remove(file)


def get_folder_json_file(folder, ext=(".png")):
    png_files = []
    open_dirs = []
    for rel, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                if rel not in open_dirs:
                    open_dirs.append(rel)
                    png_files.append(os.path.join(rel, file))

    return png_files, open_dirs


def get_all_files(folder, ext):
    png_files = []
    for rel, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                png_files.append(os.path.join(rel, file))

    return png_files


def ffmpeg_generate_avi(root_dir):
    del_all_avi(root_dir)
    source_dir = os.path.join(root_dir, f"1.Source")
    mb_dir = os.path.join(root_dir, f"5.MotionBuilderOutput")

    png_files, dirs = get_folder_json_file(source_dir)
    print(png_files)
    print(dirs)
    for dir in dirs:
        files = os.listdir(dir)
        index = 1
        for file in files:
            if file.endswith(".png"):
                new_file = pathlib.Path(file).stem[:-6] + f"{index:0>6d}.png"
                index += 1
                print(new_file)
                os.rename(os.path.join(dir, file), os.path.join(dir, new_file))

    output_avi_path = []
    os.chdir(source_dir)
    for index in range(len(png_files)):
        filename = pathlib.Path(dirs[index]).stem + ".avi"
        file_match = pathlib.Path(png_files[index]).stem[:-6] + "%6d.png"

        filepath = os.path.join(os.path.dirname(dirs[index]), filename)
        file_match = os.path.join(dirs[index], file_match).replace("\\", "/")

        print(file_match)
        cmd = f"ffmpeg -f image2 -i \"{file_match}\" {filepath}"
        subprocess_may_error(cmd, "ffmpeg error")

        target_file = filepath.replace("1.Source", "5.MotionBuilderOutput")
        shutil.copyfile(filepath, target_file)
        output_avi_path.append(target_file)


    for avi_file in output_avi_path:
        os.chdir(os.path.dirname(avi_file))
        filename = pathlib.Path(avi_file).stem
        fbx_files = get_all_files(".", (".fbx"))
        eval_list = [os.path.basename(fbx)[:-4] for fbx in fbx_files]

        task = filename
        avi = f"{filename}.avi"
        for eval in eval_list:

            cmd = f"ffmpeg -f image2 -i \"{task}/{eval}/{eval}00%4d.png\" {task}/{eval}.avi"
            subprocess_may_error(cmd, "ffmpeg error")

            cmd = f"ffmpeg -i \"{avi}\" -i {task}/{eval}.avi -filter_complex hstack output_{task}_{eval}.avi"

            subprocess_may_error(cmd, "ffmpeg error")


def pic_gen_video(input_folder, wildcard, output_video):
    input_pattern = os.path.join(input_folder, wildcard)

    # 构建 ffmpeg 命令
    command = [
        "ffmpeg",
        "-framerate", "30",  # 可以根据需要调整帧率
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]
    # cmd = f"ffmpeg -framerate 30 -i \"{input_pattern}\" -c:v libx264 -pix_fmt yuv420p \"{output_video}\""

    # 将命令转换为字符串，以便打印和调试
    command_str = " ".join(command)
    print(f"Executing command: {command_str}")

    try:
        # 执行 ffmpeg 命令
        # result = subprocess.run(command, check=True, capture_output=True, text=True)
        result = subprocess_may_error(
            command,
            error_str="error",
            log_output=True,
            encoding="utf-8",
            check=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return None

def mer_videos(input_video1, input_video2, output_video):
    with open("videos_to_concat.txt", "w") as f:
        f.write(f"file '{input_video1}'\n")
        f.write(f"file '{input_video2}'\n")

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "videos_to_concat.txt",
        "-c", "copy",
        output_video
    ]

    try:
        # result = subprocess.run(command, check=True, capture_output=True, text=True)
        result = subprocess_may_error(
            command,
            error_str="error",
            log_output=True,
            encoding="utf-8",
            check=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return None

def diff_image(folder1, folder2, output_folder):
    # 获取两个文件夹中的所有图片文件
    images1 = set(f for f in os.listdir(folder1) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')))
    images2 = set(f for f in os.listdir(folder2) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')))

    # 找出两个文件夹中共有的图片
    common_images = images1.intersection(images2)

    for image_name in common_images:
        path1 = os.path.join(folder1, image_name)
        path2 = os.path.join(folder2, image_name)
        output_path = os.path.join(output_folder, f"diff_{image_name}")

        # 构建 ffmpeg 命令
        command = [
            "ffmpeg",
            "-i", path1,
            "-i", path2,
            "-filter_complex", "[0:v][1:v]blend=difference",
            "-frames:v", "1",
            output_path
        ]

        try:
            # 执行 ffmpeg 命令
            # subprocess.run(command, check=True, capture_output=True, text=True)
            subprocess_may_error(
                command,
                error_str="error",
                log_output=True,
                encoding="utf-8",
                check=True,
                text=True
            )
            print(f"已生成差异图像: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"处理图片 {image_name} 时出错: {e.stderr}")


if __name__ == "__main__":
    root_dir = "E:/Perforce/AI_Center/Retarget/Samples/20240809"
    ffmpeg_generate_avi(root_dir)

    # print(check_ffmpeg_exist())

    pass




























