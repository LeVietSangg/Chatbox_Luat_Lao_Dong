from scripts.rag_pipeline import safe_escape, safe_render_llm_answer


def test_safe_escape_xss_vectors():
    """Kiểm tra safe_escape vô hiệu hóa mọi chuỗi HTML / JavaScript độc hại."""
    payloads = [
        ("<script>alert('xss')</script>", "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"),
        ('<img src=x onerror="alert(1)">', '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;'),
        ('"><svg/onload=alert(document.cookie)>', '&quot;&gt;&lt;svg/onload=alert(document.cookie)&gt;'),
        ("<b>Nội dung in đậm</b>", "&lt;b&gt;Nội dung in đậm&lt;/b&gt;"),
        ('<a href="javascript:steal()">link</a>', '&lt;a href=&quot;javascript:steal()&quot;&gt;link&lt;/a&gt;'),
    ]
    for raw, expected in payloads:
        escaped = safe_escape(raw)
        assert escaped == expected
        assert "<" not in escaped
        assert ">" not in escaped


def test_safe_escape_none_or_empty():
    """Kiểm tra xử lý đầu vào rỗng hoặc None an toàn."""
    assert safe_escape(None) == ""
    assert safe_escape("") == ""


def test_safe_render_llm_answer_formatting_and_escaping():
    """
    Kiểm tra câu trả lời của LLM vừa được escape an toàn thẻ HTML độc hại,
    vừa hỗ trợ hiển thị đẹp cú pháp in đậm **text** và in nghiêng *text*.
    """
    raw_llm = "<script>alert(1)</script> Căn cứ theo **Điều 113 Bộ luật Lao động 2019**, người lao động được nghỉ *12 ngày* phép năm."
    rendered = safe_render_llm_answer(raw_llm)

    # 1. Đảm bảo script độc hại đã bị vô hiệu hóa
    assert "<script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered

    # 2. Đảm bảo định dạng in đậm và in nghiêng an toàn được tạo ra
    assert "<strong>Điều 113 Bộ luật Lao động 2019</strong>" in rendered
    assert "<em>12 ngày</em>" in rendered


def test_safe_render_llm_answer_malicious_markdown():
    """Kiểm tra mã độc nằm bên trong thẻ markdown bold/italic cũng được escape an toàn."""
    malicious_md = "**<img src=x onerror=alert(1)>**"
    rendered = safe_render_llm_answer(malicious_md)

    assert "<img" not in rendered
    assert "<strong>&lt;img src=x onerror=alert(1)&gt;</strong>" == rendered

def test_safe_render_llm_answer_markdown_bullets():
    raw_llm = """Điều 5 quy định:

* Thông tin về doanh nghiệp.
* Thông tin cá nhân.
* Địa điểm làm việc."""

    rendered = safe_render_llm_answer(raw_llm)

    assert "<ul>" in rendered
    assert "<li>Thông tin về doanh nghiệp.</li>" in rendered
    assert "<li>Thông tin cá nhân.</li>" in rendered
    assert "<li>Địa điểm làm việc.</li>" in rendered
    assert "* Thông tin về doanh nghiệp." not in rendered