# edit static_server folder
import socket
import os


# this pc's ip
def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def editLevelSetting(serverPath):
    for i in os.listdir(serverPath):
        if "Project" in i or "project" in i:
            print("found UE4 Project folder\n")
            fullPath = serverPath + i + "/"
            for j in os.listdir(fullPath):
                if ("Project" in j or "project" in j) and (j.endswith("exe") == False):
                    anotherPath = fullPath + j + "/"
                    for k in os.listdir(anotherPath):
                        if "Dimensio" in k or "dimensio" in k:
                            iniPath = anotherPath + k + "/LevelSettings.ini"
                            with open(iniPath, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                            with open(iniPath, "w", encoding="utf-8") as f_w:
                                for line in lines:
                                    if "SocketAddress" in line:
                                        line = line.replace(line, "SocketAddress=ws://" + getIp() +":10002\n")
                                    f_w.write(line)
                            f_w.close()
                            print("Levelsetting.ini has been edited\n")

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
    editLevelSetting(path)
    editStaticYml(path)
