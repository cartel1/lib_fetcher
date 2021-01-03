import shutil
import tempfile

with tempfile.TemporaryDirectory() as tmp_lib_dir:
    print(f'Temp lib dir is: {tmp_lib_dir}')
    print(f'Current working dir is: {os.getcwd()}')
    # git = GitFetch("https://github.com/FFmpeg/FFmpeg.git", "ffmpeg_lib_source")
    os.chdir(tmp_lib_dir)
    print(f'New current working dir is: {os.getcwd()}')
    print('Downloading remote git repo ...')
    git = GitFetch("https://github.com/FFmpeg/FFmpeg.git")
    local_repo_dir = "target_ffmpeg_lib_source_dir"
    git.clone_repo(local_repo_dir)
    print(f'Finished cloning git repo')
    for root, dirs, files in os.walk(tmp_lib_dir):
        if local_repo_dir in dirs:
            print("Remote repo was successfully cloned")
            for r, d, f in os.walk(local_repo_dir):
                print(f'{r} {d} {f}')
            break
        else:
            print("Remote repo clone is not present")
    os.chdir("/Users/douglas/PycharmProjects/lib_fetcher")
