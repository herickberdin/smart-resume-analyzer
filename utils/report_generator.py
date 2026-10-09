"""
PDF Report Generator for ATS Resume Analysis
Uses PyMuPDF (fitz) to generate clean, professional ATS analysis report PDFs.
"""

from datetime import datetime
from typing import Dict, List, Optional
import pymupdf


# Color Palette (RGB tuples 0.0 - 1.0)
COLOR_PRIMARY = (0.486, 0.227, 0.929)     # Purple #7c3aed
COLOR_PRIMARY_DARK = (0.298, 0.114, 0.584)# Deep Purple #4c1d95
COLOR_PRIMARY_LIGHT = (0.949, 0.925, 0.984) # Light purple bg
COLOR_SECONDARY = (0.024, 0.714, 0.831)   # Cyan #06b6d4
COLOR_SECONDARY_LIGHT = (0.902, 0.976, 0.992)
COLOR_TEXT_MAIN = (0.094, 0.094, 0.145)   # #181825 Dark neutral
COLOR_TEXT_MUTED = (0.420, 0.447, 0.502)  # #6b7280 Muted gray
COLOR_BORDER = (0.898, 0.906, 0.922)      # #e5e7eb Light border
COLOR_CARD_BG = (0.976, 0.980, 0.988)     # Off-white card bg
COLOR_WHITE = (1.0, 1.0, 1.0)

# Status colors
COLOR_SUCCESS = (0.086, 0.639, 0.365)     # Green
COLOR_SUCCESS_BG = (0.925, 0.984, 0.949)  # Light green
COLOR_SUCCESS_BORDER = (0.655, 0.914, 0.765)
COLOR_WARNING = (0.961, 0.620, 0.043)     # Amber/yellow
COLOR_WARNING_BG = (1.0, 0.980, 0.902)
COLOR_DANGER = (0.937, 0.267, 0.267)      # Red
COLOR_DANGER_BG = (0.996, 0.925, 0.925)   # Light red
COLOR_DANGER_BORDER = (0.988, 0.733, 0.733)


class ReportPDFBuilder:
    """Helper class to construct multi-page ATS Analysis PDF reports."""

    def __init__(self, page_width=595.0, page_height=842.0, margin=40.0):
        self.doc = pymupdf.open()
        self.page_width = page_width
        self.page_height = page_height
        self.margin = margin
        self.content_width = page_width - (2 * margin)
        self.current_page = None
        self.cursor_y = self.margin
        self._new_page()

    def _new_page(self):
        """Creates a new A4 page and resets the vertical cursor."""
        self.current_page = self.doc.new_page(width=self.page_width, height=self.page_height)
        self.cursor_y = self.margin
        self._draw_header_strip()

    def _draw_header_strip(self):
        """Draws top decorative colored accent strip on every page."""
        shape = self.current_page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, self.page_width, 6))
        shape.finish(color=COLOR_PRIMARY, fill=COLOR_PRIMARY, width=0)
        shape.commit()

    def check_space(self, required_height: float):
        """Ensures enough space remains on the current page, or creates a new page."""
        bottom_limit = self.page_height - self.margin - 25.0  # leave room for footer
        if self.cursor_y + required_height > bottom_limit:
            self._new_page()
            self.cursor_y += 15.0

    def draw_section_heading(self, title: str, icon: str = ""):
        """Renders a section header with an accent bottom border."""
        self.check_space(34.0)
        display_title = f"{icon}  {title}".strip() if icon else title
        self.current_page.insert_text(
            pymupdf.Point(self.margin, self.cursor_y + 14.0),
            display_title,
            fontsize=12,
            fontname="helv",
            color=COLOR_PRIMARY_DARK
        )
        self.cursor_y += 18.0

        # Underline bar
        shape = self.current_page.new_shape()
        shape.draw_line(
            pymupdf.Point(self.margin, self.cursor_y),
            pymupdf.Point(self.margin + 36.0, self.cursor_y)
        )
        shape.finish(color=COLOR_PRIMARY, width=2.0)

        # Subtle separator
        shape.draw_line(
            pymupdf.Point(self.margin + 42.0, self.cursor_y),
            pymupdf.Point(self.page_width - self.margin, self.cursor_y)
        )
        shape.finish(color=COLOR_BORDER, width=0.75)
        shape.commit()

        self.cursor_y += 12.0

    def add_page_numbers_and_footers(self):
        """Appends footer on all pages with generation watermark and page numbering."""
        total_pages = len(self.doc)
        for i, page in enumerate(self.doc, start=1):
            footer_y = self.page_height - 20.0
            shape = page.new_shape()
            shape.draw_line(
                pymupdf.Point(self.margin, footer_y - 8.0),
                pymupdf.Point(self.page_width - self.margin, footer_y - 8.0)
            )
            shape.finish(color=COLOR_BORDER, width=0.5)
            shape.commit()

            page.insert_text(
                pymupdf.Point(self.margin, footer_y),
                "Smart Resume Analyzer  •  Confidential ATS Report",
                fontsize=8,
                fontname="helv",
                color=COLOR_TEXT_MUTED
            )
            page_str = f"Page {i} of {total_pages}"
            font_helv = pymupdf.Font("helv")
            pw = font_helv.text_length(page_str, 8)
            page.insert_text(
                pymupdf.Point(self.page_width - self.margin - pw, footer_y),
                page_str,
                fontsize=8,
                fontname="helv",
                color=COLOR_TEXT_MUTED
            )

    def get_pdf_bytes(self) -> bytes:
        """Returns the compiled PDF document as binary bytes."""
        self.add_page_numbers_and_footers()
        return self.doc.tobytes()


def generate_ats_report_pdf(
    analysis: Dict,
    score_data: Dict,
    job_role: str,
    resume_filename: str = "Uploaded Resume",
    analysis_time: Optional[datetime] = None
) -> bytes:
    """
    Generates a clean, professional ATS Analysis Report PDF containing:
    - ATS Score & Score Breakdown
    - Resume Overview & Metadata
    - Keyword Match Analysis (Found vs Missing)
    - Actionable Improvement Suggestions
    - Section-wise Detection Analysis
    - Timestamp & Job Role context

    Returns bytes of the generated PDF file.
    """
    builder = ReportPDFBuilder()

    if analysis_time is None:
        analysis_time = datetime.now()
    timestamp_str = analysis_time.strftime("%B %d, %Y - %I:%M %p")

    # ──────────────────────────────────────────────────────────────────────────
    # 1. REPORT HEADER BANNER
    # ──────────────────────────────────────────────────────────────────────────
    banner_height = 68.0
    shape = builder.current_page.new_shape()
    rect = pymupdf.Rect(builder.margin, builder.cursor_y, builder.page_width - builder.margin, builder.cursor_y + banner_height)
    shape.draw_rect(rect, radius=0.08)
    shape.finish(color=COLOR_PRIMARY, fill=COLOR_PRIMARY_LIGHT, width=1.0)
    shape.commit()

    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 16.0, builder.cursor_y + 24.0),
        "SMART RESUME ANALYZER",
        fontsize=16,
        fontname="helv",
        color=COLOR_PRIMARY_DARK
    )
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 16.0, builder.cursor_y + 40.0),
        "Applicant Tracking System (ATS) Evaluation & Compatibility Report",
        fontsize=9,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 16.0, builder.cursor_y + 54.0),
        f"Generated on: {timestamp_str}",
        fontsize=8,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )

    builder.cursor_y += banner_height + 14.0

    # ──────────────────────────────────────────────────────────────────────────
    # 2. TARGET ROLE & RESUME SUMMARY METADATA
    # ────────────────────────────────────────────────────────────────────────--
    builder.check_space(52.0)
    info_box_height = 46.0
    info_rect = pymupdf.Rect(builder.margin, builder.cursor_y, builder.page_width - builder.margin, builder.cursor_y + info_box_height)
    s_info = builder.current_page.new_shape()
    s_info.draw_rect(info_rect, radius=0.08)
    s_info.finish(color=COLOR_BORDER, fill=COLOR_CARD_BG, width=0.8)
    s_info.commit()

    half_w = builder.content_width / 2.0
    # Left column: Target Job Role
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 12.0, builder.cursor_y + 17.0),
        "Target Role:",
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 70.0, builder.cursor_y + 17.0),
        str(job_role)[:45],
        fontsize=9.5,
        fontname="helv",
        color=COLOR_TEXT_MAIN
    )

    # Resume File
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 12.0, builder.cursor_y + 34.0),
        "Resume File:",
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + 70.0, builder.cursor_y + 34.0),
        str(resume_filename)[:45],
        fontsize=9.0,
        fontname="helv",
        color=COLOR_TEXT_MAIN
    )

    # Right column: Word Count & Contacts detected
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + half_w + 12.0, builder.cursor_y + 17.0),
        "Word Count:",
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )
    wc = analysis.get("word_count", 0)
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + half_w + 75.0, builder.cursor_y + 17.0),
        f"{wc} words",
        fontsize=9.0,
        fontname="helv",
        color=COLOR_TEXT_MAIN
    )

    contact_items = []
    if analysis.get("has_email"): contact_items.append("Email")
    if analysis.get("has_phone"): contact_items.append("Phone")
    if analysis.get("has_linkedin"): contact_items.append("LinkedIn")
    if analysis.get("has_github"): contact_items.append("GitHub")
    contact_str = ", ".join(contact_items) if contact_items else "None detected"

    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + half_w + 12.0, builder.cursor_y + 34.0),
        "Contact Found:",
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + half_w + 75.0, builder.cursor_y + 34.0),
        contact_str,
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MAIN
    )

    builder.cursor_y += info_box_height + 16.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. OVERALL SCORE & BREAKDOWN CARDS
    # ──────────────────────────────────────────────────────────────────────────
    builder.check_space(145.0)
    builder.draw_section_heading("ATS COMPATIBILITY SCORE & BREAKDOWN")

    total_score = score_data.get("total", 0)
    if total_score >= 75:
        score_status_color = COLOR_SUCCESS
        score_status_text = "EXCELLENT MATCH"
    elif total_score >= 50:
        score_status_color = COLOR_WARNING
        score_status_text = "MODERATE MATCH"
    else:
        score_status_color = COLOR_DANGER
        score_status_text = "NEEDS ATTENTION"

    col_gap = 12.0
    left_w = 170.0
    right_w = builder.content_width - left_w - col_gap
    score_card_h = 120.0

    # Left: Score badge card
    s_score = builder.current_page.new_shape()
    score_rect = pymupdf.Rect(builder.margin, builder.cursor_y, builder.margin + left_w, builder.cursor_y + score_card_h)
    s_score.draw_rect(score_rect, radius=0.08)
    s_score.finish(color=COLOR_PRIMARY, fill=COLOR_PRIMARY_LIGHT, width=1.2)
    s_score.commit()

    score_str = str(total_score)
    font_bold = pymupdf.Font("helv")
    sw = font_bold.text_length(score_str, 42)
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + (left_w - sw) / 2.0, builder.cursor_y + 50.0),
        score_str,
        fontsize=42,
        fontname="helv",
        color=COLOR_PRIMARY_DARK
    )

    denom_str = "OUT OF 100"
    dw = font_bold.text_length(denom_str, 8.5)
    builder.current_page.insert_text(
        pymupdf.Point(builder.margin + (left_w - dw) / 2.0, builder.cursor_y + 68.0),
        denom_str,
        fontsize=8.5,
        fontname="helv",
        color=COLOR_TEXT_MUTED
    )

    # Status pill in score card
    pill_w = 110.0
    pill_h = 18.0
    pill_x = builder.margin + (left_w - pill_w) / 2.0
    pill_y = builder.cursor_y + 86.0
    s_pill = builder.current_page.new_shape()
    s_pill.draw_rect(pymupdf.Rect(pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=0.25)
    s_pill.finish(color=score_status_color, fill=COLOR_WHITE, width=1.0)
    s_pill.commit()

    pw = font_bold.text_length(score_status_text, 7.5)
    builder.current_page.insert_text(
        pymupdf.Point(pill_x + (pill_w - pw) / 2.0, pill_y + 12.0),
        score_status_text,
        fontsize=7.5,
        fontname="helv",
        color=score_status_color
    )

    # Right: Breakdown progress bars card
    right_x = builder.margin + left_w + col_gap
    s_break = builder.current_page.new_shape()
    break_rect = pymupdf.Rect(right_x, builder.cursor_y, builder.page_width - builder.margin, builder.cursor_y + score_card_h)
    s_break.draw_rect(break_rect, radius=0.08)
    s_break.finish(color=COLOR_BORDER, fill=COLOR_CARD_BG, width=0.8)
    s_break.commit()

    breakdown = score_data.get("breakdown", {})
    bar_y = builder.cursor_y + 18.0
    max_bar_w = right_w - 90.0

    for label, val in breakdown.items():
        # Clean label (strip emoji prefix if present)
        clean_label = label.split(" ", 1)[-1] if " " in label else label
        builder.current_page.insert_text(
            pymupdf.Point(right_x + 12.0, bar_y + 4.0),
            clean_label[:18],
            fontsize=8.0,
            fontname="helv",
            color=COLOR_TEXT_MAIN
        )

        bar_start_x = right_x + 105.0
        # Background bar
        s_bar = builder.current_page.new_shape()
        s_bar.draw_rect(pymupdf.Rect(bar_start_x, bar_y - 4.0, bar_start_x + max_bar_w, bar_y + 4.0), radius=0.4)
        s_bar.finish(color=COLOR_BORDER, fill=COLOR_BORDER, width=0.5)

        # Progress fill
        fill_w = max(2.0, (val / 100.0) * max_bar_w)
        s_bar.draw_rect(pymupdf.Rect(bar_start_x, bar_y - 4.0, bar_start_x + fill_w, bar_y + 4.0), radius=0.4)
        s_bar.finish(color=COLOR_PRIMARY, fill=COLOR_PRIMARY, width=0.5)
        s_bar.commit()

        # Numeric score text
        builder.current_page.insert_text(
            pymupdf.Point(bar_start_x + max_bar_w + 8.0, bar_y + 4.0),
            f"{val}%",
            fontsize=8.0,
            fontname="helv",
            color=COLOR_TEXT_MUTED
        )
        bar_y += 19.0

    builder.cursor_y += score_card_h + 18.0

    # ──────────────────────────────────────────────────────────────────────────
    # 4. KEYWORD ANALYSIS SECTION (Found & Missing chips)
    # ──────────────────────────────────────────────────────────────────────────
    found_kw = analysis.get("found_keywords", [])
    missing_kw = analysis.get("missing_keywords", [])
    total_kw = len(found_kw) + len(missing_kw)
    match_pct = int(len(found_kw) / total_kw * 100) if total_kw > 0 else 0

    builder.check_space(60.0)
    builder.draw_section_heading(f"KEYWORD MATCH ANALYSIS ({match_pct}% Match • {len(found_kw)} of {total_kw} Matched)")

    def draw_keyword_block(title: str, keywords: List[str], is_found: bool):
        builder.check_space(32.0)
        prefix = "[+] Matched Keywords" if is_found else "[-] Missing Keywords"
        color_theme = COLOR_SUCCESS if is_found else COLOR_DANGER
        bg_color = COLOR_SUCCESS_BG if is_found else COLOR_DANGER_BG
        border_color = COLOR_SUCCESS_BORDER if is_found else COLOR_DANGER_BORDER

        builder.current_page.insert_text(
            pymupdf.Point(builder.margin, builder.cursor_y + 10.0),
            f"{prefix} ({len(keywords)}):",
            fontsize=9.0,
            fontname="helv",
            color=color_theme
        )
        builder.cursor_y += 16.0

        if not keywords:
            builder.current_page.insert_text(
                pymupdf.Point(builder.margin + 8.0, builder.cursor_y + 9.0),
                "None" if is_found else "None! Excellent coverage across all target keywords.",
                fontsize=8.5,
                fontname="helv",
                color=COLOR_TEXT_MUTED
            )
            builder.cursor_y += 15.0
            return

        font_helv = pymupdf.Font("helv")
        chip_x = builder.margin
        chip_h = 16.0
        padding_x = 7.0

        for kw in keywords:
            kw_text = f"+ {kw}" if is_found else f"- {kw}"
            tw = font_helv.text_length(kw_text, 8.0)
            chip_w = tw + (padding_x * 2)

            if chip_x + chip_w > builder.page_width - builder.margin:
                chip_x = builder.margin
                builder.cursor_y += chip_h + 5.0
                builder.check_space(chip_h + 8.0)

            # Draw chip
            s_chip = builder.current_page.new_shape()
            s_chip.draw_rect(
                pymupdf.Rect(chip_x, builder.cursor_y, chip_x + chip_w, builder.cursor_y + chip_h),
                radius=0.3
            )
            s_chip.finish(color=border_color, fill=bg_color, width=0.6)
            s_chip.commit()

            builder.current_page.insert_text(
                pymupdf.Point(chip_x + padding_x, builder.cursor_y + 11.0),
                kw_text,
                fontsize=8.0,
                fontname="helv",
                color=color_theme
            )
            chip_x += chip_w + 6.0

        builder.cursor_y += chip_h + 10.0

    draw_keyword_block("Matched Keywords", found_kw, is_found=True)
    draw_keyword_block("Missing Keywords", missing_kw, is_found=False)

    # ──────────────────────────────────────────────────────────────────────────
    # 5. SECTION-WISE ANALYSIS
    # ──────────────────────────────────────────────────────────────────────────
    builder.check_space(75.0)
    builder.draw_section_heading("SECTION-WISE ANALYSIS")

    all_sections = ["Contact", "Summary", "Skills", "Experience", "Education", "Projects", "Certifications"]
    detected_sections = set(analysis.get("sections_found", []))

    sec_col_count = 3
    sec_col_w = builder.content_width / sec_col_count
    sec_row_h = 24.0

    for idx, sec in enumerate(all_sections):
        col_idx = idx % sec_col_count
        if col_idx == 0 and idx > 0:
            builder.cursor_y += sec_row_h
            builder.check_space(sec_row_h + 8.0)

        cx = builder.margin + (col_idx * sec_col_w)
        cy = builder.cursor_y

        is_present = sec in detected_sections
        status_sym = "[x]" if is_present else "[  ]"
        status_col = COLOR_SUCCESS if is_present else COLOR_DANGER
        status_lbl = "Detected" if is_present else "Missing"

        s_sec_card = builder.current_page.new_shape()
        s_sec_card.draw_rect(
            pymupdf.Rect(cx, cy, cx + sec_col_w - 6.0, cy + sec_row_h - 4.0),
            radius=0.1
        )
        s_sec_card.finish(color=COLOR_BORDER, fill=COLOR_CARD_BG, width=0.6)
        s_sec_card.commit()

        builder.current_page.insert_text(
            pymupdf.Point(cx + 8.0, cy + 13.0),
            f"{status_sym} {sec}",
            fontsize=8.5,
            fontname="helv",
            color=COLOR_TEXT_MAIN
        )
        builder.current_page.insert_text(
            pymupdf.Point(cx + sec_col_w - 52.0, cy + 13.0),
            status_lbl,
            fontsize=7.5,
            fontname="helv",
            color=status_col
        )

    builder.cursor_y += sec_row_h + 16.0

    # ──────────────────────────────────────────────────────────────────────────
    # 6. ACTIONABLE IMPROVEMENT RECOMMENDATIONS
    # ──────────────────────────────────────────────────────────────────────────
    tips = analysis.get("tips", [])
    if tips:
        builder.check_space(60.0)
        builder.draw_section_heading("RECOMMENDED ACTION ITEMS & TIPS")

        for tip in tips:
            # Clean markdown formatting like ** or *
            cleaned_tip = tip.replace("**", "").replace("*", "")
            tip_rect = pymupdf.Rect(builder.margin + 18.0, builder.cursor_y, builder.page_width - builder.margin - 8.0, builder.cursor_y + 100.0)

            # Measure height required
            temp_doc = pymupdf.open()
            temp_page = temp_doc.new_page(width=builder.page_width, height=builder.page_height)
            rem = temp_page.insert_textbox(
                pymupdf.Rect(0, 0, builder.content_width - 24.0, 100.0),
                cleaned_tip,
                fontsize=8.5,
                fontname="helv"
            )
            temp_doc.close()

            used_h = max(20.0, 100.0 - max(0.0, rem) + 8.0)
            builder.check_space(used_h + 4.0)

            # Draw bullet callout box
            s_tip = builder.current_page.new_shape()
            card_rect = pymupdf.Rect(builder.margin, builder.cursor_y, builder.page_width - builder.margin, builder.cursor_y + used_h)
            s_tip.draw_rect(card_rect, radius=0.08)
            s_tip.finish(color=COLOR_BORDER, fill=COLOR_SECONDARY_LIGHT, width=0.5)

            # Left cyan accent border
            s_tip.draw_line(
                pymupdf.Point(builder.margin, builder.cursor_y),
                pymupdf.Point(builder.margin, builder.cursor_y + used_h)
            )
            s_tip.finish(color=COLOR_SECONDARY, width=3.0)
            s_tip.commit()

            # Insert tip bullet symbol & text
            builder.current_page.insert_text(
                pymupdf.Point(builder.margin + 6.0, builder.cursor_y + 13.0),
                "*",
                fontsize=11.0,
                fontname="helv",
                color=COLOR_SECONDARY
            )

            text_box_rect = pymupdf.Rect(
                builder.margin + 16.0,
                builder.cursor_y + 4.0,
                builder.page_width - builder.margin - 8.0,
                builder.cursor_y + used_h - 2.0
            )
            builder.current_page.insert_textbox(
                text_box_rect,
                cleaned_tip,
                fontsize=8.5,
                fontname="helv",
                color=COLOR_TEXT_MAIN
            )

            builder.cursor_y += used_h + 6.0

    return builder.get_pdf_bytes()
