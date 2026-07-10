# Lộ trình học:

Bài 1: Tách dashboard_customer.html thành layout + partial (không dùng HTMX).
Bài 2: Thay onclick="showPage()" bằng HTMX.
Bài 3: Học get_template_names().
Bài 4: Học get_context_data().
Bài 5: Học get_queryset().
Bài 6: CreateView + form_valid().
Bài 7: UpdateView + form_valid().
Bài 8: DeleteView.
Bài 9: Search, filter, pagination bằng HTMX.

## 2026-07-10

- DashboardPageConfig chỉ nên chứa Configuration.
- current_page là State.
- active không nên lưu trong Config.
- View truyền current_page vào context.
- Config có thể có get_context() để giảm coupling.

## "Thầy, mình tiếp tục GTBooks. Mình đã học đến DashboardPageConfig."

## Chỉ mở rộng khi em gõ: "Giải thích sâu".

Nếu em muốn học cực tiết kiệm token

Em chỉ cần dùng các lệnh sau:

"Gọn." → Trả lời ≤ 5 câu.
"Hint." → Chỉ gợi ý, không đáp án.
"Đáp án." → Chỉ đưa đáp án.
"Giải thích sâu." → Phân tích kỹ.
"Tiếp." → Sang bài mới.

# Buổi chiều

- Template là dữ liệu(property) thì:
  - config.template không có ()
- Method (behavior) thì phải có ()
  - config.get_template()
  - config.get_context(request)
  - config.can_access(user)
- get_context() phải luông trả về một dict.

1.  Tái cấu trúc template:
    class DashboarCustomerBaseView: # code
    def get_context_date(self, \*\*kwargs):
    #...code
    context["customer_pages"]=CUSTOMER_PAGES.values()
    context["current_page"]=self.page
    return context
    Mục đích: để tạo slidebar tự động và active khi chọn
