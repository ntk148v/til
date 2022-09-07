# Chaos Engineering (VN)

Source:

- <https://principlesofchaos.org/>
- <https://en.wikipedia.org/wiki/Chaos_engineering>
- <https://devops.com/what-chaos-engineering-is-and-isnt/>
- <https://www.gremlin.com/community/tutorials/chaos-engineering-the-history-principles-and-practice/>

## 1. Giới thiệu về Chaos Engineering

Với sự phát triển của microservices và điện toán đám mây, hệ thống trở nên ngày càng phức tạp. Ô tô đương nhiên có nhiều loại hỏng hóc hơn xe đạp, và chi phí sửa chữa cũng cao hơn nhiều. Hệ thống cũng vậy, số lượng các thành phần càng nhiều, khả năng lỗi càng cao.

Một khi xảy ra lỗi, dù chỉ là một thành phần nhỏ, cũng ảnh hưởng đến hoạt động của toàn bộ hệ thống, gây ra downtime. Downtime làm giảm trải nghiệm người dùng, gây thiệt hại lớn cho công ty và tổ chức. Theo thống kê của [IHS Markit năm 2016](http://news.ihsmarkit.com/press-release/technology/businesses-losing-700-billion-year-it-downtime-says-ihs), thiệt hại do downtime của 400 công ty và tổ chức rơi vào khoảng 700 tỉ đô la mỗi năm.

Mối tương quan giữa hệ thống và thiệt hại biểu diễn như sau:

```
Công ty, tổ chức lớn -> Hệ thống lớn, phức tạp -> Thiệt hại lớn (nếu có downtime)
```

Do vậy, các công ty cần một giải pháp để giải quyết vấn đề này: Thay vì chờ cho sự cố xảy ra và xử lý, chúng ta chủ động thử nghiệm nhằm xác định lỗi trước khi xảy ra sự cố, Chaos Engineering.

Netflix là công ty tiên phong trong Chaos Engineering. Năm 2009, Netflix bắt đầu [chuyển dịch hệ thống lên môi trường điện toán đám mây Amazon Web Service](https://netflixtechblog.com/four-reasons-we-choose-amazons-cloud-as-our-computing-platform-4aceb692afec) nhằm tăng khả năng đáp ứng của hệ thống. Tuy nhiên, không có điều gì là hoàn hảo, chuyển dịch lại không đem lại hiệu quả mong muốn. Nếu như có một điểm của môi trường đám mây có vấn đề, trải nghiệm của người dùng sẽ bị ảnh hưởng. Do vậy, công ty giải quyết vấn đề này bằng cách phát triển [Chao Monkeys](https://netflix.github.io/chaosmonkey/) (2010).

Chaos Monkey đơn giản là tắt máy ảo, dịch vụ,... trên môi trường production một cách ngẫu nhiên (đương nhiên là có kế hoạch) để đảm bảo dịch vụ vẫn hoạt động tốt trong trường hợp có lỗi, sự cố.

*Chaos Engineering (Kỹ thuật hỗn loạn) là một phương pháp thử nghiệm hệ thống phân tán bằng cách định nghĩa, đưa ra và mô phỏng các tình huống lỗi vào hệ thống một cách có chủ đích. Thay vì chờ đợi lỗi xảy ra, các kỹ sư có thể thực hiện các bước có chủ đích để gây ra (hoặc mô phỏng) lỗi trong một môi trường được kiểm soát. Nói cách khác, "break things on purpose" (cố ý phá hỏng) nhằm xây dựng được một hệ thống đáng tin cậy hơn.*

## 2. Các nguyên tắc của Chaos Engineering

Chaos Engineering liên quan đến việc chạy các thử nghiệm có kế hoạch, kiểm tra cách thức hệ thống xử lý lỗi, từ đó tìm ra điểm yếu của hệ thống. Để thực hiện chaos, cần tuân theo các nguyên tắc.

### 2.1. Hình thành giả thuyết

Đây là bước khởi đầu, bạn phải xây dựng được giả thuyết về *trạng thái ổn định* của hệ thống. Xác định các thông số cần đo lường: thông lượng (throughput), tỉ lệ lỗi (error rates), độ trễ..., với giá trị như nào thì hệ thống được coi là ổn định.

### 2.2. Xác định các biến

Biến chaos phản ánh các sự kiến thực tế. Mọi sự kiện làm ảnh hưởng đến trạng thái ổn định của hệ thống đều có thể sử dụng làm biến chaos.

### 2.3. Chạy thử nghiệm trên production

Bạn phải thực hiện Chaos Engineering trên môi trường production. Không phải staging, testing mà phải là production!

### 2.4. Tự động hóa quá trình thử nghiệm

Chạy thử nghiệm theo cách thủ công tốn rất nhiều công sức. Bạn cần tự động hóa được quá trình này để điều phối cũng như phân tích sau này.

### 2.5. Tối thiểu hóa phạm vi ảnh hưởng

Thử nghiệm trên môi trường production có khả năng ảnh hưởng đến trải nghiệm khách hàng. Cho dù công ty chấp nhận rủi ro (nhỏ) khi thực hiện Chaos Engineering, bạn vẫn cần đẩm bảo phạm vi và mức độ ảnh hưởng được giảm thiểu tối đa.
