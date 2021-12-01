# -*- coding:utf-8 -*-
import os
import socket


# this pc's ip
def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def pushImage(serverPath):
    print("uploading docker image......")
    for i in os.listdir(serverPath):
        if "stream" in i:
            fullPath = serverPath + i + "/"
            os.system('cd %s && docker load -i stream_backend_v1.5.11.tar' % fullPath)
        elif i == "datacenter":
            fullPath = serverPath + i + "/"
            os.system('cd %s && docker load -i datacenter_v1.5.2.tar' % fullPath)
        elif "display" in i:
            fullPath = serverPath + i + "/"
            os.system('cd %s && docker load -i display_v1.5.2.tar' % fullPath)


def editcplusIni(serverPath):
    for i in os.listdir(serverPath):
        if "config" in i:
            fullPath = serverPath + i + "/"
            iniPath = fullPath + "cplus_config.ini"
            with open(iniPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(iniPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "stream_backend_ip" in line:
                        line = line.replace(line, "stream_backend_ip=" + getIp() + "\n")
                    elif "marker_online_ip" in line:
                        line = line.replace(line, "marker_online_ip=" + getIp() + "\n")
                    elif "postgresql_ip" in line:
                        line = line.replace(line, "postgresql_ip=" + getIp() + "\n")
                    f_w.write(line)
            f_w.close()
            print("cplus.ini has been edited\n")


def editYml(serverPath):
    for i in os.listdir(serverPath):
        if "config" in i:
            fullPath = serverPath + i + "/"
            iniPath = fullPath + "docker-compose.yml"
            with open(iniPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(iniPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "5.12" in line:
                        line = line.replace(line, "    image: stream_backend:v1.5.11\n")
                    elif "stream_server_ip:" in line:
                        line = line.replace(line, "      stream_server_ip: " + getIp() + "\n")
                    elif "datacenter_ip" in line:
                        line = line.replace(line, "      datacenter_ip: " + getIp() + "\n")
                    elif "static_file_ip" in line:
                        line = line.replace(line, "      static_file_ip: " + getIp() + "\n")
                    elif "static_file_sys" in line:
                        line = line.replace(line, "      static_file_sys: WINDOWS\n")
                    elif "static_file_absolute_path" in line:
                        line = line.replace(line, "      static_file_absolute_path: " + serverPath + "static_server\n")
                    elif "本机ip" in line:
                        line = line.replace(line, "      ip: " + getIp() + "     #需本机ip\n")
                    f_w.write(line)
            f_w.close()
            print("docker-compose.yml has been edited\n")
            os.system('cd %s && docker-compose up' % fullPath)


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.getcwd())) + "/"
    pushImage(path)
    editcplusIni(path)
    editYml(path)