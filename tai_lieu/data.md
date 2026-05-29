1. Nhóm Lệnh Định Nghĩa Dữ Liệu (DDL - Data Definition Language)
   Nhóm lệnh dùng để xây dựng, thay đổi và quản lý cấu trúc của các bảng và đối tượng trong cơ sở dữ liệu.

1.1 Lệnh CREATE TABLE (Tạo bảng mới)
Ý nghĩa: Định nghĩa một bảng mới bao gồm tên bảng, danh sách các cột, kiểu dữ liệu và các ràng buộc (Constraints).

Cú pháp chuẩn:

SQL
CREATE TABLE ten_bang (
cot_1 kieu_du_lieu rang_buoc_1,
cot_2 kieu_du_lieu rang_buoc_2,
...,
CONSTRAINT ten_rang_buoc_pk PRIMARY KEY (cot_1),
CONSTRAINT ten_rang_buoc_fk FOREIGN KEY (cot_2) REFERENCES bang_khac(cot_khoa_chinh)
);
Các ràng buộc phổ biến cần nhớ:

NOT NULL: Bắt buộc ô dữ liệu không được để trống.

UNIQUE: Giá trị trong cột không được trùng lặp giữa các hàng.

PRIMARY KEY: Khóa chính (kết hợp của NOT NULL và UNIQUE), định danh duy nhất cho hàng.

FOREIGN KEY: Khóa ngoại, dùng để liên kết cấu trúc giữa hai bảng, đảm bảo toàn vẹn tham chiếu.

CHECK (dieu_kien): Kiểm tra giá trị nạp vào có thỏa mãn điều kiện logic hay không (Ví dụ: CHECK (Tuoi >= 18)).

DEFAULT gia_tri: Tự động điền giá trị mặc định nếu người dùng không nhập khi chèn dòng mới.

Ví dụ thực tế:

SQL
CREATE TABLE SinhVien (
MaSV VARCHAR(10) NOT NULL,
HoTen NVARCHAR(50) NOT NULL,
NgaySinh DATE,
Email VARCHAR(50) UNIQUE,
DiemTB DECIMAL(3,2) CHECK (DiemTB >= 0 AND DiemTB <= 10),
MaLop VARCHAR(10),
CONSTRAINT PK_SinhVien PRIMARY KEY (MaSV)
);
1.2 Lệnh ALTER TABLE (Sửa đổi cấu trúc bảng)
Ý nghĩa: Thay đổi cấu trúc của một bảng hiện có mà không làm mất dữ liệu hiện tại (thêm cột, xóa cột, sửa kiểu dữ liệu hoặc thêm/xóa ràng buộc).

Cú pháp các trường hợp:

SQL
-- 1. Thêm cột mới vào bảng
ALTER TABLE ten_bang ADD ten_cot_moi kieu_du_lieu;

-- 2. Xóa một cột khỏi bảng
ALTER TABLE ten_bang DROP COLUMN ten_cot;

-- 3. Sửa đổi kiểu dữ liệu hoặc ràng buộc của cột (Tùy hệ quản trị: ALTER COLUMN hoặc MODIFY)
ALTER TABLE ten_bang ALTER COLUMN ten_cot kieu_du_lieu_moi; -- SQL Server / PostgreSQL
ALTER TABLE ten_bang MODIFY COLUMN ten_cot kieu_du_lieu_moi; -- MySQL

-- 4. Thêm ràng buộc khóa ngoại sau khi đã tạo bảng
ALTER TABLE ten_bang ADD CONSTRAINT ten_khoa_ngoai FOREIGN KEY (ten_cot) REFERENCES bang_khac(khoa_chinh);
1.3 Lệnh DROP TABLE và TRUNCATE TABLE (Xóa bảng / Xóa dữ liệu sạch)
DROP TABLE: Xóa toàn bộ cấu trúc của bảng và toàn bộ dữ liệu chứa trong bảng đó vĩnh viễn khỏi hệ thống.

SQL
DROP TABLE ten_bang;
TRUNCATE TABLE: Chỉ xóa sạch toàn bộ các dòng dữ liệu bên trong bảng, giữ lại cấu trúc bảng, các cột, chỉ mục (Index) và ràng buộc. Lệnh này chạy nhanh hơn lệnh DELETE không điều kiện vì không ghi nhận nhật ký (log) cho từng dòng bị xóa.

SQL
TRUNCATE TABLE ten_bang; 2. Nhóm Lệnh Thao Tác Dữ Liệu (DML - Data Manipulation Language)
Nhóm lệnh cốt lõi dùng để truy vấn, thêm, sửa, và xóa nội dung dữ liệu bên trong các bảng.

2.1 Lệnh INSERT INTO (Chèn dữ liệu mới)
Ý nghĩa: Thêm một hoặc nhiều hàng dữ liệu mới vào trong bảng.

Cú pháp:

SQL
-- Cách 1: Chèn dữ liệu tường minh theo cột chỉ định (Khuyên dùng)
INSERT INTO ten_bang (cot_1, cot_2, cot_3)
VALUES (gia_tri_1, gia_tri_2, gia_tri_3);

-- Cách 2: Chèn nhiều dòng cùng lúc
INSERT INTO ten_bang (cot_1, cot_2)
VALUES (g_tri_A1, g_tri_A2),
(g_tri_B1, g_tri_B2);
2.2 Lệnh UPDATE (Cập nhật / Sửa dữ liệu)
Ý nghĩa: Thay đổi giá trị dữ liệu hiện có của các hàng thỏa mãn điều kiện.

Cú pháp:

SQL
UPDATE ten_bang
SET cot_1 = gia_tri_moi_1, cot_2 = gia_tri_moi_2
WHERE dieu_kien_loc;
-- LƯU Ý CỰC KỲ QUAN TRỌNG: Nếu không có mệnh đề WHERE, toàn bộ các hàng trong bảng sẽ bị sửa.
Ví dụ:

SQL
UPDATE SinhVien
SET DiemTB = 8.5, Email = 'dung.nt@gmail.com'
WHERE MaSV = 'SV6901';
2.3 Lệnh DELETE (Xóa hàng dữ liệu)
Ý nghĩa: Gỡ bỏ một hoặc nhiều hàng cụ thể ra khỏi bảng dựa trên điều kiện lọc.

Cú pháp:

SQL
DELETE FROM ten_bang
WHERE dieu_kien_loc;
-- LƯU Ý CỰC KỲ QUAN TRỌNG: Nếu không có mệnh đề WHERE, toàn bộ dữ liệu trong bảng sẽ bị xóa sạch! 3. Lệnh SELECT - Truy Vấn Dữ Liệu Chuyên Sâu
Mệnh đề quan trọng nhất của SQL, dùng để trích xuất dữ liệu theo các tiêu chí phức tạp.

3.1 Cấu trúc tổng quát của lệnh SELECT phức tạp
SQL
SELECT [DISTINCT] danh_sach_cot_hoac_ham_gop
FROM bang_chinh
[LOẠI_JOIN] bang_phu ON dieu_kien_ket_noi
WHERE dieu_kien_loc_dong_don
GROUP BY danh_sach_cot_phan_nhom
HAVING dieu_kien_loc_nhom_sau_gop
ORDER BY cot_sap_xep [ASC/DESC]
LIMIT so_luong_dong_lay; -- (Hoặc TOP trong SQL Server, ROWNUM trong Oracle)
3.2 Bản chất các phép JOIN (Kết nối các bảng)
INNER JOIN: Trả về các dòng khi có dữ liệu trùng khớp xuất hiện ở cả hai bảng.

SQL
SELECT SV.HoTen, L.TenLop
FROM SinhVien SV
INNER JOIN LopHoc L ON SV.MaLop = L.MaLop;
LEFT (OUTER) JOIN: Giữ lại toàn bộ các dòng của bảng bên trái (FROM), phối hợp với dòng khớp của bảng bên phải (JOIN). Nếu bảng phải không có dữ liệu tương ứng, các ô sẽ hiển thị NULL.

SQL
SELECT SV.HoTen, DangKy.MaMonHoc
FROM SinhVien SV
LEFT JOIN DangKy ON SV.MaSV = DangKy.MaSV; -- Lấy tất cả sinh viên, kể cả những bạn chưa đăng ký môn nào.
RIGHT (OUTER) JOIN: Ngược lại với LEFT JOIN, giữ lại toàn bộ các dòng của bảng bên phải.

FULL OUTER JOIN: Giữ lại tất cả các hàng của cả hai bảng, điền NULL vào các phần không khớp nhau.

3.3 Toán tử lọc dữ liệu nâng cao (Sử dụng trong WHERE / HAVING)
LIKE: Tìm kiếm theo mẫu chuỗi (Ký tự % đại diện cho chuỗi bất kỳ, \_ đại diện cho 1 ký tự).

Ví dụ: WHERE HoTen LIKE 'Nguyễn%' (Tìm người họ Nguyễn).

IN (tập_hợp): Kiểm tra giá trị có nằm trong một danh sách hoặc một kết quả của câu lệnh con (Subquery) hay không.

Ví dụ: WHERE MaLop IN ('K69_IT1', 'K69_IT2').

BETWEEN gia_tri_1 AND gia_tri_2: Lọc giá trị nằm trong khoảng (tính cả 2 đầu mút).

IS NULL / IS NOT NULL: Kiểm tra xem ô dữ liệu có phải là giá trị rỗng hoặc không rỗng hay không (Tuyệt đối không dùng toán tử = NULL).

3.4 Phân biệt WHERE và HAVING (Điểm cốt lõi trong các bài thi)
WHERE: Bộ lọc chạy ở cấp độ từng dòng đơn lẻ. Nó lọc dữ liệu trước khi gom nhóm dữ liệu bằng GROUP BY. Do đó, WHERE không được phép chứa các hàm gộp (Aggregate Functions).

HAVING: Bộ lọc chạy ở cấp độ nhóm dữ liệu. Nó lọc các nhóm dữ liệu sau khi dữ liệu đã được gom cụm bởi GROUP BY. Do đó, HAVING thường xuyên chứa các hàm gộp.

Ví dụ minh họa:

SQL
SELECT MaLop, COUNT(MaSV) AS Siso, AVG(DiemTB) AS DiemTrungBinhLop
FROM SinhVien
WHERE DiemTB >= 5.0 -- Bước 1: Chỉ lấy những sinh viên có điểm từ 5 trở lên
GROUP BY MaLop -- Bước 2: Gom nhóm theo từng lớp
HAVING COUNT(MaSV) >= 10; -- Bước 3: Chỉ giữ lại các lớp có từ 10 sinh viên trở lên thỏa mãn điều kiện trên 4. Các Hàm Gộp Và Xử Lý Dữ Liệu Phổ Biến (Aggregate & Built-in Functions)
4.1 Hàm gộp toán học (Luôn đi kèm GROUP BY khi chọn thêm cột thường)
COUNT(ten_cot): Đếm số lượng giá trị không null trong cột. COUNT(\*) dùng để đếm tổng số hàng.

SUM(ten_cot): Tính tổng giá trị số trong cột.

AVG(ten_cot): Tính giá trị trung bình của cột số.

MAX(ten_cot) / MIN(ten_cot): Tìm giá trị lớn nhất / nhỏ nhất trong cột (áp dụng được cả cho kiểu chuỗi và ngày tháng).

4.2 Các hàm xử lý Chuỗi và Thời gian thông dụng
Xử lý chuỗi:

CONCAT(chuoi_1, chuoi_2): Nối các chuỗi ký tự lại với nhau.

UPPER(chuoi) / LOWER(chuoi): Chuyển chữ hoa / chữ thường.

SUBSTRING(chuoi, vi_tri_bat_dau, do_dai): Cắt chuỗi con.

Xử lý thời gian (Cú pháp có sự khác biệt nhỏ tùy DBMS):

YEAR(ngay), MONTH(ngay), DAY(ngay): Trích xuất năm, tháng, ngày từ dữ liệu Date.

GETDATE() (SQL Server) / NOW() (MySQL) / CURRENT_DATE (PostgreSQL): Lấy thời gian hiện tại của hệ thống.
