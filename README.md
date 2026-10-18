# IMP-Jp-Trans

Skill riêng cho báo cáo tiếng Nhật của IMP/EE: **`hai-jp-report`**.

Mục tiêu: dịch Việt/Anh → Nhật, biên tập bản Nhật và kiểm tra lại với bản nguồn; giữ nguyên kết luận, điều kiện, mức độ chắc chắn, số liệu và nguồn trích dẫn.

## Skill

Mã nguồn nằm tại [`skills/hai-jp-report/`](./skills/hai-jp-report/). Điểm vào là [`SKILL.md`](./skills/hai-jp-report/SKILL.md).

Sau khi được cài và nhận diện trong môi trường Codex phù hợp, cách gọi dự kiến là:

```text
$hai-jp-report <báo cáo nguồn>
$hai-jp-report polish <bản Nhật> <bản nguồn nếu có>
$hai-jp-report review <bản nguồn> <bản Nhật>
```

Repo này lưu gói skill; việc ghi lên GitHub không cài hay kích hoạt skill trên máy người dùng. Chưa thực hiện cài đặt hoặc kiểm thử gọi skill trong máy của chủ repo. Cấu hình `agents/openai.yaml` đặt chế độ gọi tường minh, không tự kích hoạt theo nội dung chat.

## Cách hoạt động

1. Đọc đầy đủ và khóa nội dung bản nguồn.
2. Dịch trực tiếp sang Nhật; giữ ý nghĩa và cấu trúc đã chốt.
3. Biên tập bằng bộ `natural-japanese` đóng gói theo commit cố định.
4. Kiểm tra số liệu, link, mã nguồn trích dẫn và credit phát sinh; đối chiếu lại nghĩa với bản gốc. Dùng reviewer riêng khi môi trường hỗ trợ, không giả lập việc review độc lập.
5. Xuất báo cáo sạch; ghi rõ phần chưa kiểm hoặc lỗi còn tồn tại bên ngoài nội dung báo cáo.

Không thêm watermark, tên tác giả công cụ hoặc dòng `powered by` vào báo cáo chỉ vì đã dùng skill. Các nguồn nghiên cứu thực sự có trong báo cáo vẫn giữ nguyên. LICENSE và ghi nhận bộ gốc nằm trong mã nguồn.

## Kiểm thử

```bash
python3 -m unittest discover -s skills/hai-jp-report/tests -v
```

18 unit test của bộ kiểm tra văn bản đã chạy đạt trong môi trường build tách biệt. Đây không phải bằng chứng bản dịch tốt hơn GPT thường. Chưa chạy đánh giá mù chất lượng Việt/Anh → Nhật trên báo cáo IMP/EE thật hoặc kiểm thử cài đặt trên máy người dùng. Xem [`tests/README.md`](./skills/hai-jp-report/tests/README.md).

## Bộ nền và cập nhật

Bộ gốc vẫn được giữ tại [`skills/natural-japanese/`](./skills/natural-japanese/). Skill riêng có bản đóng gói tại `skills/hai-jp-report/vendor/natural-japanese/`, kèm giấy phép để có thể chuyển cả thư mục skill mà không phụ thuộc đường dẫn bên ngoài.

Nguồn và phiên bản cố định: [`UPSTREAM.lock.json`](./skills/hai-jp-report/UPSTREAM.lock.json). Không tự cập nhật bộ nền trong khi dịch. Một lần cập nhật cần được review, thay bản đóng gói và chạy lại kiểm thử; cập nhật bộ gốc không tự thay đổi bản đã pin.

### Offline integrity and preserved evaluation cases

`python3 dev/sync_hai_jp_vendor.py --check` verifies all copied dependency bytes, modes, paths, the per-file `vendor/natural-japanese/UPSTREAM.json` manifest and the bundle tree recorded in `UPSTREAM.lock.json`, using local pinned Git objects only. The check is read-only. Regeneration is explicit: `--sync --commit 03bc944a0c4a9f0b2a66eab065b30de5c529bf08`; it repairs the vendor bundle and updates its tree hash in the lock. Review that diff before committing. The dependency keeps its existing `SKILL.md` path; no `GUIDE.md` alias is needed.

The eight [synthetic evaluation files](./evals/hai-jp-report/) are preserved byte-for-byte from PR #1 commit `84f3288f0dccbd1b3fe7c53327dc14c3fa2febaa`. Their `RESULTS.md` records that earlier candidate's observations and limits, not a replay or translation-quality approval of the current package. The offline verifier has separate regression tests under `skills/hai-jp-report/tests/`; run them with `PYTHONDONTWRITEBYTECODE=1` so generated caches do not enter the pinned trees. Skill invocation, upstream morphology helpers and human translation review remain separate checks.

Giấy phép gốc: [MIT](./LICENSE). Chi tiết: [`THIRD_PARTY_NOTICES.md`](./skills/hai-jp-report/THIRD_PARTY_NOTICES.md). Tài liệu bộ gốc trước khi thêm wrapper còn trong [lịch sử repository](https://github.com/hailuongrp/IMP-Jp-Trans/blob/03bc944a0c4a9f0b2a66eab065b30de5c529bf08/README.md).

Định dạng skill và cách gọi Codex tham chiếu [tài liệu OpenAI](https://developers.openai.com/codex/skills). Không đưa báo cáo khách hàng, dữ liệu riêng hoặc credential vào repo công khai này khi chưa có yêu cầu rõ ràng.
