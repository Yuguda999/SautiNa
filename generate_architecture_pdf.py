import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group
from reportlab.graphics import renderPDF

def create_architecture_pdf():
    doc = SimpleDocTemplate("SautiNa_Technical_Architecture.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles
    title_style = styles['Title']
    heading1_style = styles['Heading1']
    heading2_style = styles['Heading2']
    normal_style = styles['Normal']
    code_style = ParagraphStyle('Code', parent=styles['Code'], backColor=colors.lightgrey)

    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("SautiNa", title_style))
    story.append(Paragraph("Technical Architecture Document", title_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Version 1.0", normal_style))
    story.append(Paragraph("Date: December 16, 2025", normal_style))
    story.append(PageBreak())

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", heading1_style))
    story.append(Paragraph("""
    SautiNa is a voice-first AI assistant tailored for the Nigerian market. It addresses the digital divide by providing
    access to technology in native languages: Hausa, Yoruba, Igbo, and Nigerian Pidgin, alongside English.
    The system leverages advanced AI models for Speech-to-Text (STT), Large Language Model (LLM) processing, and
    Text-to-Speech (TTS) to create a seamless conversational experience.
    """, normal_style))
    story.append(Spacer(1, 0.2*inch))

    # 2. System Architecture
    story.append(Paragraph("2. System Architecture", heading1_style))
    story.append(Paragraph("""
    The SautiNa system follows a modern client-server architecture, integrating cloud-based AI services.
    """, normal_style))
    story.append(Spacer(1, 0.2*inch))

    # Architecture Diagram (Simple Block Diagram using ReportLab Graphics)
    d = Drawing(400, 200)
    
    # Frontend Box
    d.add(Rect(10, 80, 100, 60, fillColor=colors.lightblue, strokeColor=colors.blue))
    d.add(String(60, 110, "Frontend", textAnchor="middle"))
    d.add(String(60, 95, "(React/Vite)", textAnchor="middle"))

    # Backend Box
    d.add(Rect(150, 80, 100, 60, fillColor=colors.lightgreen, strokeColor=colors.green))
    d.add(String(200, 110, "Backend", textAnchor="middle"))
    d.add(String(200, 95, "(FastAPI)", textAnchor="middle"))

    # AI Services Box
    d.add(Rect(290, 130, 100, 60, fillColor=colors.lightpink, strokeColor=colors.red))
    d.add(String(340, 160, "N-ATLaS LLM", textAnchor="middle"))
    d.add(String(340, 145, "(Modal)", textAnchor="middle"))

    d.add(Rect(290, 30, 100, 60, fillColor=colors.lightyellow, strokeColor=colors.orange))
    d.add(String(340, 60, "YarnGPT TTS", textAnchor="middle"))
    d.add(String(340, 45, "(External API)", textAnchor="middle"))

    # Arrows
    d.add(Line(110, 110, 150, 110, strokeWidth=2, arrow=True)) # Frontend -> Backend
    d.add(Line(250, 110, 290, 160, strokeWidth=2, arrow=True)) # Backend -> LLM
    d.add(Line(250, 110, 290, 60, strokeWidth=2, arrow=True))  # Backend -> TTS

    story.append(d)
    story.append(Spacer(1, 0.2*inch))

    # 3. Component Details
    story.append(Paragraph("3. Component Details", heading1_style))
    
    story.append(Paragraph("3.1 Frontend (Client)", heading2_style))
    story.append(Paragraph("""
    - **Framework**: React with TypeScript and Vite for fast development and build performance.
    - **Styling**: Tailwind CSS for responsive and modern UI design.
    - **Audio Handling**: Uses Web Audio API for recording user speech and playing back audio responses.
    - **State Management**: React Hooks for managing conversation state and language preferences.
    """, normal_style))

    story.append(Paragraph("3.2 Backend (Server)", heading2_style))
    story.append(Paragraph("""
    - **Framework**: FastAPI (Python) for high-performance async API handling.
    - **API Routes**:
        - `/api/text`: Handles text-based queries.
        - `/api/voice`: Handles voice input (STT processing).
        - `/api/tts`: Proxies requests to YarnGPT.
    - **Orchestration**: Manages the flow between STT, LLM, and TTS services.
    """, normal_style))

    story.append(Paragraph("3.3 AI Services", heading2_style))
    story.append(Paragraph("""
    - **LLM (N-ATLaS)**:
        - **Model**: N-ATLaS (Nigerian-Adaptive Transfer Learning and Speech), based on Llama-3-8B.
        - **Deployment**: Hosted on Modal using vLLM for efficient inference.
        - **Optimization**: Uses FP8 quantization for H100 GPU performance.
    - **TTS (YarnGPT)**:
        - **Service**: External API providing natural-sounding Nigerian voices.
        - **Voices**: Supports multiple characters (e.g., Idera, Emma, Zainab).
    """, normal_style))

    # 4. Data Flow
    story.append(Paragraph("4. Data Flow", heading1_style))
    story.append(Paragraph("""
    1. **User Input**: User speaks into the microphone on the frontend.
    2. **STT Processing**: Audio is sent to the backend and converted to text (using Google Speech Recognition or similar).
    3. **Intent Processing**: The text is sent to the N-ATLaS LLM on Modal to generate a response in the target language.
    4. **Audio Generation**: The text response is sent to YarnGPT to generate audio.
    5. **Response**: The backend returns both the text and the audio URL to the frontend.
    6. **Playback**: The frontend displays the text and plays the audio.
    """, normal_style))

    # 5. Security
    story.append(Paragraph("5. Security Considerations", heading1_style))
    story.append(Paragraph("""
    - **API Keys**: Sensitive keys (YarnGPT, Modal) are stored in environment variables (`.env`).
    - **CORS**: Configured to allow requests from the frontend origin.
    - **Input Validation**: Pydantic models ensure data integrity for API requests.
    """, normal_style))

    # 6. Deployment Strategy
    story.append(Paragraph("6. Deployment Strategy", heading1_style))
    story.append(Paragraph("""
    - **Frontend**: Can be deployed on Vercel, Netlify, or similar static hosts.
    - **Backend**: Suitable for containerized deployment (Docker) on Cloud Run, Railway, or a VPS.
    - **LLM**: Deployed as a serverless function on Modal, scaling to zero when not in use to save costs.
    """, normal_style))

    doc.build(story)
    print("PDF generated successfully: SautiNa_Technical_Architecture.pdf")

if __name__ == "__main__":
    create_architecture_pdf()
