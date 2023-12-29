# Conway's Game of Life

Source:

- <https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>
- <https://notes.huy.rocks/posts/game-of-life.html>

Game of Life hay còn gọi là Life là bài toán thuộc lĩnh vực cellular automation được đưa ra bởi John Horton Conway vào năm 1970. Đây là một trò chơi không có người chơi. Sự tiến hóa của trò chơi được xác định bởi trạng thái ban đầu, và không cần thêm đầu vào nữa. Người chơi khởi tạo và quan sát sự tiến hóa.

## Luật chơi

Trò chơi gồm một ô lưới n×m không giới hạn, mỗi ô (cell) có hai trạng thái alive hoặc dead.

Ở mỗi một thời điểm, toàn bộ ô lưới này được gọi là một thế hệ (generation), và máy tính sẽ tự động biến đổi từ thế hệ này sang thế hệ tiếp theo bằng cách thay đổi các cell trên lưới, theo quy tắc:

- Ô sống nào có đúng 2 hoặc 3 ô sống lân cận thì sẽ tiếp tục sống đến thế hệ tiếp theo. Ngược lại thì sẽ thành ô chết.
- Ô chết nào có đúng 3 ô sống lân cận thì sẽ trở thành ô sống ở thế hệ tiếp theo.

![](https://notes.huy.rocks/posts/img/game-of-life-visual.png)
