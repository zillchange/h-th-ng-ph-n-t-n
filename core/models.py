import db
class user_avatar():
    idprofile=""
    pic_name=""

    def __init__(self, idprofile, pic_name):
        self.idprofile = idprofile
        self.pic_name = pic_name
    
    def save(self):
        # Kết nối đến SQL Server
        conn = db.connection()
        cursor=conn.cursor()

        # insert data
        sql = "insert into user_avatar(idprofile,pic_name) values(%s,%s)"
        cursor.execute(sql,(self.idprofile,self.pic_name,))
        conn.commit()
        conn.close()     
        # Trả về ID của tài liệu đã chèn
        return True
    
    
    def find_picture_name_by_id(idprofile):
        # Kết nối đến SQL server
        conn = db.connection()
        cursor=conn.cursor()

        # Tìm kiếm theo informationuserid
        sql = "select* from user_avatar where idprofile=%s"
        value=(idprofile,)
        cursor.execute(sql,value)
        user_avatar = cursor.fetchone()
        conn.commit()

        # Đóng kết nối
        conn.close() 

        # Trả về một đối tượng User hoặc None nếu không tìm thấy
        return user_avatar if user_avatar else None

    def update_pic_name(idprofile, new_pic_name):
        # Kết nối đến SQL server
        conn = db.connection()
        cursor=conn.cursor()

        # Cập nhật tài liệu dựa trên username
        sql = "update user_avatar set pic_name = %s where idprofile =%s"
        cursor.execute(sql,(new_pic_name,idprofile))
        conn.commit()

        # Đóng kết nối
        conn.close() 

        return True 

