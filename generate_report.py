from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

def build_report(filename="AdvancedPasswordTool_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading', parent=styles['Heading2'], spaceAfter=6))
    styles.add(ParagraphStyle(name='Body', parent=styles['BodyText'], spaceAfter=4))

    story = []
    story.append(Paragraph("Advanced Password Tool – Project Report", styles['Heading']))
    story.append(Spacer(1, 0.2*inch))

    # Sections
    sections = [
        ("Abstract",
         "This report presents the Advanced Password Tool, a desktop application built in Python to enhance user password security. The tool integrates entropy-based strength metrics, pattern evaluation via zxcvbn, and breach detection through the Have I Been Pwned API. It also features strong password generation using cryptographically secure methods, and a highly configurable wordlist builder, supporting leetspeak, casing, symbols, and year-suffix variants. A Tkinter GUI offers an intuitive multi-tab interface, theme toggling, clipboard copying, and export functionality. Packaged via PyInstaller, it delivers a single‑file executable for easy distribution. A suite of pytest unit tests ensures reliability."),
        ("Introduction",
         "Weak or reused passwords continue to pose a major risk—studies indicate low entropy and patterns are easily guessable. The Advanced Password Tool was built to address this gap: offering both novice and security-savvy users a unified interface to assess password robustness, generate secure passwords, and build tailored wordlists for testing or educational purposes. The modular design ensures extensibility, while GUI-based interactions make security accessible without overwhelming users"),
        ("Tools Used",
         "Python 3.x, Tkinter, zxcvbn-python (for scoring), secrets and random modules, ReportLab (for PDF reporting), pytest (for testing), PyInstaller (for packaging)"),
        ("Steps Involved",
         "1. Requirement gathering and modular design\n"
         "2. Implemented core modules: analyzer (entropy + breach), generator (secure passwords), wordlist builder (transforms with combinatorial limits)\n"
         "3. Built Tkinter GUI with tabbed interface and theme toggling\n"
         "4. Added CLI script (cli.py) and used PyInstaller for creating a single-file executable\n"
         "5. Wrote unit tests to ensure reliability"),
        ("Conclusion",
         "The Advanced Password Tool delivers functional and secure utility for password strength evaluation, generation, and tailored wordlists. Its GUI and executable packaging enhance accessibility, while future enhancements could include vault features, mnemonic generation, or CLI expansions.")
    ]

    for title, text in sections:
        story.append(Paragraph(title, styles['Heading']))
        story.append(Paragraph(text, styles['Body']))
        story.append(Spacer(1, 0.2*inch))

    doc.build(story)
    print(f"Report generated: {filename}")

if __name__ == "__main__":
    build_report()
