from ftplib import FTP

def ftp_ops():
    try:
        ftp = FTP("ftp.dlptest.com")
        ftp.login("dlpuser", "rNrKYTX9g7z3RgJRmxWuGHbeu")
        ftp.retrlines("LIST")

        with open("up.txt", "w") as f: f.write("test")
        with open("up.txt", "rb") as f: ftp.storbinary("STOR up.txt", f)
        print("Uploaded")

        with open("down.txt", "wb") as f: ftp.retrbinary("RETR up.txt", f.write)
        print("Downloaded")

        ftp.quit()
    except Exception as e:
        print("Error:", e)

ftp_ops()
