# Tìm hiểu về OpenStack Kolla

## Vấn đề của OpenStack

- OpenStack trong lý thuyết: Các service tách biệt, kiến trúc rất đơn giản.

![The Beautify of OpenStack](https://allthingsopendotcom.files.wordpress.com/2014/10/screen-shot-2014-10-22-at-8-39-48-am.png)

- OpenStack trong thực tế: Không có sự riêng biệt rõ ràng giữa các service, chúng liên kết chặt chẽ với nhau, khiến cho việc triển khai chu kỳ vòng đời của OpenStack trở nên hết sức phức tạp.

![The Reality of OpenStack](https://allthingsopendotcom.files.wordpress.com/2014/10/screen-shot-2014-10-22-at-8-42-30-am.png)

- Những thành phần riêng biệt của OpenStack cùng chia sẻ những thư viện common với những phiên bản khác nhau.

- Khả năng nâng cấp phiên bản của OpenStack.

- Những vấn đề khi test và dev: "Cái này chạy trên môi trường devstack của tôi", "Cái kia hoạt động bình thường trong môi trường test"...

- Những khác biệt có thể xảy ra trong việc triển khai bởi nhiều lí do ví dụ như cài đặt các package ở những thời điểm khác nhau.

- Nhiều vấn đề bắt đầu nảy sinh:
  - Làm thế nào để tôi có thể nhiều node hoặc cả hệ thống mới vào cluster của mình.

  - Nếu tôi chạy `apt-get update` hoặc `yum update` tại 1 node, chuyện gì sẽ xảy ra? Trạng thái của hệ thống OpenStack.

  - Làm thế nào đồng bộ những config đến toàn bộ môi trường OpenStack?

  - Làm thế nào để tôi thực hiện upgrade chỉ 1 phần/1 service của OpenStack để sửa lỗi?

  - Tôi muốn test việc sửa lỗi của tôi một cách riêng biệt mà không ảnh hưởng đến toàn bộ hệ thống.

  - Làm thế nào để tôi quay lại trạng thái trước khi sửa lỗi nếu việc sửa lỗi không thành công, sinh ra nhiều vấn đề khác?

  - Làm thế nào để update phiên bản OpenStack từ A lên B (Kilo lên Mitaka chăng hạn) với downtime = 0?

  - Và còn rất nhiều vấn đề khác...

--> **Những câu hỏi trên bắt đầu có câu trả lời khi triển khai OpenStack trên Cơ sở hạ tầng không thay đổi.(immutable infrastructure).**

--> **Dockerizing OpenStack.**

## Giới thiệu chung về Kolla

Kolla cung cấp Docker container và Ansible playbooks. Sứ mệnh của Kolla là cung cấp container và công cụ triển khai nền tảng đám mây OpenStack.

Kolla cho phép tùy biến tùy biến tối đa. Điều này cho phép operator ít kinh nghiệm có thể triển khai OpenStack một cách nhanh chóng cũng như những người giàu kinh nghiệm hơn có thể tùy chỉnh cấu hình nhằm phù hợp với từng yêu cầu đặt ra.

## Kiến trúc Kolla

## Tài liệu tham khảo

1. [Kolla's Documentation](http://docs.openstack.org/developer/kolla/)

2. [IaaS Part 2 - Openstack Kolla All-In-One](http://mntdevops.com/2016/08/08/iaas-2/)

3. [OpenStack Contained Slide](http://events.linuxfoundation.org/sites/events/files/slides/CloudOpen2015.pdf)
