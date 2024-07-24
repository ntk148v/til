# SLAs, SLOs, SLIs

Source:

- <https://newsletter.grokking.org/p/178-do-l-ng-site-reliability-v-i-sli-slo-va-sla-672711>
- <https://www.pagerduty.com/resources/learn/what-is-slo-sla-sli/>

Trọng tâm chính của Site reliability engineering (SRE) là xây dựng và chạy một ứng dụng đáng tin cậy mà không ảnh hưởng đến tốc độ delivery sản phẩm - hai điều hoàn toàn trái ngược nhau (tức là “Tạo ra phần mềm tốt hơn, nhanh hơn”).

Các kỹ sư SRE đo lường mọi thứ, đồng thời xác định và đồng thuận dựa trên các chỉ số có thể đo lường, để đảm bảo công việc hướng tới một mục tiêu có thể đo lường được. Ví dụ, nói rằng trang web đang chạy chậm là một tuyên bố mơ hồ vì nó không có ý nghĩa gì về mặt kỹ thuật. Nhưng nói rằng 95% lượng phản hồi có thời gian vượt quá SLO 10%, thì sẽ mang lại nhiều giá trị hơn. SRE cũng đo lường các công việc lặp đi lặp lại theo thời gian và tìm cách tự động hóa chúng.

Có ba tham số độ tin cậy chính mà SRE xử lý: Definition of availability (SLO), Indicators of Availability (SLI), và Consequences of Unavailability (SLA)

**Service Level Indicators (SLI)** là các thước đo định lượng được xác định cẩn thận về một số khía cạnh của mức độ dịch vụ được cung cấp. Một số ví dụ phổ biến có thể là độ trễ yêu cầu, tỷ lệ lỗi, thông lượng dữ liệu, ... SLI dành riêng cho user journeys và chúng khác nhau giữa các ứng dụng. User journey là một chuỗi các hoạt động được người dùng thực hiện để đạt được một mục đích cụ thể. Ví dụ: user journey để thực hiện chuyển khoản ngân hàng có thể là thêm người nhận thanh toán và thực hiện chuyển tiền.

**Service Level Objectives (SLO)** chỉ định mức mục tiêu cho độ tin cậy của dịch vụ của bạn. SRE team sẽ xác định phần trăm SLI bạn nên đáp ứng để coi trang web của bạn là đáng tin cậy. SLO được tạo bằng cách kết hợp một hoặc nhiều SLI. Ví dụ: nếu bạn có SLI yêu cầu độ trễ dưới 500 ms trong 15 phút qua với phân vị 95%, SLO sẽ cần SLI được đáp ứng 99% thời gian đối với SLO 99%.

**Service Level Agreements (SLAs)** là một hợp đồng rõ ràng hoặc được ngầm hiểu đối với người dùng dịch vụ bao gồm các hậu quả của việc đáp ứng (hoặc thiếu) SLO được nêu ra. SLA là một thỏa thuận mang tính chính thức với khách hàng nêu rõ điều gì sẽ xảy ra nếu tổ chức không đáp ứng SLA. Chúng có thể vừa rõ ràng (explicit), vừa ẩn ý (implicit). Explicit SLA là một SLA có hậu quả xác định (chủ yếu là về tín dụng dịch vụ) do không đáp ứng độ tin cậy đã đặt. Implicit SLA ngầm được đo lường về mức độ mất uy tín đối với doanh nghiệp và khách hàng.

$$ \Large Error\ rate = {(1 - {Good\ events \over Total\ events})} \* 100\% $$

$$ \Large SLI = {Good\ events \over Total\ events} \* 100\% $$

$$ \Large SLI = 100\% - Error\ rate $$

$$ \Large SLO = {(SLI <= Target)}\ or\ {(Lower\ bound <= SLI <= Upper\ bound)}$$

$$ \Large Error\ budget = 100\% - SLO $$

$$ \Large Burn\ rate = {Error\ rate \over Error\ budget} $$

$$ \Large {0 < {Burn\ rate} <= {100\% \over Error\ budget}} $$
