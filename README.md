# IMP-Jp-Trans

**Bộ skill của Hải để hoàn thiện bản tiếng Nhật cho báo cáo IMP/EE.**

Gọi `$hai-jp-report` cùng báo cáo tiếng Việt, tiếng Anh hoặc bản Nhật cần sửa. Skill dịch và biên tập tiếng Nhật, sau đó đối chiếu lại với nguồn để giữ đúng kết luận, bằng chứng, điều kiện, số liệu và trích dẫn.

## Cài bản v1 cho Codex

```bash
npx skills add https://github.com/hailuongrp/IMP-Jp-Trans/tree/hai-jp-report-v1/skills/hai-jp-report --agent codex --global
```

Lệnh cài dùng [Skills CLI](https://github.com/vercel-labs/skills). Mở lại phiên làm việc nếu công cụ chưa làm mới danh sách skill. Đây là cài cho Codex; việc chỉ lưu repo trên GitHub không tự cài vào mọi tài khoản ChatGPT.

Gói đã chứa phần cần thiết của `natural-japanese`; không cần cài thêm skill đó. Hướng dẫn dùng được cả khi không có shell. Các công cụ lint tùy chọn dùng Python 3.10+ và [uv](https://docs.astral.sh/uv/); lần đầu chạy, uv có thể tải các thư viện được khai báo trong script.

## Cách gọi

```text
$hai-jp-report
Dịch toàn bộ báo cáo này sang JP.
```

```text
$hai-jp-report
Sửa bản JP này cho tự nhiên, đối chiếu với bản VI đính kèm.
Giữ nguyên kết luận, điều kiện và citation.
```

```text
$hai-jp-report review
Chỉ kiểm tra bản JP với bản gốc, chỉ ra lỗi và đề xuất sửa.
```

Nếu chỉ có bản Nhật, skill vẫn biên tập được và nói rõ rằng chưa đối chiếu bản gốc. Mặc định là văn phong báo cáo trung tính `である`; glossary, mẫu JP đã duyệt và yêu cầu cụ thể của người dùng được ưu tiên. Skill không tự đoán IMP/EE viết tắt của gì hoặc tự định nghĩa lại thang đánh giá.

Báo cáo đầu ra không được tự thêm tên tác giả/công cụ, logo, watermark, dòng “dịch bằng…” hoặc ghi chú kỹ thuật. Phần kiểm tra bao gồm nội dung, footer, comment, ghi chú slide và metadata khi có thể truy cập. Tên tác giả nguồn dẫn vốn có trong báo cáo vẫn được giữ. Giấy phép của phần mã sao chép chỉ nằm trong gói phần mềm.

## Skill có những gì?

| Thành phần | Vai trò |
|---|---|
| [SKILL.md](skills/hai-jp-report/SKILL.md) | Một lệnh gọi, quy trình dịch → biên tập → kiểm nghĩa. |
| [Quy tắc bảo toàn nội dung](skills/hai-jp-report/references/fidelity.md) | Giữ đúng mức chắc chắn, phạm vi, tác nhân, điều kiện, số liệu và nguồn. |
| [Văn phong JP](skills/hai-jp-report/references/jp-style.md) | Tiếng Nhật báo cáo rõ và tự nhiên, tránh câu dịch sát chữ. |
| [Thuật ngữ](skills/hai-jp-report/references/terminology.md) | Các phân biệt dễ dịch nhầm và [mẫu glossary](skills/hai-jp-report/assets/glossary-template.tsv). Chưa phải glossary RP đã duyệt. |
| [Checklist QA](skills/hai-jp-report/references/qa.md) | Đối chiếu nguồn với JP cuối; tách lỗi nghĩa khỏi gợi ý văn phong. |
| [natural-japanese đóng gói](skills/hai-jp-report/vendor/natural-japanese) | Hướng dẫn biên tập và các script lint từ phiên bản cố định, kèm license và nguồn gốc. |

Ví dụ cần giữ nguyên: **“Chưa đủ bằng chứng để đầu tư”** không được dịch thành **“Không nên đầu tư”**. **“Chỉ khi cả A và B”** không được đổi thành **“A hoặc B”**. **“Công ty tự báo cáo”** không được đổi thành **“Đã xác minh”**.

## Nguồn gốc và giấy phép

Phần workflow IMP/EE, quy tắc đối chiếu, hướng dẫn thuật ngữ và cấu hình `hai-jp-report` được xây dựng riêng cho dự án này. Phần biên tập tiếng Nhật sử dụng [natural-japanese của coji](https://github.com/coji/natural-japanese), theo giấy phép MIT.

Bản upstream được khóa tại commit `03bc944a0c4a9f0b2a66eab065b30de5c529bf08`. Bản quyền và MIT license được giữ nguyên trong [gói vendor](skills/hai-jp-report/vendor/natural-japanese/LICENSE). [UPSTREAM.json](skills/hai-jp-report/vendor/natural-japanese/UPSTREAM.json) ghi nguồn và checksum. File `SKILL.md` upstream được đổi tên thành `GUIDE.md` trong vendor để chỉ có một skill được phát hiện; nội dung sao chép giữ nguyên.

Việc repo hiển thị “forked from” do GitHub quản lý, độc lập với tên skill. Xem [hướng dẫn chính thức về tách fork](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/detaching-a-fork) trước khi thay đổi quan hệ repo.

## Bảo trì và kiểm tra

Giữ cây `skills/natural-japanese/` nguyên trạng theo pin. Không cập nhật vendor tự động lúc dịch báo cáo.

```bash
python3 dev/sync_hai_jp_vendor.py --check
```

Lệnh kiểm tra chạy offline và cần Git object của commit đã khóa; bản clone quá nông có thể cần lấy thêm lịch sử trước. Người dùng cài riêng skill không cần chạy công cụ bảo trì này.

Các ca thử tổng hợp và tiêu chí đối chiếu nằm tại [evals/hai-jp-report](evals/hai-jp-report). Kết quả thử không thay thế đánh giá trên báo cáo thực tế và không chứng minh skill chính xác tuyệt đối hoặc luôn tốt hơn GPT thông thường.

Các thay đổi mới của dự án nguồn vẫn có thể được lấy bằng Git kể cả khi repo đã tách quan hệ fork. Việc nâng bản cần xem diff, cập nhật cây nguồn và pin, tái tạo vendor bằng `--sync --commit`, rồi chạy lại các ca thử trước khi cập nhật skill đã cài. Bản fork và bản skill cài trên máy là hai bản riêng; đồng bộ repo không tự thay đổi gói đang dùng.
