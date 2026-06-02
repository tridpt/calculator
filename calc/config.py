"""Toàn bộ dữ liệu/nội dung cấu hình cho phần troll.

Tách riêng để dễ chỉnh sửa câu chữ mà không đụng tới logic.
"""

PREMIUM_PLANS = [
    ("Gói Cơ Bản",       "29.000đ / phép tính",     "Bao gồm: 1 phép tính. Không hỗ trợ dấu bằng nâng cao."),
    ("Gói Tiêu Chuẩn",   "199.000đ / tháng",        "Mở khoá phép cộng. Phép trừ tính phí thêm."),
    ("Gói Nâng Cao",     "999.000đ / tháng",        "Mở khoá nhân chia. Tặng kèm 1 lỗi sai miễn phí."),
    ("Gói Doanh Nghiệp", "Liên hệ để biết giá",     "Có thể đắt hơn cả cái máy tính Casio thật."),
]

# Mỗi gói chỉ "mở khoá" một số phép tính nhất định -> mô tả gói có tác dụng thật.
# allowed: tập các toán tử được phép. blocked sẽ bị chặn và đòi nâng cấp.
PLAN_PERMISSIONS = {
    "Gói Cơ Bản":       {"allowed": set(),                "next": "Gói Tiêu Chuẩn"},
    "Gói Tiêu Chuẩn":   {"allowed": {"+"},                "next": "Gói Nâng Cao"},
    "Gói Nâng Cao":     {"allowed": {"+", "-", "*", "/"}, "next": "Gói Doanh Nghiệp"},
    "Gói Doanh Nghiệp": {"allowed": {"+", "-", "*", "/"}, "next": None},
}

OP_NAMES = {"+": "phép cộng", "-": "phép trừ", "*": "phép nhân", "/": "phép chia"}

AD_LINES = [
    "🎉 Chúc mừng! Bạn là người dùng thứ 1.000.000 của ứng dụng.",
    "💸 Vay tiền online lãi suất 0% (chỉ trong 3 giây đầu).",
    "🔥 Cô đơn? Tải ngay app hẹn hò với cái máy tính.",
    "📈 Đầu tư coin XYZ - x1000 lần (hoặc về 0).",
    "🧴 Thuốc mọc tóc cho lập trình viên - 100% có gàu.",
    "🍜 Mì tôm vị 'máy tính rang bơ' - ăn là tính nhanh hơn.",
    "🛏️ Nệm thông minh: ngủ quên vẫn trả phí đều đặn.",
    "🎓 Khoá học 'Bấm dấu = chuyên nghiệp' - học phí chỉ 49 triệu.",
    "🐱 Nuôi mèo ảo trong máy tính - mỗi phép tính cho mèo ăn 1 lần.",
    "🚀 Du lịch sao Hoả - đặt cọc bằng kết quả phép tính của bạn.",
    "💍 Cưới luôn cái máy tính đi, nó chung thuỷ hơn người yêu cũ.",
    "🧦 Mua 1 tặng 0 - ưu đãi có hạn (đã hết hạn từ năm ngoái).",
]

CAPTCHA_QUESTIONS = [
    ("Bạn có phải con người không?", ["Có", "Không", "Tôi là cái máy tính"]),
    ("2 + 2 = ?  (chứng minh bạn không phải robot)", ["3", "5", "Cá vàng"]),
    ("Chọn đáp án sai:", ["Trời xanh", "Nước ướt", "App này hữu ích"]),
    ("Hôm nay là thứ mấy?", ["Thứ 8", "Thứ Hư Vô", "Không biết, hỏi sếp"]),
    ("Con gì sủa gâu gâu?", ["Con mèo", "Con bò", "Cái máy tính"]),
    ("Chọn hình có chứa 'lòng tin của bạn':", ["Ô trống", "Ô cũng trống", "Ô trống nốt"]),
    ("Bạn đã đọc điều khoản chưa?", ["Rồi (nói dối)", "Chưa (thành thật)", "Điều khoản nào?"]),
    ("1 + 1 bằng mấy trong hệ nhị phân của trái tim?", ["10", "Tình yêu", "Đừng hỏi khó"]),
    ("Chọn thứ đắt nhất:", ["Vàng", "Kim cương", "App này"]),
]

LOADING_MESSAGES = [
    "Đang kết nối tới máy chủ tính toán...",
    "Đang xác thực thẻ tín dụng của bạn...",
    "Đang hỏi ý kiến của AI...",
    "AI đang suy nghĩ rất lung tung...",
    "Đang tính toán bằng bàn tính tre...",
    "Đang chờ ông bảo vệ bật lại router...",
    "Đang đánh thức nhân viên trực tổng đài...",
    "Đang quy đổi kết quả sang đơn vị 'đại khái'...",
    "Đang hối lộ con số để nó chịu hiện ra...",
    "Đang tải thêm RAM từ trên mạng về...",
    "Đang dịch kết quả từ tiếng máy sang tiếng người...",
    "Đang chờ phép tính nguội bớt...",
]

DISCOUNT_CODES = {
    # mã -> (giảm %, message)
    "FREE":   (0.01, "Áp dụng thành công! Giảm 0.01%."),
    "SALE":   (0.10, "Áp dụng thành công! Giảm 0.10%."),
    "BANK":   (None, "Mã chỉ áp dụng cho khách hàng VIP."),
    "VIP":    (None, "Mã đã hết lượt sử dụng (vừa nãy)."),
    "ADMIN":  (None, "Phát hiện gian lận. Giao dịch bị đánh dấu."),
}

# Các ô trên vòng quay may mắn - toàn ô "trượt", chỉ 1 ô hời nhưng kim không bao giờ dừng ở đó
WHEEL_SEGMENTS = [
    "Chúc may mắn lần sau",
    "Trượt rồi 😢",
    "Gần trúng!",
    "Hụt mất tiêu",
    "Thử lại nhé",
    "Sắp trúng tới nơi",
    "🎁 MIỄN PHÍ TRỌN ĐỜI",   # ô xịn - nhưng sẽ không bao giờ trúng
    "Quay lại từ đầu",
    "Trúng... cái nịt",
    "Ô này cố tình để trống",
    "Mất thêm 1 lượt",
    "Suýt nữa thì trúng (không)",
]

# Câu thần chú cho minigame gõ chữ
SPELL_PHRASES = [
    "toi khong phai robot",
    "may tinh nay tinh dung",
    "xin hay cho toi tinh toan",
    "9 cong 10 bang 21",
    "toi tu nguyen tra phi dich vu",
    "con so la ban cua toi",
    "lam on hien ket qua ra di",
    "toi se khong so sanh voi casio",
]

EXTRA_FEES = [
    ("Phí xử lý giao dịch",       "19.000đ"),
    ("Phí tiện ích nền tảng",     "25.000đ"),
    ("Phí duy trì máy chủ AI",    "49.000đ"),
    ("VAT",                       "10%"),
    ("VAT của VAT",               "10% của 10%"),
    ("Phí làm tròn lên",          "0.99đ"),
    ("Phí hiển thị bảng phí này", "9.000đ"),
]

SURVEY_QUESTIONS = [
    ("Bạn hài lòng với trải nghiệm thanh toán chứ?",
     ["Rất hài lòng", "Cực kỳ hài lòng", "Hài lòng đến phát khóc"]),
    ("Bạn sẽ giới thiệu app này cho kẻ thù chứ?",
     ["Chắc chắn rồi", "Đã giới thiệu sẵn", "Để dành troll sau"]),
    ("Mức giá có hợp lý không?",
     ["Quá rẻ", "Rẻ như cho", "Tôi muốn trả thêm"]),
    ("Bạn đánh giá thế nào về tốc độ tính toán?",
     ["Nhanh như rùa", "Chậm mà chắc (sai)", "Thời gian là khái niệm"]),
    ("Nếu app này là người, bạn sẽ?",
     ["Mời đi cà phê", "Chặn số ngay", "Cưới luôn"]),
    ("Cảm xúc của bạn lúc này?",
     ["Vui (gượng)", "Tức (thật)", "Đã chấp nhận số phận"]),
]

# Điều khoản dịch vụ vô lý - phải cuộn hết mới cho đồng ý
EULA_TEXT = """ĐIỀU KHOẢN SỬ DỤNG DỊCH VỤ MÁY TÍNH

Vui lòng đọc kỹ toàn bộ điều khoản trước khi tiếp tục.
Bạn phải cuộn xuống tận cuối để có thể đồng ý.

Điều 1. Bằng việc sử dụng dấu "=", bạn đồng ý trả phí cho mỗi
kết quả, kể cả kết quả sai.

Điều 2. Mọi kết quả do ứng dụng cung cấp chỉ mang tính tham khảo
và có thể đúng một cách tình cờ.

Điều 3. Bạn không được phép so sánh ứng dụng này với máy tính
Casio, máy tính Windows, hay bất kỳ thiết bị nào tính đúng.

Điều 4. Bạn đồng ý rằng số 7 là một con số nhạy cảm và có thể
bị từ chối mà không cần lý do.

Điều 5. Trong trường hợp kết quả đúng, đó là lỗi của hệ thống
và sẽ được khắc phục trong bản cập nhật tiếp theo.

Điều 6. Bạn đồng ý nhận quảng cáo vào bất kỳ thời điểm nào,
kể cả lúc 3 giờ sáng.

Điều 7. Ứng dụng có quyền hết hạn giấy phép bất cứ lúc nào nó
thấy buồn.

Điều 8. Bạn xác nhận đã đọc hết các điều khoản này, điều mà
chúng tôi biết chắc là không ai làm.

Điều 9. Nếu bạn đọc tới đây, xin chúc mừng, bạn vẫn chưa được
tính toán gì cả.

Điều 10. Mọi tranh chấp sẽ được giải quyết bằng oẳn tù tì.

--- HẾT ĐIỀU KHOẢN ---
Cảm ơn bạn đã giả vờ đọc."""

# Các lỗi vô lý khi "kiểm tra" số thẻ
CARD_REJECTIONS = [
    "Số thẻ không được chứa chữ số 7.",
    "Tổng các chữ số phải chia hết cho 13.",
    "Số thẻ trông giống số thật quá, nghi ngờ gian lận.",
    "Số thẻ phải có đúng 19 chữ số (ô chỉ cho nhập 16).",
    "Chữ số đầu tiên không được là số nguyên tố.",
    "Hệ thống không thích con số này lắm.",
    "Số thẻ phải đối xứng như gương. Của bạn thì không.",
    "Thẻ này phát hành ở vũ trụ khác, không hỗ trợ.",
    "Số thẻ vừa nhập trùng với số nhà của sếp. Cấm.",
    "Vui lòng nhập số thẻ bằng số La Mã.",
]

# Lý do từ chối khi nạn nhân cố thoát app
EXIT_EXCUSES = [
    "Bạn có chắc muốn thoát? Ưu đãi sẽ không còn nữa đâu.",
    "Khoan đã! Bạn vẫn chưa tính được phép nào mà.",
    "Hệ thống đang lưu... thói quen rời bỏ của bạn.",
    "Thật sự thoát? Cái máy tính sẽ buồn lắm đấy.",
    "Vui lòng xác nhận lần cuối: bạn nỡ bỏ đi sao?",
    "Đợi đã, vừa có ưu đãi mới dành riêng cho người sắp thoát!",
    "Thoát bây giờ thì phí dịch vụ vẫn tính nhé, biết chưa.",
    "Máy tính: 'Đừng đi mà... tui tính sai sửa lại được mà...'",
]

# Mật khẩu nào cũng bị chê - đăng nhập bất khả thi
PASSWORD_COMPLAINTS = [
    "Mật khẩu phải chứa ít nhất 1 chữ Hán.",
    "Mật khẩu không được giống 10.000 mật khẩu phổ biến (kể cả cái bạn vừa nghĩ).",
    "Mật khẩu phải chứa cảm xúc tích cực.",
    "Mật khẩu quá mạnh, làm máy chủ tự ti. Vui lòng yếu hơn.",
    "Tài khoản này có thể tồn tại hoặc không. Vui lòng thử lại.",
    "Mật khẩu phải chứa tên người yêu cũ (để bảo mật cảm xúc).",
    "Mật khẩu không được chứa nguyên âm, phụ âm, hoặc số.",
    "Mật khẩu phải dài hơn bài văn nghị luận lớp 9.",
    "Mật khẩu vừa nhập đã được người khác mơ thấy. Trùng rồi.",
]

# Các dòng hiển thị khi "cập nhật bắt buộc" lúc mở app
UPDATE_STEPS = [
    "Đang kiểm tra phiên bản...",
    "Đang tải bản cập nhật quan trọng (0%)...",
    "Đang tải bản cập nhật quan trọng (47%)...",
    "Đang tải bản cập nhật quan trọng (88%)...",
    "Đang cài đặt (99%)...",
]

# "Nội dung" quảng cáo video bắt xem hết mới được tính
VIDEO_AD_TITLES = [
    "Quảng cáo: Nước tăng lực Bò Mộng 🐂",
    "Quảng cáo: Khoá học làm giàu sau 1 đêm 💰",
    "Quảng cáo: App giao đồ ăn nhanh hơn ánh sáng 🛵",
    "Quảng cáo: Bột giặt trắng hơn cả sự thật 🧺",
    "Quảng cáo: Game mới - nạp là mạnh 🎮",
]

# Các nền tảng "phải chia sẻ" để mở khoá (bấm cái nào cũng không thật sự chia sẻ)
SHARE_PLATFORMS = [
    ("📘 Facebook",  "Đang mở Facebook... à mà thôi, chưa tích hợp."),
    ("📷 Instagram", "Story của bạn đẹp lắm, tiếc là chưa đăng được."),
    ("🎵 TikTok",    "Bạn chưa đủ nổi để chia sẻ lên TikTok."),
    ("🐦 X (Twitter)", "Đã hết lượt tweet miễn phí hôm nay."),
]

# Bảng màu dùng chung
COLORS = {
    "bg":        "#1e1e2e",
    "panel":     "#181825",
    "display":   "#11111b",
    "fg":        "#cdd6f4",
    "muted":     "#a6adc8",
    "dim":       "#6c7086",
    "accent":    "#74c7ec",
    "key":       "#313244",
    "key_op":    "#45475a",
    "ok":        "#a6e3a1",
    "warn":      "#f9e2af",
    "danger":    "#f38ba8",
    "blue":      "#89b4fa",
    "active":    "#585b70",
}
