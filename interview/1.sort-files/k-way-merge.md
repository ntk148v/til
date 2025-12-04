**K-way merge** (trộn K dãy) là một kỹ thuật trong khoa học máy tính dùng để hợp nhất **K danh sách hoặc K luồng dữ liệu đã được sắp xếp** thành một danh sách duy nhất cũng được sắp xếp. Đây là một bước quan trọng trong các thuật toán xử lý dữ liệu lớn như **external sorting**, **merge sort đa đường**, hay khi trộn nhiều file log đã sắp xếp.

Dưới đây là phần giải thích đầy đủ và có hệ thống:

---

## 1. Vấn đề đặt ra

Bạn có **K danh sách đã được sắp xếp theo thứ tự tăng dần**, ví dụ:

- L1: 1, 9, 17
- L2: 2, 3, 20
- L3: 4, 8, 15
- … đến LK

Yêu cầu: trộn K danh sách này thành một danh sách duy nhất vẫn theo thứ tự tăng dần.

Nếu trộn hai danh sách (2-way merge) thì dễ. Nhưng khi số danh sách tăng lên K, hiệu quả trở thành vấn đề.

---

## 2. Ý tưởng chính

Để tìm phần tử tiếp theo nhỏ nhất, ta chỉ cần nhìn **phần tử đầu tiên** của mỗi danh sách (vì từng danh sách đã được sắp xếp).

Tuy nhiên, nếu K lớn, mỗi lần tìm phần tử nhỏ nhất bằng cách quét tất cả K phần tử đầu là O(K), và tổng thời gian sẽ là O(N\*K) — rất chậm.

---

## 3. Tối ưu hóa bằng Min-Heap (bảo đảm hiệu suất tốt)

Giải pháp chuẩn cho K-way merge là sử dụng **min-heap** (priority queue):

1. Đưa phần tử đầu của mỗi danh sách vào một min-heap.
2. Lặp lại cho đến khi heap rỗng:
   - Lấy phần tử nhỏ nhất từ heap (O(log K)).
   - Đẩy phần tử tiếp theo của danh sách mà phần tử đó thuộc về vào heap (nếu còn).

### Độ phức tạp:

- Có tổng cộng N phần tử.
- Mỗi phần tử được push và pop một lần.
- Chi phí mỗi thao tác là log K.

=> **Tổng thời gian = O(N log K)**
=> Đây là mức tối ưu trong thực tế.

---

## 4. Ứng dụng thực tế

- **External Merge Sort** (sắp xếp dữ liệu lớn hơn bộ nhớ): chia file thành nhiều “run” đã sắp xếp rồi dùng K-way merge để hợp nhất.
- Hệ thống log phân tán: hợp nhất log từ nhiều máy đã sắp xếp theo timestamp.
- Các thuật toán streaming, database engines, hệ thống tìm kiếm (search engines).

---

## 5. Minh họa nhỏ

Giả sử K = 3:

Heap ban đầu: [1 (L1), 2 (L2), 4 (L3)]
Lấy ra 1 → thêm phần tử tiếp theo của L1 (9)
Heap: [2, 4, 9]
Lấy ra 2 → thêm 3
Heap: [3, 4, 9]
Lấy ra 3 → thêm 20
Heap: [4, 9, 20]
… tiếp tục cho đến khi trộn xong.

---

Nếu bạn muốn, tôi có thể cung cấp:

- Mã minh họa (Python, Java, C++, v.v.)
- So sánh với 2-way merge
- Phân tích chi tiết hơn về hiệu suất bộ nhớ hoặc external sorting.
