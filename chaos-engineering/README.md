# Chaos Engineering (VN)

Source:

- <https://principlesofchaos.org/>
- <https://en.wikipedia.org/wiki/Chaos_engineering>
- <https://devops.com/what-chaos-engineering-is-and-isnt/>
- <https://www.gremlin.com/community/tutorials/chaos-engineering-the-history-principles-and-practice/>
- <https://www.infoq.com/articles/chaos-engineering/>

- [Chaos Engineering (VN)](#chaos-engineering-vn)
  - [1. Dẫn dắt và giới thiệu về Chaos Engineering](#1-dẫn-dắt-và-giới-thiệu-về-chaos-engineering)
  - [2. Các nguyên tắc của Chaos Engineering](#2-các-nguyên-tắc-của-chaos-engineering)
    - [2.1. Hình thành giả thuyết quanh trạng thái ổn định](#21-hình-thành-giả-thuyết-quanh-trạng-thái-ổn-định)
    - [2.2. Xác định biến đầu vào từ sự kiện thực tế](#22-xác-định-biến-đầu-vào-từ-sự-kiện-thực-tế)
    - [2.3. Chạy thử nghiệm trên production](#23-chạy-thử-nghiệm-trên-production)
    - [2.4. Tự động hóa quá trình thử nghiệm](#24-tự-động-hóa-quá-trình-thử-nghiệm)
    - [2.5. Tối thiểu hóa phạm vi ảnh hưởng](#25-tối-thiểu-hóa-phạm-vi-ảnh-hưởng)

## 1. Dẫn dắt và giới thiệu về Chaos Engineering

Với sự phát triển của microservices và điện toán đám mây, hệ thống trở nên ngày càng phức tạp. Ô tô đương nhiên có nhiều loại hỏng hóc hơn xe đạp, và chi phí sửa chữa cũng cao hơn nhiều. Hệ thống cũng vậy, số lượng các thành phần càng nhiều, khả năng lỗi càng cao.

Một khi xảy ra lỗi, dù chỉ là một thành phần nhỏ, cũng ảnh hưởng đến hoạt động của toàn bộ hệ thống, gây ra downtime. Downtime làm giảm trải nghiệm người dùng, gây thiệt hại lớn cho công ty và tổ chức. Theo thống kê của [IHS Markit năm 2016](http://news.ihsmarkit.com/press-release/technology/businesses-losing-700-billion-year-it-downtime-says-ihs), thiệt hại do downtime của 400 công ty và tổ chức rơi vào khoảng 700 tỉ đô la mỗi năm.

Mối tương quan giữa hệ thống và thiệt hại biểu diễn như sau:

```
Công ty, tổ chức lớn -> Hệ thống lớn, phức tạp -> Thiệt hại lớn (nếu có downtime)
```

Do vậy, các công ty cần một giải pháp để giải quyết vấn đề này: Thay vì chờ cho sự cố xảy ra và xử lý, chúng ta chủ động thử nghiệm nhằm xác định lỗi trước khi xảy ra sự cố, Chaos Engineering.

Netflix là công ty tiên phong trong Chaos Engineering. Năm 2009, Netflix bắt đầu [chuyển dịch hệ thống lên môi trường điện toán đám mây Amazon Web Service](https://netflixtechblog.com/four-reasons-we-choose-amazons-cloud-as-our-computing-platform-4aceb692afec) nhằm tăng khả năng đáp ứng của hệ thống. Tuy nhiên, không có điều gì là hoàn hảo, chuyển dịch lại không đem lại hiệu quả mong muốn. Nếu như có một điểm của môi trường đám mây có vấn đề, trải nghiệm của người dùng sẽ bị ảnh hưởng. Do vậy, công ty giải quyết vấn đề này bằng cách phát triển [Chao Monkeys](https://netflix.github.io/chaosmonkey/) (2010).

Chaos Monkey đơn giản là tắt máy ảo, dịch vụ,... trên môi trường production một cách ngẫu nhiên (đương nhiên là có kế hoạch) để đảm bảo dịch vụ vẫn hoạt động tốt trong trường hợp có lỗi, sự cố.

_Chaos Engineering (Kỹ thuật hỗn loạn) là một phương pháp thử nghiệm hệ thống phân tán bằng cách định nghĩa, đưa ra và mô phỏng các tình huống lỗi vào hệ thống một cách có chủ đích. Thay vì chờ đợi lỗi xảy ra, các kỹ sư có thể thực hiện các bước có chủ đích để gây ra (hoặc mô phỏng) lỗi trong một môi trường được kiểm soát. Nói cách khác, "break things on purpose" (cố ý phá hỏng) nhằm xây dựng được một hệ thống đáng tin cậy hơn._

## 2. Các nguyên tắc của Chaos Engineering

Chaos Engineering liên quan đến việc chạy các thử nghiệm (experiment) có kế hoạch, kiểm tra cách thức hệ thống xử lý lỗi, từ đó tìm ra điểm yếu của hệ thống. Để thực hiện chaos, cần tuân theo các nguyên tắc.

Một thử nghiệm thường bao gồm 4 bước:

- Xác định _trạng thái ổn định_ (steady-state) của hệ thống bằng cách đo lường các thông số: thông lượng (throughput), tỉ lệ lỗi (error rates), độ trễ..., với giá trị như nào thì hệ thống được coi là ổn định, hoạt động bình thường.
- Đưa ra giả thuyết rằng cả hệ thống thử nghiệm (experimental group) và hệ thống ổn định (stable control group) luôn ở trạng thái ổn định.
- Đưa các sự kiện thực tế (được mô phỏng) vào hệ thống thử nghiệm: máy chủ gặp sự cố, phản hồi không đúng định dạng (malformed response), hoặc lưu lượng truy cập tăng đột biến.
- Kiểm tra, đánh giá lại giả thuyết bằng cách so sánh trạng thái ổn định của hệ thống ổn định và thử nghiệm. Càng ít khác biệt càng tốt.

Từ các bước trên, để ứng dụng Chaos Engineering cần tuân thủ theo các nguyên tắc sau:

### 2.1. Hình thành giả thuyết quanh trạng thái ổn định

Khi thiết kế các thử nghiệm, đầu tiên cần hình thành các giả thuyết xung quanh việc trạng thái ổn định (steady-state) của hệ thống thay đổi ra sao khi có sự cố. Netflix triển khai hệ thống tại nhiều region địa lý (Northern Virginia, Oregon, and Ireland). Nếu có một sự cố xảy ra tại một region, Netflix chuyển sang sử dụng một trong các region còn lại bằng cách điều hướng requests từ unhealthy region sang healthy region. Khi điều đó xảy ra, giả thuyết rằng việc điều hướng này có tác động nhỏ nhất.

Làm thể nào để đánh giá mức độ tác động? Bạn cần xác định, đo lường được các thông số. Các thông số này phải được đo tại biên của hệ thống, mang tính tổng quan và có thể dùng để đánh giá mức độ khả dụng của hệ thống: tỉ lệ lỗi, độ trễ khi xử lý của toàn hệ thống...

### 2.2. Xác định biến đầu vào từ sự kiện thực tế

Khi thiết kế thử nghiệm, hãy lấy biến từ tất cả các đầu vào có thể xảy ra trong thực tế. Bạn có thể tạo biến đầu vào bằng cách xem lại lịch sử các sự cố đã xảy ra. Sự kiện như Máy chủ gặp sự cố, cân bằng tải không hoạt động,... tất cả đều có thể được sử dụng làm biến đầu vào cho cuộc thử nghiệm, đảm bảo sự cố không tái diễn. Mở rộng ra, mọi sự kiện có khả năng phá hỏng trạng thái ổn định của hệ thống đều có thể là đầu vào cho quá trình thử nghiệm.

Bạn có thể tham khảo sự kiện đầu vào của Netflix áp dụng trong Chaos Engineering:

- Tắt máy ảo (một hoặc nhiều).
- Tăng độ trễ khi gửi request giữa các dịch vụ.
- Request giữa các dịch vụ không thành công.
- Lỗi dịch vụ nội bộ (internal service).
- Làm cho toàn bộ Amazon Region trở nên bất khả dụng.

### 2.3. Chạy thử nghiệm trên production

Bạn phải thực hiện Chaos Engineering trên môi trường production. Không phải staging, testing mà phải là production!

### 2.4. Tự động hóa quá trình thử nghiệm

Chạy thử nghiệm theo cách thủ công tốn rất nhiều công sức. Hệ thống luôn thay đổi, kéo theo thay đổi việc thử nghiệm. Bạn cần tự động hóa được quá trình này để điều phối cũng như phân tích sau này.

### 2.5. Tối thiểu hóa phạm vi ảnh hưởng

Thử nghiệm trên môi trường production có khả năng ảnh hưởng đến trải nghiệm khách hàng. Cho dù công ty chấp nhận rủi ro (nhỏ) khi thực hiện Chaos Engineering, bạn vẫn cần đẩm bảo phạm vi và mức độ ảnh hưởng được giảm thiểu tối đa.
