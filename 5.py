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

# edit yml files
def editDist(serverPath):
    distPath = ""
    for j in os.listdir(serverPath):
        if "dist" in j:
            distPath = serverPath + j
            jsPath = distPath + "/" + "config.js"
            with open(jsPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(jsPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "inner'; // pixelstreaming" in line:
                        line = line.replace(line, "window.ws_url = 'http://" + getIp() +"/inner'; // pixelstreaming\n")
                    f_w.write(line)
            f_w.close()
            print("config.js has been edited")

def startNginx(serverPath, dist):
    for i in os.listdir(serverPath):
        if "nginx" in i:
            distPath = dist
            fullPath = serverPath + i + "/"
            nginxPath = fullPath + "nginx.exe"
            confPath = fullPath + "conf/nginx.conf"
            print(nginxPath)
            print(confPath)
            print(distPath)
            with open(confPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(confPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "listen 8" in line:
                        line = line.replace(line, "        listen 6555;\n")
                    if "server_name 192" in line:
                        line = line.replace(line, "        server_name " + getIp() + ";\n")
                    if "dist" in line:
                        line = line.replace(line, "            root " + distPath + ";\n")
                    f_w.write(line)
            f_w.close()
            print("nginx.conf has been edited")
            os.system('cd %s && nginx.exe' % fullPath)

if __name__ == '__main__':
    path = os.getcwd() + "/"
    newPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/"
    distpath = newPath + "dist"
    editDist(newPath)
    startNginx(path, distpath)