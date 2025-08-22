from flask import Flask, render_template, send_file
import io
from fpdf import FPDF
import scheduler

app = Flask(__name__)

@app.route('/')
def home():
    timetable = scheduler.generate_timetable_data()
    return render_template('home.html', timetable=timetable, lesson_times=scheduler.LESSON_TIMES)

@app.route('/download-pdf')
def download_pdf():
    timetable = scheduler.generate_timetable_data()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for grade, days in timetable.items():
        pdf.cell(200, 10, txt=f"Grade {grade}", ln=True)
        for day, lessons in days.items():
            pdf.cell(200, 10, txt=f"{day}:", ln=True)
            for i, subject in enumerate(lessons):
                time = scheduler.LESSON_TIMES[i]
                pdf.cell(200, 10, txt=f"  {time} - {subject}", ln=True)
        pdf.ln(5)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)

    return send_file(output, download_name="timetable.pdf", as_attachment=True)

@app.route('/api')
def api_status():
    return "Timetable API is live!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
