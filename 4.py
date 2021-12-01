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
def editStaticYml(serverPath):
    for i in os.listdir(serverPath):
        if "frontend" in i:
            print("found datacenter_frontend folder\n")
            fullPath = serverPath + i + "/"
            ymlPath = fullPath + "config.js"
            with open(ymlPath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(ymlPath, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if "window.ws_url = 'ws://" in line:
                        line = line.replace(line, "window.ws_url = 'ws://" + getIp() + ":9090'\n")
                    elif "window.api_domain = 'http://" in line:
                        line = line.replace(line, "window.api_domain = 'http://" + getIp() +":9999'\n")
                    elif "window.ue_editor = 'http://" in line:
                        line = line.replace(line, "window.ue_editor = 'http://" + getIp() + ":80/editor'\n")
                    f_w.write(line)
            f_w.close()
            print("docker-compose.yml has been edited\n")
            os.system('cd %s && docker load -i image.tar && docker-compose up' % fullPath)

# edit yml files
def editbat(serverPath):
    projectPath = ""
    webRtcPath = ""
    exePath = ""
    grootPath = ""
    msg = ""
    name = "start.bat"
    full_Path = serverPath + name
    for i in os.listdir(serverPath):
        if "Project" in i:
            projectPath = serverPath + i
            for j in os.listdir(projectPath):
                if ".exe" in j:
                    exePath = j
        elif "signal" in i:
            webRtcPath = serverPath + i
        elif "groot" in i:
            grootPath = serverPath + i 

    msg = msg + 'cd %s\n' % projectPath
    msg = msg + 'start %s -PixelStreamingIP=localhost -PixelStreamingPort=8888 -ExecCmds=DisableAllScreenMessages -NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52 -RenderOffScreen -ResX=1920 -ResY=1080 -ForceRes -ExecCmds="PixelStreaming.Encoder.MaxQP 33,PixelStreaming.Encoder.MinQP 25,t.MaxFPS 30"\n' % exePath
    msg = msg + 'cd %s\n' % webRtcPath
    msg = msg + 'start run.bat\n'
    msg = msg + 'cd %s\n' % grootPath
    msg = msg + 'groot.exe --control-center '+ getIp() +':10002'
    file = open(full_Path, 'w')
    file.write(msg)
    file.close()
    print("start.bat has been edited\n")

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.getcwd())) + "/"
    editbat(path)
    editStaticYml(path)
