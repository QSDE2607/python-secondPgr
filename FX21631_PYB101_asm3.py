import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import json

DIRECTORY = 'FX21631_asm3.json' 
employee_list = []
manage_list = []
department_list = []
employee_list_text = []
manage_list_text = []
department_list_text = []



class Department:       #tạo class Department nhận thông tin về phòng ban
    def __init__(self, id_dp, BSalary, name):
        self.dp_id = id_dp
        self.bsalary = BSalary
        self.name = name
        self.employees = []
        
    def add_employee(self,employee):
        return self.employees.append(employee)
    def get_employees_list(self):
        return self.employees
    def get_BSalary(self): #lấy thưởng phòng ban
        return int(self.bsalary)
    def getName(self):  #lấy tên phòng ban
        return self.name
    def get_thongtin(self):     #lấy tất cả thông tin về phòng ban
        a = {'ID_DP' : self.dp_id, 'Name_DP' : self.name, 'Bonus' : self.bsalary}
        return a

def kiemtrainput_so(a):
    if a == '':
        print('Bạn không được bỏ trống thông tin này')
    elif a != '': 
        try:
            a = int(a)
            if a <= 0: 
                print("Số nhập vào phải lớn hơn 0. Vui lòng nhập lại!")
            else:
                return True
        except ValueError:
            print("Số nhập vào phải là số tự nhiên. Vui lòng nhập lại!")
            return False

def kiemtrainput_chu(b):
    if b == '':
        print('Bạn không được bỏ trống thông tin này')
        return False
    else: 
        return True



class Employee():       # tạo class Employee nhận thông tin về thông tin nhân viên
    def __init__(self, id, name, salary_base, working_day,department,working_performance, bonus, late_comming_days): #tạo class gồm các thuộc tính về nhân viên
        self.id = id
        self.name = name
        self. salary_base = salary_base
        self.working_day = working_day
        self.department = department
        self.working_performance = working_performance
        self.bonus = bonus
        self.late_comming_days = late_comming_days
        self.DB_salary = 0
        for i in company['Departments']:            # lấy thông tin thưởng phòng ban nếu thông tin nhập vào ứng với phòng ban đã có sẵn
            if department == i['Name_DP']:
                self.DB_salary += i['Bonus']
    def Phat_DM(self):                              # lấy thông tin thưởng phạt từ site JSON
        co_che = urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Flate_coming.json?alt=media&token=55246ee9-44fa-4642-aca2-dde101d705de').read()
        info = json.loads(co_che)
        for i in info:
            di_muon = []
            try:
                a = int(i['max'])
            except KeyError:
                a = 10
            b = int(i['min'])
            di_muon.append(a)
            di_muon.append(b)
            
            if di_muon[0] >= self.late_comming_days > di_muon[1]:       #so sánh số ngày đi muộn với cơ chế phạt để trả về kết quả phạt
                Phat_DM = self.late_comming_days * int(i['value'])
            else:
                continue
        return Phat_DM
    
    def Luong_TN_chuathue(self):    #tính lương khi chưa có thuế
        chua_thuong = (self.salary_base * self.working_day) * self.working_performance
        TTN_chuathue = (chua_thuong + self.bonus + self.DB_salary - self.Phat_DM()) * 89.5 / 100
        return TTN_chuathue

    def thue_chiu(self): # lấy thông tin thuế từ site XML
        thue = urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Ftax.xml?alt=media&token=f7a6f73d-9e6d-4807-bb14-efc6875442c7').read()
        root = ET.fromstring(thue)
        list = root.findall('tax')
        for i in list:
            sosanh = []
            try:
                a = int(i.find('max').text)
            except AttributeError:
                a = 100
            b = int(i.find('min').text)
            sosanh.append(a)
            sosanh.append(b)
            if sosanh[0] >= self.Luong_TN_chuathue()/1000000 > sosanh[1]:           # So sánh thông tin thu nhập chưa thuế để trả về số thuế phải chịu
                thue_chiu = self.Luong_TN_chuathue() * int(i.find('value').text) /100
            else:
                continue
        return thue_chiu
    
    def Luong_TN(self):   #tính lương thực nhân
        Luong_TN = self.Luong_TN_chuathue() - self.thue_chiu()
        return Luong_TN
    
    def get_thongtin(self): 
        a = {'ID': self.id, 'Department' : self.department, 'Chuc vu': 'Nhan vien', 'Ho va ten: ': self.name, 'He so luong: ': self.salary_base, 'Ngay lam viec': self.working_day, 'He so hieu qua: ' : self.working_performance, 'Thuong: ': self.bonus, 'So ngay di muon: ': self.late_comming_days, 'Luong_TN: ' : self.Luong_TN() }
        return a

class Manage (Employee):#tạo class Manage nhận thông tin về thông tin nhân viên quản lý và kế thừa class Employee
    def __init__(self, id, name, salary_base, working_day,department,working_performance, bonus, late_comming_days):
        super().__init__(id, name, salary_base, working_day,department,working_performance, bonus, late_comming_days)
        
    def Luong_TN_chuathue_MN(self):
        chua_thuong = (self.salary_base * self.working_day) * self.working_performance
        TTN_chuathue_MN = (chua_thuong + self.bonus + self.DB_salary + self.DB_salary*10/100 - self.Phat_DM()) * 89.5 / 100
        return TTN_chuathue_MN
    
    def thue_chiu_MN(self):
        thue = urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/funix-way.appspot.com/o/xSeries%2FChung%20chi%20dieu%20kien%2FPYB101x_1.1%2FASM_Resources%2Ftax.xml?alt=media&token=f7a6f73d-9e6d-4807-bb14-efc6875442c7').read()
        root = ET.fromstring(thue)
        list = root.findall('tax')
        for i in list:
            sosanh = []
            try:
                a = int(i.find('max').text)
            except AttributeError:
                a = 100
            b = int(i.find('min').text)
            sosanh.append(a)
            sosanh.append(b)
            if sosanh[0] >= self.Luong_TN_chuathue_MN()/1000000 > sosanh[1]:
                thue_chiu = self.Luong_TN_chuathue_MN() * int(i.find('value').text) /100
            else:
                continue
        return thue_chiu
        
    def Luong_TN_Manage(self):
        Luong_TN_Manage = self.Luong_TN_chuathue_MN() - self.thue_chiu()
        return Luong_TN_Manage

    def get_thongtin(self): 
        a = {'ID': self.id, 'Department' : self.department, 'Chuc vu': 'Quan lý', 'Ho va ten: ': self.name, 'He so luong: ': self.salary_base, 'Ngay lam viec': self.working_day, 'He so hieu qua: ' : self.working_performance, 'Thuong: ': self.bonus, 'So ngay di muon: ': self.late_comming_days, 'Luong_TN: ' : self.Luong_TN_Manage() }
        return a


def add_employee():     
    chuc_vu = input('Bạn muốn thêm nhân viên hay quản lý? - Nhân viên điền NV, Quản lý điền QL: ')    #kiểm tra xem người dùng muốn thêm nhân viên hay quản lý
    if chuc_vu == ('NV'):
        while True:
            id = input("Nhập ID cho nhân viên: ")
            if id in ID_NV_list:
                print('Mã nhân viên đã tồn tại')
            elif id == '':
                print('Bạn không được bỏ trống thông tin này')
            elif not id.isdigit():
                print("Vui lòng nhập vào 1 số tự nhiên!")        
            else:
                break
        while True:        
            name = input("Nhập tên cho nhân viên: ")
            if kiemtrainput_chu(name) == True:
                break
            else: continue
        while True:
            salary_base = input("Nhập lương cơ bản: ")
            if kiemtrainput_so(salary_base) == True:
                salary_base = int(salary_base)
                break
        while True:        
            working_day = input("Nhập số ngày làm việc: ")
            if kiemtrainput_so(working_day) == True:
                working_day = int(working_day)
                break
        while True:
            department = input("Nhập tên phòng ban (viết hoa chữ cái đầu): ")
            if department == '':
                print("Không được bỏ trống chỗ này!")
            elif department not in NAMEDP_list:                     #Kiểm tra nếu thông tin phòng ban nhập vào chưa có sẵn thì thêm phòng ban mới
                a = input("Chưa có sẵn phòng ban này tạo mới nhé! \n OK nhập ok: ")
                if a == 'ok':
                    add_department()
                    break
                else: 
                    print("Nhập lại tên phòng ban đi")
                return True
            else:
                break
        while True:
            try:
                working_performance = float(input("Nhập hệ số hiệu quả: "))
                break
            except:
                print('Vui lòng nhập vào 1 số thập phân')
                
        while True:
            try:
                bonus = int(input('Nhập thưởng cố định: '))
                break
            except:
                print('Vui lòng nhập vào 1 số tự nhiên')
        while True:
            try:
                late_comming_days = int(input("Nhập số ngày đi muộn: "))
                break
            except:
                print('vui lòng nhập vào 1 số tự nhiên')
        new_employee = Employee(id, name, salary_base, working_day,department,working_performance, bonus, late_comming_days)
        employee_list.append(new_employee)
        employee_list_text.append(new_employee.get_thongtin())
        print(f"{name} đã được thêm vào danh sách nhân viên.")
    elif chuc_vu == 'QL':            #Nếu thêm quản lý thì gọi đến hàm thêm quản lý
        add_manage()
def remove_employee_by_id():
    while True:         #kiểm tra input có đúng định dạng hay chưa
        remove_id = input("Nhập mã nhân viên muốn xóa: ")
        if remove_id == '':
            print("Bạn không được để trống thông tin này!")
        elif not remove_id.isdigit():
            print("Thông tin nhập vào phải là số tự nhiên!")
        elif remove_id not in ID_NV_list:
            print("Không có nhân viên nào có ID này")
        else:
            for employee in employee_list_text:         #kiểm tra đã có thông tin về nhân viên ứng với số ID vừa nhập hay chưa
                if employee['ID'] == remove_id:
                    employee_list_text.remove(employee)
                    print("Đã xóa nhân viên thành công!")
            break
def remove_department_by_id():
    while True: #kiểm tra input có đúng định dạng hay chưa
        remove_id = input("Nhập mã phòng bạn muốn xóa: ")
        if remove_id == '':
            print("Bạn không được để trống thông tin này!")
        else:
            try: 
                remove_id = int(remove_id)
                if remove_id <=0:
                    print('Vui lòng nhập vào 1 số dương')
                elif remove_id not in ID_DP_list:
                    print("Không có phòng ban nào có ID này") #kiểm tra đã có thông tin về phòng ban ứng với số ID vừa nhập hay chưa
                elif remove_id in ID_DP_Have_EMPs:
                    print("Phòng, ban này đã có nhân viên không thể xóa")
                else:
                    for department in department_list_text:
                        if int(department['ID_DP']) == remove_id:
                            department_list_text.remove(department)
                            print("Đã xóa phòng ban thành công!")
                    break
            except ValueError:
                print("Thông tin nhập vào phải là số tự nhiên!")
def edit_employee_info(employees_list):
    while True:
        id_to_edit = input('Nhập mã nhân viên muốn chỉnh sửa: ')
        if id_to_edit == '':
            print('Không được để trông thông tin này')
        else:
            try:
                id_to_edit = int(id_to_edit)
                if id_to_edit <= 0:
                    print('Vui lòng nhập vào 1 số dương')
                elif id_to_edit not in ID_NV_list:
                    print('Không tồn tại nhân viên có ID này')
                else:
                    for employee in employees_list:
                        if employee['ID'] == str(id_to_edit):
                            print(employee)
                            new_name = input("Nhập họ và tên mới: ")
                            if new_name != "":
                                employee["Ho va ten: "] = new_name

                            new_position = input("Nhập chức vụ mới: ")
                            if new_position != "":
                                employee["Chuc vu"] = new_position

                            new_coefficient = input("Nhập hệ số lương mới: ")
                            if new_coefficient != "" and new_coefficient.isnumeric():
                                employee["He so luong: "] = float(new_coefficient)
                            elif new_coefficient != "":
                                print("Bạn cần nhập đúng định dạng.")

                            new_days_worked = input("Nhập số ngày làm việc mới: ")
                            if new_days_worked != "" and new_days_worked.isnumeric():
                                employee["Ngay lam viec"] = int(new_days_worked)
                            elif new_days_worked != "":
                                print("Bạn cần nhập đúng định dạng.")

                            new_efficiency_coefficient = input("Nhập hệ số hiệu quả mới: ")
                            if new_efficiency_coefficient != "" and new_efficiency_coefficient.isnumeric():
                                employee["He so hieu qua: "] = float(new_efficiency_coefficient)
                            elif new_efficiency_coefficient != "":
                                print("Bạn cần nhập đúng định dạng.")

                            new_bonus = input("Nhập số tiền thưởng mới: ")
                            if new_bonus != "" and new_bonus.isnumeric():
                                employee["Thuong: "] = int(new_bonus)
                            elif new_bonus != "":
                                print("Bạn cần nhập đúng định dạng.")

                            new_days_late = input("Nhập số ngày đi muộn mới: ")
                            if new_days_late != "" and new_days_late.isnumeric():
                                employee["So ngay di muon: "] = int(new_days_late)
                            elif new_days_late != "":
                                print("Bạn cần nhập đúng định dạng.")
                                
                                
                            print('\n Thông tin sau chỉnh sửa là')
                            print("Mã nhân viên: {}".format(employee["ID"]))
                            print("Họ và tên: {}".format(employee["Ho va ten: "]))
                            print("Chức vụ: {}".format(employee["Chuc vu"]))
                            print("Hệ số lương: {}".format(employee["He so luong: "]))
                            print("Số ngày làm việc: {}".format(employee["Ngay lam viec"]))
                            print("Hệ số hiệu quả: {}".format(employee["He so hieu qua: "]))
                            print("Thưởng: {}".format(employee["Thuong: "]))
                            print("Số ngày đi muộn: {}".format(employee["So ngay di muon: "]))
                            print('Đã hoàn tất chỉnh sửa')
                    break
            except ValueError:
                print('Vui lòng nhập vào 1 số tự nhiên')
            

    
def add_manage():
        while True:     # Đặt và kiểm tra ID quản lý đã tồn tại hay chưa
            id = input("Nhập ID cho quản lý: ")
            if id in ID_NV_list:
                print('Mã quản lý này đã tồn tại')
            elif id == '':
                print('Bạn không được bỏ trống thông tin này')
            elif not id.isdigit():
                print("Vui lòng nhập vào 1 số tự nhiên!")        
            else:
                break
        
        while True:
            name = input("Nhập tên quản lý: ")
            if kiemtrainput_chu(name) == True:
                break
        while True:
            salary_base = input("Nhập lương cơ bản: ")
            if kiemtrainput_so(salary_base) == True:
                salary_base = int(salary_base)
                break
        while True:        
            working_day = input("Nhập số ngày làm việc: ")
            if kiemtrainput_so(working_day) == True:
                working_day = int(working_day)
                break
        while True:
            department = input("Nhập tên phòng ban (viết hoa chữ cái đầu): ")
            if department == '':
                print("Không được bỏ trống chỗ này!")
            elif department not in NAMEDP_list:
                a = input("Chưa có sẵn phòng ban này tạo mới nhé! \n OK nhập ok: ")
                if a == 'ok':
                    add_department()
                    break
                else: 
                    print("Nhập lại tên phòng ban đi")
                    continue
            else:
                break
        while True:
            try:
                working_performance = float(input("Nhập hệ số hiệu quả: "))
                break
            except:
                print('Vui lòng nhập vào 1 số thập phân')
                
        while True:
            try:
                bonus = int(input('Nhập thưởng cố định: '))
                break
            except:
                print('Vui lòng nhập vào 1 số tự nhiên')
        while True:
            try:
                late_comming_days = int(input("Nhập số ngày đi muộn: "))
                break
            except:
                print('vui lòng nhập vào 1 số tự nhiên')
        new_employee = Manage(id, name, salary_base, working_day,department,working_performance, bonus, late_comming_days)
        employee_list.append(new_employee)
        employee_list_text.append(new_employee.get_thongtin())
        print(f"{name} đã được thêm vào danh sách nhân viên quản lý.")
def add_department():
    while True:
        id_dp = input('Nhập ID phòng ban: ')
        if id_dp in ID_DP_list:
            print('Mã phòng ban đã tồn tại')
        elif id_dp == '':
            print('Bạn không được bỏ trống thông tin này')
        elif not id_dp.isdigit():
            print("Vui lòng nhập vào 1 số tự nhiên!")        
        else:
            break
    while True:
        try:
            BSalary = int(input('Nhập thưởng phòng ban: '))
            break
        except:
            print('Vui lòng nhập vào 1 số tự nhiên')
    while True:
        name = input('Nhập tên phòng ban: ')
        if name == '':
            print('Bạn không được bỏ trông thông tin này')
        else:
            break
    new_department = Department(id_dp, BSalary, name)
    department_list.append(new_department)
    department_list_text.append(new_department.get_thongtin())
    print(f"{name} has been added as a new Department.")
def display_employees():
    for employee in company['Employees']:
        CH_HSL = "{:,}".format(int(employee['He so luong: ']))
        CH_Thuong = "{:,}".format(int(employee['Thuong: ']))
        print("----")
        print(f"Mã số: {employee['ID']}")
        print(f"Mã bộ phận: {employee['Department']}")
        print(f"Chức vụ: {employee['Chuc vu']}")
        print(f"Họ và tên: {employee['Ho va ten: ']}")
        print( "Hệ số lương: ", CH_HSL, "(VND)")
        print(f"Số ngày làm việc: {employee['Ngay lam viec']} (ngày)")
        print(f"Hệ số hiệu quả: {employee['He so hieu qua: ']}")
        print(f"Thưởng: " , CH_Thuong, "(VND)")
        print(f"Số ngày đi muộn: {employee['So ngay di muon: ']}")
        print("----")
def display_department():
    for dm in company['Departments']:
        CH_Bonus = '{:,}'.format(int(dm['Bonus']))
        print("----")
        print(f"Mã số: {dm['ID_DP']}")
        print(f"Tên phòng: {dm['Name_DP']}")
        print(f"Thưởng:" , CH_Bonus)    
        print("----")        
def load_data(): #loadfile input nếu không tìm thấy file thì tạo 1 file chứ 1 dict gồm 2 dict con Employees và Departments rỗng
    try:
        with open(DIRECTORY, 'r') as file:
            company = json.load(file)
    except FileNotFoundError:
        company = {'Employees': {}, 'Departments': {}}
    return company
def save_data(company):
    with open(DIRECTORY, 'w') as file:
        json.dump(company, file, indent=4)

def dispaly_salary():
    for employee in company['Employees']:
        print (f"Mã số: {employee['ID']}")
        CH_TNTN = "{:,}".format(int(employee['Luong_TN: '])) # chuẩn hóa số tiền từ dạng 1000000 thành 1,000,000
        print (f"Thu nhập thực nhận: {CH_TNTN} (VND)")


def main():
    global company
    company = load_data()
    for i in company['Departments']:
        department_list_text.append(i)
    for v in company['Employees']:
        employee_list_text.append(v)        #load data từ file input và cập nhật thông tin sẵn có vào các list tương ứng
    global ID_NV_list
    ID_NV_list = []
    for i in company['Employees']:
        ID_NV_list.append(int(i['ID']))
    global ID_DP_list
    ID_DP_list = []
    for i in company['Departments']:
        ID_DP_list.append(int(i['ID_DP']))
    global NAMEDP_list
    NAMEDP_list = []
    for i in company['Departments']:
        NAMEDP_list.append(i['Name_DP'])
        
        
    a = list()                          #lấy ra list tên các phòng ban có nhân viên từ file JSON
    for i in company['Employees']:
        a.append(i['Department'])
    global DP_Have_EMP
    DP_Have_EMP = list(set(a))
    global ID_DP_Have_EMPs
    ID_DP_Have_EMPs = []
    for i in DP_Have_EMP:
        for j in company['Departments']:
            if j['Name_DP'] == i:
                ID_DP_Have_EMPs.append(int(j['ID_DP']))     #lấy ra list ID các phòng ban có nhân viên từ file JSON
    while True:
        print("\nMenu")
        print("1. Hien thi nhan vien")
        print("2. Hien thi phòng ban")
        print("3. Thêm nhân viên")
        print("4. Xóa nhân viên theo ID")
        print("5. Xóa phòng ban theo ID")
        print("6. Hiển thị bảng lương")
        print("7. Chỉnh sửa thông tin nhân viên")        
        print("8. Exit")
        choice = input("Enter your choice: ")
        try: 
            choice = int(choice)
            if choice == 1:
                display_employees()
            elif choice == 2:
                display_department()
            elif choice == 3:
                add_employee()
            elif choice == 4:
                remove_employee_by_id()
            elif choice == 5:
                remove_department_by_id()
            elif choice == 6:
                dispaly_salary()
            elif choice == 7:
                edit_employee_info(employee_list_text)
            elif choice == 8:
                break
            else:
                print("Invalid choice. Please try again.")   
        except ValueError:
            print('Vui lòng nhập vào 1 số tự nhiên tương ứng với những chức năng ở trên!')
            
            
    company = {'Departments' : department_list_text, 'Employees' : employee_list_text}          #Gom data sau khi đã chỉnh sửa vào và lưu xuống file
    save_data(company)

if __name__ == '__main__':
    main()

