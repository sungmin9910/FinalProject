# -*- coding: utf-8 -*-
import os
import sys
from fpdf import FPDF

class KoreanPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Malgun', 'B', 8)
        self.set_text_color(150, 150, 150)
        # "연구 코드 최적화 및 구조 개선 결과 보고서"를 UTF-8 바이트 디코딩으로 안전하게 표현
        header_text = b'\xec\x97\xb0\xea\xb5\xac \xec\xbd\x94\xeb\x93\x9c \xec\xb3\x8c\xec\xa0\x81\xed\x99\x94 \xeb\xb0\x8f \xea\xb5\xac\xec\xa1\xb0 \xea\xb0\x9c\xec\x84\xa0 \xea\xb2\xb0\xea\xb3\xbc \xeb\xb3\xb4\xea\xb3\xac\xec\x84\x9c'.decode('utf-8')
        self.cell(0, 10, header_text, new_x="LMARGIN", new_y="NEXT", align='R')
        self.line(10, 17, 200, 17)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Malgun', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    md_path = os.path.join(project_dir, "report/report.md")
    report_pdf_path = os.path.join(project_dir, "report/report.pdf")
    
    # 윈도우 한글 폰트 추가
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"
    font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
    
    if not os.path.exists(font_path):
        alt_paths = [
            "C:\\Windows\\Fonts\\batang.ttc",
            "C:\\Windows\\Fonts\\gulim.ttc",
            "C:\\Windows\\Fonts\\맑은고딕.ttf"
        ]
        found = False
        for p in alt_paths:
            if os.path.exists(p):
                font_path = p
                font_bold_path = p
                found = True
                break
        if not found:
            print("Error: Korean font not found.")
            sys.exit(1)
            
    import json
    metadata_path = os.path.join(project_dir, "report/metadata.json")
    if not os.path.exists(metadata_path):
        print(f"metadata.json 파일을 찾을 수 없습니다: {metadata_path}")
        sys.exit(1)
        
    with open(metadata_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    pdf = KoreanPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Malgun", "", font_path)
    pdf.add_font("Malgun", "B", font_bold_path)
    
    # ==================== PAGE 1: 표지 ====================
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font('Malgun', 'B', 24)
    pdf.set_text_color(33, 37, 41)
    
    # JSON 메타데이터에서 동적으로 읽어 표지 텍스트 출력
    title_1 = meta["title_line1"]
    title_2 = meta["title_line2"]
    pdf.cell(0, 15, title_1, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 15, title_2, new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.ln(5)
    pdf.set_draw_color(33, 150, 243)
    pdf.set_line_width(1.5)
    pdf.line(50, 80, 160, 80)
    
    pdf.set_y(100)
    pdf.set_font('Malgun', '', 14)
    pdf.set_text_color(73, 80, 87)
    sub_1 = meta["course"]
    sub_2 = meta["subject"]
    pdf.cell(0, 10, sub_1, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 10, sub_2, new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_y(220)
    pdf.set_font('Malgun', 'B', 12)
    pdf.set_text_color(33, 37, 41)
    info_1 = meta["submitter"]
    info_2 = meta["date"]
    pdf.cell(0, 8, info_1, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0, 8, info_2, new_x="LMARGIN", new_y="NEXT", align='C')
    
    # ==================== report.md 동적 파싱 ====================
    if not os.path.exists(md_path):
        print(f"report.md 파일을 찾을 수 없습니다: {md_path}")
        sys.exit(1)
        
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    # 헤더(##)를 기준으로 본문 파싱
    sections = md_content.split("\n## ")
    
    # 페이지 조정을 위해 각 단락을 배치
    # Page 2: Section 1 & Section 2
    pdf.add_page()
    render_section(pdf, sections[1])
    pdf.ln(5)
    render_section(pdf, sections[2])
    
    # Page 3: Section 3 & Section 4
    pdf.add_page()
    render_section(pdf, sections[3])
    pdf.ln(5)
    render_section(pdf, sections[4])
    
    # Page 4: Section 5 & Section 6
    pdf.add_page()
    render_section(pdf, sections[5])
    pdf.ln(5)
    render_section(pdf, sections[6])
    
    pdf.output(report_pdf_path)
    print(f"PDF 보고서 생성 완료: {report_pdf_path}")

def render_section(pdf, section_text):
    lines = section_text.strip().split("\n")
    if not lines:
        return
        
    # 섹션 제목 출력 (첫 줄)
    title = lines[0].strip()
    pdf.set_font('Malgun', 'B', 14)
    pdf.set_text_color(13, 110, 253) # Primary Blue
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(13, 110, 253)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    table_lines = []
    in_table = False
    
    for line in lines[1:]:
        line = line.strip()
        if not line:
            if table_lines:
                render_table(pdf, table_lines)
                table_lines = []
                in_table = False
            continue
            
        # 테이블 파싱 감지
        if line.startswith("|"):
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            # 테이블 도중 빈 라인이 아닌 문자가 왔는데 |로 시작 안 하면 테이블 종료 처리
            render_table(pdf, table_lines)
            table_lines = []
            in_table = False
            
        # Heading 3 (###)
        if line.startswith("### "):
            pdf.set_font('Malgun', 'B', 11)
            pdf.set_text_color(33, 37, 41)
            pdf.cell(0, 8, line.replace("### ", "").strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        # Bullet list (- 또는 *)
        elif line.startswith("- ") or line.startswith("* ") or line.startswith(" - "):
            pdf.set_font('Malgun', '', 10)
            pdf.set_text_color(33, 37, 41)
            clean_line = line.replace("- ", "").replace("* ", "").strip()
            bullet_char = b'\xe2\x80\xa2'.decode('utf-8')
            pdf.multi_cell(0, 6, f"  {bullet_char} {clean_line}")
            pdf.set_x(10.0)
        # 번호 리스트 (예: 1), 2))
        elif (line.startswith("1)") or line.startswith("2)") or line.startswith("3)") or line.startswith("4)")) or (line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ")):
            pdf.set_font('Malgun', 'B', 10)
            pdf.set_text_color(33, 37, 41)
            pdf.multi_cell(0, 6, line)
            pdf.set_x(10.0)
        # 일반 단락
        else:
            pdf.set_font('Malgun', '', 10)
            pdf.set_text_color(33, 37, 41)
            pdf.multi_cell(0, 6, line)
            pdf.set_x(10.0)
            
    if table_lines:
        render_table(pdf, table_lines)

def render_table(pdf, table_lines):
    rows = []
    for line in table_lines:
        if '---' in line:
            continue
        # 마크다운 표 셀 분리 및 볼드 제거
        cells = [c.strip().replace('**', '') for c in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)
            
    if not rows:
        return
        
    pdf.ln(2)
    with pdf.table() as table:
        for r_idx, r_content in enumerate(rows):
            row = table.row()
            for datum in r_content:
                # FPDF2 table API cell에 텍스트 주입
                row.cell(datum)
    pdf.ln(3)

if __name__ == "__main__":
    generate_pdf()
