import os
import subprocess


IP = os.getenv("IP")
SMB_IP = os.getenv("SMB_IP")
PASSWORD = os.getenv("PASSWORD")
LOGIN = os.getenv("LOGIN")
DIR_NAME = os.getenv("DIR_NAME")
SMBCREDS_FILE = os.getenv("SMBCREDS_FILE")
SMB_LOGIN = os.getenv("SMB_LOGIN")
SMB_PASSWORD = os.getenv("SMB_PASSWORD")


def ssh_command(ip, line, use_sudo=True):
    if use_sudo:
        command = f"sudo bash -c \"{line}\""
    else:
        command = line

    result = subprocess.run(
        [
            "sshpass", "-p", f"{PASSWORD}",
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"{LOGIN}@{ip}",
            command
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    return result


print(f"\n{'='*50}")
print(f"Обрабатываем хост: {IP}")
print(f"{'='*50}")

        
try:
      
    ping_result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", IP],
        capture_output=True,
        text=True
        )

    if ping_result.returncode != 0:
        print(f"Хост {IP} не пингуется!")
        exit()
               

     
    result = ssh_command(IP, f"mkdir -p /shared/{DIR_NAME}")
    if result.returncode != 0:
        print(f"Ошибка создания директории /shared/{DIR_NAME} на {IP}")
        exit()
              


    result = ssh_command(IP, f"cat > /opt/{SMBCREDS_FILE} << 'EOF'\nuser={SMB_LOGIN}\npassword={SMB_PASSWORD}\nEOF")
    if result.returncode != 0:
        print(f"Ошибка создания {SMBCREDS_FILE}")
 

      
           
    fstab_line = f"//{SMB_IP}/{DIR_NAME} /shared/{DIR_NAME} cifs credentials=/opt/{SMBCREDS_FILE},x-systemd.automount,rw,file_mode=0777,dir_mode=0777 0 0"

    result = ssh_command(IP, f"echo '{fstab_line}' | tee -a /etc/fstab > /dev/null")
    if result.returncode != 0:
        print(f"Ошибка добавления в fstab")
        exit()


 
    result = ssh_command(IP, f"mkdir -p ~/Desktop/ && ln -sf /shared/{DIR_NAME} ~/Desktop/\"Общая папка\"", use_sudo=False)
    if result.returncode != 0:
        print(f"Не удалось создать ярлык для {LOGIN}")
        exit()
    

          
    result = ssh_command(IP, "cp /home/adm114/Desktop/shortcut.desktop ~/Desktop/ 2>/dev/null || echo 'Файл shortcut.desktop не найден'", use_sudo=False)


    result = ssh_command(IP, "mount -a")
    if result.returncode != 0:
        print(f"Ошибка монтирования, но продолжаем")

    print(f"Работа на хосте {IP} завершена успешно!")

           

except subprocess.TimeoutExpired:
    print(f"Хост {IP}: Таймаут подключения")

except Exception as e:
    print(f" Хост {IP}: Ошибка - {e}")

            

            


