# Tìm hiểu về Zabbix

## Giới thiệu

Zabbix là giải pháp mã nguồn mở cho việc giám sát tài nguyên phân tán.

Phần mềm zabbix có thể theo dõi các thông số của mạng và tình trạng của server. Zabbix sử dụng các phương pháp cảnh báo linh hoạt, cho phép bạn cấu hình cảnh báo dựa trên email cho hầu hết các sự kiện xảy ra, nắm bắt nhanh các sự cố xảy ra của server. Ngoài ra, zabbix còn hỗ trợ chức năng báo cáo, tổng hợp và dự đoán dữ liệu tốt dựa trên những dữ liệu có sẵn đã được lưu trữ. Do đó, zabbix có khả năng lập kế hoạch cho khả năng đáp ứng của server.

## Kiến trúc cơ bản

## Khái niệm và thành phần cơ bản

1. Zabbix Server.

   - Là thành phần trung tâm của Zabbix.
   - Kiểm tra dịch vụ, giám sát tài nguyên thông qua các báo cáo được gửi về từ Agent.
   - Lưu trữ tất cả cấu hình và số liệu thống kê trong Database.

2. Zabbix Proxy.

   - Tùy chọn.
   - Thu thập dữ liệu, lưu trong bộ nhớ đệm và chuyển đến Zabbix Server.
   - Giám sát tập trung các địa điểm từ xa, các chi nhánh công ty.
   - Cân bằng tải cho Zabbix Server.

3. Zabbix Agent.

   - Cài đặt trên các host được giám sát.
   - Định kỳ gửi báo cáo, thông tin tài nguyên được giám sát về Server.

4. Web Interface-frontend.

   - Giúp việc thao tác trở nên dễ dàng hơn.
   - Có thể không chạy trên cùng 1 host chạy Server.(tuy nhiên, nếu SQLite được sử dụng, việc cài đặt trên cùng 1 host là bắt buộc).

5. Zabbix Database.

   - Mọi thông tin cấu hình được lưu trữ database, cả Server và Web interface đều tương tác cùng. Ví dụ, khi tạo item mới sử dụng web frontend(/ API), item được thêm vào item table trong database. Sau đó, Zabbix Server sẽ query items table để lấy danh sách các item hiện active - để lưu cache tại Server. Do vậy, thường mất khoảng 2' để những thay đổi được hiện thị ở Latest data section.
   - MySql, PostGreSql, Sqlite.

6. Active Check và Passive Check.

   - Zabbix Server thu thập thông tin từ Agent thông qua các item tương ứng.
   - Zabbix Passive Check -Pull.
     - Service checks: HTTP, SSH, IMAP, NTP, etc.
     - Script thực thi sử dụng SSH và Telnet.
     - Zabbix Server yêu cầu thông tin đến Agent trong các khoảng thời gian được cấu hình (interval time).
     - Agent lấy các thông tin đó, sau đó gửi trả về Server.
     - Server khởi tạo kết nối, Agent ở chế độ lắng nghe kết nối từ Server
   - Zabbix Active Check - Push.
     - Zabbix Trapper and SNMP Traps.
     - Agent chủ động yêu cầu thông tin về item cần báo cáo. (Thường được sử dụng khi Zabbix Server không thể kết nối trực tiếp đến Agent, có thể do firewall...)
     - Server chỉ định sẵn, gửi trả danh sách cho Agent.
     - Sau khi lấy được danh sách, Agent xử lý sau đó gửi trả tuần tự thông tin về Server.
     - Server không khởi tạo kết nối, mà chỉ trả lời request item list và nhận thông tin trả về.

![Zabbix Passive](https://camo.githubusercontent.com/bd41c14ab920462a11c818ecc5a62c3422d6d939/687474703a2f2f692e696d6775722e636f6d2f516130337948522e706e67)

![Zabbix Active](https://camo.githubusercontent.com/e3b6e63cd8d40a5d198b1354018a18f241269b18/687474703a2f2f692e696d6775722e636f6d2f585570626a39532e706e67)

![Active vs Passive](http://image.slidesharecdn.com/fisl2015workshoponproblemdetection-150710104738-lva1-app6892/95/zabbix-smart-problem-detection-fisl-2015-workshop-8-638.jpg?cb=1436526745)

7. Item.

   - Thành phần thu thập dữ liệu từ 1 host dựa trên item key, ví dụ _system.cpu.load_ sẽ thu thập dữ liệu của processor load.
   - Chi tiết xem tại [đây](https://www.zabbix.com/documentation/3.2/manual/config/items)

8. Trigger.

   - Detect problems in data flow! --> Trigger is problem definition
   - Biểu thức logic để "đánh giá" dữ liệu thu thập được bởi item, từ đó "đánh giá" trạng thái hiện tại của host.
   - Trigger Expression cho phép định nghĩa threshold - ngưỡng mà trạng thái của dữ liệu là chấp nhận được - OK. Ngược lại, là Problem.(Trigger Status)
   - Trigger status được tính lại mỗi lần Zabbix Server nhận được giá trị mới liên quan đến Expression.
   - Trigger dependencies: nhiều khi sự khả dụng của host A tồn tại vào host B. Ví dụ, 1 server nằm sau 1 router sẽ không thể truy cập được nếu như router chết.
   - Trigger severity - mức độ nghiêm trọng: Not classified, Information, Warning, Average, High, Disater.
   - Predictive trigger functions: dựa vào lịch sử dữ liệu để dự đoán.[Tài liệu](http://zabbix.org/mw/images/1/18/Prediction_docs.pdf)
     - Cần biết: làm thế nào để xác định được trạng thái lỗi và khoảng thời gian cần để thực hiện việc detect.
     - Có 2 cách để kích hoạt trigger:
       - forecast (sec|#num,<time_shift>,time,<fit>,<mode>): dự đoán giá trị item sau khoảng thời gian time dựa trên dữ liệu của khoảng thời gian sec hoặc #num mới nhất trước đó. Ví dụ: forecast(1h,,30m) → dự đoán giá trị item sau 30' dựa trên dữ liệu của 1h. Nếu giá trị thật sự khác giá trị dự đoán --> Problem.
       - timeleft (sec|#num,<time_shift>,threshold,<fit>): tính toán thời gian cần thiết để giá trị item đạt ngưỡng threshold dựa trên dữ liệu . Ví dụ: timeleft(1h,,100) → thời gian cần để item đạt giá trị 100 dựa trên dữ liệu 1h trước đó.
     - Lựa chọn interval và forecast horizon.
     - Dự đoán trong thực tế (và nó ảnh hưởng như thế nào đến interval).
     - Khi nào và tại sao nên sử dụng timeshift.
     - Xác định tham số fit.
     - Khi nào và tại sao sử dụng các mode khác ngoài "value" (min(), max(), avg(), delta())

9. Proxy.

   - Zabbix cung cấp 1 giải pháp hiệu quả để monitor hệ thống phân tán sử
     dụng Zabbix Proxy.

   - Zabbix proxy sẽ thay Zabbix Server, thu thập dữ liệu ở mạng internal,
     lưu lại ở Database (Zabbix Proxy có local db độc lập), sau đó gửi về
     Server.

   - Phương thức giúp giảm tải cho Zabbix Server, thay vì phải nhận request
     response từ M agent, server chỉ cần nhận từ N proxy.

   - Tính năng:

![zabbix-proxy-features](https://github.com/ntk148v/zabbix_research/blob/master/images/Screenshot%20from%202017-01-13%2010-11-18.png?raw=true)

    - Do proxy chỉ cân duy nhất 1 kết nối TCP đến Zabbix Server. --> dễ cấu
      hình firewall hơn.

    - Dữ liệu được lưu trữ local trước khi chuyển đến server nên sẽ không bị
      mất dữ liệu nếu có mất kết nối dữ liệu tạm thời với server.

    - Zabbix Proxy chỉ là _thành phần thu thập dữ liệu_ , không xử lý việc
      tính toán triggers, xử lý events hay gửi alert.

## Cài đặt

Sử dụng script install_zabbix_server.sh để cài đặt (Zabbix 3.2 - Centos 7)

# chmod +x install_zabbix.sh

# ./install_zabbix.sh

## Cấu hình gửi mail dùng gmail

    # chmod +x configure_smtp.sh
    # ./configure_smtp.sh

## Yêu cầu bài toán

1. Monitoring:

   - Host vật lý: Disk, RAM, CPU, Network
   - VM: CPU, Disk, RAM, Network.
   - Process Openstack.

2. Alerting:
   - Email.
   - SMS.

## Tài liệu tham khảo

1. [Zabbix Documentation](https://www.zabbix.com/documentation/3.2/)
