# edit java_video_streaming
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


# edit yml files
def editVideoBackendJava(serverPath):
    for i in os.listdir(serverPath):
        if "java" in i:
            print("found video_backend_java folder")
            fullPath = serverPath + i + "/"
            name = "start_stream.bat"
            full_Path = fullPath + name
            msg ='powershell.exe -command Set-executionpolicy "bypass"\n'
            msg = msg + 'powershell.exe -command get-executionpolicy\n'
            msg = msg + 'echo "' + getIp() + '"| PowerShell.exe -file start_server.ps1\n'
            file = open(full_Path, 'w')
            file.write(msg)
            file.close()
            os.system('cd %s && start %s' % (fullPath, name))


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(os.getcwd())) + "/"
    editVideoBackendJava(path)
