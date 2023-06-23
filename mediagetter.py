from savedfile import pexels_api
import requests
import json
import mysql.connector

class downloader:
    def __init__(self):
        self.my_videodb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="H.no194/3A",
        database="video_db")


    def video_downloader(self,id):
        response = requests.get(f"https://api.pexels.com/videos/videos/{id}", headers={"Authorization": pexels_api()})
        data = json.loads(response.text)["video_files"]
        for dat in data:
            if dat["width"] == 720 and dat["height"] == 1280 or dat["width"] == 1280 and dat["height"] == 720:
                link = dat["link"]
                break
            else:
                pass      
        with open("video_demo.mp4", "wb") as f:
            f.write(requests.get(link).content)
            print("Video downloaded")
            f.close()

    def create_database(self):
        return self.my_videodb.cursor().execute("CREATE DATABASE video_db")
    
    def create_table(self):
        return self.my_videodb.cursor().execute("CREATE TABLE videos (id INT AUTO_INCREMENT PRIMARY KEY, video_id VARCHAR(255) )")
    
    def create_column(self):
        return self.my_videodb.cursor().execute("ALTER TABLE videos ADD COLUMN used VARCHAR(255) DEFAULT 'No'")
    
    def insert_video(self,video_id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"INSERT INTO videos (video_id) VALUES ('{video_id}');")
        self.my_videodb.commit()
        print(cursor.rowcount, "records inserted.")

    def get_random_video(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SELECT * FROM videos ORDER BY RAND() LIMIT 1")
        myresult = cursor.fetchall()[0][1]
        return myresult
    
    def show_columns(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SHOW COLUMNS FROM videos")
        for x in cursor:
            print(x)

    def show_all_video_id(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SELECT * FROM videos")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x[1])
        return myresult
    
    def delete_video_byid(self,id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"DELETE FROM videos WHERE id = {id};")
        self.my_videodb.commit()
        print(cursor.rowcount, "record(s) deleted")

    def delete_video_byvideo_id(self,video_id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"DELETE FROM videos WHERE video_id = '{video_id}';")
        self.my_videodb.commit()
        print(cursor.rowcount, "record(s) deleted")



