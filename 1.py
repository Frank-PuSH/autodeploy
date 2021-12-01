# edit static_server folder
import os


# edit yml files
def editStaticYml(serverPath):
    for i in os.listdir(serverPath):
        if "static" in i:
            print("found static_server folder\n")
            fullPath = serverPath + i + "/"
            ymlPath = fullPath + "docker-compose.yml"
            with open(ymlPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(ymlPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "image" in line:
                        line = line.replace(line, "    image: static_file_server:latest\n")
                    f_w.write(line)
            f_w.close()
            print("docker-compose.yml has been edited\n")
            os.system('cd %s && docker import static_image_v1.0.tar static_file_server:latest && docker-compose up' % fullPath)


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.getcwd())) + "/"
    editStaticYml(path)
